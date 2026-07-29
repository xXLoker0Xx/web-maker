"""
Amazon product scraper module.
Extracts product data from Amazon search results using web scraping.
Supports both single searches and bulk ASIN processing.
"""

import re
import json
import time
from typing import List, Dict, Optional, Any
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class AmazonScraper:
    """Scrapes Amazon product information."""

    # Realistic browser user agents
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]

    def __init__(self, base_url: str = "https://www.amazon.es", timeout: int = 10):
        """
        Initialize Amazon scraper.
        
        Args:
            base_url: Amazon domain base URL
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = self._create_session()
        self.current_user_agent_idx = 0

    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry strategy.
        
        Returns:
            Configured requests.Session object
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _get_user_agent(self) -> str:
        """
        Rotate between user agents.
        
        Returns:
            Random-like user agent string
        """
        user_agent = self.USER_AGENTS[self.current_user_agent_idx]
        self.current_user_agent_idx = (self.current_user_agent_idx + 1) % len(self.USER_AGENTS)
        return user_agent

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate realistic request headers.
        
        Returns:
            Dictionary of HTTP headers
        """
        return {
            'User-Agent': self._get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def _extract_asin_from_url(self, url: str) -> Optional[str]:
        """
        Extract ASIN from Amazon product URL.
        
        Args:
            url: Amazon product URL
            
        Returns:
            ASIN string or None if not found
        """
        match = re.search(r'/dp/([A-Z0-9]{10})', url)
        return match.group(1) if match else None

    def scrape_search_results(self, search_term: str, num_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Scrape Amazon search results for a given term.
        
        Args:
            search_term: Product search term
            num_pages: Number of results pages to scrape
            
        Returns:
            List of product dictionaries
        """
        products = []
        
        for page in range(1, num_pages + 1):
            try:
                print(f"📄 Scrapeando página {page} para: {search_term}")
                
                # Build search URL
                params = {'k': search_term, 'page': page}
                search_url = f"{self.base_url}/s?{urlencode(params)}"
                
                response = self.session.get(
                    search_url,
                    headers=self._get_headers(),
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find product containers
                product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
                
                if not product_containers:
                    print(f"⚠ No se encontraron productos en la página {page}")
                    break
                
                for container in product_containers:
                    try:
                        product = self._parse_product_container(container)
                        if product:
                            products.append(product)
                    except Exception as e:
                        print(f"⚠ Error al procesar producto: {e}")
                        continue
                
                # Be nice to Amazon's servers
                time.sleep(2)
                
            except requests.RequestException as e:
                print(f"✗ Error de red en página {page}: {e}")
                break
            except Exception as e:
                print(f"✗ Error inesperado en página {page}: {e}")
                break
        
        print(f"✓ Se extrajeron {len(products)} productos")
        return products

    def _parse_product_container(self, container) -> Optional[Dict[str, Any]]:
        """
        Parse a single product container from search results.
        
        Args:
            container: BeautifulSoup element containing product info
            
        Returns:
            Product dictionary or None if parsing fails
        """
        try:
            # Extract product URL and ASIN
            link_element = container.find('a', {'class': 's-underline-text'})
            if not link_element or not link_element.get('href'):
                return None
            
            product_url = link_element['href']
            if not product_url.startswith('http'):
                product_url = self.base_url + product_url
            
            asin = self._extract_asin_from_url(product_url)
            if not asin:
                return None
            
            # Extract title
            title_elem = container.find('h2', {'class': 's-size-mini'})
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Extract price
            price = self._extract_price(container)
            
            # Extract image URL
            image_elem = container.find('img', {'class': 's-image'})
            image_url = image_elem.get('src', '') if image_elem else ''
            
            # Extract rating and reviews count
            rating, reviews_count = self._extract_rating_info(container)
            
            # Extract features (bullet points) from the search result preview
            features = self._extract_features_from_preview(container)
            
            product = {
                'asin': asin,
                'title': title,
                'price': price,
                'rating': rating,
                'reviews_count': reviews_count,
                'features': features,
                'image_url': image_url,
                'url': product_url
            }
            
            return product
            
        except Exception as e:
            print(f"⚠ Error al parsear contenedor: {e}")
            return None

    def _extract_price(self, container) -> str:
        """Extract product price from container."""
        try:
            price_elem = container.find('span', {'class': 'a-price-whole'})
            if price_elem:
                return price_elem.get_text(strip=True)
            
            # Alternative price extraction
            price_elem = container.find('span', string=re.compile(r'€|\$'))
            if price_elem:
                return price_elem.get_text(strip=True)
            
            return "N/A"
        except:
            return "N/A"

    def _extract_rating_info(self, container) -> tuple:
        """Extract rating and review count from container."""
        try:
            rating = 0.0
            reviews_count = 0
            
            # Find rating stars
            rating_elem = container.find('span', {'class': 'a-icon-star-small'})
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+[.,]\d+)', rating_text)
                if rating_match:
                    rating = float(rating_match.group(1).replace(',', '.'))
            
            # Find review count
            reviews_elem = container.find('span', {'aria-label': re.compile(r'número de')})
            if reviews_elem:
                reviews_text = reviews_elem.get_text(strip=True)
                reviews_match = re.search(r'(\d+)', reviews_text.replace('.', ''))
                if reviews_match:
                    reviews_count = int(reviews_match.group(1))
            
            return rating, reviews_count
        except:
            return 0.0, 0

    def _extract_features_from_preview(self, container) -> List[str]:
        """
        Extract feature bullet points from search result preview.
        
        Args:
            container: BeautifulSoup element
            
        Returns:
            List of feature strings (max 5)
        """
        try:
            features = []
            
            # Look for feature list in the container
            feature_list = container.find('ul', {'class': 'a-unordered-list'})
            if feature_list:
                items = feature_list.find_all('span', {'class': 'a-list-item'})
                for item in items[:5]:  # Max 5 features
                    feature_text = item.get_text(strip=True)
                    if feature_text:
                        features.append(feature_text)
            
            return features if features else ["Producto sin descripción detallada disponible"]
        except:
            return ["Características no disponibles"]

    def scrape_product_details(self, asin: str) -> Optional[Dict[str, Any]]:
        """
        Scrape detailed information from a single product page.
        
        Args:
            asin: Amazon Standard Identification Number
            
        Returns:
            Detailed product dictionary or None if scraping fails
        """
        try:
            print(f"🔗 Obteniendo detalles del producto: {asin}")
            
            url = f"{self.base_url}/dp/{asin}"
            response = self.session.get(
                url,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1', {'class': 'product-title'})
            if not title_elem:
                title_elem = soup.find('span', {'id': 'productTitle'})
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Extract price
            price = "N/A"
            price_elem = soup.find('span', {'class': 'a-price-whole'})
            if price_elem:
                price = price_elem.get_text(strip=True)
            
            # Extract main image
            image_url = ""
            image_elem = soup.find('img', {'id': 'landingImage'})
            if image_elem:
                image_url = image_elem.get('src', '')
            
            # Extract rating
            rating = 0.0
            rating_elem = soup.find('span', {'class': 'a-icon-star'})
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'(\d+[.,]\d+)', rating_text)
                if rating_match:
                    rating = float(rating_match.group(1).replace(',', '.'))
            
            # Extract feature bullets
            features = []
            feature_bullets = soup.find('ul', {'class': 'a-unordered-list'})
            if feature_bullets:
                items = feature_bullets.find_all('li')
                for item in items[:5]:
                    feature_text = item.get_text(strip=True)
                    if feature_text:
                        features.append(feature_text)
            
            product = {
                'asin': asin,
                'title': title,
                'price': price,
                'rating': rating,
                'reviews_count': 0,
                'features': features if features else ["Descripción no disponible"],
                'image_url': image_url
            }
            
            time.sleep(1)
            return product
            
        except requests.RequestException as e:
            print(f"✗ Error de red al obtener detalles: {e}")
            return None
        except Exception as e:
            print(f"✗ Error al obtener detalles del producto: {e}")
            return None

    def scrape_multiple_asins(self, asins: List[str]) -> List[Dict[str, Any]]:
        """
        Scrape details for multiple ASINs.
        
        Args:
            asins: List of Amazon Standard Identification Numbers
            
        Returns:
            List of product dictionaries
        """
        products = []
        for idx, asin in enumerate(asins, 1):
            print(f"📦 [{idx}/{len(asins)}] Scrapeando ASIN: {asin}")
            product = self.scrape_product_details(asin)
            if product:
                products.append(product)
                time.sleep(1)  # Be respectful
        return products

    def close(self) -> None:
        """Close the session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

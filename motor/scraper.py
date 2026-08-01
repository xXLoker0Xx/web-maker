"""
Amazon product scraper module.
Extracts product data from Amazon search results using Playwright.
Handles Akamai challenges and dynamic content loading.
"""

import re
import json
import time
from typing import List, Dict, Optional, Any
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeoutError


class AmazonScraper:
    """Scrapes Amazon product information using Playwright (handles Akamai)."""

    # Realistic browser user agents
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]

    def __init__(self, base_url: str = "https://www.amazon.es", headless: bool = True):
        """
        Initialize Amazon scraper with Playwright.
        
        Args:
            base_url: Amazon domain base URL
            headless: Run browser in headless mode (invisible)
        """
        self.base_url = base_url
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.current_user_agent_idx = 0

    def _get_user_agent(self) -> str:
        """Rotate between user agents."""
        user_agent = self.USER_AGENTS[self.current_user_agent_idx]
        self.current_user_agent_idx = (self.current_user_agent_idx + 1) % len(self.USER_AGENTS)
        return user_agent

    def _init_browser(self):
        """Initialize Playwright browser."""
        if self.browser is None:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=['--disable-blink-features=AutomationControlled']
            )
            print("✓ Navegador Playwright iniciado")

    def _close_browser(self):
        """Close Playwright browser."""
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
            print("✓ Navegador Playwright cerrado")

    def _create_page(self) -> Page:
        """Create and configure a new page."""
        self._init_browser()
        page = self.browser.new_page(
            user_agent=self._get_user_agent(),
            viewport={'width': 1920, 'height': 1080},
        )
        # Set headers to look like a real browser
        page.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        return page

    def _extract_asin_from_url(self, url: str) -> Optional[str]:
        """Extract ASIN from Amazon product URL."""
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
        page = None
        
        try:
            page = self._create_page()
            
            for page_num in range(1, num_pages + 1):
                try:
                    print(f"📄 Scrapeando página {page_num} para: {search_term}")
                    
                    # Build search URL
                    params = {'k': search_term}
                    if page_num > 1:
                        params['page'] = page_num
                    search_url = f"{self.base_url}/s?{urlencode(params)}"
                    
                    # Navigate with timeout
                    try:
                        page.goto(search_url, wait_until='networkidle', timeout=30000)
                    except PlaywrightTimeoutError:
                        print("⚠ Timeout esperando página, intentando de todas formas...")
                    
                    # Wait for product containers to load
                    try:
                        page.wait_for_selector('div[data-component-type="s-search-result"]', timeout=10000)
                    except:
                        print("⚠ No se encontraron contenedores de productos (esperado en algunos casos)")
                    
                    # Get all product containers
                    product_containers = page.query_selector_all('div[data-component-type="s-search-result"]')
                    
                    if not product_containers:
                        print(f"⚠ No se encontraron productos en la página {page_num}")
                        break
                    
                    print(f"  Encontrados {len(product_containers)} contenedores de productos")
                    
                    for container in product_containers:
                        try:
                            product = self._parse_product_container(container)
                            if product:
                                products.append(product)
                        except Exception as e:
                            print(f"  ⚠ Error al procesar producto: {e}")
                            continue
                    
                    # Be nice to Amazon's servers
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"✗ Error en página {page_num}: {e}")
                    break
            
            print(f"✓ Se extrajeron {len(products)} productos")
            return products
            
        except Exception as e:
            print(f"✗ Error general en scraping: {e}")
            return products
        finally:
            if page:
                page.close()

    def _parse_product_container(self, container) -> Optional[Dict[str, Any]]:
        """Parse a single product container from search results."""
        try:
            # Extract product URL and ASIN
            link_element = container.query_selector('a[class*="s-underline-text"]')
            if not link_element:
                link_element = container.query_selector('h2 a')
            
            if not link_element:
                return None
            
            product_url = link_element.get_attribute('href')
            if not product_url:
                return None
            
            if not product_url.startswith('http'):
                product_url = self.base_url + product_url
            
            asin = self._extract_asin_from_url(product_url)
            if not asin:
                return None
            
            # Extract title
            title_elem = container.query_selector('h2 span')
            title = title_elem.text_content().strip() if title_elem else "N/A"
            
            # Extract price
            price = self._extract_price(container)
            
            # Extract image URL
            image_elem = container.query_selector('img[class*="s-image"]')
            image_url = image_elem.get_attribute('src') if image_elem else ''
            
            # Extract rating and reviews count
            rating, reviews_count = self._extract_rating_info(container)
            
            # Extract features
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
            print(f"  ⚠ Error al parsear contenedor: {e}")
            return None

    def _extract_price(self, container) -> str:
        """Extract product price from container."""
        try:
            price_elem = container.query_selector('span[class*="a-price-whole"]')
            if price_elem:
                return price_elem.text_content().strip()
            
            # Alternative: look for any currency symbol
            price_elem = container.query_selector('span[class*="a-price"]')
            if price_elem:
                text = price_elem.text_content().strip()
                if '€' in text or '$' in text:
                    return text
            
            return "N/A"
        except:
            return "N/A"

    def _extract_rating_info(self, container) -> tuple:
        """Extract rating and review count from container."""
        try:
            rating = 0.0
            reviews_count = 0
            
            # Find rating stars
            rating_elem = container.query_selector('span[class*="a-icon-star"]')
            if rating_elem:
                rating_text = rating_elem.text_content().strip()
                rating_match = re.search(r'(\d+[.,]\d+)', rating_text)
                if rating_match:
                    rating = float(rating_match.group(1).replace(',', '.'))
            
            # Find review count
            reviews_elem = container.query_selector('span[aria-label*="número de"]')
            if not reviews_elem:
                reviews_elem = container.query_selector('span[aria-label*="ratings"]')
            
            if reviews_elem:
                reviews_text = reviews_elem.text_content().strip()
                reviews_match = re.search(r'(\d+(?:\.\d+)?)', reviews_text)
                if reviews_match:
                    reviews_count = int(reviews_match.group(1).replace('.', ''))
            
            return rating, reviews_count
        except:
            return 0.0, 0

    def _extract_features_from_preview(self, container) -> List[str]:
        """Extract product features from search result preview."""
        features = []
        try:
            # Look for bullet points in the product preview
            ul_elem = container.query_selector('ul[class*="a-unordered-list"]')
            if ul_elem:
                li_elements = ul_elem.query_selector_all('li span')
                features = [li.text_content().strip() for li in li_elements[:3]]
        except:
            pass
        
        return features
    
    def __del__(self):
        """Cleanup on deletion."""
        self._close_browser()
    
    def close(self) -> None:
        """Close browser and cleanup."""
        self._close_browser()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

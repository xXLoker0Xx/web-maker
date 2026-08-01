"""
Step 1: Pure Web Scraping
Extracts products from Amazon and saves raw JSON without AI analysis.
This allows reusing scraped data for multiple AI iterations.
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Import from parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))
from scraper import AmazonScraper
from database import ProductDatabase


class Step1ScrapeOnly:
    """Step 1: Pure scraping without AI."""
    
    def __init__(self):
        self.db = ProductDatabase("local_cache.db")
    
    def _slugify(self, text: str) -> str:
        """Convert text to URL-safe slug."""
        text = text.lower().strip()
        text = re.sub(r'[áéíóúñ]', lambda m: {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n'
        }[m.group()], text)
        text = re.sub(r'[^a-z0-9]+', '-', text)
        text = text.strip('-')
        return text
    
    def scrape(self, search_term: str, num_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Scrape products from Amazon.
        
        Args:
            search_term: Search query (e.g., "Freidoras de Aire")
            num_pages: Number of pages to scrape (1-3)
            
        Returns:
            List of product dictionaries
        """
        print("\n" + "="*70)
        print("📥 STEP 1: PURE SCRAPING")
        print("="*70)
        print(f"\n🔎 Searching for: {search_term}")
        print(f"📄 Pages to scrape: {num_pages}")
        
        products = []
        
        try:
            with AmazonScraper() as scraper:
                print("\n⏳ Starting scraping... (this may take 1-2 minutes)")
                products = scraper.scrape_search_results(search_term, num_pages=num_pages)
        
        except Exception as e:
            print(f"✗ Scraping error: {e}")
            return []
        
        if not products:
            print("✗ No products found")
            return []
        
        print(f"\n✓ Successfully scraped {len(products)} products")
        
        # Save to database
        print("\n💾 Saving to database...")
        inserted = self.db.insert_products_batch(products)
        print(f"✓ {inserted}/{len(products)} products saved")
        
        return products
    
    def create_raw_json(self, products: List[Dict[str, Any]], search_term: str, amazon_tag: str) -> Dict[str, Any]:
        """
        Create raw JSON structure with scraped data (without AI).
        
        Args:
            products: List of scraped products
            search_term: Search term (used for title)
            amazon_tag: Amazon affiliate tag
            
        Returns:
            Raw JSON structure
        """
        print("\n📝 Creating raw JSON structure...")
        
        # Prepare product data with affiliate URLs
        product_data = []
        for i, product in enumerate(products[:5], 1):  # Top 5 products
            asin = product.get('asin', '')
            title = product.get('title', 'Unknown Product')
            
            product_data.append({
                "asin": asin,
                "title": title,  # Product name (used in ProductCard)
                "image_url": product.get('image_url'),
                "price": product.get('price'),
                "rating": product.get('rating', 0.0),
                "reviews_count": product.get('reviews_count', 0),
                "badge": f"Opción {i}",  # Will be replaced by AI
                "pros": [],  # Will be filled by AI in Step 2
                "cons": [],  # Will be filled by AI in Step 2
                "summary": f"{title} - Precio: {product.get('price')}€. Con {product.get('reviews_count', 0)} reseñas y una valoración de {product.get('rating', 0.0)} estrellas.",
                "affiliate_url": f"https://amazon.es/dp/{asin}?tag={amazon_tag}"
            })
        
        raw_content = {
            "title": f"Los 5 mejores productos en {search_term.lower()} de 2026",
            "description": f"Descubre las mejores opciones en {search_term.lower()}. Análisis completo y comparativa de productos.",
            "intro": f"En este artículo te presentamos un análisis detallado de los mejores productos en {search_term.lower()}.",
            "verdict": f"Después de analizar estas opciones, cualquiera de estos productos en {search_term.lower()} es una excelente opción según tus necesidades específicas.",
            "products": product_data,
            "_metadata": {
                "search_term": search_term,
                "total_scraped": len(products),
                "products_selected": len(product_data),
                "created_at": datetime.now().isoformat(),
                "step": "1_scraping_only",
                "next_step": "Run Step 2 (AI Analysis) to add pros/cons and improve content"
            }
        }
        
        return raw_content
    
    def save_raw_json(self, content: Dict[str, Any], niche_slug: str) -> bool:
        """
        Save raw JSON to file.
        
        Args:
            content: JSON content
            niche_slug: Slug for filename
            
        Returns:
            True if successful
        """
        try:
            niches_dir = Path(__file__).parent.parent.parent / "plantilla-astro" / "src" / "content" / "niches"
            niches_dir.mkdir(parents=True, exist_ok=True)
            
            output_file = niches_dir / f"{niche_slug}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            
            print(f"\n✓ Raw JSON saved to: {output_file}")
            print(f"✓ File size: {output_file.stat().st_size} bytes")
            
            return True
            
        except Exception as e:
            print(f"✗ Error saving file: {e}")
            return False
    
    def run(self) -> None:
        """Run Step 1 interactively."""
        try:
            print("\n" + "="*70)
            print("🚀 AMAZON NICHE PAGE GENERATOR - STEP 1: SCRAPING ONLY")
            print("="*70)
            
            # Get search term
            search_term = input("\n🔎 Enter search term (e.g., 'Freidoras de Aire'): ").strip()
            if not search_term:
                print("✗ Search term cannot be empty")
                return
            
            # Get number of pages
            pages_input = input("📄 How many pages to scrape (1-3)? (default: 1): ").strip()
            try:
                num_pages = int(pages_input) if pages_input else 1
                num_pages = min(max(num_pages, 1), 3)
            except ValueError:
                num_pages = 1
            
            # Get Amazon affiliate tag
            amazon_tag = input("\n🏷️  Enter your Amazon affiliate tag (e.g., mi-tag-21): ").strip()
            if not amazon_tag:
                amazon_tag = "tu-tag-20"  # Default tag
            
            # Scrape
            products = self.scrape(search_term, num_pages)
            if not products:
                return
            
            # Create raw JSON
            content = self.create_raw_json(products, search_term, amazon_tag)
            
            # Save
            niche_slug = self._slugify(search_term)
            success = self.save_raw_json(content, niche_slug)
            
            if success:
                print("\n" + "="*70)
                print("📊 SUMMARY")
                print("="*70)
                print(f"\n✓ Niche slug: {niche_slug}")
                print(f"✓ Products scraped: {content['_metadata']['total_scraped']}")
                print(f"✓ Products in JSON: {content['_metadata']['products_selected']}")
                print(f"\n📝 Next step: Run Step 2 (AI Analysis)")
                print(f"   This will add pros/cons and improve content")
                print("\n💡 To run Step 2:")
                print(f"   python steps/step2_ai_analysis.py {niche_slug}")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation cancelled by user")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    step1 = Step1ScrapeOnly()
    step1.run()

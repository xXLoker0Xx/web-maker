"""
Step 2: AI Content Analysis
Reads JSON from Step 1 and enriches with AI-generated content:
- Product names and summaries
- Pro/cons for each product
- Page intro, verdict, and descriptions
This allows iterating on AI prompts without re-scraping.
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Import from parent directory
sys.path.insert(0, str(Path(__file__).parent.parent))
from ai_generator import AIContentGenerator
from internet_search import get_criteria_finder


class Step2AIAnalysis:
    """Step 2: AI content enrichment."""
    
    def __init__(self):
        load_dotenv()
        self.ai_provider = None
    
    def _setup_ai(self) -> bool:
        """Setup AI provider (Ollama by default)."""
        # Try Ollama first (local, free)
        try:
            self.ai_provider = AIContentGenerator('ollama', model='mistral')
            print("✓ AI Provider: Ollama (local)")
            return True
        except Exception as e:
            print(f"⚠ Ollama not available: {e}")
        
        # Try OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            try:
                self.ai_provider = AIContentGenerator('openai', openai_key)
                print("✓ AI Provider: OpenAI")
                return True
            except Exception as e:
                print(f"⚠ OpenAI error: {e}")
        
        # Try Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            try:
                self.ai_provider = AIContentGenerator('anthropic', anthropic_key)
                print("✓ AI Provider: Anthropic (Claude)")
                return True
            except Exception as e:
                print(f"⚠ Anthropic error: {e}")
        
        # Try DeepSeek
        deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        if deepseek_key:
            try:
                self.ai_provider = AIContentGenerator('deepseek', deepseek_key)
                print("✓ AI Provider: DeepSeek")
                return True
            except Exception as e:
                print(f"⚠ DeepSeek error: {e}")
        
        print("✗ No AI provider available")
        print("\nOptions:")
        print("  1. Ollama (local, free): https://ollama.ai")
        print("     Run: ollama serve")
        print("     Then: ollama pull mistral")
        print("  2. OpenAI API key → OPENAI_API_KEY in .env")
        print("  3. Anthropic API key → ANTHROPIC_API_KEY in .env")
        print("  4. DeepSeek API key → DEEPSEEK_API_KEY in .env")
        return False
    
    def load_raw_json(self, niche_slug: str) -> Optional[Dict[str, Any]]:
        """
        Load raw JSON from Step 1.
        
        Args:
            niche_slug: Niche slug (e.g., 'freidoras-de-aire')
            
        Returns:
            JSON content or None
        """
        print("\n" + "="*70)
        print("📥 STEP 2: AI CONTENT ANALYSIS")
        print("="*70)
        
        try:
            niches_dir = Path(__file__).parent.parent.parent / "plantilla-astro" / "src" / "content" / "niches"
            json_file = niches_dir / f"{niche_slug}.json"
            
            if not json_file.exists():
                print(f"✗ File not found: {json_file}")
                return None
            
            with open(json_file, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            print(f"✓ Loaded: {json_file}")
            print(f"✓ Products in file: {len(content.get('products', []))}")
            
            return content
            
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return None
    
    def get_buying_criteria(self, search_term: str) -> List[Dict[str, str]]:
        """
        Get buying criteria from internet search.
        
        Args:
            search_term: Product category (e.g., 'Freidoras de Aire')
            
        Returns:
            List of buying criteria
        """
        print(f"\n🔎 Finding buying criteria for: {search_term}...")
        
        try:
            criteria_finder = get_criteria_finder()
            criteria_data = criteria_finder.find_criteria(search_term)
            criteria = criteria_data.get('criteria', [])
            
            if criteria:
                print(f"✓ Found {len(criteria)} buying criteria")
                return criteria
            else:
                print("⚠ No criteria found, using default")
                return []
        
        except Exception as e:
            print(f"⚠ Error finding criteria: {e}")
            return []
    
    def enrich_with_ai(self, raw_content: Dict[str, Any], search_term: str, buying_criteria: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Enrich raw content with AI analysis.
        
        Args:
            raw_content: Raw JSON from Step 1
            search_term: Product category
            buying_criteria: Optional buying criteria
            
        Returns:
            Enriched content
        """
        print("\n🤖 Running AI analysis...")
        print("   This may take a minute or two depending on AI provider...")
        
        if not self.ai_provider:
            print("✗ No AI provider available")
            return raw_content
        
        # Extract products from raw content
        products = raw_content.get('products', [])
        
        if not products:
            print("✗ No products to analyze")
            return raw_content
        
        # Generate AI content
        print(f"   Analyzing {len(products)} products...")
        ai_content = self.ai_provider.generate(products, search_term, buying_criteria or [])
        
        if not ai_content:
            print("✗ AI generation failed")
            return raw_content
        
        print("✓ AI analysis complete")
        
        # Merge: AI content with affiliate URLs and images from raw content
        product_map = {p['asin']: p for p in raw_content.get('products', [])}
        
        for ai_product in ai_content.get('products', []):
            asin = ai_product.get('asin')
            if asin in product_map:
                raw_product = product_map[asin]
                # Keep images, prices, ratings from raw
                ai_product['image_url'] = raw_product.get('image_url')
                ai_product['price'] = raw_product.get('price')
                ai_product['rating'] = raw_product.get('rating', 0.0)
                ai_product['reviews_count'] = raw_product.get('reviews_count', 0)
                ai_product['affiliate_url'] = raw_product.get('affiliate_url')
        
        # Preserve metadata
        ai_content['_metadata'] = {
            **raw_content.get('_metadata', {}),
            'step': '2_ai_analysis',
            'ai_provider': self.ai_provider.__class__.__name__ if self.ai_provider else 'none',
            'enriched': True
        }
        
        return ai_content
    
    def save_enriched_json(self, content: Dict[str, Any], niche_slug: str) -> bool:
        """
        Save enriched JSON back to file.
        
        Args:
            content: Enriched JSON content
            niche_slug: Niche slug
            
        Returns:
            True if successful
        """
        try:
            niches_dir = Path(__file__).parent.parent.parent / "plantilla-astro" / "src" / "content" / "niches"
            json_file = niches_dir / f"{niche_slug}.json"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            
            print(f"\n✓ Enriched JSON saved to: {json_file}")
            print(f"✓ File size: {json_file.stat().st_size} bytes")
            
            return True
            
        except Exception as e:
            print(f"✗ Error saving file: {e}")
            return False
    
    def run(self, niche_slug: str = None) -> None:
        """
        Run Step 2 interactively.
        
        Args:
            niche_slug: Optional niche slug to process (if not provided, ask user)
        """
        try:
            print("\n" + "="*70)
            print("🤖 AMAZON NICHE PAGE GENERATOR - STEP 2: AI ANALYSIS")
            print("="*70)
            
            # Setup AI
            if not self._setup_ai():
                print("\n✗ Cannot continue without AI provider")
                return
            
            # Get niche slug
            if not niche_slug:
                niche_slug = input("\n📁 Enter niche slug (e.g., 'freidoras-de-aire'): ").strip()
                if not niche_slug:
                    print("✗ Niche slug cannot be empty")
                    return
            
            # Load raw JSON
            raw_content = self.load_raw_json(niche_slug)
            if not raw_content:
                return
            
            # Get search term
            search_term = raw_content.get('title', niche_slug).replace('Los 5 mejores productos en ', '').replace(' de 2026', '')
            
            # Get buying criteria
            buying_criteria = self.get_buying_criteria(search_term)
            
            # Enrich with AI
            enriched_content = self.enrich_with_ai(raw_content, search_term, buying_criteria)
            
            # Save
            success = self.save_enriched_json(enriched_content, niche_slug)
            
            if success:
                print("\n" + "="*70)
                print("📊 SUMMARY")
                print("="*70)
                print(f"\n✓ Niche slug: {niche_slug}")
                print(f"✓ Search term: {search_term}")
                print(f"✓ Products analyzed: {len(enriched_content.get('products', []))}")
                print(f"✓ Products with pros/cons: {sum(1 for p in enriched_content.get('products', []) if p.get('pros') and p.get('cons'))}")
                print(f"\n✨ Content enriched successfully!")
                print(f"\n📝 Next step: Rebuild Astro and deploy")
                print(f"   In plantilla-astro/: npm run build && vercel --prod")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation cancelled by user")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    niche_slug = sys.argv[1] if len(sys.argv) > 1 else None
    step2 = Step2AIAnalysis()
    step2.run(niche_slug)

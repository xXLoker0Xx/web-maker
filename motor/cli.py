"""
Main CLI: Choose between Step 1 (Scraping) or Step 2 (AI Analysis)
This decouples scraping from analysis for better workflow control.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from steps.step1_scraper_only import Step1ScrapeOnly
from steps.step2_ai_analysis import Step2AIAnalysis


def show_menu():
    """Display main menu."""
    print("\n" + "="*70)
    print("🚀 AMAZON NICHE PAGE GENERATOR - TWO-STEP WORKFLOW")
    print("="*70)
    print("\nChoose an action:\n")
    print("  1️⃣  STEP 1: SCRAPE AMAZON")
    print("      • Extract products from Amazon search results")
    print("      • Save raw JSON data (without AI)")
    print("      • Fast and reusable for multiple AI iterations")
    print()
    print("  2️⃣  STEP 2: AI ANALYSIS")
    print("      • Read existing JSON from Step 1")
    print("      • Add pros/cons, descriptions, and verdict")
    print("      • Use Ollama, OpenAI, Claude, or DeepSeek")
    print("      • Iterate on prompts without re-scraping")
    print()
    print("  3️⃣  FULL PIPELINE (Step 1 + 2)")
    print("      • Classic workflow: Scrape → AI → Done")
    print()
    print("  4️⃣  EXIT")
    print()


def main():
    """Main CLI loop."""
    print("\n")
    
    while True:
        show_menu()
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            print("\n" + "="*70)
            print("📥 STARTING STEP 1: SCRAPING")
            print("="*70)
            step1 = Step1ScrapeOnly()
            step1.run()
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            print("\n" + "="*70)
            print("🤖 STARTING STEP 2: AI ANALYSIS")
            print("="*70)
            step2 = Step2AIAnalysis()
            step2.run()
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            print("\n" + "="*70)
            print("🔗 STARTING FULL PIPELINE")
            print("="*70)
            
            # Step 1
            step1 = Step1ScrapeOnly()
            search_term = input("\n🔎 Enter search term (e.g., 'Freidoras de Aire'): ").strip()
            if not search_term:
                print("✗ Search term cannot be empty")
                continue
            
            pages_input = input("📄 How many pages to scrape (1-3)? (default: 1): ").strip()
            try:
                num_pages = int(pages_input) if pages_input else 1
                num_pages = min(max(num_pages, 1), 3)
            except ValueError:
                num_pages = 1
            
            amazon_tag = input("\n🏷️  Enter your Amazon affiliate tag (e.g., mi-tag-21): ").strip()
            if not amazon_tag:
                amazon_tag = "tu-tag-20"
            
            # Scrape
            products = step1.scrape(search_term, num_pages)
            if not products:
                continue
            
            # Create and save raw JSON
            content = step1.create_raw_json(products, search_term, amazon_tag)
            import re
            niche_slug = re.sub(r'[áéíóúñ]', lambda m: {
                'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n'
            }[m.group()], search_term.lower().strip())
            niche_slug = re.sub(r'[^a-z0-9]+', '-', niche_slug).strip('-')
            
            step1.save_raw_json(content, niche_slug)
            
            # Step 2
            print("\n" + "="*70)
            print("🤖 PROCEEDING TO STEP 2: AI ANALYSIS")
            print("="*70)
            
            step2 = Step2AIAnalysis()
            if not step2._setup_ai():
                print("⚠ Skipping AI analysis - no provider available")
                input("\nPress Enter to continue...")
                continue
            
            raw_content = step2.load_raw_json(niche_slug)
            if not raw_content:
                input("\nPress Enter to continue...")
                continue
            
            search_term_extracted = raw_content.get('title', niche_slug).replace('Los 5 mejores productos en ', '').replace(' de 2026', '')
            buying_criteria = step2.get_buying_criteria(search_term_extracted)
            enriched_content = step2.enrich_with_ai(raw_content, search_term_extracted, buying_criteria)
            step2.save_enriched_json(enriched_content, niche_slug)
            
            print("\n✨ Full pipeline complete!")
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            sys.exit(0)
        
        else:
            print("\n✗ Invalid option. Please select 1-4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled by user")
        sys.exit(0)

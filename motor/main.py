#!/usr/bin/env python3
"""
Content Generation Workflow - Main Entry Point
==============================================

High-performance three-step workflow for generating production-ready affiliate content:

  Step 1: Intro Texts     → Title, description, intro, verdict, buying criteria
  Step 2: FAQ Generation  → 7-8 semantic Q&A items (uses Step 1 context)
  Step 3: Pros & Cons     → Product advantages/disadvantages (uses Step 2 context)

CLI Usage (for automation):
  python main.py                              # All steps, all niches
  python main.py --niche freidoras --force   # Regenerate specific niche
  python main.py --step 1 2 --niche balones  # Specific steps only
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from run_specialized_workflow import SpecializedWorkflow
from scraper import AmazonScraper


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 70)
    print("🚀  AFFILIATE CONTENT GENERATOR  (Three-Step Workflow)")
    print("=" * 70 + "\n")


def get_niche_directory() -> Path:
    """Get path to niches directory."""
    niche_dir = Path(__file__).parent.parent / 'plantilla-astro' / 'src' / 'content' / 'niches'
    niche_dir.mkdir(parents=True, exist_ok=True)
    return niche_dir


def run_scraping(search_term: str, niche_name: str, num_pages: int = 3) -> bool:
    """
    Scrape Amazon for products and save to JSON file.
    
    Args:
        search_term: What to search for on Amazon
        niche_name: Niche identifier for the JSON file
        num_pages: Number of search results pages to scrape
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\n⏳ Starting scraper for '{search_term}'...")
        print(f"   Pages to scrape: {num_pages}\n")
        
        with AmazonScraper() as scraper:
            products = scraper.scrape_search_results(search_term, num_pages=num_pages)
        
        if not products:
            print(f"❌ No products found for '{search_term}'")
            return False
        
        print(f"✓ Scraped {len(products)} products")
        
        # Prepare JSON structure
        niche_data = {
            "title": f"Los mejores productos en {search_term} 2026",
            "description": f"Descubre las mejores opciones en {search_term}. Análisis completo y comparativa de productos.",
            "intro": f"En este artículo te presentamos un análisis detallado de los mejores productos en {search_term}.",
            "verdict": f"Después de analizar estas opciones, cualquiera de estos productos en {search_term} es una excelente opción según tus necesidades específicas.",
            "products": products[:5],  # Limit to 5 products
            "_metadata": {
                "search_term": search_term,
                "total_scraped": len(products),
                "products_selected": min(5, len(products)),
                "created_at": datetime.now().isoformat(),
                "step": "scraping_only",
                "next_step": "Run AI generation (Step 1-3) to add content"
            }
        }
        
        # Save to file
        niche_dir = get_niche_directory()
        filename = niche_dir / f"{niche_name}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(niche_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved to: {filename}\n")
        return True
        
    except Exception as e:
        print(f"❌ Scraping error: {e}\n")
        return False


def advanced_menu(workflow: SpecializedWorkflow):
    """Display advanced options submenu."""
    while True:
        print("\n--- Advanced Options ---\n")
        print("  [1] Generate ALL niches (all 3 steps)")
        print("  [2] Generate SPECIFIC niche (all 3 steps)")
        print("  [3] Run specific STEPS only")
        print("  [4] Regenerate everything (--force)")
        print("  [5] Change Ollama model")
        print("  [6] Back to main menu\n")
        
        choice = input("Enter option (1-6): ").strip()
        
        if choice == "1":
            print("\n⏳ Generating all niches (all 3 steps)...\n")
            return workflow.run([1, 2, 3], None, False)
        
        elif choice == "2":
            # Generate specific niche - with auto-detection
            niche_dir = get_niche_directory()
            json_files = list(niche_dir.glob("*.json"))
            
            if not json_files:
                print("❌ No niche JSON files found\n")
                continue
            
            print("\n📂 Available niches:\n")
            niche_options = []
            for i, json_file in enumerate(json_files, 1):
                niche_name = json_file.stem  # Filename without .json
                niche_options.append(niche_name)
                print(f"  [{i}] {niche_name}")
            print()
            
            selection = input("Select niche (number): ").strip()
            
            try:
                sel_num = int(selection)
                if 1 <= sel_num <= len(niche_options):
                    niche = niche_options[sel_num - 1]
                    print(f"\n⏳ Generating '{niche}' (all 3 steps)...\n")
                    return workflow.run([1, 2, 3], niche, False)
                else:
                    print("❌ Invalid selection\n")
                    continue
            except ValueError:
                print("❌ Invalid input. Please enter a number.\n")
                continue
        
        elif choice == "3":
            print("\nWhich steps? (separate with spaces)")
            print("  1 = Intro texts")
            print("  2 = FAQ generation")
            print("  3 = Pros & cons\n")
            steps_input = input("Enter steps (e.g., 1 2 3): ").strip()
            try:
                steps = [int(s) for s in steps_input.split() if s in "123"]
                if not steps:
                    print("❌ Invalid steps. Use 1, 2, or 3.\n")
                    continue
                niche = input("Enter niche name (leave empty for all): ").strip() or None
                print(f"\n⏳ Running steps {steps}...\n")
                return workflow.run(steps, niche, False)
            except ValueError:
                print("❌ Invalid input. Please use numbers only.\n")
                continue
        
        elif choice == "4":
            print("\n⚠️  Regenerating ALL content (this will overwrite existing)...\n")
            return workflow.run([1, 2, 3], None, force=True)
        
        elif choice == "5":
            model = input("Enter Ollama model (qwen3:14b, mistral, llama3, llama3.2): ").strip()
            if model in ["qwen3:14b", "mistral", "llama3", "llama3.2"]:
                workflow.model = model
                print(f"✓ Model changed to: {model}\n")
            else:
                print("❌ Invalid model. Use qwen3:14b, mistral, llama3, or llama3.2\n")
        
        elif choice == "6":
            return 0
        
        else:
            print("❌ Invalid option. Please enter 1-6.\n")


def print_menu():
    """Display interactive menu."""
    print("What do you want to do?\n")
    print("  [1] 🌐 Scraping only (extract products from Amazon)")
    print("  [2] 🤖 AI only (generate content for existing niches)")
    print("  [3] 🔄 Scraping + AI (scrape then generate content)")
    print("  [4] 🔧 Advanced options")
    print("  [5] Exit\n")


def interactive_mode():
    """Interactive menu-driven workflow."""
    print_banner()
    
    workflow = SpecializedWorkflow()

    while True:
        print_menu()
        choice = input("Enter option (1-5): ").strip()

        if choice == "1":
            # Scraping only
            search_term = input("\nWhat to scrape? (e.g., 'freidoras de aire'): ").strip()
            if not search_term:
                print("❌ Search term cannot be empty\n")
                continue
            
            # Auto-generate niche name from search term (replace spaces with hyphens)
            niche_name = search_term.lower().replace(" ", "-")
            print(f"✓ Niche name: {niche_name}")
            
            confirm = input(f"Is this correct? (press Enter to confirm, or type new name): ").strip()
            if confirm:
                niche_name = confirm.lower().replace(" ", "-")
            
            pages = input("Number of pages to scrape (default: 3): ").strip()
            try:
                num_pages = int(pages) if pages else 3
            except ValueError:
                num_pages = 3
            
            return run_scraping(search_term, niche_name, num_pages)

        elif choice == "2":
            # AI only - detect available niches from JSON files
            niche_dir = get_niche_directory()
            json_files = list(niche_dir.glob("*.json"))
            
            if not json_files:
                print("❌ No niche JSON files found in:")
                print(f"   {niche_dir}\n")
                print("   First use option [1] or [3] to scrape and create niches.\n")
                continue
            
            print("\n📂 Available niches:\n")
            niche_options = []
            for i, json_file in enumerate(json_files, 1):
                niche_name = json_file.stem  # Filename without .json
                niche_options.append(niche_name)
                print(f"  [{i}] {niche_name}")
            
            print(f"  [0] Generate ALL niches\n")
            
            selection = input("Select niche (0 for all, or number): ").strip()
            
            try:
                sel_num = int(selection)
                if sel_num == 0:
                    # Generate all
                    print("\n⏳ Generating AI content for all niches...\n")
                    return workflow.run([1, 2, 3], None, False)
                elif 1 <= sel_num <= len(niche_options):
                    niche = niche_options[sel_num - 1]
                    print(f"\n⏳ Generating AI content for '{niche}'...\n")
                    return workflow.run([1, 2, 3], niche, False)
                else:
                    print("❌ Invalid selection\n")
                    continue
            except ValueError:
                print("❌ Invalid input. Please enter a number.\n")
                continue

        elif choice == "3":
            # Scraping + AI
            search_term = input("\nWhat to scrape? (e.g., 'freidoras de aire'): ").strip()
            if not search_term:
                print("❌ Search term cannot be empty\n")
                continue
            
            # Auto-generate niche name from search term (replace spaces with hyphens)
            niche_name = search_term.lower().replace(" ", "-")
            print(f"✓ Niche name: {niche_name}")
            
            confirm = input(f"Is this correct? (press Enter to confirm, or type new name): ").strip()
            if confirm:
                niche_name = confirm.lower().replace(" ", "-")
            
            pages = input("Number of pages to scrape (default: 3): ").strip()
            try:
                num_pages = int(pages) if pages else 3
            except ValueError:
                num_pages = 3
            
            # Step 1: Scraping
            if not run_scraping(search_term, niche_name, num_pages):
                continue
            
            # Step 2: AI generation
            print(f"✓ Scraping complete. Starting AI generation for '{niche_name}'...\n")
            return workflow.run([1, 2, 3], niche_name, False)

        elif choice == "4":
            # Advanced options
            return advanced_menu(workflow)

        elif choice == "5":
            print("\n✓ Goodbye!\n")
            return 0

        else:
            print("❌ Invalid option. Please enter 1-5.\n")


def cli_mode(args):
    """CLI-based workflow (for automation & scripting)."""
    workflow = SpecializedWorkflow()
    workflow.model = args.model
    return workflow.run(args.step, args.niche, args.force)


def main():
    """Main entry point - routes to interactive or CLI mode."""
    parser = argparse.ArgumentParser(
        description="Affiliate Content Generator - Three-Step Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
CLI Examples:
  python main.py --help                           Show all options
  python main.py                                  Run interactive menu
  python main.py --niche freidoras                Generate freidoras niche
  python main.py --step 1                         Run only Step 1
  python main.py --step 1 2 3 --niche balones    Full workflow for balones
  python main.py --force                          Regenerate everything
  python main.py --model llama3.2                 Use different model
        """
    )
    parser.add_argument(
        "--niche",
        metavar="NAME",
        help="Process specific niche (e.g., freidoras, balones)"
    )
    parser.add_argument(
        "--step",
        type=int,
        nargs="+",
        choices=[1, 2, 3],
        metavar="STEP",
        help="Run specific steps (1=intro, 2=faq, 3=pros-cons)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate even if already completed"
    )
    parser.add_argument(
        "--model",
        default="qwen3:14b",
        metavar="MODEL",
        help="Ollama model to use (default: qwen3:14b)"
    )

    args = parser.parse_args()

    try:
        # If any CLI args provided, use CLI mode. Otherwise, use interactive menu.
        if args.niche or args.step or args.force or len(sys.argv) > 1:
            # CLI mode
            if not args.step:
                args.step = [1, 2, 3]
            return cli_mode(args)
        else:
            # Interactive mode
            return interactive_mode()

    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user\n")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

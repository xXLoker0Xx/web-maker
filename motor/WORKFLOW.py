#!/usr/bin/env python3
"""
=============================================================================
    AMAZON NICHE PAGE GENERATOR - TWO-STEP WORKFLOW
=============================================================================

This refactored motor (engine) separates scraping from AI analysis,
allowing you to:

1. Run STEP 1 (Scraping) → Extract products from Amazon (reusable JSON)
2. Run STEP 2 (AI Analysis) → Enrich with AI-generated content (pros/cons)
3. Skip scraping if you already have JSON from previous runs
4. Iterate on AI prompts without re-scraping

=============================================================================
    QUICK START
=============================================================================

1. Open a terminal in this directory (motor/)

2. Activate the virtual environment:
   Windows:  .\venv\Scripts\Activate.ps1
   Linux/Mac: source venv/bin/activate

3. Run the CLI menu:
   python cli.py

4. Choose an option:
   1 = STEP 1: Scrape Amazon
   2 = STEP 2: AI Analysis (enrich existing JSON)
   3 = FULL PIPELINE (Step 1 + 2 automatically)
   4 = Exit

=============================================================================
    DETAILED WORKFLOW
=============================================================================

STEP 1: SCRAPING ONLY
─────────────────────
Command:  python steps/step1_scraper_only.py

What it does:
  • Extracts 48+ products from Amazon search results using Playwright
  • Creates raw JSON with basic product info (no AI)
  • Saves to: plantilla-astro/src/content/niches/{niche-slug}.json

Output structure:
  {
    "title": "Los 5 mejores productos en freidoras de aire de 2026",
    "description": "...",
    "intro": "...",
    "verdict": "...",
    "products": [
      {
        "asin": "B0G7HSS6JP",
        "title": "Product Name",
        "price": "54,",
        "rating": 0.0,
        "reviews_count": 0,
        "badge": "Opción 1",  # Will be replaced by AI
        "pros": [],           # Empty - will be filled by AI
        "cons": [],           # Empty - will be filled by AI
        "summary": "...",     # Will be improved by AI
        "image_url": "...",
        "affiliate_url": "..."
      },
      ...
    ]
  }

Why separate scraping?
  • Scraping is SLOW (1-2 minutes per niche) - only do it once
  • Reuse the same JSON for multiple AI iterations
  • Fix products/prices without re-scraping
  • Build a product database for future uses


STEP 2: AI ANALYSIS
───────────────────
Command:  python steps/step2_ai_analysis.py {niche-slug}

What it does:
  • Reads existing JSON from Step 1
  • Generates AI content (pros, cons, summaries)
  • Uses Ollama, OpenAI, Claude, or DeepSeek
  • Preserves original product data (images, prices, ratings)

AI providers (tried in this order):
  1. Ollama (local, free) - RECOMMENDED
     Requirements: https://ollama.ai
     Setup:
       $ ollama serve           (terminal 1)
       $ ollama pull mistral    (terminal 2)
  
  2. OpenAI (costs money)
     Setup: .env → OPENAI_API_KEY=sk-...
  
  3. Claude/Anthropic (costs money)
     Setup: .env → ANTHROPIC_API_KEY=claude-...
  
  4. DeepSeek (costs money)
     Setup: .env → DEEPSEEK_API_KEY=sk-...

Output enriched fields:
  • product.badge: "Mejor Calidad", "Mejor Precio", etc.
  • product.pros: ["Feature 1", "Feature 2", ...]
  • product.cons: ["Drawback 1", "Drawback 2", ...]
  • product.summary: Improved description

Why separate AI analysis?
  • Iterate on prompts without re-scraping
  • Test different AI providers quickly
  • Fix/improve descriptions without re-scraping
  • Save time and money on scraping operations

=============================================================================
    EXAMPLES
=============================================================================

EXAMPLE 1: Full workflow (scrape → AI → done)
──────────────────────────────────────────────
$ python cli.py
→ Select option 3 (FULL PIPELINE)
→ Enter: "Freidoras de Aire"
→ Enter: 1 (one page)
→ AI analysis starts automatically
→ Result: freidoras-de-aire.json (complete with AI)
→ Deploy: cd ../plantilla-astro && npm run build && vercel --prod


EXAMPLE 2: Reuse scraped data (optimize AI)
─────────────────────────────────────────────
Step 1 (done earlier):
$ python steps/step1_scraper_only.py
→ Created: freidoras-de-aire.json (with empty pros/cons)

Step 2 (now):
$ python steps/step2_ai_analysis.py freidoras-de-aire
→ Enriches existing JSON with AI content
→ Same JSON file, now with pros/cons filled
→ Cost: Only AI API calls, NO scraping

Iterate on AI (if not happy with results):
$ python steps/step2_ai_analysis.py freidoras-de-aire
→ Runs AI again with potentially better prompts
→ Each run is faster (no scraping)


EXAMPLE 3: Multiple niches from command line
──────────────────────────────────────────────
# Niche 1
python steps/step1_scraper_only.py
# → freidoras-de-aire.json

# Niche 2
python steps/step1_scraper_only.py
# → cafeteras.json

# Enrich all with AI
python steps/step2_ai_analysis.py freidoras-de-aire
python steps/step2_ai_analysis.py cafeteras

# Rebuild and deploy once
cd ../plantilla-astro && npm run build && vercel --prod

=============================================================================
    TROUBLESHOOTING
=============================================================================

❌ "Ollama not available"
   ✓ Make sure Ollama is running:
     - Install: https://ollama.ai
     - Run in terminal: ollama serve
     - In another terminal: ollama pull mistral
     - Then retry Step 2

❌ "No AI provider available"
   ✓ Use one of these:
     - Ollama (free, local): https://ollama.ai
     - OpenAI: Add OPENAI_API_KEY to .env
     - Claude: Add ANTHROPIC_API_KEY to .env
     - DeepSeek: Add DEEPSEEK_API_KEY to .env

❌ "Comparison table not showing"
   ✓ Make sure:
     - products have "title" field
     - products have "pros" and "cons" arrays (can be empty)
     - Run npm run build to regenerate HTML
     - Deploy with vercel --prod

❌ "Playwright browser not found"
   ✓ Install browsers:
     $ python -m playwright install

=============================================================================
    FILE STRUCTURE
=============================================================================

motor/
├── cli.py                         # Main menu (choose workflow)
├── main.py                        # Original full pipeline (still works)
├── scraper.py                     # Playwright-based Amazon scraper
├── ai_generator.py                # AI provider integrations
├── internet_search.py             # Find buying criteria
├── database.py                    # SQLite product cache
├── steps/                         # New modular workflow
│   ├── __init__.py
│   ├── step1_scraper_only.py      # Pure scraping (no AI)
│   └── step2_ai_analysis.py       # AI enrichment
├── requirements.txt               # Python dependencies
├── local_cache.db                 # SQLite database (auto-created)
└── .env.example                   # Copy to .env and add API keys

plantilla-astro/
├── src/
│   ├── content/
│   │   └── niches/                # JSON files from motor output
│   │       ├── freidoras-de-aire.json
│   │       └── balon-de-futbol.json
│   ├── components/
│   │   ├── ProductCard.astro      # Single product card
│   │   └── ComparisonTable.astro  # Comparison table/cards
│   └── pages/
│       ├── index.astro            # Homepage
│       ├── [slug].astro           # Dynamic niche pages
│       ├── afiliados.astro        # Affiliate disclaimer
│       ├── aviso-legal.astro      # Legal notice
│       └── politica-de-privacidad.astro
├── npm run build                  # Generate static HTML
└── npm run dev                    # Local preview (for testing)

=============================================================================
    BEST PRACTICES
=============================================================================

1. Scraping (Step 1)
   • Only run once per niche (takes 1-2 minutes)
   • Store the JSON file safely
   • Reuse for multiple AI iterations

2. AI Analysis (Step 2)
   • Start with Ollama (free, local)
   • If results are poor, try OpenAI or Claude
   • Iterate on prompts before deploying
   • Run multiple times to test variations

3. Deployment
   • Always run: cd plantilla-astro && npm run build
   • Verify HTML in dist/ folder contains pros/cons
   • Deploy with: vercel --prod
   • Test in browser before declaring complete

4. Adding New Niches
   • For 5 niches: ~5-10 minutes total (1-2 min per niche × 5)
   • Scrape all 5 first (Step 1 × 5)
   • Enrich all 5 with AI (Step 2 × 5)
   • Build and deploy once

=============================================================================
"""

if __name__ == "__main__":
    print(__doc__)

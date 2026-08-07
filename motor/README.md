# Content Generation Workflow

High-performance three-step content generation pipeline with integrated Amazon product scraping.

## Quick Start

### Interactive Mode (Recommended)
```bash
cd motor
python main.py
```

**Menu Options:**
```
  [1] 🌐 Scraping only (extract products from Amazon)
  [2] 🤖 AI only (generate content for existing niches)
  [3] 🔄 Scraping + AI (scrape then generate content)
  [4] 🔧 Advanced options
  [5] Exit
```

### CLI Mode (Automation)
```bash
# Interactive menu
python main.py

# Generate all niches
python main.py --step 1 2 3

# Specific niche
python main.py --niche freidoras

# Specific steps only
python main.py --step 1 2

# Regenerate everything
python main.py --force

# Custom Ollama model
python main.py --model llama3.2
```

## How It Works

### Option [1]: Scraping Only
Extract Amazon product data and save to JSON:
- Search Amazon for products
- Extract: ASIN, title, price, rating, image URL
- Save to JSON file in `plantilla-astro/src/content/niches/`
- Ready for AI generation in next step

*Time: ~60-120 seconds for 3 pages*

### Option [2]: AI Only
Generate content for existing niches (Steps 1-3):
- Reads existing JSON files
- Generates intro, verdict, buying criteria
- Generates FAQ items
- Generates pros/cons for each product

*Time: ~70-110 seconds per niche*

### Option [3]: Scraping + AI (Recommended)
End-to-end workflow:
1. Scrape Amazon products
2. Generate intro texts
3. Generate FAQ
4. Generate pros/cons
5. Save complete JSON ready for Astro

*Time: ~150-200 seconds total*

---

## Detailed Steps (Option [3] Workflow)

### Step 1: Intro Texts
Generates high-quality introductory content:
- **Title** (8-12 words, includes year)
- **Description** (meta-optimized for LLMs)
- **Intro** (200-300 words with authority signals)
- **Verdict** (150-200 words with key differentiators)
- **Buying Criteria** (5-7 key factors)

*Time: ~20-30 seconds per niche*

### Step 2: FAQ Generation
Creates semantic, LLM-friendly Q&A content:
- **7-8 FAQ items** (real user questions)
- **Context-aware** (uses Step 1 output)
- **Structured HTML** (semantic `<details>` elements)
- **One fact per paragraph** (AI-extraction optimized)

*Time: ~20-30 seconds per niche*

### Step 3: Pros & Cons
Generates product-specific advantages/disadvantages:
- **3-10 pros** per product (specific benefits)
- **2-5 cons** per product (honest limitations)
- **Context-aware** (uses Step 2 FAQ concerns)
- **Balanced perspective** (E-E-A-T optimized)

*Time: ~30-50 seconds per niche*

## Architecture

### Core Components

| File | Purpose |
|------|---------|
| `main.py` | Entry point with interactive menu + CLI interface |
| `run_specialized_workflow.py` | Three-step orchestration engine |
| `run_specialized_workflow.py` | SpecializedPrompts class with focused prompts |
| `scraper.py` | Product data collection from Amazon |
| `ai_generator.py` | Legacy AI providers (reference only) |

### Data Pipeline

```
Products (JSON) 
    ↓
Step 1: Generate intro/buying criteria
    ↓
Step 2: Generate FAQ (using Step 1 context)
    ↓
Step 3: Generate pros/cons (using Step 2 context)
    ↓
Publish to plantilla-astro/src/content/niches/
```

## Output Format

Generated JSON files contain:
```json
{
  "title": "Best [Product] 2024: [Value Prop]",
  "description": "Meta-optimized description...",
  "intro": "Long-form introduction...",
  "verdict": "Summary and differentiators...",
  "buying_criteria": ["Factor 1", "Factor 2", ...],
  "products": [
    {
      "title": "...",
      "price": "...",
      "pros": ["Pro 1", "Pro 2", ...],
      "cons": ["Con 1", "Con 2", ...],
      ...
    }
  ],
  "faq": [
    {
      "question": "¿Question?",
      "answer": "Detailed answer..."
    }
  ]
}
```

## Configuration

### Environment Variables
Create `.env` file in `motor/` directory:

```env
# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral

# Development
DEBUG=false
LOG_LEVEL=INFO
```

### Supported Ollama Models
- `mistral` (recommended - fast, good quality)
- `llama3`
- `llama3.2`

Test connectivity:
```bash
curl http://localhost:11434/api/tags
```

## Performance

Typical generation times:

| Step | Time |
|------|------|
| Step 1 | 20-30s |
| Step 2 | 20-30s |
| Step 3 | 30-50s |
| **Total** | **70-110s** |

## Requirements

- Python 3.8+
- Ollama running (default: `http://localhost:11434`)
- Packages: `requests`, `python-dotenv`

## Quality Assurance

All generated content follows these principles:

✅ **E-E-A-T**: Experience, Expertise, Authoritativeness, Trustworthiness  
✅ **GEO**: Optimized for Generative Engine Optimization (AI extraction)  
✅ **Semantic HTML**: Structured data for LLMs  
✅ **One fact per paragraph**: Clear, scannable content  
✅ **Balanced perspective**: Honest pros AND cons  
✅ **Brand accuracy**: Exact model numbers and terminology  

## Troubleshooting

### "No JSON files found"
- Check: `plantilla-astro/src/content/niches/` contains `*.json` files
- Ensure niche name matches JSON filename (without `.json`)

### "Cannot connect to Ollama"
- Check: Ollama is running on `http://localhost:11434`
- Test: `curl http://localhost:11434/api/tags`
- If not running: `ollama serve`

### Content quality issues
- Try regenerating with `--force`
- Use different model: `python main.py --model llama3.2`
- Check FAQ validation in `run_specialized_workflow.py`

## Next Steps

1. ✅ Generate content: `python main.py`
2. ✅ Review in `plantilla-astro/src/content/niches/`
3. ✅ Build site: `cd plantilla-astro && npm run build`
4. ✅ Deploy: `vercel --prod`

---

**Status**: Production Ready ✓  
**Last Updated**: 2026-08-06

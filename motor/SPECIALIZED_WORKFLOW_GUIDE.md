# 🚀 Specialized Three-Step Content Generation Workflow

**Status: ✅ Production Ready**

New simplified and optimized workflow for generating high-quality affiliate content with E-E-A-T signals and GEO optimization.

## 🎯 Why This Workflow?

### The Problem with Single-Pass Generation
The original monolithic AI generation was:
- ❌ Generating all content in one pass (too overwhelming for AI)
- ❌ Skipping pros/cons when generating FAQs simultaneously
- ❌ Failing validation due to mixing multiple generation tasks
- ❌ Producing generic, thin-affiliate content without E-E-A-T

### The Solution: Specialized Focused Prompts
The new workflow uses **3 separate, focused prompts**:

```
Step 1: Generate ONLY intro texts
   ↓ (title, description, intro, verdict, buying_criteria)
   ↓
Step 2: Generate ONLY FAQs (using intro as context)
   ↓ (7-8 questions with 80-120 word answers)
   ↓
Step 3: Generate ONLY pros/cons (using FAQ concerns as context)
   ↓ (3-10 pros, 2-5 cons per product)
```

## 📊 Quick Stats

- **Step 1 (Intro)**: ~20-30 seconds per niche
- **Step 2 (FAQ)**: ~30-40 seconds per niche
- **Step 3 (Pros/Cons)**: ~20-30 seconds per niche
- **Total**: ~70-100 seconds per niche
- **Output Quality**: Production-ready with E-E-A-T signals

## 🔧 Usage

### Basic Usage (All Steps, All Niches)
```bash
cd motor
python run_specialized_workflow.py
```

### Run Specific Steps
```bash
# Only Step 1 (intro texts)
python run_specialized_workflow.py --step 1

# Steps 1 and 2
python run_specialized_workflow.py --step 1 2

# All steps (default)
python run_specialized_workflow.py --step 1 2 3
```

### Process Specific Niche
```bash
# Only process 'freidoras' niche
python run_specialized_workflow.py --niche freidoras

# Process 'balones' niche, step 2 only
python run_specialized_workflow.py --niche balones --step 2
```

### Force Regeneration
```bash
# Regenerate everything, even if already done
python run_specialized_workflow.py --force

# Regenerate only freidoras
python run_specialized_workflow.py --niche freidoras --force

# Regenerate only Step 3 (pros/cons)
python run_specialized_workflow.py --step 3 --force
```

### Change Ollama Model
```bash
# Use llama3.2 instead of mistral
python run_specialized_workflow.py --model llama3.2

# Use llama3
python run_specialized_workflow.py --model llama3
```

### Complete Example: Regenerate Everything for One Niche
```bash
python run_specialized_workflow.py --niche freidoras --force --model mistral
```

## 📁 File Structure

Input files (from Step 1 scraping):
```
plantilla-astro/src/content/niches/
├── freidoras-de-aire.json          (products + metadata)
└── balones-de-futbol.json          (products + metadata)
```

Output structure after workflow:
```json
{
  "niche": "freidoras de aire",
  "title": "...",
  "description": "...",
  "intro": "...",
  "verdict": "...",
  "buying_criteria": [...],
  "products": [
    {
      "asin": "...",
      "title": "...",
      "pros": ["...", "..."],
      "cons": ["...", "..."]
    }
  ],
  "faq": [
    {
      "question": "¿...?",
      "answer": "..."
    }
  ]
}
```

## 🎨 E-E-A-T + GEO Features

### Experience
- First-person buyer perspective language
- Practical, actionable advice
- Real examples with prices and specs

### Expertise
- Buying criteria clearly explained
- Warranty/guarantee information
- Years in market mentioned
- Comparative analysis

### Authoritativeness
- Exact brand names and model numbers
- Specific prices and specifications
- Authority signals ("our team of experts")
- Professional writing style

### Trustworthiness
- One fact per paragraph
- Specific numbers, not generic statements
- Balanced pros and cons
- Honest limitations mentioned
- FAQ answers 80-120 words each

### GEO Optimization
- Title with year (2024/2025)
- Meta description optimized for LLM extraction
- Keywords naturally integrated
- Structured FAQ for LLM parsing
- Product specs formatted for zero-click answers

## 🛠️ Behind the Scenes

### How It Works

**Step 1: Intro Texts Prompt**
```python
# Focused only on:
# - title (8-12 words, keyword-natural, year included)
# - description (150-160 chars, meta-optimized)
# - intro (200-300 words, hook + authority + price ranges)
# - verdict (150-200 words, price/capacity/warranty info)
# - buying_criteria (3-7 factors)
```

**Step 2: FAQ Prompt**
```python
# Uses intro from Step 1 as context
# Generates 7-8 questions related to buying_criteria
# Each answer: 80-120 words, specific examples
# Topics: capacity, power, safety, maintenance, warranty, etc.
```

**Step 3: Pros/Cons Prompt**
```python
# Uses FAQ questions as context
# Generates 3-10 pros per product
# Generates 2-5 cons per product
# Pros/cons relate to FAQ concerns (better relevance)
```

### Why Specialized Prompts Work Better
1. **Single Focus**: Each prompt has ONE job
2. **Context Chaining**: Each step uses previous output
3. **Less Hallucination**: AI less overwhelmed
4. **Better Quality**: Each output is specialized
5. **Faster Iteration**: Can regenerate one step without affecting others

## 📋 Verification Checklist

After running workflow:

- [ ] Title: 8-12 words, includes year (e.g., "2025")
- [ ] Description: 150-160 chars, starts with category + keyword
- [ ] Intro: 200-300 words, mentions authority and price ranges
- [ ] Verdict: 150-200 words, explains each product type
- [ ] Buying Criteria: 3-7 specific decision factors
- [ ] FAQ: 7-8 questions with 80-120 word answers
- [ ] Pros: 3-10 per product, relate to FAQ concerns
- [ ] Cons: 2-5 per product, balanced and honest
- [ ] All text in Spanish (or specified language)

## 🚀 Next Steps

### 1. Review Generated Content
```bash
# Check the JSON files
ls -la plantilla-astro/src/content/niches/

# Or open in editor
code plantilla-astro/src/content/niches/freidoras-de-aire.json
```

### 2. Build and Test Locally
```bash
cd plantilla-astro
npm run build      # Check for errors
npm run dev        # Run local server
# Visit http://localhost:3000
```

### 3. Generate More Niches
```bash
cd motor

# Create new niche JSON with products
# Then run:
python run_specialized_workflow.py --niche new-niche

# Or create multiple niches at once
python run_specialized_workflow.py
```

### 4. Deploy to Production
```bash
cd plantilla-astro
npm run build
vercel --prod      # Or your deploy command
```

## 🔧 Troubleshooting

### "Cannot connect to Ollama"
```bash
# Make sure Ollama is running:
ollama serve

# In another terminal, verify model:
ollama list
# Should show: mistral, llama3.2, llama3
```

### "Invalid JSON in response"
- Ollama might be generating non-JSON output
- Try with a simpler niche or less product data
- Increase timeout: `--timeout 600000`

### "FAQ validation failed"
- Ensure Step 1 completed successfully (has intro)
- Check that products are valid JSON
- Try again with: `python run_specialized_workflow.py --step 2 --force`

### "Pros/cons not generating"
- Ensure Step 2 completed (has FAQ array)
- Check FAQ array has 7+ items
- Run with: `python run_specialized_workflow.py --step 3 --force`

## 📞 Support

If issues persist:
1. Check Ollama logs: `ollama logs`
2. Verify network: `curl http://localhost:11434/api/tags`
3. Try different model: `python run_specialized_workflow.py --model llama3.2`
4. Check JSON formatting: `python -m json.tool freidoras-de-aire.json`

## 📚 Related Files

- `run_specialized_workflow.py` - Main workflow script (this is the one to use)
- `ai_generator.py` - Core AI provider classes
- `plantilla-astro/src/pages/[slug].astro` - Dynamic page template
- `plantilla-astro/src/components/FAQSection.astro` - FAQ rendering
- `plantilla-astro/src/components/ProductCard.astro` - Product rendering

---

**Generated with ❤️ for high-quality, E-E-A-T optimized affiliate content**

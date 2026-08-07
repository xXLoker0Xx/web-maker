#!/usr/bin/env python3
"""
Specialized Three-Step Workflow with Custom Prompts
Each step has its own focused prompt to maximize generation quality
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import argparse
import os
import requests


class SpecializedPrompts:
    """Specialized prompts for each workflow step"""
    
    @staticmethod
    def intro_texts_prompt(products: List[Dict], niche: str, buying_criteria: List[str]) -> str:
        """Prompt for Step 1: Generate intro texts ONLY"""
        
        product_list = "\n".join([
            f"- {p.get('title', 'Unknown')} (${p.get('price', 'N/A')}, Rating: {p.get('rating', 'N/A')}★)"
            for p in products
        ])
        
        criteria_str = "\n".join(f"- {c}" for c in buying_criteria) if buying_criteria else "- Quality\n- Price\n- Performance"
        
        return f"""You are an expert product reviewer. Generate introduction content for a product comparison article about: {niche}

PRODUCTS TO ANALYZE:
{product_list}

KEY BUYING CRITERIA:
{criteria_str}

Generate ONLY these 5 fields (in JSON format):
1. "title" - SEO-optimized title (8-12 words, includes "2026", format: "Los X mejores [PRODUCT] 2026: [DIFFERENTIATOR]")
2. "description" - Meta description (150-160 chars, starts with category + keyword, includes benefit and price range)
3. "intro" - Introduction text (200-300 words, starts with buyer problem/opportunity, mentions authority signals and price/capacity ranges)
4. "verdict" - Final summary (150-200 words, explains why each product type matters, mentions warranty/guarantee info, price ranges)
5. "buying_criteria" - Array of 3-7 buying decision factors

Requirements:
- All text must be in Spanish
- One fact per paragraph
- Include specific numbers, prices, and specs where applicable
- Optimize for LLM extraction
- NO pros/cons, NO FAQ items in this step
- Build E-E-A-T signals (Experience, Expertise, Authoritativeness, Trustworthiness)

Return ONLY valid JSON, no markdown, no comments.

Generate now:"""
    
    @staticmethod
    def faq_prompt(niche: str, intro: str, buying_criteria: List[str], products: List[Dict]) -> str:
        """Prompt for Step 2: Generate FAQ ONLY"""
        
        product_titles = ", ".join([p.get('title', '')[:40] for p in products[:3]])
        criteria_str = "\n".join(f"- {c}" for c in buying_criteria) if buying_criteria else "- Quality\n- Price\n- Features"
        
        return f"""You are a helpful product advisor creating FAQ content for: {niche}

CONTEXT FROM ARTICLE:
- Intro: {intro[:300]}...
- Key Criteria: {criteria_str}
- Top Products: {product_titles}

Generate ONLY a JSON object with exactly this structure:
{{
  "faq": [
    {{"question": "¿...?", "answer": "..."}},
    ... (repeat for total of 7-8 items)
  ]
}}

Requirements:
- 7-8 FAQ items total
- Each question: practical buyer question (starts with "¿" in Spanish)
- Each answer: 80-120 words, specific and actionable
- Topics should cover: size/capacity, power/efficiency, safety, best practices, maintenance, alternatives, value, warranty
- Answers must use one fact per paragraph
- Include specific numbers/specs where relevant
- Optimize for LLM extraction
- ALL TEXT IN SPANISH

Return ONLY the JSON object, no markdown or comments.

Generate now:"""
    
    @staticmethod
    def pros_cons_prompt(niche: str, products: List[Dict], faq_questions: List[str], buying_criteria: List[str]) -> str:
        """Prompt for Step 3: Generate pros/cons ONLY"""
        
        product_list = "\n".join([
            f"\nProduct {i+1}: {p.get('title', 'Unknown')}\nPrice: ${p.get('price', 'N/A')}\nRating: {p.get('rating', 'N/A')}★"
            for i, p in enumerate(products)
        ])
        
        faq_context = "\n".join(f"- {q}" for q in faq_questions[:5]) if faq_questions else ""
        criteria_str = "\n".join(f"- {c}" for c in buying_criteria) if buying_criteria else ""
        
        return f"""You are a product expert analyzing {niche} products for an affiliate comparison article.

PRODUCTS TO ANALYZE:
{product_list}

KEY BUYING CRITERIA:
{criteria_str}

COMMON BUYER CONCERNS (from FAQ):
{faq_context}

Generate a JSON object with pros and cons for EACH product. Structure:
{{
  "products": [
    {{
      "asin": "ORIGINAL_ASIN",
      "pros": ["pro1", "pro2", ...],
      "cons": ["con1", "con2", ...]
    }},
    ... (one object per product)
  ]
}}

Requirements:
- 3-10 pros per product (focus on quality, not quantity)
- 2-5 cons per product (realistic, balanced)
- Each pro/con is 1-2 short sentences in Spanish
- Pros should relate to buying criteria and FAQ concerns
- Cons should be specific and actionable (not generic)
- Include warranty/durability info in pros where relevant
- Be honest about limitations
- Optimize for LLM extraction

Return ONLY valid JSON, no markdown.

Generate now:"""


class SpecializedWorkflow:
    """Three-step workflow with specialized prompts"""
    
    def __init__(self):
        load_dotenv()
        self.ollama_url = "http://localhost:11434"
        self.model = 'qwen3:14b'
        self.timeout = 300  # 5 minutes per request
    
    def init_ollama(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = set([m.get('name', '') for m in models])
                print(f"✓ Ollama conectado en {self.ollama_url}")
                print(f"  Modelos disponibles: {', '.join(sorted(model_names))}")
                
                # Verify model is available
                if self.model not in model_names:
                    print(f"⚠️  Model '{self.model}' not found, using first available")
                    if models:
                        self.model = models[0].get('name', '')
                
                print(f"  Usando modelo: {self.model}")
                return True
            return False
        except Exception as e:
            print(f"✗ Cannot connect to Ollama: {e}")
            print("  Make sure Ollama is running: ollama serve")
            return False
    
    def call_ollama(self, prompt: str) -> Optional[str]:
        """Call Ollama directly with raw prompt"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                print(f"   ✗ Ollama error: {response.status_code}")
                return None
                
        except requests.Timeout:
            print(f"   ✗ Ollama call timed out (>{self.timeout}s)")
            return None
        except Exception as e:
            print(f"   ✗ Ollama call failed: {e}")
            return None
    
    def extract_json_from_response(self, response: str) -> Optional[Dict]:
        """Extract JSON from response text"""
        if not response:
            return None
        
        # Try to find JSON block
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return None
        
        return None
    
    def find_niche_dir(self) -> Path:
        """Find niche directory - try multiple paths"""
        # Try relative from current working directory
        niche_dir = Path.cwd() / 'plantilla-astro' / 'src' / 'content' / 'niches'
        if niche_dir.exists():
            return niche_dir
        
        # Try from motor directory (where this script is)
        niche_dir = Path(__file__).parent / '..' / 'plantilla-astro' / 'src' / 'content' / 'niches'
        if niche_dir.exists():
            return niche_dir.resolve()
        
        # Try parent directories
        niche_dir = Path(__file__).parent.parent / 'plantilla-astro' / 'src' / 'content' / 'niches'
        if niche_dir.exists():
            return niche_dir.resolve()
        
        # Last resort: check home directory project
        niche_dir = Path.home() / 'Proyectos' / '19.Web_Maker' / 'plantilla-astro' / 'src' / 'content' / 'niches'
        if niche_dir.exists():
            return niche_dir.resolve()
        
        print(f"✗ Tried paths:")
        print(f"  1. {Path.cwd() / 'plantilla-astro' / 'src' / 'content' / 'niches'}")
        print(f"  2. {(Path(__file__).parent / '..' / 'plantilla-astro' / 'src' / 'content' / 'niches').resolve()}")
        print(f"  3. {(Path(__file__).parent.parent / 'plantilla-astro' / 'src' / 'content' / 'niches').resolve()}")
        raise FileNotFoundError("Cannot find niches directory")
    
    def step_1_intro_texts(self, json_file: Path, force: bool = False) -> bool:
        """Step 1: Generate intro texts (title, description, intro, verdict, buying_criteria)"""
        print(f"\n📝 STEP 1: Intro Texts for {json_file.stem}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products = data.get('products', [])
        niche = json_file.stem
        buying_criteria = data.get('buying_criteria', [])
        
        if not products:
            print("   ✗ No products found")
            return False
        
        # Generate prompt and call Ollama
        prompt = SpecializedPrompts.intro_texts_prompt(products, niche, buying_criteria)
        
        print("   🤖 Calling Ollama...")
        response = self.call_ollama(prompt)
        
        if not response:
            print("   ✗ No response from Ollama")
            return False
        
        # Extract JSON
        content = self.extract_json_from_response(response)
        if not content:
            print("   ✗ Could not extract JSON")
            return False
        
        # Update data
        updated = False
        for field in ['title', 'description', 'intro', 'verdict', 'buying_criteria']:
            if field in content and content[field]:
                data[field] = content[field]
                if field == 'buying_criteria':
                    print(f"   ✓ {field}: {len(content[field])} items")
                elif len(str(content[field])) > 60:
                    print(f"   ✓ {field}: {str(content[field])[:60]}...")
                else:
                    print(f"   ✓ {field}: OK")
                updated = True
        
        if not updated:
            print("   ✗ No valid fields extracted")
            return False
        
        # Save
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"   ✓ Saved: {json_file.name}")
        return True
    
    def step_2_faq(self, json_file: Path, force: bool = False) -> bool:
        """Step 2: Generate FAQ"""
        print(f"\n❓ STEP 2: FAQ for {json_file.stem}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check prerequisites
        if not data.get('intro'):
            print("   ⚠️  No intro text. Run Step 1 first")
            return False
              
        niche = json_file.stem
        intro = data.get('intro', '')
        buying_criteria = data.get('buying_criteria', [])
        products = data.get('products', [])
        
        # Generate prompt
        prompt = SpecializedPrompts.faq_prompt(niche, intro, buying_criteria, products)
        
        print("   🤖 Calling Ollama...")
        response = self.call_ollama(prompt)
        
        if not response:
            print("   ✗ No response from Ollama")
            return False
        
        # Extract JSON
        content = self.extract_json_from_response(response)
        if not content or 'faq' not in content:
            print("   ✗ No FAQ in response")
            return False
        
        faq_items = content['faq']
        if not faq_items or len(faq_items) < 7:
            print(f"   ✗ Only {len(faq_items)} FAQ items (need 7+)")
            return False
        
        data['faq'] = faq_items
        print(f"   ✓ Generated {len(faq_items)} FAQ items")
        
        # Show first 3
        for i, item in enumerate(faq_items[:3], 1):
            q = item.get('question', '')[:60] if isinstance(item, dict) else ''
            print(f"      {i}. {q}...")
        
        # Save
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    
    def step_3_pros_cons(self, json_file: Path, force: bool = False) -> bool:
        """Step 3: Generate pros/cons"""
        print(f"\n⭐ STEP 3: Pros/Cons for {json_file.stem}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check prerequisites
        if not data.get('faq'):
            print("   ⚠️  No FAQ. Run Step 2 first")
            return False
        
        products = data.get('products', [])
        if not products:
            print("   ✗ No products")
            return False
        
        # Skip if already done
        if not force:
            all_done = all(
                p.get('pros') and len(p['pros']) > 0 and p.get('cons') and len(p['cons']) > 0
                for p in products
            )
            if all_done:
                print(f"   ⏭️  All products have pros/cons")
                return True
        
        niche = json_file.stem
        faq_questions = [f.get('question', '') for f in data.get('faq', []) if f.get('question')]
        buying_criteria = data.get('buying_criteria', [])
        
        # Generate prompt
        prompt = SpecializedPrompts.pros_cons_prompt(niche, products, faq_questions, buying_criteria)
        
        print("   🤖 Calling Ollama...")
        response = self.call_ollama(prompt)
        
        if not response:
            print("   ✗ No response from Ollama")
            return False
        
        # Extract JSON
        content = self.extract_json_from_response(response)
        if not content or 'products' not in content:
            print("   ✗ No products in response")
            return False
        
        # Map back to original products
        gen_products = content['products']
        for i, gen_prod in enumerate(gen_products):
            if i < len(products):
                if gen_prod.get('pros'):
                    products[i]['pros'] = gen_prod['pros']
                    print(f"   ✓ Product {i+1}: {len(gen_prod['pros'])} pros")
                
                if gen_prod.get('cons'):
                    products[i]['cons'] = gen_prod['cons']
                    print(f"   ✓ Product {i+1}: {len(gen_prod['cons'])} cons")
        
        data['products'] = products
        
        # Save
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    
    def run(self, steps: List[int], niche_filter: Optional[str] = None, force: bool = False):
        """Run workflow"""
        print("\n" + "="*70)
        print("🚀 SPECIALIZED THREE-STEP WORKFLOW")
        print("="*70)
        
        if not self.init_ollama():
            print("✗ Cannot initialize Ollama")
            return 1
        
        try:
            niche_dir = self.find_niche_dir()
            print(f"✓ Niche directory: {niche_dir}\n")
        except FileNotFoundError as e:
            print(f"✗ {e}")
            return 1
        
        # Find files
        if niche_filter:
            json_files = list(niche_dir.glob(f'{niche_filter}*.json'))
        else:
            json_files = list(niche_dir.glob('*.json'))
        
        if not json_files:
            print(f"✗ No JSON files found")
            return 1
        
        print(f"✓ Found {len(json_files)} file(s)\n")
        
        # Process each file
        for json_file in sorted(json_files):
            print(f"\n{'='*70}")
            print(f"📂 {json_file.name}")
            print('='*70)
            
            success_count = 0
            
            # Step 1
            if 1 in steps:
                if self.step_1_intro_texts(json_file, force):
                    success_count += 1
                else:
                    print("   ⚠️  Skipping remaining steps")
                    continue
            
            # Step 2
            if 2 in steps:
                if self.step_2_faq(json_file, force):
                    success_count += 1
                else:
                    print("   ⚠️  Skipping Step 3")
                    continue
            
            # Step 3
            if 3 in steps:
                if self.step_3_pros_cons(json_file, force):
                    success_count += 1
        
        print("\n" + "="*70)
        print("✓ WORKFLOW COMPLETE!")
        print("="*70)
        print("\nNext steps:")
        print("  1. Review content in plantilla-astro/src/content/niches/")
        print("  2. Build: cd plantilla-astro && npm run build")
        print("  3. Test: npm run dev")
        print()
        
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Specialized Three-Step Workflow')
    parser.add_argument(
        '--step',
        type=int,
        nargs='+',
        choices=[1, 2, 3],
        default=[1, 2, 3],
        help='Steps to run (default: all)'
    )
    parser.add_argument(
        '--niche',
        help='Filter to specific niche'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Regenerate even if done'
    )
    parser.add_argument(
        '--model',
        default='qwen3:14b',
        help='Ollama model (default: qwen3:14b)'
    )
    
    args = parser.parse_args()
    
    workflow = SpecializedWorkflow()
    workflow.model = args.model
    
    sys.exit(workflow.run(args.step, args.niche, args.force))

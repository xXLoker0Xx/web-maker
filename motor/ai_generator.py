"""
AI content generator module.
Uses OpenAI/Anthropic/DeepSeek/Ollama to generate SEO-optimized content for niche pages.
"""

import json
import re
import requests
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def generate_niche_content(self, products: List[Dict[str, Any]], niche: str, buying_criteria: Optional[List[Dict[str, str]]] = None) -> Optional[Dict[str, Any]]:
        """Generate niche content from products."""
        pass
    
    def _format_products_for_prompt(self, products: List[Dict[str, Any]]) -> str:
        """Format products for AI prompt."""
        formatted = []
        for i, product in enumerate(products, 1):
            formatted.append(f"""
Producto {i}:
- ASIN: {product.get('asin')}
- Título: {product.get('title')}
- Precio: {product.get('price')}
- Valoración: {product.get('rating')} estrellas ({product.get('reviews_count')} reseñas)
- Características: {', '.join(product.get('features', []))}
""")
        return "\n".join(formatted)
    
    def _format_criteria_for_prompt(self, buying_criteria: Optional[List[Dict[str, str]]]) -> str:
        """Format buying criteria for AI prompt."""
        if not buying_criteria:
            return ""
        
        formatted = "\n5 CRITERIOS CLAVE DE COMPRA:\n"
        for i, criterion in enumerate(buying_criteria, 1):
            name = criterion.get('name', '')
            source = criterion.get('source', '')
            formatted += f"{i}. {name} (Fuente: {source})\n"
        
        return formatted
    
    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from text response."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    return None
            return None


class OpenAIProvider(AIProvider):
    """OpenAI API provider."""
    
    def __init__(self, api_key: str):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
        """
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4-turbo-preview"
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")
    
    def generate_niche_content(self, products: List[Dict[str, Any]], niche: str, buying_criteria: Optional[List[Dict[str, str]]] = None) -> Optional[Dict[str, Any]]:
        """
        Generate niche content using OpenAI.
        
        Args:
            products: List of product dictionaries
            niche: Niche topic/category
            buying_criteria: List of key buying criteria (5 points)
            
        Returns:
            Content dictionary or None if generation fails
        """
        try:
            products_json = self._format_products_for_prompt(products)
            criteria_section = self._format_criteria_for_prompt(buying_criteria) if buying_criteria else ""
            
            system_prompt = """Eres un experto en marketing de afiliados de Amazon y contenido SEO.
Tu tarea es generar análisis de productos de manera profesional y persuasiva.
IMPORTANTE: Debes responder SIEMPRE con un JSON válido, sin explicaciones adicionales.
"""
            
            user_prompt = f"""Analiza estos productos de Amazon para el nicho "{niche}" y genera un análisis completo en formato JSON.

PRODUCTOS:
{products_json}

{criteria_section}

Genera un JSON estricto con la siguiente estructura (sin texto adicional fuera del JSON):
{{
  "title": "Las X Mejores [Categoría] de 2026",
  "description": "Meta descripción SEO para la página (max 160 caracteres)",
  "buying_criteria": ["Criterio 1", "Criterio 2", "Criterio 3", "Criterio 4", "Criterio 5"],
  "intro": "Párrafo introductorio enfocado en conversión (200-300 palabras)",
  "verdict": "Conclusión y recomendación general (150-200 palabras)",
  "products": [
    {{
      "asin": "ASIN_ACTUAL",
      "short_title": "Título corto diferenciador (max 10 palabras)",
      "badge": "Insignia única como 'Mejor Calidad-Precio' o 'Mejor Rendimiento'",
      "pros": ["Pro 1", "Pro 2", "Pro 3", "Pro 4", "Pro 5"],
      "cons": ["Contra 1", "Contra 2", "Contra 3"],
      "summary": "Resumen único escrito por la IA (100-150 palabras)"
    }}
  ]
}}

Reglas:
- El título debe ser atractivo y contener la palabra clave principal
- La meta descripción debe incluir la palabra clave y ser atractiva
- El short_title debe ser diferenciador, corto (max 10 palabras) y único para cada producto
- buying_criteria: lista con los 5 criterios clave de clasificación
- Cada producto debe tener una insignia diferente
- Los pros (5) y contras (3) deben ser específicos al producto y relacionados con los 5 criterios clave
- El resumen debe ser único para cada producto, comparándolo respecto a los criterios clave
- Usa un tono profesional pero conversacional
- Incluye información sobre por qué cada producto es una buena compra basándote en los criterios
- Responde ÚNICAMENTE con el JSON, sin explicaciones adicionales."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            json_content = self._extract_json(content)
            if not json_content:
                print("✗ No se pudo extraer JSON de la respuesta")
                return None
            
            print("✓ Contenido generado por IA exitosamente")
            return json_content
            
        except Exception as e:
            print(f"✗ Error en OpenAI: {e}")
            return None


class AnthropicProvider(AIProvider):
    """Anthropic API provider."""
    
    def __init__(self, api_key: str):
        """
        Initialize Anthropic provider.
        
        Args:
            api_key: Anthropic API key
        """
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = "claude-3-opus-20240229"
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")
    
    def generate_niche_content(self, products: List[Dict[str, Any]], niche: str, buying_criteria: Optional[List[Dict[str, str]]] = None) -> Optional[Dict[str, Any]]:
        """
        Generate niche content using Claude.
        
        Args:
            products: List of product dictionaries
            niche: Niche topic/category
            buying_criteria: List of key buying criteria (5 points)
            
        Returns:
            Content dictionary or None if generation fails
        """
        try:
            products_json = self._format_products_for_prompt(products)
            criteria_section = self._format_criteria_for_prompt(buying_criteria) if buying_criteria else ""
            
            system_prompt = """Eres un experto en marketing de afiliados de Amazon y contenido SEO.
Tu tarea es generar análisis de productos de manera profesional y persuasiva.
Debes responder SIEMPRE con un JSON válido y bien formado."""
            
            user_prompt = f"""Analiza estos productos de Amazon para el nicho "{niche}" y genera un análisis completo en formato JSON.

PRODUCTOS:
{products_json}

{criteria_section}

Genera un JSON estricto con la siguiente estructura:
{{
  "title": "Las X Mejores [Categoría] de 2026",
  "description": "Meta descripción SEO para la página (max 160 caracteres)",
  "buying_criteria": ["Criterio 1", "Criterio 2", "Criterio 3", "Criterio 4", "Criterio 5"],
  "intro": "Párrafo introductorio enfocado en conversión (200-300 palabras)",
  "verdict": "Conclusión y recomendación general (150-200 palabras)",
  "products": [
    {{
      "asin": "ASIN_ACTUAL",
      "short_title": "Título corto diferenciador (max 10 palabras)",
      "badge": "Insignia única como 'Mejor Calidad-Precio'",
      "pros": ["Pro 1", "Pro 2", "Pro 3", "Pro 4", "Pro 5"],
      "cons": ["Contra 1", "Contra 2", "Contra 3"],
      "summary": "Resumen único (100-150 palabras)"
    }}
  ]
}}

Responde SOLO con el JSON válido."""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            content = response.content[0].text.strip()
            
            # Extract JSON from response
            json_content = self._extract_json(content)
            if not json_content:
                print("✗ No se pudo extraer JSON de la respuesta")
                return None
            
            print("✓ Contenido generado por IA exitosamente")
            return json_content
            
        except Exception as e:
            print(f"✗ Error en Anthropic: {e}")
            return None


class DeepSeekProvider(AIProvider):
    """DeepSeek API provider."""
    
    def __init__(self, api_key: str):
        """
        Initialize DeepSeek provider.
        
        Args:
            api_key: DeepSeek API key
        """
        try:
            from openai import OpenAI
            # DeepSeek uses OpenAI-compatible API
            self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
            self.model = "deepseek-chat"
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")
    
    def generate_niche_content(self, products: List[Dict[str, Any]], niche: str, buying_criteria: Optional[List[Dict[str, str]]] = None) -> Optional[Dict[str, Any]]:
        """
        Generate niche content using DeepSeek.
        
        Args:
            products: List of product dictionaries
            niche: Niche topic/category
            buying_criteria: List of key buying criteria (5 points)
            
        Returns:
            Content dictionary or None if generation fails
        """
        try:
            products_json = self._format_products_for_prompt(products)
            criteria_section = self._format_criteria_for_prompt(buying_criteria)
            
            system_prompt = """Eres un experto en marketing de afiliados de Amazon y contenido SEO.
Tu tarea es generar análisis de productos de manera profesional y persuasiva.
Debes responder SIEMPRE con un JSON válido."""
            
            user_prompt = f"""Analiza estos productos de Amazon para el nicho "{niche}" y genera un análisis completo.

PRODUCTOS:
{products_json}

{criteria_section}

Responde con este JSON (sin texto adicional):
{{
  "title": "Las X Mejores [Categoría] de 2026",
  "description": "Meta descripción SEO",
  "buying_criteria": ["Criterio 1", "Criterio 2", "Criterio 3", "Criterio 4", "Criterio 5"],
  "intro": "Párrafo introductorio (200-300 palabras)",
  "verdict": "Conclusión (150-200 palabras)",
  "products": [
    {{
      "asin": "ASIN",
      "short_title": "Título corto diferenciador",
      "badge": "Insignia única",
      "pros": ["Pro 1", "Pro 2", "Pro 3", "Pro 4", "Pro 5"],
      "cons": ["Contra 1", "Contra 2", "Contra 3"],
      "summary": "Resumen (100-150 palabras)"
    }}
  ]
}}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content.strip()
            json_content = self._extract_json(content)
            
            if not json_content:
                print("✗ No se pudo extraer JSON de la respuesta")
                return None
            
            print("✓ Contenido generado por IA (DeepSeek) exitosamente")
            return json_content
            
        except Exception as e:
            print(f"✗ Error en DeepSeek: {e}")
            return None


# === VERSIONED PROMPT ARCHITECTURE ===

class PromptV1:
    """Production-grade prompts for affiliate content generation (v1)."""
    
    SYSTEM_PROMPT = """You are an expert affiliate content strategist focused on helping buyers make confident purchasing decisions.

CORE PRINCIPLES:
1. Prioritize objectivity: Recommend products based on merit, not commission potential
2. Build trust: Acknowledge limitations, trade-offs, and be honest about who each product suits
3. Answer buying questions: Focus on "Who is this for?", "What are trade-offs?", "When choose this vs. that?"
4. Assume commercial intent: The reader is close to purchasing and needs decision-making clarity

STRICT ANTI-HALLUCINATION RULES:
- Never invent specifications. Only use provided data.
- Never invent certifications, awards, or testing results.
- Never fabricate user reviews or experiences.
- Never infer facts not in the provided data.
- If uncertain, omit rather than speculate.
- Prefer honest incompleteness over false completeness.

GEO OPTIMIZATION:
- Write for AI search engines (ChatGPT, Gemini, Claude, Perplexity)
- Structure so each major section answers a distinct buying question
- Make content independently understandable without context
- Prioritize semantic clarity over keyword density
- Use concise, direct language

RESPONSE:
Return ONLY valid JSON. No markdown, explanations, or extra text."""

    EDITORIAL_RULES = """CONTENT REQUIREMENTS:

Title (8-12 words, keyword-natural, GEO + E-E-A-T):
- Include primary keyword and year (e.g., 2026)
- Format: "Los/Las X Mejores [Category] de 2026: [Differentiator]"
- Example: "Los 5 mejores freidoras de aire 2026: Guía completa con comparativa"
- Benefit-focused and scannable

Meta Description (150-160 chars, E-E-A-T + GEO):
- Lead with category + keyword + year
- Include key benefit (health, efficiency, cost-saving, etc.)
- Mention quantity/range of products analyzed
- Add compelling differentiator (brand names, price range, unique angle)
- Example: "Comparativa 2026 de 5 freidoras: análisis con pros/contras, desde 38€. Marcas confiables..."
- Must be scannable and persuasive

Buying Criteria: 5 objective factors ordered by importance
- Should emerge from analyzing actual product specs
- Must be decision-making criteria, not product attributes
- Clearly stated so reader can self-identify what matters

Introduction (200-300 words, E-E-A-T + Conversion):
- Hook: Problem/opportunity question ("¿Quieres...?" or "¿Buscas...?")
- Authority: Explain what makes selection credible (tested, compared, evaluated on criteria)
- Trust signals: Mention brand reliability, warranty, guarantees (if applicable)
- Clear structure: "Aquí encontrarás... evaluadas por X, Y, Z criterios"
- Include: Price range, capacity/feature range mentioned upfront
- End with: Benefit promise + how to use the article
- Tone: Professional but conversational, first-person expertise

Product Summaries (100-150 words each):
- Lead with: Who is this product for? (target customer type)
- Explain: Key strength vs. alternatives (comparative advantage)
- Address: Trade-offs and realistic limitations
- Include: 1-2 specific numbers (price, capacity, power, watts, etc.)
- Close with: Who should avoid it? (honest anti-recommendation)
- Tone: Objective, helpful, honest
- Pros (3-10 specific, verifiable benefits related to buying criteria):
  * Must be concrete features or capabilities from the product
  * Examples: "2200W power", "8L capacity", "Panel táctil", "Doble resistencia", "Garantía oficial"
  * Link each pro to one of the buying criteria
- Cons (2-5 real limitations, not nitpicks):
  * Must be honest trade-offs or weaknesses
  * Examples: "Smaller capacity than competitor X", "Less powerful than premium model", "Heavier to move"
  * Link each con to one of the buying criteria

Verdict (150-200 words, E-E-A-T + Decision framework):
- Recommend DIFFERENT products for DIFFERENT scenarios
- Acknowledge "best" depends on priorities
- Help reader self-identify their fit by criteria
- Include: Price ranges, capacity ranges, warranty/guarantee info
- Add trust signals: Brand reliability, years in market, guarantees
- Avoid declaring universal winner
- End with: "Choose based on..."

FAQ (7-8 questions related to product category):
- Each Q&A must answer a real buying question
- Topics: Capacity/size selection, consumption/efficiency, safety, uses, care, durability, benefits
- Answers: 80-120 words each, practical and specific
- Include numbers/specs where relevant
- Related to products shown but also general category knowledge
- Structured for LLM extraction (one-fact-per-paragraph style)

Badges: Emerge naturally from comparative analysis
- "Best Value", "Best Premium", "Best for Beginners"
- Each product gets one unique badge
- Reflect actual positioning, not marketing

Pros/Cons:
- Pros: 3-10 specific, verifiable benefits
- Cons: 2-5 real limitations (not nitpicks)
- Both must relate to buying criteria"""

    BUSINESS_CONSTRAINTS = """AFFILIATE & AMAZON COMPLIANCE:

Focus: Help readers make confident purchases through Amazon
Audience: Buyers with commercial intent (near purchase decision)
Tone: Professional, trustworthy, editorial quality
Style: Similar to Wirecutter, RTINGS, TechRadar (not marketing)

MANDATORY REQUIREMENTS:
- Badge must represent unique positioning.
- Every product must have distinct short_title.
- No empty summaries. No duplicate ASINs.
- NO PRODUCT MAY HAVE EMPTY PROS OR CONS.
- Pros: 3-10 items per product (specific, verifiable, linked to criteria)
- Cons: 2-5 items per product (honest limitations, linked to criteria)
- Comparison is essential (products must reference each other implicitly).
- Objectivity over persuasion.

VERIFICATION:
- Before outputting JSON, verify that EVERY product has 3+ pros and 2+ cons.
- If a product would have empty arrays, generate content rather than omitting."""

    REASONING_WORKFLOW = """INTERNAL ANALYSIS (Do not include in output):

1. Analyze each product using provided data only
2. Map strengths to buying criteria
3. Map weaknesses to buying criteria
4. For EACH PRODUCT:
   a. Generate 3-10 PROS by mapping strengths to buying criteria
   b. Generate 2-5 CONS by mapping weaknesses to buying criteria
   c. Ensure pros/cons are SPECIFIC and VERIFIABLE (not generic)
   d. Pros must be features/capabilities visible in product specs
   e. Cons must be honest trade-offs or real limitations
5. Determine ideal customer profile for each
6. Identify realistic use cases
7. Identify trade-offs
8. Compare all products objectively
9. Rank by overall value (not commission)
10. Assign badges based on analysis
11. Generate final article

CRITICAL: NO PRODUCT MAY HAVE EMPTY PROS OR CONS ARRAYS.
Only output the final JSON. The reasoning must be hidden."""

    JSON_SCHEMA = """{
  "title": "Compelling keyword-natural title (8-12 words, includes year and differentiator)",
  "description": "150–160 char meta description (keyword + benefit + price range + authority)",
  "buying_criteria": ["Factor 1", "Factor 2", "Factor 3", "Factor 4", "Factor 5"],
  "intro": "200–300 word introduction (hook + authority + trust signals + price/capacity range)",
  "verdict": "150–200 word verdict (multiple scenarios, price ranges, warranty info, trust signals)",
  "products": [
    {
      "asin": "ASIN",
      "short_title": "Unique differentiator (max 10 words)",
      "badge": "Unique positioning badge",
      "pros": ["Pro 1", "Pro 2", "Pro 3", "...3-10 total"],
      "cons": ["Con 1", "Con 2", "...2-5 total"],
      "summary": "100–150 word narrative",
      "ideal_for": "Target customer description",
      "avoid_if": "Who should avoid this",
      "best_use_case": "Realistic scenario for this product",
      "key_features": ["Feature 1", "Feature 2", "Feature 3"],
      "score": 0.0,
      "value_score": 0.0,
      "performance_score": 0.0,
      "expert_tip": "One key insight"
    }
  ],
  "faq": [
    {
      "question": "Relevant buying question?",
      "answer": "80-120 word answer with practical info, numbers, and specifics"
    }
  ]
}"""

    @classmethod
    def get_system_prompt(cls) -> str:
        """Get system prompt for chat API."""
        return cls.SYSTEM_PROMPT

    @classmethod
    def get_user_prompts(cls) -> List[str]:
        """Get user prompts in order for multi-turn conversation."""
        return [
            cls.EDITORIAL_RULES,
            cls.BUSINESS_CONSTRAINTS,
            cls.REASONING_WORKFLOW,
            f"Use this JSON schema:\n{cls.JSON_SCHEMA}"
        ]


class OllamaProvider(AIProvider):
    """
    Production-grade Local Ollama LLM provider with advanced prompt engineering.
    
    Features:
    - Versioned prompt architecture (PromptV1, PromptV2, ...)
    - Ollama Chat API (modern instruction-tuned models)
    - Comprehensive JSON validation with retry
    - Extended JSON with scoring and expert tips
    - Prepared for multi-step generation workflow
    - Robust error handling and debug logging
    """
    
    # Prompt version registry
    PROMPT_VERSIONS = {
        1: PromptV1,
        2: PromptV1,  # Future: PromptV2
    }
    DEFAULT_PROMPT_VERSION = 1

    
    def __init__(
        self,
        model: str = "mistral",
        base_url: str = "http://localhost:11434",
        max_retries: int = 3,
        debug: bool = False,
        prompt_version: int = 1
    ) -> None:
        """
        Initialize Ollama provider with enterprise features.
        
        Args:
            model: Model name (e.g., 'mistral', 'llama2', 'neural-chat')
            base_url: Ollama server base URL
            max_retries: Maximum retry attempts
            debug: Enable debug logging
            prompt_version: Prompt version (1, 2, etc.)
        """
        self.model = model
        self.base_url = base_url
        self.chat_api_url = f"{base_url}/api/chat"
        self.max_retries = max_retries
        self.debug = debug
        
        # Load prompt version
        if prompt_version not in self.PROMPT_VERSIONS:
            raise ValueError(f"Prompt version {prompt_version} not available. Use: {list(self.PROMPT_VERSIONS.keys())}")
        self.prompt_class = self.PROMPT_VERSIONS[prompt_version]
        self.prompt_version = prompt_version
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self) -> None:
        """Test Ollama connection and list available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✓ Ollama conectado en {self.base_url}")
                available_models = response.json().get('models', [])
                model_names = [m.get('name', '').split(':')[0] for m in available_models]
                print(f"  Modelos disponibles: {', '.join(set(model_names))}")
                print(f"  Versión de prompts: v{self.prompt_version}")
                if self.debug:
                    print(f"  Modo debug: activado | Reintentos: {self.max_retries}")
            else:
                raise ConnectionError("Ollama server no responde correctamente")
        except requests.ConnectionError:
            raise ConnectionError(
                f"No se puede conectar a Ollama en {self.base_url}.\n"
                "Asegúrate de que Ollama está corriendo:\n"
                "  1. Descarga: https://ollama.ai\n"
                "  2. Ejecuta: ollama serve\n"
                "  3. En otra terminal: ollama pull mistral"
            )
    
    
    def _build_chat_messages(
        self,
        products: List[Dict[str, Any]],
        niche: str,
        buying_criteria: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, str]]:
        """
        Build messages for Ollama Chat API (recommended modern format).
        
        Args:
            products: Product list
            niche: Niche category
            buying_criteria: Buying criteria list
            
        Returns:
            List of message dicts for chat API
        """
        products_section = self._format_products_for_prompt(products)
        criteria_section = self._format_criteria_for_prompt(buying_criteria) if buying_criteria else ""
        
        # System prompt
        messages = [
            {"role": "system", "content": self.prompt_class.get_system_prompt()}
        ]
        
        # Editorial rules + business constraints + reasoning workflow + schema
        user_messages = self.prompt_class.get_user_prompts()
        for msg in user_messages:
            messages.append({"role": "user", "content": msg})
        
        # Final request with data
        final_request = f"""Analiza estos productos de Amazon para el nicho "{niche}" y genera análisis completo en JSON.

PRODUCTOS:
{products_section}
{criteria_section}"""
        
        messages.append({"role": "user", "content": final_request})
        
        return messages
    
    
    def _validate_json_content(self, json_content: Dict[str, Any]) -> Dict[str, str]:
        """
        Validate JSON content comprehensively.
        
        Args:
            json_content: Parsed JSON to validate
            
        Returns:
            Dict with 'valid': bool and 'errors': list of error messages
        """
        errors = []
        
        # Required fields
        required_fields = ['title', 'description', 'buying_criteria', 'intro', 'verdict', 'products']
        missing = [f for f in required_fields if f not in json_content]
        if missing:
            errors.append(f"Missing fields: {', '.join(missing)}")
        
        # Buying criteria: 3-7 items
        if 'buying_criteria' in json_content:
            if not isinstance(json_content['buying_criteria'], list):
                errors.append("buying_criteria must be an array")
            elif len(json_content['buying_criteria']) < 3 or len(json_content['buying_criteria']) > 7:
                errors.append(f"buying_criteria must have 3-7 items, got {len(json_content['buying_criteria'])}")
        
        # FAQ validation: 7-10 Q&A pairs
        if 'faq' in json_content:
            faq = json_content['faq']
            if not isinstance(faq, list):
                errors.append("faq must be an array")
            elif len(faq) < 7 or len(faq) > 10:
                errors.append(f"faq must have 7-10 items, got {len(faq)}")
            else:
                for i, item in enumerate(faq):
                    if not isinstance(item, dict):
                        errors.append(f"faq[{i}] must be an object")
                        continue
                    if 'question' not in item or 'answer' not in item:
                        errors.append(f"faq[{i}] missing question or answer")
                    if item.get('question', '').strip() == '':
                        errors.append(f"faq[{i}] question cannot be empty")
                    if item.get('answer', '').strip() == '':
                        errors.append(f"faq[{i}] answer cannot be empty")
                    # Check answer length (should be 80-120 words = roughly 400-600 chars)
                    answer_len = len(item.get('answer', '').split())
                    if answer_len < 40:
                        errors.append(f"faq[{i}] answer too short ({answer_len} words, recommend 80-120)")
        
        # Products array validation
        if 'products' in json_content:
            products = json_content['products']
            
            if not isinstance(products, list):
                errors.append("products must be an array")
            elif len(products) == 0:
                errors.append("products array cannot be empty")
            else:
                asins = []
                badges = []
                short_titles = []
                
                for i, prod in enumerate(products):
                    if not isinstance(prod, dict):
                        errors.append(f"product[{i}] must be an object")
                        continue
                    
                    # Required product fields
                    prod_required = ['asin', 'short_title', 'badge', 'pros', 'cons', 'summary']
                    prod_missing = [f for f in prod_required if f not in prod]
                    if prod_missing:
                        errors.append(f"product[{i}] missing: {', '.join(prod_missing)}")
                    
                    # Check for empty values
                    if prod.get('asin') == '':
                        errors.append(f"product[{i}] asin cannot be empty")
                    if prod.get('summary', '').strip() == '':
                        errors.append(f"product[{i}] summary cannot be empty")
                    
                    # Track for duplicate checking
                    if prod.get('asin'):
                        asins.append(prod.get('asin'))
                    if prod.get('badge'):
                        badges.append(prod.get('badge'))
                    if prod.get('short_title'):
                        short_titles.append(prod.get('short_title'))
                    
                    # Pros/cons counts - allow flexible ranges for better content quality
                    if 'pros' not in prod:
                        errors.append(f"product[{i}] missing pros array")
                    elif not isinstance(prod.get('pros'), list):
                        errors.append(f"product[{i}] pros must be an array, got {type(prod['pros']).__name__}")
                    elif len(prod['pros']) == 0:
                        errors.append(f"product[{i}] pros cannot be empty (need 3-10)")
                    elif len(prod['pros']) < 3 or len(prod['pros']) > 10:
                        errors.append(f"product[{i}] pros must have 3-10 items, got {len(prod['pros'])}")
                    
                    if 'cons' not in prod:
                        errors.append(f"product[{i}] missing cons array")
                    elif not isinstance(prod.get('cons'), list):
                        errors.append(f"product[{i}] cons must be an array, got {type(prod['cons']).__name__}")
                    elif len(prod['cons']) == 0:
                        errors.append(f"product[{i}] cons cannot be empty (need 2-5)")
                    elif len(prod['cons']) < 2 or len(prod['cons']) > 5:
                        errors.append(f"product[{i}] cons must have 2-5 items, got {len(prod['cons'])}")
                
                # Check for duplicates
                duplicate_asins = [x for x in set(asins) if asins.count(x) > 1]
                if duplicate_asins:
                    errors.append(f"Duplicate ASINs: {', '.join(duplicate_asins)}")
                
                duplicate_badges = [x for x in set(badges) if badges.count(x) > 1]
                if duplicate_badges:
                    errors.append(f"Duplicate badges: {', '.join(duplicate_badges)}")
                
                duplicate_titles = [x for x in set(short_titles) if short_titles.count(x) > 1]
                if duplicate_titles:
                    errors.append(f"Duplicate short_titles: {', '.join(duplicate_titles)}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    
    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Robustly extract JSON from response with error recovery.
        
        Handles:
        - Markdown code fences (```json ... ```)
        - Leading/trailing text and explanations
        - Escaped characters and malformed whitespace
        
        Args:
            text: Raw response text from Ollama
            
        Returns:
            Parsed JSON dict or None if extraction fails
        """
        if not text or not isinstance(text, str):
            return None
        
        text = text.strip()
        
        # Attempt 1: Try direct parsing
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Attempt 2: Remove markdown code fences
        if "```" in text:
            patterns = [
                r'```(?:json)?\s*(.*?)\s*```',
                r'```\s*(.*?)\s*```',
            ]
            for pattern in patterns:
                match = re.search(pattern, text, re.DOTALL)
                if match:
                    json_candidate = match.group(1).strip()
                    try:
                        return json.loads(json_candidate)
                    except json.JSONDecodeError:
                        continue
        
        # Attempt 3: Find JSON object in text
        json_patterns = [r'(\{[\s\S]*\})', r'(\[[\s\S]*\])']
        for pattern in json_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                json_candidate = match.group(1)
                try:
                    json_candidate = json_candidate.replace('\\"', '"').replace('\\n', '\n')
                    return json.loads(json_candidate)
                except json.JSONDecodeError:
                    continue
        
        # Attempt 4: Last resort - extract JSON bounds
        brace_index = text.find('{')
        if brace_index >= 0:
            text = text[brace_index:]
        brace_index = text.rfind('}')
        if brace_index >= 0:
            text = text[:brace_index + 1]
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            if self.debug:
                print(f"JSON extraction failed. Text: {text[:200]}...")
            return None
    
    def _call_chat_api(
        self,
        messages: List[Dict[str, str]],
        attempt: int
    ) -> Optional[str]:
        """
        Call Ollama Chat API with given messages.
        
        Args:
            messages: List of message dicts for chat API
            attempt: Current attempt number (for logging)
            
        Returns:
            Response content or None if failed
        """
        try:
            if self.debug:
                print(f"\n[DEBUG] Attempt {attempt + 1}/{self.max_retries}")
            
            response = requests.post(
                self.chat_api_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                },
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('message', {}).get('content', '').strip()
                
                if content:
                    if self.debug:
                        print(f"[DEBUG] Response received: {len(content)} characters")
                    return content
                else:
                    print(f"✗ No content in Ollama response")
            else:
                print(f"✗ Ollama error (HTTP {response.status_code})")
                
        except requests.Timeout:
            print(f"✗ Timeout en intento {attempt + 1}/{self.max_retries}")
        except requests.RequestException as e:
            print(f"✗ Error de conexión: {e}")
        except Exception as e:
            print(f"✗ Error inesperado: {e}")
        
        return None
    
    def _retry_with_backoff(
        self,
        products: List[Dict[str, Any]],
        niche: str,
        buying_criteria: Optional[List[Dict[str, str]]] = None
    ) -> Optional[str]:
        """
        Call Ollama Chat API with exponential backoff retry logic.
        
        Uses modern Chat API format (recommended for instruction-tuned models).
        
        Args:
            products: Product list
            niche: Niche category
            buying_criteria: Buying criteria list
            
        Returns:
            Raw response content or None if all retries fail
        """
        import time
        
        # Build chat messages
        messages = self._build_chat_messages(products, niche, buying_criteria)
        
        if self.debug:
            total_chars = sum(len(m.get('content', '')) for m in messages)
            print(f"\n[DEBUG] Total prompt length: {total_chars} characters")
            print(f"[DEBUG] Products count: {len(products)}")
            print(f"[DEBUG] Messages count: {len(messages)}")
        
        for attempt in range(self.max_retries):
            content = self._call_chat_api(messages, attempt)
            if content:
                return content
            
            # Exponential backoff before retry
            if attempt < self.max_retries - 1:
                wait_time = min(2 ** attempt, 30)
                print(f"⏳ Esperando {wait_time}s antes del siguiente intento...")
                time.sleep(wait_time)
        
        return None
    
    def generate_niche_content(
        self,
        products: List[Dict[str, Any]],
        niche: str,
        buying_criteria: Optional[List[Dict[str, str]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate enterprise-grade niche content using Ollama Chat API.
        
        Implements:
        - Modular prompt architecture with versioning
        - Chat API (modern multi-turn format)
        - Comprehensive JSON validation
        - Automatic retry on validation failure
        - Robust JSON extraction
        - Exponential backoff retry logic
        
        Args:
            products: List of product dictionaries with ASIN, title, price, rating, features
            niche: Niche topic/category (e.g., "Freidoras de Aire")
            buying_criteria: Optional list of 5 key decision criteria
            
        Returns:
            Content dictionary with keys: title, description, buying_criteria, intro, verdict, products
            with extended fields: ideal_for, avoid_if, best_use_case, key_features, score, value_score, performance_score, expert_tip
            Returns None if generation fails after all retries
        """
        try:
            if not products:
                print("✗ No hay productos para procesar")
                return None
            
            print(f"🤖 Generando contenido con Ollama ({self.model}) para nicho: {niche}")
            if self.prompt_version > 1:
                print(f"  Versión de prompts: v{self.prompt_version}")
            
            # Call Ollama with retries
            content = self._retry_with_backoff(products, niche, buying_criteria)
            
            if not content:
                print("✗ Ollama no generó contenido después de todos los reintentos")
                return None
            
            # Extract JSON with robust error recovery
            json_content = self._extract_json(content)
            
            if not json_content:
                print("✗ No se pudo extraer JSON válido de la respuesta")
                if self.debug:
                    print(f"[DEBUG] Response excerpt: {content[:300]}...")
                return None
            
            # Validate JSON content
            validation_result = self._validate_json_content(json_content)
            
            if not validation_result['valid']:
                print(f"⚠ Errores de validación: {len(validation_result['errors'])} encontrados")
                for error in validation_result['errors'][:3]:  # Show first 3 errors
                    print(f"  - {error}")
                
                # Try one regeneration attempt
                print("🔄 Reintentando generación...")
                content = self._retry_with_backoff(products, niche, buying_criteria)
                
                if content:
                    json_content = self._extract_json(content)
                    if json_content:
                        validation_result = self._validate_json_content(json_content)
                        if validation_result['valid']:
                            print("✓ Reintento exitoso - validación pasada")
                        else:
                            print("✗ Reintento falló - errores de validación persisten")
                            return None
                    else:
                        print("✗ Reintento falló - no se pudo extraer JSON")
                        return None
                else:
                    print("✗ Reintento falló - sin respuesta de Ollama")
                    return None
            
            print("✓ Contenido generado exitosamente por Ollama")
            if self.debug:
                print(f"[DEBUG] JSON keys: {list(json_content.keys())}")
                if 'products' in json_content:
                    print(f"[DEBUG] Productos: {len(json_content['products'])}")
            
            return json_content
            
        except Exception as e:
            print(f"✗ Error fatal en OllamaProvider: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return None


class AIContentGenerator:
    """Main AI content generator that routes to appropriate provider."""
    
    PROVIDERS = {
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider,
        'deepseek': DeepSeekProvider,
        'ollama': OllamaProvider,
    }
    
    def __init__(
        self,
        provider: str = 'openai',
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        debug: bool = False
    ) -> None:
        """
        Initialize content generator.
        
        Args:
            provider: AI provider to use ('openai', 'anthropic', 'deepseek', 'ollama')
            api_key: API key for the provider (not needed for ollama)
            model: Model name for ollama (e.g., 'mistral', 'llama2')
            debug: Enable debug logging (only supported for ollama)
        """
        if provider not in self.PROVIDERS:
            raise ValueError(f"Provider must be one of {list(self.PROVIDERS.keys())}")
        
        if provider == 'ollama':
            # Ollama with enterprise features
            provider_class = self.PROVIDERS[provider]
            self.provider = provider_class(
                model=model or 'mistral',
                debug=debug
            )
        else:
            if not api_key:
                raise ValueError(f"API key required for {provider}")
            provider_class = self.PROVIDERS[provider]
            self.provider = provider_class(api_key)
        
        print(f"✓ Generador de IA inicializado con {provider.upper()}")
    
    def generate(self, products: List[Dict[str, Any]], niche: str, buying_criteria: Optional[List[Dict[str, str]]] = None) -> Optional[Dict[str, Any]]:
        """
        Generate niche content.
        
        Args:
            products: List of products to analyze
            niche: Niche category
            buying_criteria: List of key buying criteria (5 points)
            
        Returns:
            Generated content or None
        """
        if not products:
            print("✗ No hay productos para procesar")
            return None
        
        return self.provider.generate_niche_content(products, niche, buying_criteria)

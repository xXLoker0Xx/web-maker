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
    def generate_niche_content(self, products: List[Dict[str, Any]], niche: str, buying_criteria: List[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """Generate niche content from products."""
        pass


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
    
    def generate_niche_content(self, products: List[Dict[str, Any]], niche: str, buying_criteria: List[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
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
  "intro": "Párrafo introductorio enfocado en conversión (200-300 palabras)",
  "verdict": "Conclusión y recomendación general (150-200 palabras)",
  "products": [
    {{
      "asin": "ASIN_ACTUAL",
      "badge": "Insignia única como 'Mejor Calidad-Precio' o 'Mejor Rendimiento'",
      "pros": ["Pro 1", "Pro 2", "Pro 3"],
      "cons": ["Contra 1", "Contra 2"],
      "summary": "Resumen único escrito por la IA (100-150 palabras)"
    }}
  ]
}}

Reglas:
- El título debe ser atractivo y contener la palabra clave principal
- La meta descripción debe incluir la palabra clave y ser atractiva
- Cada producto debe tener una insignia diferente
- Los pros y contras deben ser específicos al producto y relacionados con los 5 criterios clave
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

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from text response."""
        try:
            # Try direct JSON parsing
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON in the response
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    return None
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
    
    def generate_niche_content(self, products: List[Dict[str, Any]], niche: str, buying_criteria: List[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
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
  "intro": "Párrafo introductorio enfocado en conversión (200-300 palabras)",
  "verdict": "Conclusión y recomendación general (150-200 palabras)",
  "products": [
    {{
      "asin": "ASIN_ACTUAL",
      "badge": "Insignia única como 'Mejor Calidad-Precio' o 'Mejor Rendimiento'",
      "pros": ["Pro 1", "Pro 2", "Pro 3"],
      "cons": ["Contra 1", "Contra 2"],
      "summary": "Resumen único escrito por la IA (100-150 palabras)"
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


class OllamaProvider(AIProvider):
    """Local Ollama LLM provider."""
    
    def __init__(self, model: str = "mistral", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama provider.
        
        Args:
            model: Model name to use (e.g., 'mistral', 'llama2', 'neural-chat')
            base_url: Ollama server base URL
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        
        # Test connection
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✓ Ollama conectado en {base_url}")
                available_models = response.json().get('models', [])
                model_names = [m.get('name', '').split(':')[0] for m in available_models]
                print(f"  Modelos disponibles: {', '.join(set(model_names))}")
            else:
                raise ConnectionError("Ollama server no responde correctamente")
        except requests.ConnectionError:
            raise ConnectionError(
                f"No se puede conectar a Ollama en {base_url}.\n"
                "Asegúrate de que Ollama está corriendo:\n"
                "  1. Descarga: https://ollama.ai\n"
                "  2. Ejecuta: ollama serve\n"
                "  3. En otra terminal: ollama pull mistral\n"
                "  O usa otro modelo: ollama pull llama2"
            )
    
    def generate_niche_content(self, products: List[Dict[str, Any]], niche: str, buying_criteria: List[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """
        Generate niche content using local Ollama.
        
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
            
            prompt = f"""Eres un experto en marketing de afiliados de Amazon y contenido SEO.
Tu tarea es generar análisis de productos de manera profesional y persuasiva.
IMPORTANTE: Debes responder SIEMPRE con un JSON válido, sin explicaciones adicionales.

Analiza estos productos de Amazon para el nicho "{niche}" y genera un análisis completo en formato JSON.

PRODUCTOS:
{products_json}

{criteria_section}

Genera un JSON estricto con la siguiente estructura (sin texto adicional fuera del JSON):
{{
  "title": "Las X Mejores [Categoría] de 2026",
  "description": "Meta descripción SEO para la página (max 160 caracteres)",
  "intro": "Párrafo introductorio enfocado en conversión (200-300 palabras)",
  "verdict": "Conclusión y recomendación general (150-200 palabras)",
  "products": [
    {{
      "asin": "ASIN_ACTUAL",
      "badge": "Insignia única como 'Mejor Calidad-Precio' o 'Mejor Rendimiento'",
      "pros": ["Pro 1", "Pro 2", "Pro 3"],
      "cons": ["Contra 1", "Contra 2"],
      "summary": "Resumen único escrito por la IA (100-150 palabras)"
    }}
  ]
}}

Reglas:
- El título debe ser atractivo y contener la palabra clave principal
- La meta descripción debe incluir la palabra clave y ser atractiva
- Cada producto debe tener una insignia diferente
- Los pros y contras deben ser específicos al producto y relacionados con los criterios clave
- El resumen debe ser único para cada producto, comparándolo respecto a los criterios
- Usa un tono profesional pero conversacional
- Responde ÚNICAMENTE con el JSON, sin explicaciones adicionales."""

            print(f"🤖 Usando Ollama ({self.model}) para generar contenido...")
            
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                },
                timeout=300  # Ollama puede tardar más
            )
            
            if response.status_code != 200:
                print(f"✗ Error de Ollama: {response.status_code}")
                return None
            
            result = response.json()
            content = result.get('response', '').strip()
            
            if not content:
                print("✗ Ollama no generó contenido")
                return None
            
            # Extract JSON from response
            json_content = self._extract_json(content)
            if not json_content:
                print("✗ No se pudo extraer JSON de la respuesta")
                # Mostrar respuesta para debugging
                print(f"Respuesta: {content[:500]}")
                return None
            
            print("✓ Contenido generado por Ollama exitosamente")
            return json_content
            
        except requests.Timeout:
            print("✗ Ollama tardó demasiado (timeout)")
            return None
        except Exception as e:
            print(f"✗ Error en Ollama: {e}")
            return None

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
    
    def generate_niche_content(self, products: List[Dict[str, Any]], niche: str, buying_criteria: List[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
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
            criteria_section = self._format_criteria_for_prompt(buying_criteria) if buying_criteria else ""
            
            system_prompt = """Eres un experto en marketing de afiliados de Amazon y contenido SEO.
Tu tarea es generar análisis de productos de manera profesional y persuasiva.
Debes responder SIEMPRE con un JSON válido."""
            
            user_prompt = f"""Analiza estos productos de Amazon para el nicho "{niche}" y genera un análisis completo.

PRODUCTOS:
{products_json}

{criteria_section}

Responde con este JSON:
{{
  "title": "Las X Mejores [Categoría] de 2026",
  "description": "Meta descripción SEO",
  "intro": "Párrafo introductorio (200-300 palabras)",
  "verdict": "Conclusión (150-200 palabras)",
  "products": [
    {{
      "asin": "ASIN",
      "badge": "Insignia única",
      "pros": ["Pro 1", "Pro 2"],
      "cons": ["Contra"],
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

    def _format_products_for_prompt(self, products: List[Dict[str, Any]]) -> str:
        """Format products for AI prompt."""
        formatted = []
        for i, product in enumerate(products, 1):
            formatted.append(f"""
Producto {i}:
- ASIN: {product.get('asin')}
- Título: {product.get('title')}
- Precio: {product.get('price')}
- Valoración: {product.get('rating')} estrellas
- Características: {', '.join(product.get('features', []))}
""")
        return "\n".join(formatted)
    
    def _format_criteria_for_prompt(self, buying_criteria: List[Dict[str, str]]) -> str:
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


class AIContentGenerator:
    """Main AI content generator that routes to appropriate provider."""
    
    PROVIDERS = {
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider,
        'deepseek': DeepSeekProvider,
        'ollama': OllamaProvider,
    }
    
    def __init__(self, provider: str = 'openai', api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize content generator.
        
        Args:
            provider: AI provider to use ('openai', 'anthropic', 'deepseek', 'ollama')
            api_key: API key for the provider (not needed for ollama)
            model: Model name for ollama (e.g., 'mistral', 'llama2')
        """
        if provider not in self.PROVIDERS:
            raise ValueError(f"Provider must be one of {list(self.PROVIDERS.keys())}")
        
        if provider == 'ollama':
            # Ollama doesn't need API key
            provider_class = self.PROVIDERS[provider]
            self.provider = provider_class(model=model or 'mistral')
        else:
            if not api_key:
                raise ValueError(f"API key required for {provider}")
            provider_class = self.PROVIDERS[provider]
            self.provider = provider_class(api_key)
        
        print(f"✓ Generador de IA inicializado con {provider.upper()}")
    
    def generate(self, products: List[Dict[str, Any]], niche: str, buying_criteria: List[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
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

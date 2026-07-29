"""
Main CLI orchestrator for the Amazon Niche Page Generator.
Coordinates scraping, AI content generation, and output creation.
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

from database import ProductDatabase
from scraper import AmazonScraper
from ai_generator import AIContentGenerator


class WebMakerOrchestrator:
    """Orchestrates the complete niche page generation workflow."""
    
    def __init__(self):
        """Initialize the orchestrator."""
        load_dotenv()
        self.db = ProductDatabase("local_cache.db")
        self.ai_provider = None
        self.amazon_tag = None
        
    def _setup_ai(self) -> bool:
        """
        Setup AI provider based on environment variables or user choice.
        
        Returns:
            True if AI is set up successfully
        """
        # Check for Ollama first (local, no API key needed)
        try:
            from ai_generator import AIContentGenerator
            self.ai_provider = AIContentGenerator('ollama', model='mistral')
            return True
        except Exception as e:
            print(f"⚠ Ollama no disponible: {e}")
        
        # Try OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            try:
                self.ai_provider = AIContentGenerator('openai', openai_key)
                return True
            except Exception as e:
                print(f"⚠ Error al configurar OpenAI: {e}")
        
        # Try Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            try:
                self.ai_provider = AIContentGenerator('anthropic', anthropic_key)
                return True
            except Exception as e:
                print(f"⚠ Error al configurar Anthropic: {e}")
        
        # Try DeepSeek
        deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        if deepseek_key:
            try:
                self.ai_provider = AIContentGenerator('deepseek', deepseek_key)
                return True
            except Exception as e:
                print(f"⚠ Error al configurar DeepSeek: {e}")
        
        print("✗ No se encontró ningún proveedor de IA disponible")
        print("  Opciones:")
        print("  1. 🔹 Ollama (local, gratis): https://ollama.ai")
        print("     Ejecuta: ollama serve")
        print("     En otra terminal: ollama pull mistral")
        print("  2. 🔑 OpenAI: OPENAI_API_KEY en .env")
        print("  3. 🔑 Anthropic: ANTHROPIC_API_KEY en .env")
        print("  4. 🔑 DeepSeek: DEEPSEEK_API_KEY en .env")
        return False
    
    def _get_amazon_tag(self) -> str:
        """
        Get Amazon affiliate tag from user or environment.
        
        Returns:
            Amazon affiliate tag
        """
        # Try environment variable first
        tag = os.getenv('AMAZON_AFFILIATE_TAG')
        if tag:
            return tag
        
        # Ask user
        tag = input("\n🏷️  Ingresa tu ID de afiliado de Amazon (ej: mi-tag-21): ").strip()
        if not tag:
            print("✗ Tag de afiliado es requerido")
            sys.exit(1)
        return tag
    
    def _get_search_input(self) -> tuple:
        """
        Get search input from user (search term or ASINs).
        
        Returns:
            Tuple of (input_type, data, niche_name)
        """
        print("\n" + "="*60)
        print("🚀 GENERADOR DE PÁGINAS DE NICHO PARA AFILIADOS DE AMAZON")
        print("="*60)
        
        print("\nElige un modo de entrada:")
        print("1. Buscar por término (ej: 'freidoras de aire')")
        print("2. Por ASINs específicos (ej: 'B08ABC123,B08XYZ456')")
        
        choice = input("\nOpción (1 o 2): ").strip()
        
        if choice == "2":
            asins_input = input("Ingresa los ASINs separados por comas: ").strip()
            asins = [asin.strip().upper() for asin in asins_input.split(',')]
            niche = input("¿Cuál es el nicho/categoría de estos productos?: ").strip()
            return 'asins', asins, niche
        else:
            search_term = input("Ingresa el término de búsqueda: ").strip()
            pages = input("¿Cuántas páginas de resultados deseas (1-3)?: ").strip()
            try:
                pages = int(pages)
                pages = min(max(pages, 1), 3)
            except ValueError:
                pages = 1
            return 'search', search_term, search_term

    def scrape_and_process(self, input_type: str, data: Any, niche: str) -> List[Dict[str, Any]]:
        """
        Scrape products from Amazon.
        
        Args:
            input_type: 'search' or 'asins'
            data: Search term or list of ASINs
            niche: Niche category name
            
        Returns:
            List of products
        """
        print("\n" + "="*60)
        print("📥 FASE 1: SCRAPING DE PRODUCTOS")
        print("="*60)
        
        products = []
        
        with AmazonScraper() as scraper:
            if input_type == 'search':
                pages = 1  # Default to 1 page for search
                products = scraper.scrape_search_results(data, num_pages=pages)
            else:  # asins
                products = scraper.scrape_multiple_asins(data)
        
        if not products:
            print("✗ No se encontraron productos")
            return []
        
        # Save to database
        print("\n💾 Guardando productos en base de datos...")
        inserted = self.db.insert_products_batch(products)
        print(f"✓ {inserted}/{len(products)} productos guardados")
        
        return products

    def generate_ai_content(self, products: List[Dict[str, Any]], niche: str) -> Optional[Dict[str, Any]]:
        """
        Generate AI content for products.
        
        Args:
            products: List of product dictionaries
            niche: Niche category
            
        Returns:
            Generated content or None
        """
        print("\n" + "="*60)
        print("🤖 FASE 2: GENERACIÓN DE CONTENIDO CON IA")
        print("="*60)
        
        if not self.ai_provider:
            print("✗ Proveedor de IA no configurado")
            return None
        
        ai_content = self.ai_provider.generate(products, niche)
        return ai_content

    def merge_content(self, products: List[Dict[str, Any]], ai_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge scraper data with AI-generated content.
        
        Args:
            products: Original product data from scraper
            ai_content: AI-generated content
            
        Returns:
            Merged content dictionary
        """
        print("\n" + "="*60)
        print("🔗 FASE 3: FUSIÓN DE DATOS")
        print("="*60)
        
        # Create ASIN to product mapping
        product_map = {p['asin']: p for p in products}
        
        # Enhance AI content with scraper data
        for ai_product in ai_content.get('products', []):
            asin = ai_product.get('asin')
            if asin in product_map:
                original = product_map[asin]
                ai_product['image_url'] = original.get('image_url')
                ai_product['price'] = original.get('price')
                ai_product['rating'] = original.get('rating')
                ai_product['reviews_count'] = original.get('reviews_count')
                ai_product['affiliate_url'] = f"https://amazon.es/dp/{asin}?tag={self.amazon_tag}"
        
        print("✓ Contenido fusionado exitosamente")
        return ai_content

    def save_output(self, content: Dict[str, Any], output_path: str) -> bool:
        """
        Save merged content to JSON file for Astro template.
        
        Args:
            content: Content dictionary
            output_path: Path to save JSON
            
        Returns:
            True if successful
        """
        print("\n" + "="*60)
        print("💾 FASE 4: GUARDADO DE SALIDA")
        print("="*60)
        
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            
            print(f"✓ JSON guardado en: {output_file}")
            print(f"✓ Tamaño: {output_file.stat().st_size} bytes")
            return True
            
        except Exception as e:
            print(f"✗ Error al guardar archivo: {e}")
            return False

    def show_summary(self, products: List[Dict[str, Any]], ai_content: Dict[str, Any]) -> None:
        """
        Show summary of generated content.
        
        Args:
            products: Product list
            ai_content: Generated content
        """
        print("\n" + "="*60)
        print("📊 RESUMEN DE GENERACIÓN")
        print("="*60)
        
        print(f"\n📦 Productos procesados: {len(products)}")
        print(f"🎯 Título de la página: {ai_content.get('title', 'N/A')}")
        print(f"📝 Meta descripción: {ai_content.get('description', 'N/A')}")
        
        products_in_content = len(ai_content.get('products', []))
        print(f"🔗 Productos en contenido: {products_in_content}")
        
        db_stats = self.db.get_stats()
        print(f"💾 Total en base de datos: {db_stats['total_products']}")
        
        print("\n✨ ¡Página de nicho generada exitosamente!")
        print("📂 Próximo paso: Ejecutar 'npm run dev' en la carpeta plantilla-astro/")

    def run(self, skip_scraping: bool = False) -> None:
        """
        Run the complete workflow.
        
        Args:
            skip_scraping: If True, use cached products from DB
        """
        try:
            # Setup
            if not self._setup_ai():
                print("\n⚠️  Continuando sin IA (modo demo)")
            
            self.amazon_tag = self._get_amazon_tag()
            
            # Get input
            input_type, data, niche = self._get_search_input()
            
            # Scrape
            if skip_scraping:
                print("\n⏭️  Saltando scraping, usando productos en caché...")
                products = self.db.get_all_products()
                if not products:
                    print("✗ No hay productos en caché")
                    products = self.scrape_and_process(input_type, data, niche)
            else:
                products = self.scrape_and_process(input_type, data, niche)
            
            if not products:
                print("✗ Abortando: No hay productos para procesar")
                return
            
            # Generate AI content
            ai_content = self.generate_ai_content(products, niche)
            
            if not ai_content:
                print("⚠️  No se pudo generar contenido con IA, usando datos básicos...")
                ai_content = self._generate_fallback_content(products, niche)
            
            # Merge
            merged_content = self.merge_content(products, ai_content)
            
            # Save
            astro_content_path = Path(__file__).parent.parent / "plantilla-astro" / "src" / "content" / "niche.json"
            success = self.save_output(merged_content, str(astro_content_path))
            
            if success:
                self.show_summary(products, merged_content)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Operación cancelada por el usuario")
        except Exception as e:
            print(f"\n✗ Error inesperado: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.db.close()

    def _generate_fallback_content(self, products: List[Dict[str, Any]], niche: str) -> Dict[str, Any]:
        """
        Generate fallback content when AI is not available.
        
        Args:
            products: List of products
            niche: Niche category
            
        Returns:
            Fallback content dictionary
        """
        badges = ["Mejor Calidad", "Mejor Precio", "Mejor Rendimiento", "Mejor Diseño", "Mejor Valoración"]
        
        ai_products = []
        for idx, product in enumerate(products):
            ai_products.append({
                "asin": product.get('asin'),
                "badge": badges[idx % len(badges)],
                "pros": product.get('features', ["Producto de calidad"])[:3],
                "cons": ["Sin información de contras"],
                "summary": f"{product.get('title', 'Producto')} - Precio: {product.get('price', 'N/A')}. Con {product.get('reviews_count', 0)} reseñas y una valoración de {product.get('rating', 0)} estrellas."
            })
        
        return {
            "title": f"Las mejores opciones en {niche} de 2026",
            "description": f"Descubre las mejores opciones en {niche}. Análisis completo y comparativa de productos.",
            "intro": f"En este artículo te presentamos un análisis detallado de los mejores productos en {niche}. Hemos seleccionado cuidadosamente cada opción para ayudarte a encontrar el producto perfecto para tus necesidades.",
            "verdict": f"Después de analizar estas opciones, creemos que cualquiera de estos productos en {niche} es una excelente opción según tus necesidades específicas.",
            "products": ai_products
        }


def main():
    """Main entry point."""
    orchestrator = WebMakerOrchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Web Maker - Ejemplo de uso completo
Demuestra cómo usar programáticamente los módulos
"""

from pathlib import Path
import json

# Ejemplo 1: Usar la base de datos
print("=" * 60)
print("EJEMPLO 1: Base de Datos SQLite")
print("=" * 60)

from motor.database import ProductDatabase

# Crear instancia
db = ProductDatabase("products_example.db")

# Insertar un producto de ejemplo
sample_product = {
    'asin': 'B08TEST123',
    'title': 'Freidora Ejemplo Premium',
    'price': '99,99€',
    'rating': 4.8,
    'reviews_count': 1250,
    'features': ['Capacidad 6L', 'Control digital', 'Bajo consumo'],
    'image_url': 'https://example.com/image.jpg'
}

print("\n📦 Insertando producto...")
success = db.insert_product(sample_product)
print(f"✓ Insertado: {success}")

# Verificar que existe
exists = db.product_exists('B08TEST123')
print(f"✓ Producto existe: {exists}")

# Obtener producto
product = db.get_product('B08TEST123')
print(f"✓ Datos recuperados: {product.get('title')}")

# Obtener estadísticas
stats = db.get_stats()
print(f"✓ Total en BD: {stats['total_products']} productos")

db.close()


# Ejemplo 2: Usar el scraper
print("\n" + "=" * 60)
print("EJEMPLO 2: Web Scraper (DEMO - sin ejecutar)")
print("=" * 60)

print("""
from motor.scraper import AmazonScraper

with AmazonScraper() as scraper:
    # Buscar productos
    products = scraper.scrape_search_results(
        search_term="freidoras de aire",
        num_pages=1
    )
    
    # O scraper específicos por ASIN
    products = scraper.scrape_multiple_asins([
        'B08ABC123',
        'B08XYZ456'
    ])
    
    for product in products:
        print(f"- {product['title']}: {product['price']}")
""")


# Ejemplo 3: Usar el generador de IA
print("\n" + "=" * 60)
print("EJEMPLO 3: Generador de IA (DEMO - requiere clave API)")
print("=" * 60)

print("""
import os
from motor.ai_generator import AIContentGenerator

# Necesita variable de entorno OPENAI_API_KEY
api_key = os.getenv('OPENAI_API_KEY')

if api_key:
    generator = AIContentGenerator('openai', api_key)
    
    products = [
        {
            'asin': 'B08TEST123',
            'title': 'Freidora Premium',
            'price': '99,99€',
            'rating': 4.8,
            'reviews_count': 1250,
            'features': ['Capacidad 6L', 'Control digital']
        }
    ]
    
    content = generator.generate(products, niche='Freidoras de Aire')
    
    print(content['title'])
    print(content['description'])
    print(f"Productos analizados: {len(content['products'])}")
""")


# Ejemplo 4: Estructura del JSON final
print("\n" + "=" * 60)
print("EJEMPLO 4: Estructura JSON Final")
print("=" * 60)

example_json = {
    "title": "Las 5 Mejores Freidoras de Aire de 2024",
    "description": "Análisis y comparativa de las mejores freidoras de aire",
    "intro": "En este artículo analizamos...",
    "verdict": "Cualquiera de estos productos es una buena opción...",
    "products": [
        {
            "asin": "B08ABC123",
            "badge": "Mejor Valoración",
            "pros": ["Pro 1", "Pro 2", "Pro 3"],
            "cons": ["Contra 1"],
            "summary": "Resumen generado por IA...",
            "image_url": "https://...",
            "price": "99,99€",
            "rating": 4.8,
            "reviews_count": 1250,
            "affiliate_url": "https://amazon.es/dp/B08ABC123?tag=tu-tag"
        }
    ]
}

print(json.dumps(example_json, indent=2, ensure_ascii=False)[:500] + "...\n")


# Ejemplo 5: Estructura del HTML en Astro
print("=" * 60)
print("EJEMPLO 5: Cómo Astro renderiza el JSON")
print("=" * 60)

print("""
<!-- src/pages/index.astro -->
---
import content from '../content/niche.json'
---

<!DOCTYPE html>
<html>
<head>
  <title>{content.title}</title>
  <meta name="description" content={content.description} />
</head>
<body>
  <h1>{content.title}</h1>
  <p>{content.intro}</p>
  
  <!-- Loop de productos -->
  {content.products.map(product => (
    <div class="product">
      <h3>{product.title}</h3>
      <img src={product.image_url} />
      <p>{product.summary}</p>
      <a href={product.affiliate_url}>Ver en Amazon →</a>
    </div>
  ))}
  
  <p>{content.verdict}</p>
</body>
</html>

✓ Astro genera: dist/index.html (estático, optimizado, SEO-ready)
""")


# Ejemplo 6: Comandos para ejecutar
print("=" * 60)
print("EJEMPLO 6: Comandos para Ejecutar")
print("=" * 60)

commands = """
🔹 SETUP INICIAL
  cd motor
  python -m venv venv
  venv\\Scripts\\activate
  pip install -r requirements.txt

🔹 EJECUTAR GENERADOR
  python main.py
  
  1. Elige búsqueda o ASINs
  2. Ingresa término o lista de ASINs
  3. Espera a que se complete
  4. Revisa plantilla-astro/src/content/niche.json

🔹 VER RESULTADO
  cd ../plantilla-astro
  npm install
  npm run dev
  
  Abre: http://localhost:3000

🔹 GENERAR PARA PRODUCCIÓN
  npm run build
  
  Archivos en: plantilla-astro/dist/
"""

print(commands)


# Ejemplo 7: Casos de Uso
print("=" * 60)
print("EJEMPLO 7: Casos de Uso Comunes")
print("=" * 60)

print("""
✅ Crear sitio de reseñas
   - Scrape: "auriculares inalámbricos"
   - IA genera: Análisis comparativo
   - Resultado: Página de comparativa

✅ Monetizar con afiliación
   - Genera sitios para varios nichos
   - Monetiza con links de Amazon
   - Potencial: $100-500/mes por sitio

✅ Base de datos de productos
   - Scrape continuamente
   - SQLite almacena histórico
   - Reutiliza datos en múltiples páginas

✅ Blog de reseñas automático
   - Cron job: ejecuta daily
   - Genera nuevas páginas
   - Deploy automático

✅ Investigación de mercado
   - Analiza tendencias de precios
   - Compara ratings históricos
   - Identifica oportunidades
""")


# Ejemplo 8: Customización
print("\n" + "=" * 60)
print("EJEMPLO 8: Customización Fácil")
print("=" * 60)

print("""
🎨 CAMBIAR COLORES
  Edita: plantilla-astro/src/components/ProductCard.astro
  Busca: background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
  Cambia por: background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%)

📝 CAMBIAR PROMPTS DE IA
  Edita: motor/ai_generator.py
  Busca: system_prompt = "..."
  Personaliza: el prompt del sistema

🏷️ AGREGAR MÁS COMPONENTES
  1. Crea: src/components/MiComponente.astro
  2. Importa en: src/pages/index.astro
  3. Úsalo: <MiComponente products={content.products} />

🔐 CAMBIAR PROVEEDOR DE IA
  En motor/.env:
  # Descomenta el que quieras
  # OPENAI_API_KEY=...
  ANTHROPIC_API_KEY=...
  # DEEPSEEK_API_KEY=...
""")


print("\n" + "=" * 60)
print("✨ ¡Listo! Tu proyecto Web Maker está completo")
print("=" * 60)
print("""
Próximos pasos:

1. 📖 Lee: INDEX.md (tabla de contenidos)
2. 🚀 Ejecuta: python main.py
3. 🎨 Personaliza: CSS y contenido
4. 📦 Despliega: en Vercel, Netlify o tu servidor
5. 💰 Monetiza: con Amazon Associates

¡Buena suerte! 🎉
""")

# 🏗️ Arquitectura Técnica - Web Maker

## Resumen de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    MOTOR PYTHON (motor/)                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐      ┌──────────────┐     ┌────────────┐  │
│  │  scraper.py │─────▶│ database.py  │────▶│ main.py    │  │
│  │ (Web Scrape)│      │  (SQLite)    │     │ (CLI)      │  │
│  └─────────────┘      └──────────────┘     └────────────┘  │
│         │                                         │          │
│         │ Extrae:                                │          │
│         │ - ASIN, Título                         │          │
│         │ - Precio, Rating                       │          │
│         │ - Imagen, Características              │          │
│         │                                        │          │
│         └───────────────────────┬────────────────┘          │
│                                 │                            │
│  ┌──────────────────────────────▼─────────────────────┐    │
│  │           ai_generator.py (OpenAI/Anthropic)       │    │
│  │  Genera:                                           │    │
│  │  - Título SEO                                      │    │
│  │  - Meta descripción                                │    │
│  │  - Intro/Veredicto                                 │    │
│  │  - Insignias, Pros/Contras                        │    │
│  │  - Resúmenes únicos                                │    │
│  └──────────────────────────────────────┬────────────┘    │
│                                         │                  │
│  ┌──────────────────────────────────────▼────────────┐    │
│  │  SALIDA: niche.json (datos + IA)                 │    │
│  └──────────────────────────────────────────────────┘    │
│                                                           │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ (JSON)
                          │
┌─────────────────────────▼──────────────────────────────────┐
│              PLANTILLA ASTRO (plantilla-astro/)             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │  src/pages/index.astro (Página Principal)         │    │
│  │  - Lee niche.json                                 │    │
│  │  - Renderiza header + intro                       │    │
│  │  - Monta componentes                              │    │
│  └───────────────────────────────────────────────────┘    │
│                          │                                  │
│         ┌────────────────┼────────────────┐               │
│         │                │                │               │
│  ┌──────▼────┐    ┌────────▼──────┐    ┌──▼──────────┐  │
│  │ProductCard│    │ComparisonTable│    │  Footer     │  │
│  │.astro     │    │.astro         │    │  + Legal    │  │
│  │           │    │               │    │             │  │
│  │- Tarjeta  │    │- Tabla        │    │- Descargo   │  │
│  │- Imagen   │    │- Comparativa  │    │- Aviso      │  │
│  │- Pros/Con │    │- Responsive   │    │ afiliado    │  │
│  │- Rating   │    │- Mobile       │    │             │  │
│  │- Botón    │    │- Desktop      │    │             │  │
│  │  afiliado  │    │               │    │             │  │
│  └───────────┘    └───────────────┘    └─────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │  SALIDA: dist/ (HTML/CSS/JS estático)             │    │
│  │  100% optimizado para SEO, ultra rápido           │    │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## Flujo de Datos Detallado

### Fase 1: Web Scraping

```python
# scraper.py
AmazonScraper()
  ├─ scrape_search_results() 
  │  └─ Conecta a Amazon
  │     └─ Extrae HTML
  │        └─ ParseaHTML con BeautifulSoup
  │           └─ Extrae: ASIN, Título, Precio, Rating, Imagen, Features
  │
  └─ scrape_product_details()
     └─ Accede a página individual
        └─ Obtiene detalles completos
           └─ Retorna Dict con datos
```

**Entrada:** Término de búsqueda o lista de ASINs  
**Salida:** List[Dict] con datos brutos

---

### Fase 2: Base de Datos

```python
# database.py
ProductDatabase()
  ├─ _connect()
  │  └─ Crea conexión SQLite
  │
  ├─ _create_tables()
  │  └─ CREATE TABLE products(...)
  │
  └─ insert_products_batch()
     └─ Evita duplicados (ASIN única)
        └─ Almacena en local_cache.db
           └─ Permite reutilizar productos
```

**Tabla:**
```sql
CREATE TABLE products (
  asin TEXT PRIMARY KEY,
  title TEXT,
  price TEXT,
  rating REAL,
  reviews_count INTEGER,
  features TEXT (JSON),
  image_url TEXT,
  created_at TIMESTAMP
)
```

---

### Fase 3: Generación de Contenido con IA

```python
# ai_generator.py
AIContentGenerator(provider='openai')
  ├─ Formatea productos para prompt
  │
  ├─ Envía a OpenAI/Anthropic/DeepSeek
  │  └─ Sistema: "Eres un experto en contenido de afiliados"
  │     └─ Usuario: "Analiza estos 5 productos..."
  │
  └─ Recibe JSON estructurado:
     {
       "title": "Las 5 Mejores...",
       "description": "Meta SEO...",
       "intro": "Párrafo...",
       "verdict": "Conclusión...",
       "products": [
         {
           "asin": "...",
           "badge": "Mejor...",
           "pros": [...],
           "cons": [...],
           "summary": "..."
         }
       ]
     }
```

---

### Fase 4: Fusión de Datos

```python
# main.py - merge_content()
Productos Scraper + Respuesta IA = JSON Final
│                    │              │
├─ ASIN             │              │
├─ Título           │              │
├─ Precio           │              ├─ ASIN
├─ Rating           │              ├─ Título completo
├─ Reviews          │              ├─ Precio
├─ Imagen           │              ├─ Rating
└─ URL              │              ├─ Reviews
                    │              ├─ Imagen
                    ├─ Título SEO  ├─ Badge
                    ├─ Meta desc   ├─ Pros/Contras
                    ├─ Intro       ├─ Resumen único
                    ├─ Veredicto   ├─ URL afiliado
                    └─ Insignias   └─ Todo integrado
```

---

### Fase 5: Renderizado Astro

```astro
// src/pages/index.astro
---
// Leer niche.json
import content from '../content/niche.json'

// Content:
// {
//   title: "...",
//   description: "...",
//   products: [...]
// }
---

<!-- Header -->
<h1>{content.title}</h1>
<meta name="description" content={content.description} />

<!-- Loop de productos -->
{content.products.map(product => (
  <ProductCard {product} />
))}

<!-- Tabla comparativa -->
<ComparisonTable products={content.products} />

<!-- Footer con avisos legales -->
```

**Salida:** `dist/index.html` (HTML estático, zero JS innecesario)

---

## Tecnologías Utilizadas

### Backend (Motor Python)

| Librería | Uso |
|----------|-----|
| `requests` | HTTP requests a Amazon |
| `beautifulsoup4` | Parsing HTML |
| `openai` | Conexión a OpenAI API |
| `anthropic` | Conexión a Claude API |
| `sqlite3` | Base de datos local |
| `python-dotenv` | Manejo de .env |

### Frontend (Plantilla Astro)

| Tecnología | Uso |
|-----------|-----|
| `Astro 4.x` | Framework estático |
| `HTML5` | Estructura |
| `CSS3` | Estilos (sin dependencias) |
| `TypeScript` | Tipado (opcional) |

---

## Patrones de Diseño

### 1. **Context Manager Pattern** (Python)

```python
# Uso automático de recursos
with ProductDatabase() as db:
    db.insert_product(data)
    # Se cierra automáticamente
```

### 2. **Strategy Pattern** (AI Providers)

```python
# Intercambiables:
AIContentGenerator(provider='openai')
AIContentGenerator(provider='anthropic')
AIContentGenerator(provider='deepseek')
```

### 3. **Repository Pattern** (Database)

```python
# Abstrae acceso a datos
db.product_exists(asin)
db.insert_product(data)
db.get_products_by_asins([...])
```

---

## Performance

### Optimizaciones Implementadas

**Python:**
- ✅ Reutilización de sesiones HTTP (retry strategy)
- ✅ Cache en SQLite (evita rescrapear)
- ✅ User-Agent rotation
- ✅ Delays respetables entre requests

**Astro:**
- ✅ Build time SSR (Server-Side Rendering)
- ✅ Zero JavaScript por defecto
- ✅ Lazy loading de imágenes
- ✅ CSS inline (reduce requests)
- ✅ HTML comprimido automáticamente

### Métricas Esperadas

```
Lighthouse Scores:
- Performance: 95+
- Accessibility: 90+
- Best Practices: 95+
- SEO: 100

Page Speed:
- First Contentful Paint: < 1s
- Largest Contentful Paint: < 1.5s
- Time to Interactive: < 2s

File Sizes:
- HTML: 15-25 KB
- CSS: inline (2-5 KB)
- JS: 0 KB (zero JS)
- Total: < 50 KB inicial
```

---

## Extensibilidad

### Agregar nuevo scraper (ej: eBay)

```python
class EBayScraper(Scraper):  # Hereda interfaz
    def scrape_search_results(self, term):
        # Implementar lógica eBay
        pass
```

### Agregar nueva sección en página

```astro
<!-- src/components/NewSection.astro -->
<section>
  {/* Tu HTML aquí */}
</section>

<!-- Importar en index.astro -->
<NewSection products={content.products} />
```

### Agregar nuevo proveedor de IA

```python
class NewProviderAI(AIProvider):
    def generate_niche_content(self, products, niche):
        # Tu lógica aquí
        return json_response
```

---

## Seguridad

### Medidas Implementadas

✅ **Credenciales:**
- Variables de entorno (.env)
- Nunca en código fuente
- .gitignore las excluye

✅ **Scraping Ético:**
- User-Agents realistas
- Delays entre requests
- Respeta robots.txt (consideraciones)

✅ **HTML Output:**
- Sanitizado automáticamente
- rel="noopener noreferrer" en links externos
- rel="sponsored" para afiliación

---

## Debugging

### Logs Útiles

```bash
# Ver logs de scraping
python -u main.py 2>&1 | tee scraping.log

# Ver requests HTTP
import logging
logging.basicConfig(level=logging.DEBUG)
```

### SQLite CLI

```bash
# Verificar base de datos
sqlite3 motor/local_cache.db

# Ver tabla
SELECT * FROM products;

# Contar productos
SELECT COUNT(*) FROM products;
```

---

**Versión:** 1.0.0  
**Última actualización:** Enero 2026

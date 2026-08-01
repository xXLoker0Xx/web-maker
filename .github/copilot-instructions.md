Estoy construyendo un sitio web de comparativas y recomendaciones de productos para monetizar mediante el programa de Afiliados de Amazon. 

CONTEXTO Y OBJETIVO ACTUAL:
- Dominio objetivo: losmejores5.com (o similar).
- Propósito actual: Crear un MVP (Producto Mínimo Viable) funcional, rápido y pulcro que cumpla al 100% con los requisitos de la revisión humana de Amazon Afiliados para obtener las credenciales de la API oficial (PA-API).
- Tengo la parte de automatización/scraping bastante avanzada, pero necesito la web lista e indexable para solicitar la cuenta de afiliados, colocar los enlaces provisionales, realizar las primeras 3 ventas y obtener el acceso definitivo a las API Keys.

TECNOLOGÍA Y REQUISITOS TÉCNICOS DE LA WEB:
1. Arquitectura: Un sitio estático/SSR moderno, ultrarrápido y limpio (prioriza Next.js con Tailwind CSS, Astro o un template HTML/CSS limpio según la estructura del proyecto).
2. Diseño & UX:
   - Apariencia de portal/blog de análisis y comparativas profesional y neutro.
   - Diseño responsive móvil primero.
   - Estructura limpia de encabezados (H1, H2, H3), tablas comparativas de productos y cajas de "Pros y Contras".
3. Secciones Obligatorias para el MVP (Contenido Semilla):
   - Home Page: Presentación del sitio como buscador/comparador de "Los 5 Mejores Productos" en diversas categorías. Muestra de las últimas comparativas/categorías destacadas.
   - Plantilla de Artículo Comparativo (/comparativas/[slug]):
     - Título del artículo (ej. "Los 5 Mejores Aspiradores Sin Cable de 2026").
     - Resumen ejecutivo / Tabla comparativa rápida.
     - Análisis individualizado de cada uno de los 5 productos (Imagen, Características principales, Pros, Contras, Enlace de Afiliado con CTA destacado tipo "Ver precio en Amazon").
     - Guía de compra breve al final del artículo.
   - Páginas Legales y de Cumplimiento de Amazon (CRÍTICO):
     - /aviso-legal
     - /politica-de-privacidad
     - /disclaimer-afiliados (Debe incluir explícitamente el texto exigido por Amazon: "Como afiliado de Amazon, obtengo ingresos por las compras adscritas que cumplen los requisitos aplicables").
4. SEO & Rendimiento:
   - Meta tags dinámicos (title, description, OpenGraph).
   - Sitemap.xml y robots.txt listos.
   - Estructura JSON-LD de datos estructurados para artículos / revisiones de productos.

TAREA INICIAL:
Ayúdame a generar la estructura base del proyecto, los componentes clave del UI (especialmente la Tabla Comparativa de 5 productos y la Ficha de Producto con pros/contras) y las páginas legales requeridas para desplegar el sitio en producción inmediatamente.
# 📰 Web Maker - Generador de Páginas de Nicho para Afiliados de Amazon

Aplicación **local** completa que genera automáticamente páginas web estáticas de nicho para afiliados de Amazon usando Web Scraping, IA y Astro.build.

## ✨ Características

✅ **Web Scraping inteligente** - Extrae datos de productos de Amazon (título, precio, rating, características)  
✅ **Integración con IA local o cloud** - Genera contenido SEO optimizado con Ollama (local), OpenAI, Anthropic o DeepSeek  
✅ **Base de datos local** - SQLite para cachear productos y evitar repetir peticiones  
✅ **CLI interactiva** - Interfaz por consola fácil de usar  
✅ **Plantilla Astro** - Genera páginas 100% responsivas, ultra rápidas y optimizadas para SEO  
✅ **Totalmente local** - Usa Ollama para pruebas sin costo, o APIs de IA para producción  

---

## 📋 Requisitos Previos

- **Python 3.8+**
- **Node.js 18+** (para Astro)
- **npm** o **yarn**
- **Ollama** (RECOMENDADO - https://ollama.ai) O claves de API de:
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Anthropic](https://console.anthropic.com/)
  - [DeepSeek](https://platform.deepseek.com/api)

---

## 🚀 Instalación Rápida (Con Ollama)

### 1️⃣ Instalar Ollama
```bash
# Descargar desde: https://ollama.ai
# Ejecutar instalador
# Terminal 1: ollama serve
# Terminal 2: ollama pull mistral
```

### 2️⃣ Clonar/Descargar el proyecto
```bash
cd c:\Users\diego\Proyectos\19.Web_Maker
```

### 3️⃣ Configurar motor Python
```bash
cd motor

# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4️⃣ Ejecutar
```bash
python main.py
```

### 5️⃣ Ver resultado
```bash
cd ../plantilla-astro
npm install
npm run dev
```

---

## 🎯 Uso

### Con Ollama (RECOMENDADO - Local, Gratis)

```bash
# Terminal 1: Iniciar Ollama
ollama serve

# Terminal 2: Descargar modelo
ollama pull mistral

# Terminal 3: Ejecutar
cd motor
venv\Scripts\activate
python main.py

# Ollama se detecta automáticamente, sin necesidad de .env
```

### Con OpenAI u otro proveedor de API

```bash
# Configurar .env
cd motor
copy .env.example .env
# Edita con tu API key

# Ejecutar
python main.py
```

**Para detalles completos:** Ver [`OLLAMA_SETUP.md`](OLLAMA_SETUP.md) o [`SETUP.md`](SETUP.md)

---

## 🎯 Paso 1: Ejecutar el motor

```bash
cd motor

# Activar venv si no está ya activado
venv\Scripts\activate

# Ejecutar el CLI
python main.py
```

### Paso 2: Seguir el asistente

El programa te pedirá:

1. **Modo de entrada:**
   - Opción 1: Buscar por término (ej: "freidoras de aire")
   - Opción 2: Proporcionar ASINs específicos

2. **Tu ID de afiliado de Amazon** (ej: `mi-tag-21`)

3. **Categoría/Nicho** (solo si usas ASINs)

El proceso generará un archivo `plantilla-astro/src/content/niche.json` con los datos completos.

### Paso 3: Visualizar la página

```bash
cd plantilla-astro

# Iniciar servidor de desarrollo
npm run dev
```

Abre tu navegador en `http://localhost:3000` y verás tu página de nicho renderizada.

### Paso 4: Generar para producción

```bash
# Construir sitio estático
npm run build

# Los archivos listos para producción estarán en `dist/`
```

---

## 📂 Estructura del Proyecto

```
19.Web_Maker/
├── motor/
│   ├── database.py          # SQLite local cache
│   ├── scraper.py           # Web scraper de Amazon
│   ├── ai_generator.py      # Generador de contenido IA
│   ├── main.py              # CLI orquestador
│   ├── requirements.txt      # Dependencias Python
│   ├── .env.example          # Plantilla de variables
│   └── local_cache.db        # (Generado) Base de datos SQLite
│
└── plantilla-astro/
    ├── src/
    │   ├── content/
    │   │   ├── config.ts         # Tipos TypeScript
    │   │   └── niche.json        # (Generado) Datos del nicho
    │   ├── pages/
    │   │   └── index.astro       # Página principal
    │   └── components/
    │       ├── ProductCard.astro       # Tarjeta individual
    │       └── ComparisonTable.astro   # Tabla comparativa
    ├── astro.config.mjs          # Configuración de Astro
    ├── package.json              # Dependencias Node
    └── dist/                     # (Generado) Salida final
```

---

## 🔧 Configuración

### Opción 1: Ollama (LOCAL - RECOMENDADO PARA PRUEBAS)

Detecta automáticamente si Ollama está corriendo en `localhost:11434`.

**Instalación rápida:**
```bash
# 1. Descargar: https://ollama.ai
# 2. Ejecutar: ollama serve
# 3. Otro terminal: ollama pull mistral
# ✓ Listo - No necesitas .env
```

**Modelos disponibles:**
- `mistral` (rápido, 4GB)
- `llama2` (preciso, 3.8GB)
- `neural-chat` (balance, 3.9GB)

**Ver guía completa:** [`OLLAMA_SETUP.md`](OLLAMA_SETUP.md)

### Opción 2: Variables de Entorno

**Ubicación:** `motor/.env`

```env
# Elige UNA opción:

# OpenAI (máxima calidad)
OPENAI_API_KEY=sk_test_xxxxx

# O Anthropic
ANTHROPIC_API_KEY=sk-ant-xxxxx

# O DeepSeek  
DEEPSEEK_API_KEY=sk_xxxxx

# Amazon (obligatorio)
AMAZON_AFFILIATE_TAG=tu-tag-20
```

**Ver plantilla:** [`motor/.env.example`](motor/.env.example)

---

## 📊 Flujo de Datos

```
┌─────────────────┐
│ Usuario ingresa │
│ búsqueda/ASINs  │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│ Scraper extrae datos │
│ de Amazon            │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Se guardan en SQLite │
│ (local_cache.db)     │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ IA genera contenido  │
│ (OpenAI/Anthropic)   │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Se genera niche.json │
│ con datos + IA       │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Astro renderiza      │
│ página HTML estática │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ 🎉 Página lista para │
│ desplegar            │
└──────────────────────┘
```

---

## 🎨 Personalización

### Editar colores y estilos

Todos los componentes Astro tienen estilos integrados. Modifica las propiedades CSS en:

- `src/components/ProductCard.astro` - Tarjetas de productos
- `src/components/ComparisonTable.astro` - Tabla comparativa
- `src/pages/index.astro` - Página principal

### Cambiar estructura HTML

Edita directamente los componentes `.astro`:

```astro
<!-- ProductCard.astro -->
<article class="product-card">
  {/* Personaliza aquí */}
</article>
```

### Agregar componentes nuevos

1. Crea un archivo `.astro` en `src/components/`
2. Impórtalo en `src/pages/index.astro`
3. Úsalo en el layout

---

## 🐛 Solución de Problemas

### Error: "No se encontraron productos"

- Verifica que Amazon no está bloqueando tus peticiones
- Intenta con términos de búsqueda diferentes
- Aumenta los delays en `scraper.py` si recibes 429

### Error de API de IA

- Verifica que tu clave API es correcta
- Revisa que tienes créditos disponibles en el proveedor
- Comprueba la conexión a internet

### Astro no genera la página

- Verifica que `niche.json` existe en `src/content/`
- Ejecuta `npm run dev` nuevamente
- Limpia caché con `npm run build && npm run preview`

---

## 📈 Casos de Uso

✅ Crear sitios de reseñas de productos  
✅ Generar comparativas de precio  
✅ Monetizar contenido con afiliación  
✅ Crear bases de datos de productos  
✅ Automatizar análisis de mercado  
✅ Comparar características de productos  

---

## ⚖️ Cumplimiento Legal

**IMPORTANTE:** Este software es solo para propósitos educativos y de investigación.

⚠️ **Avisos legales:**

- Respeta los `Terms of Service` de Amazon
- No sobrecargues los servidores de Amazon (usa delays adecuados)
- Incluye siempre avisos de afiliado en tu página
- Cumple con la regulación sobre divulgación de afiliados (FTC, AEPD, etc.)
- No copies contenido sin permiso

**Amazon requiere:**
- Declarar claramente que usas enlaces de afiliación
- No garantizar comisiones ni ventas
- No hacer spam

---

## 📝 Licencia

MIT - Libre para uso personal y comercial

---

## 🤝 Contribuciones

Para reportar bugs o sugerir mejoras, contacta al autor.

---

## 📧 Soporte

Para dudas sobre:
- **Configuración de IA:** Consulta la documentación del proveedor
- **Astro:** [Documentación oficial de Astro](https://docs.astro.build)
- **Web Scraping:** Revisa comentarios en `scraper.py`

---

**Versión:** 1.0.0  
**Última actualización:** Enero 2026

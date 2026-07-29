# 🚀 Quick Start Guide

## ⚡ OPCIÓN RÁPIDA: Con Ollama (Local, Sin API Keys)

### 1. Terminal 1: Iniciar Ollama
```bash
ollama serve
```

### 2. Terminal 2: Descargar modelo (primera vez)
```bash
ollama pull mistral
```

### 3. Terminal 3: Ejecutar Web Maker
```bash
cd motor
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**¡Listo!** Ollama se detecta automáticamente. No necesitas .env.

---

## 🚀 OPCIÓN CLÁSICA: Con OpenAI (30 segundos)

### 1. Configurar entorno Python
```bash
cd motor
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Crear archivo .env
```bash
copy .env.example .env
# Editar .env con tu clave de OpenAI y Amazon tag
```

### 3. Ejecutar el generador
```bash
python main.py
```

### 4. Ver resultado
```bash
cd ../plantilla-astro
npm install
npm run dev
```

---

## Ejemplo de ejecución

```
======================================================
🚀 GENERADOR DE PÁGINAS DE NICHO PARA AFILIADOS DE AMAZON
======================================================

Elige un modo de entrada:
1. Buscar por término (ej: 'freidoras de aire')
2. Por ASINs específicos (ej: 'B08ABC123,B08XYZ456')

Opción (1 o 2): 1
Ingresa el término de búsqueda: freidoras de aire
¿Cuántas páginas de resultados deseas (1-3)?: 1

🏷️  Ingresa tu ID de afiliado de Amazon (ej: mi-tag-21): mi-tag-20

============================================================
📥 FASE 1: SCRAPING DE PRODUCTOS
============================================================

📄 Scrapeando página 1 para: freidoras de aire
✓ Se extrajeron 5 productos

💾 Guardando productos en base de datos...
✓ 5/5 productos guardados

============================================================
🤖 FASE 2: GENERACIÓN DE CONTENIDO CON IA
============================================================

✓ Contenido generado por IA exitosamente

============================================================
🔗 FASE 3: FUSIÓN DE DATOS
============================================================

✓ Contenido fusionado exitosamente

============================================================
💾 FASE 4: GUARDADO DE SALIDA
============================================================

✓ JSON guardado en: plantilla-astro/src/content/niche.json
✓ Tamaño: 45321 bytes

============================================================
📊 RESUMEN DE GENERACIÓN
============================================================

📦 Productos procesados: 5
🎯 Título de la página: Las 5 Mejores Freidoras de Aire de 2024
📝 Meta descripción: Análisis completo...
🔗 Productos en contenido: 5
💾 Total en base de datos: 5

✨ ¡Página de nicho generada exitosamente!
📂 Próximo paso: Ejecutar 'npm run dev' en la carpeta plantilla-astro/
```

---

## Estructura de salida (niche.json)

```json
{
  "title": "Las 5 Mejores Freidoras...",
  "description": "Meta SEO...",
  "intro": "Párrafo introductorio...",
  "verdict": "Conclusión...",
  "products": [
    {
      "asin": "B08ABC123",
      "title": "...",
      "badge": "Mejor Calidad-Precio",
      "price": "99,99€",
      "rating": 4.8,
      "reviews_count": 1250,
      "image_url": "https://...",
      "pros": ["Pro 1", "Pro 2"],
      "cons": ["Contra"],
      "summary": "Resumen generado por IA...",
      "affiliate_url": "https://amazon.es/dp/B08ABC123?tag=tu-tag"
    }
  ]
}
```

---

## Archivos clave

- `motor/main.py` - Ejecuta esto para generar
- `plantilla-astro/src/content/niche.json` - Salida generada
- `plantilla-astro/src/pages/index.astro` - Página principal
- `motor/.env` - Tus credenciales (no compartir)

---

**¡Listo!** Tu primera página de nicho está lista 🎉

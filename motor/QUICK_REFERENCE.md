# Quick Reference Guide

## 🚀 Empezar

### Menú Interactivo (Recomendado)
```bash
cd motor
python main.py
```

**Menú Principal:**
```
  [1] 🌐 Scraping only (extract products from Amazon)
  [2] 🤖 AI only (generate content for existing niches)
  [3] 🔄 Scraping + AI (scrape then generate content)
  [4] 🔧 Advanced options
  [5] Exit
```

---

## 📋 Opción [1]: Scraping Only

Extrae productos de Amazon y guarda en JSON (con nombre auto-generado):

```bash
# Desde menú:
# [1] 
# "freidoras de aire" (search term)
# → ✓ Niche name: freidoras-de-aire (AUTO-GENERATED!)
# → Press Enter to confirm or type new name
# 3 (pages to scrape)
# ✓ Guarda: plantilla-astro/src/content/niches/freidoras-de-aire.json
```

**Proceso:**
1. Ingresas el término de búsqueda (ej: "freidoras de aire")
2. El sistema **automáticamente genera** el nombre del niche (ej: "freidoras-de-aire")
3. Puedes confirmar presionando Enter o tipear uno diferente
4. El scraping comienza

---

## 📋 Opción [2]: AI Only

Detecta automáticamente los niches disponibles y permite seleccionar cuál procesar:

```bash
# Desde menú:
# [2]
# Se muestran los niches disponibles:
#   [1] bici de montaña
#   [2] freidora-de-aire
#   [0] Generate ALL niches
# [1] (select option)
# ✓ Genera contenido para ese niche (Steps 1-3)
```

**Proceso:**
1. El sistema **lista automáticamente** los JSON disponibles
2. Seleccionas cuál procesar (o [0] para todos)
3. El sistema extrae el nombre del archivo y genera contenido
4. **No necesitas escribir nada** - todo es auto-generado

---

## 📋 Opción [3]: Scraping + AI (RECOMENDADO)

Scrape automático + generación de contenido en una sola acción:

```bash
python main.py
# [3] 
# "freidoras de aire" (search term)
# → ✓ Niche name: freidoras-de-aire (AUTO-GENERATED!)
# → Press Enter to confirm
# 3 (pages)
# ✅ Scrape + IA completo en ~150-200s
```

**Proceso:**
1. Ingresas qué buscar (ej: "freidoras de aire")
2. **Auto-genera** el nombre del niche (ej: "freidoras-de-aire")
3. Confirmas o editas
4. Seleccionas páginas a scrapear (default: 3)
5. **Scraping** (60-120s)
6. **AI Generation** Steps 1-3 (70-110s)
7. ✅ Listo para deploy

---

## 📋 Opción [4]: Advanced Options

```bash
  [1] Generate ALL niches (all 3 steps)
     → Genera contenido para TODOS los niches disponibles

  [2] Generate SPECIFIC niche
     → Muestra lista de niches disponibles
     → Seleccionas cuál procesar (niche name auto-detected)
     → ✓ Genera los 3 steps para ese niche

  [3] Run specific STEPS only
     → Elige qué steps ejecutar (1, 2, 3)
     → Elige qué niche (o todos)

  [4] Regenerate everything (--force)
     → Sobrescribe TODO incluso si ya existe

  [5] Change Ollama model
     → Cambiar modelo: mistral, llama3, llama3.2

  [6] Back to main menu
```

---

## ⏱️ Tiempos de Ejecución

| Operación | Tiempo |
|-----------|--------|
| Scraping (3 pages) | ~60-120s |
| Step 1 (Intro) | ~20-30s |
| Step 2 (FAQ) | ~20-30s |
| Step 3 (Pros/Cons) | ~30-50s |
| **Scraping + AI** | **~150-200s** |

---

## 🔧 Troubleshooting

### Error: "Cannot connect to Ollama"
```bash
# Terminal 1:
ollama serve

# Terminal 2:
cd motor
python main.py
```

### Playwright no instalado (necesario para scraping)
```bash
pip install playwright
playwright install chromium
```

### Content vacío o incompleto
```bash
python main.py
# [4] → [4] → Regenerate everything
```

---

## 📂 Archivos Generados

```
plantilla-astro/src/content/niches/
├── freidora-de-aire.json      ← title, intro, verdict, 
│                                 buying_criteria, products, FAQ
└── balones-de-futbol.json
```

Cada JSON contiene:
- ✅ Title (con año 2025, etc.)
- ✅ Description (meta-optimizada)
- ✅ Intro (200-300 palabras)
- ✅ Verdict (150-200 palabras)
- ✅ Buying Criteria (5-7 factores)
- ✅ Products (5 items con pros/cons)
- ✅ FAQ (7-8 preguntas semánticas)

---

## ✅ Flujo de Trabajo Típico

### Crear niche NUEVO (Recomendado)
```bash
cd motor
python main.py
# [3] Scraping + AI
# "freidoras de aire" ← Ingresas búsqueda
# [Enter] → Auto-detecta "freidoras-de-aire"
# [Enter] → Confirmas (o editas)
# 3 → Páginas (default)
# ⏳ ~150-200s
# ✓ Listo para deploy
```

### Generar contenido IA para niche existente
```bash
python main.py
# [2] AI Only
# Se muestran niches disponibles:
#   [1] freidora-de-aire
#   [2] bici de montaña
# [1] → Seleccionas
# ⏳ ~70-110s
# ✓ Contenido generado
```

### Regenerar niche existente
```bash
python main.py
# [4] Advanced
# [4] Regenerate everything
```

### Cambiar modelo Ollama
```bash
python main.py
# [4] Advanced
# [5] Change model
# "llama3.2"
```

---

## 📋 CLI Mode (Para Scripts/Automatización)

```bash
# Generar todos
python main.py --step 1 2 3

# Generar niche específico
python main.py --niche freidoras

# Regenerar con force
python main.py --force

# Cambiar modelo
python main.py --model llama3.2 --niche balones

# Ver ayuda
python main.py --help
```

---

## ✅ Checklist Previo a Deploy

- [ ] Ejecutar menú [3]: Scraping + AI
- [ ] Revisar `plantilla-astro/src/content/niches/`
- [ ] Verificar título con año
- [ ] Verificar pros/cons en productos
- [ ] Verificar 7-8 FAQ items
- [ ] Build: `cd plantilla-astro && npm run build`
- [ ] Deploy: `vercel --prod`

---

**Estado**: Production Ready ✅  
**Nuevas Features**: Scraping Integrado + Menú Interactivo  
**Última Actualización**: 2026-08-06

# ⚡ Referencia Rápida - Web Maker

## 🎯 Flujo Completamente Local (Ollama)

### Terminal 1: Servidor Ollama
```bash
ollama serve
```

### Terminal 2: Descargar Modelo
```bash
ollama pull mistral
```
*(Solo la primera vez)*

### Terminal 3: Ejecutar Web Maker
```bash
cd c:\Users\diego\Proyectos\19.Web_Maker\motor

# Si es primera vez
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# O si ya existe el venv
venv\Scripts\activate

# Ejecutar
python main.py
```

## 📍 Comandos Principales

### Motor Python
```bash
cd motor
venv\Scripts\activate
python main.py
```

### Astro Frontend
```bash
cd plantilla-astro
npm install                    # Primera vez
npm run dev                   # Desarrollo (http://localhost:3000)
npm run build                 # Producción
npm run preview               # Ver compilado
```

---

## 🔧 Configuración Rápida

### .env (solo si NO usas Ollama)
```bash
# Crear desde plantilla
copy motor\.env.example motor\.env

# Editar con tus claves
OPENAI_API_KEY=sk_...
AMAZON_AFFILIATE_TAG=tu-tag
```

### Cambiar Modelo de Ollama
```bash
# Editar motor/.env
OLLAMA_MODEL=llama2          # O neural-chat, dolphin-mixtral
```

---

## 📁 Estructura

```
motor/                   # Backend Python
├── database.py         # SQLite + scraping cache
├── scraper.py          # Web scraper Amazon
├── ai_generator.py     # Ollama + OpenAI + más
├── main.py             # CLI orquestador
├── requirements.txt
└── .env.example

plantilla-astro/         # Frontend Astro
├── src/
│   ├── pages/index.astro
│   ├── components/
│   │   ├── ProductCard.astro
│   │   └── ComparisonTable.astro
│   └── content/
│       └── niche.json  # Generado por motor
└── astro.config.mjs
```

---

## 🚀 Primera Ejecución Paso a Paso

1. **Instalar Ollama**
   ```bash
   # https://ollama.ai → descargar e instalar
   ```

2. **Activar Ollama**
   ```bash
   # Terminal 1
   ollama serve
   
   # Terminal 2
   ollama pull mistral
   ```

3. **Configurar Python**
   ```bash
   cd motor
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Ejecutar Motor**
   ```bash
   python main.py
   
   # Seguir prompts:
   # - Opción: buscar por término o ASINs
   # - Término: ej "freidoras de aire"
   # - Tag: tu-tag-20
   ```

5. **Ver Resultado**
   ```bash
   cd ..\plantilla-astro
   npm install
   npm run dev
   # Abre http://localhost:3000
   ```

---

## 🐛 Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| No encuentra Ollama | Verifica `ollama serve` en Terminal 1 |
| Modelo no encontrado | Ejecuta `ollama pull mistral` en Terminal 2 |
| Error "No se pudo crear tabla" | Elimina `motor/products.db` e intenta de nuevo |
| Puerto 3000 ocupado | Cambia en `plantilla-astro/astro.config.mjs` |
| API key inválida | Verifica `.env` (solo si NO usas Ollama) |

---

## 💡 Tips

✅ **Primera prueba:** Usa solo 2-3 productos para ir rápido  
✅ **Mejor velocidad:** Usa GPU (NVIDIA/AMD/Apple Silicon)  
✅ **Mejor modelo:** Mistral para velocidad, Llama2 para calidad  
✅ **Guardar logs:** `python main.py > log.txt 2>&1`  
✅ **Multiproceso:** Abre 3 terminales (Ollama, Python, npm run dev)  

---

## 📚 Documentación Completa

- [`README.md`](README.md) - Visión general
- [`SETUP.md`](SETUP.md) - Configuración detallada
- [`OLLAMA_SETUP.md`](OLLAMA_SETUP.md) - Guía Ollama completa
- [`ARCHITECTURE.md`](ARCHITECTURE.md) - Detalles técnicos
- [`QUICKSTART.md`](QUICKSTART.md) - Inicio rápido

---

## 🎯 Próximos Pasos

1. Instala Ollama (5 min)
2. Ejecuta `ollama serve` + `ollama pull mistral` (10 min)
3. Corre `python main.py` (1-2 min por página)
4. Abre `npm run dev` (visualiza resultado)
5. ¡Genera más páginas!

---

**v1.0.0** | Enero 2026

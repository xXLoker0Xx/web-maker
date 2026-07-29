# 📚 Guía de Configuración - Web Maker

## 🔑 OPCIÓN 1: Ollama (LOCAL - RECOMENDADO PARA PRUEBAS) ⭐

La forma más sencilla para empezar es usar **Ollama**, que ejecuta modelos de IA localmente sin API keys.

### Paso 1: Instalar Ollama

1. Descarga desde https://ollama.ai
2. Ejecuta el instalador
3. En terminal: `ollama serve` (mantén abierto)
4. En otra terminal: `ollama pull mistral`
5. ✓ ¡Listo!

**Tiempo:** 15 minutos  
**Costo:** $0  
**Ventajas:** No necesitas API keys, privado, offline

**Ver guía completa:** [`OLLAMA_SETUP.md`](OLLAMA_SETUP.md)

---

## 🔑 OPCIÓN 2: OpenAI (Recomendado si quieres máxima calidad)

### Opción A: OpenAI (RECOMENDADO) ⭐

### Opción A: OpenAI (RECOMENDADO) ⭐

1. Ir a https://platform.openai.com/api-keys
2. Crear una cuenta o iniciar sesión
3. Click en "Create new secret key"
4. Copiar la clave (comienza con `sk-`)
5. Guardar en `.env`:
   ```
   OPENAI_API_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxx
   ```

**Modelos disponibles:**
- gpt-4-turbo-preview (mejor calidad)
- gpt-3.5-turbo (más rápido/barato)

---

### Opción A2: OpenAI (RECOMENDADO) ⭐

1. Ir a https://platform.openai.com/api-keys

1. Ir a https://console.anthropic.com/
2. Crear cuenta
3. Ir a "API Keys"
4. Generar nueva clave
5. Guardar en `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
   ```

---

### Opción C: DeepSeek 🟢

1. Ir a https://platform.deepseek.com/api
2. Crear cuenta
3. Ir a "API Keys"
4. Copiar la clave
5. Guardar en `.env`:
   ```
   DEEPSEEK_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxx
   ```

---

## 💰 Paso 1 (alternativa): Configurar Amazon Affiliate

### Registrarse como Afiliado de Amazon

1. Ir a https://asociados.amazon.es/ (España)
2. Click en "Inscribirse ahora"
3. Seguir el registro
4. Una vez aprobado, obtener tu **ID de etiqueta** (tag)

**Ejemplo:** `mi-tag-21`

**Guardar en `.env`:**
```
AMAZON_AFFILIATE_TAG=mi-tag-21
```

---

## 🐍 Paso 3: Instalar Python

### Windows

1. Descargar desde https://www.python.org/downloads/
2. **IMPORTANTE:** Marcar "Add Python to PATH"
3. Siguiente → Instalar

**Verificar instalación:**
```bash
python --version
```

---

## ⚙️ Paso 4: Crear `.env` en motor/

```bash
cd motor

# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**Editar `.env` con tus claves:**

```env
# Elige UNA de estas (descomenta la que uses)

# OPENAI_API_KEY=sk_test_xxxxx
# ANTHROPIC_API_KEY=sk-ant-xxxxx  
# DEEPSEEK_API_KEY=sk_xxxxx

AMAZON_AFFILIATE_TAG=tu-tag-20
```

---

## 🔍 Paso 5: Configurar Entorno Virtual Python

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## 📦 Paso 6: Instalar Dependencias de Node

```bash
cd plantilla-astro

npm install
# o
yarn install
```

---

## ✅ Paso 7: Verificar Configuración

```bash
cd motor

# Activar venv
venv\Scripts\activate

# Ejecutar
python main.py
```

**Si todo funciona correctamente:**
- ✅ Se abrirá la interfaz interactiva
- ✅ Podrás elegir buscar productos o ingresar ASINs
- ✅ Se generará el archivo `niche.json`

---

## 🚨 Errores Comunes

### Error: "ModuleNotFoundError: No module named 'requests'"

**Solución:**
```bash
# Asegúrate de estar en el venv
# Luego reinstala
pip install -r requirements.txt
```

### Error: "OPENAI_API_KEY not found"

**Solución:**
- Revisa que el archivo `.env` existe en `motor/`
- Verifica que tu clave está correcta en `.env`
- Reinicia la terminal

### Error: "No se pueden conectar a Amazon"

**Solución:**
- Verifica tu conexión a internet
- Intenta con un VPN (si Amazon te bloquea)
- Espera unos minutos y reintenta

### Astro no genera la página

**Solución:**
```bash
cd plantilla-astro
rm -rf dist/
npm run build
npm run dev
```

---

## 📊 Pricings Aproximados (2026)

### OpenAI
- **Entrada:** $0.01 / 1K tokens
- **Salida:** $0.03 / 1K tokens
- **Costo por página:** $0.10 - $0.50

### Anthropic
- **Entrada:** $0.008 / 1K tokens
- **Salida:** $0.024 / 1K tokens
- **Costo por página:** $0.08 - $0.40

### DeepSeek
- **Más económico que OpenAI**
- **Costo por página:** $0.03 - $0.15

---

## 🎯 Tips de Optimización

### Para reducir costos de IA:

1. **Usar GPT-3.5 en lugar de GPT-4**
2. **Limitar cantidad de productos** (3-5 máximo)
3. **Usar DeepSeek** (es más barato)
4. **Reutilizar productos en caché** (opción "skip scraping")

### Para mejorar calidad de scraping:

1. **Usar menos páginas** (1-2 máximo)
2. **Búsquedas específicas** (no genéricas)
3. **ASINs directos** (si los tienes)
4. **Horarios específicos** (Amazon es más rápido de madrugada)

---

## 📱 Próximos Pasos

1. ✅ Configuración completada
2. 🚀 Ejecutar `python main.py`
3. 🎨 Personalizar estilos CSS
4. 📦 Generar sitios
5. 📈 Monetizar con Amazon Associates

---

**¿Listo?** ¡Ejecuta `python main.py` y comienza a generar páginas de nicho! 🚀

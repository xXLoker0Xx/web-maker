# 🤖 Guía Completa de Ollama - LLM Local

## ¿Qué es Ollama?

**Ollama** es un cliente que te permite ejecutar modelos de lenguaje grandes (LLMs) completamente **LOCAL** en tu máquina sin depender de APIs externas.

### Ventajas:
✅ **Gratis** - No hay costo por token  
✅ **Privado** - Tus datos nunca salen de tu máquina  
✅ **Rápido** - Latencia baja  
✅ **Offline** - No necesitas internet  
✅ **Perfecto para pruebas** - Desarrollo sin límites  

---

## 📥 Instalación

### Paso 1: Descargar Ollama

1. Ve a https://ollama.ai
2. Descarga según tu sistema:
   - **Windows:** ollama-windows.exe
   - **Mac:** ollama-arm64.zip (Apple Silicon) o ollama-amd64.zip (Intel)
   - **Linux:** `curl https://ollama.ai/install.sh | sh`

### Paso 2: Instalar

**Windows:**
- Ejecuta el `.exe`
- Sigue el instalador
- Se instalará como servicio

**Mac:**
- Descomprime el .zip
- Ejecuta `./ollama`
- O instálalo como app: arrastra a Applications

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

### Paso 3: Verificar Instalación

```bash
ollama --version
# Output: ollama version X.X.X
```

---

## 🚀 Usando Ollama

### Paso 1: Iniciar Servidor

Abre una terminal y ejecuta:

```bash
ollama serve
```

**Output esperado:**
```
2026/01/29 10:15:32 "GET / HTTP/1.1" 404 Not Found
```

Mantén esta terminal abierta. Ollama ahora está corriendo en `localhost:11434`

### Paso 2: Descargar un Modelo

Abre **otra terminal** (la primera debe seguir corriendo) y ejecuta:

```bash
# Para Mistral (recomendado - más rápido)
ollama pull mistral

# O para Llama 2 (más preciso pero más lento)
ollama pull llama2

# O para Neural Chat (buena alternativa)
ollama pull neural-chat
```

**Tiempo esperado:** 5-15 minutos (depende de tu conexión)  
**Espacio:** 3-7 GB por modelo

### Paso 3: Verificar Modelos

```bash
ollama list
```

**Output:**
```
NAME                SIZE      MODIFIED
mistral:latest      4.0 GB    2 minutes ago
llama2:latest       3.8 GB    5 minutes ago
```

---

## 🧪 Probar Ollama Manualmente

```bash
ollama run mistral
```

Luego escribe un prompt:

```
>>> Escribe un título SEO para una página sobre freidoras de aire
```

Verás la respuesta generada en tiempo real. Presiona Ctrl+D para salir.

---

## 💻 Usar en Web Maker

### Configuración Automática

Web Maker detecta Ollama automáticamente si está corriendo:

```bash
cd motor
python main.py
```

El sistema intentará usar Ollama primero, luego otros proveedores.

### Configuración Manual (opcional)

Edita `motor/.env`:

```env
# Para especificar modelo diferente
OLLAMA_MODEL=llama2
# O
OLLAMA_MODEL=neural-chat
```

### Ejecutar Generador

```bash
python main.py

# Sigue los pasos:
# 1. Elige búsqueda o ASINs
# 2. Ingresa término
# 3. ¡El generador usa Ollama automáticamente!
```

---

## 🎯 Modelos Disponibles

### Mistral (RECOMENDADO)
```bash
ollama pull mistral
```
- ⚡ **Velocidad:** Muy rápido (1-2 seg por respuesta)
- 🎯 **Calidad:** Buena
- 💾 **Tamaño:** 4 GB
- 📊 **Mejor para:** Producción rápida

### Llama 2
```bash
ollama pull llama2
```
- ⚡ **Velocidad:** Medio (3-5 seg por respuesta)
- 🎯 **Calidad:** Muy buena
- 💾 **Tamaño:** 3.8 GB
- 📊 **Mejor para:** Calidad de contenido

### Neural Chat
```bash
ollama pull neural-chat
```
- ⚡ **Velocidad:** Rápido (2-3 seg por respuesta)
- 🎯 **Calidad:** Excelente
- 💾 **Tamaño:** 3.9 GB
- 📊 **Mejor para:** Balance velocidad/calidad

### Dolphin Mixtral
```bash
ollama pull dolphin-mixtral
```
- ⚡ **Velocidad:** Lento (8-10 seg por respuesta)
- 🎯 **Calidad:** Excelente
- 💾 **Tamaño:** 26 GB
- 📊 **Mejor para:** Máxima calidad (requiere GPU potente)

---

## ⚙️ Optimización para Hardware

### GPU (Recomendado)

**NVIDIA (CUDA):**
```bash
# Ollama detecta automáticamente
ollama serve

# Verifica que usa GPU en los logs
# "llamafile: compute gpu inference"
```

**AMD (ROCm):**
```bash
export ROCR_VISIBLE_DEVICES=0
ollama serve
```

**Apple Silicon (Metal):**
```bash
# Ollama lo hace automáticamente
ollama serve
```

### CPU Solamente

```bash
# Funciona pero es más lento
ollama serve
```

**Recomendación:** Usa Mistral con CPU, es muy eficiente.

---

## 🔧 Ajustes de Rendimiento

### Cambiar cantidad de contexto

Por defecto: 2048 tokens

```bash
ollama run mistral /set parameter num_ctx 4096
```

### Cambiar threads de CPU

```bash
export OLLAMA_NUM_THREAD=8  # Usa 8 cores
ollama serve
```

### Cambiar temperatura (creatividad)

Edita `ai_generator.py` en `OllamaProvider`:

```python
response = requests.post(
    self.api_url,
    json={
        "model": self.model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.5,  # Cambiar aquí (0.0=determinístico, 1.0=creativo)
    },
    timeout=300
)
```

---

## 📊 Performance Esperado

Con **Mistral** y **GPU NVIDIA**:
- Primera respuesta: 2-3 segundos
- Resto de tokens: 50-100 ms por token
- Total para página de nicho: 10-30 segundos

Con **Mistral** y **CPU**:
- Primera respuesta: 5-10 segundos  
- Resto de tokens: 200-500 ms por token
- Total para página de nicho: 30-60 segundos

---

## 🐛 Solución de Problemas

### Error: "No se puede conectar a Ollama"

**Solución:**
1. Verifica que tienes una terminal con `ollama serve` corriendo
2. Verifica que no está bloqueado por firewall
3. Prueba: `curl http://localhost:11434/api/tags`

### Error: "Modelo no encontrado"

**Solución:**
```bash
# En otra terminal
ollama pull mistral

# Verifica
ollama list
```

### Ollama muy lento

**Soluciones:**
1. Usa GPU en lugar de CPU
2. Cambia a modelo más pequeño (Mistral)
3. Cierra otras aplicaciones
4. Aumenta RAM disponible

### Memoria insuficiente

**Síntomas:**
- Ollama se congela o falla
- Respuestas incompletas

**Soluciones:**
```bash
# Usa modelo más pequeño
ollama pull mistral  # 4GB

# O reduce contexto
export OLLAMA_NUM_CTX=1024
ollama serve
```

### Output extraño o incompleto

**Solución:**
- El modelo generó un JSON inválido
- Intenta nuevamente
- O cambia de modelo (Llama2 es más preciso)

---

## 🔌 API REST de Ollama

Si quieres usar Ollama directamente (sin Web Maker):

```python
import requests

url = "http://localhost:11434/api/generate"
data = {
    "model": "mistral",
    "prompt": "¿Cuál es la capital de Francia?",
    "stream": False
}

response = requests.post(url, json=data)
result = response.json()
print(result['response'])
```

---

## 📝 Comandos Útiles

```bash
# Ver modelos
ollama list

# Descargar modelo
ollama pull nombre_modelo

# Ejecutar modelo interactivamente
ollama run mistral

# Ver información del servidor
curl http://localhost:11434/api/tags

# Eliminar modelo
ollama rm mistral

# Actualizar Ollama
# Windows: Ejecuta el instalador de nuevo
# Mac: brew upgrade ollama
# Linux: curl https://ollama.ai/install.sh | sh
```

---

## 🚀 Flujo Completo (para pruebas)

### Terminal 1: Servidor Ollama
```bash
ollama serve
```

### Terminal 2: Descargar modelo (una sola vez)
```bash
ollama pull mistral
```

### Terminal 3: Ejecutar Web Maker
```bash
cd c:\Users\diego\Proyectos\19.Web_Maker\motor

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python main.py
```

¡Listo! Ollama está funcionando con Web Maker.

---

## 💡 Tips

✅ **Para comenzar:** Usa **Mistral** (rápido y bueno)  
✅ **Para calidad:** Usa **Llama2** (más preciso)  
✅ **Para máxima calidad:** Usa **Dolphin Mixtral** (mejor pero más lento)  
✅ **Con GPU:** Todas las pruebas son prácticas  
✅ **Con CPU:** Mistral es la mejor opción  
✅ **Primeras pruebas:** Generas 2-3 productos (es más rápido)  

---

## 📈 Próximos Pasos

1. ✅ Instala Ollama
2. ✅ Ejecuta `ollama serve`
3. ✅ Descarga un modelo: `ollama pull mistral`
4. ✅ Ejecuta Web Maker
5. ✅ ¡Genera tu primera página!

---

**Versión:** 1.0.0  
**Última actualización:** Enero 2026  

¡Disfruta usando LLMs locales sin costo! 🎉

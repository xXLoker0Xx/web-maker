# 🚀 Sistema Multi-Página - Web Maker

## ¿Qué Cambió?

Ahora puedes generar **múltiples páginas de nicho** que se mostrarán en rutas diferentes:

- **Página Principal:** `/` - Índice con lista de todos los nichos
- **Página de Nicho:** `/freidoras/` - Tu página sobre freidoras
- **Otra Página:** `/cafetera/` - Tu página sobre cafeteras
- **Y más:** `/tv/`, `/smartwatch/`, etc.

Antes sobrescribía `niche.json`. **Ahora cada nicho tiene su propio archivo JSON.**

---

## 🎯 Cómo Funciona

### Estructura de Archivos

```
plantilla-astro/src/content/
├── freidoras.json        ← Generado por python main.py (primer run)
├── cafetera.json         ← Generado por python main.py (segundo run)
├── tv.json               ← Generado por python main.py (tercer run)
└── config.ts             ← (Sin cambios)
```

### Rutas Generadas

Astro genera automáticamente:

```
dist/
├── index.html                    ← Página principal (lista todos)
├── freidoras/index.html          ← /freidoras/
├── cafetera/index.html           ← /cafetera/
└── tv/index.html                 ← /tv/
```

---

## 📝 Flujo de Trabajo

### Primera Página

```bash
# Terminal 1: Ollama (si lo usas)
ollama serve

# Terminal 2: Generar página 1
cd motor
python main.py

# Prompts:
# 1. Buscar o ASINs? → 1
# 2. Término: freidoras de aire
# 3. Páginas: 2
# 4. Tag: tu-tag-20

# ✓ Genera: plantilla-astro/src/content/freidoras.json
# ✓ Astro genera: /freidoras/
```

### Segunda Página

```bash
# Terminal 3: Generar página 2
cd motor
python main.py

# Prompts:
# 1. Buscar o ASINs? → 1
# 2. Término: cafetera
# 3. Páginas: 2
# 4. Tag: tu-tag-20

# ✓ Genera: plantilla-astro/src/content/cafetera.json
# ✓ Astro genera: /cafetera/
```

### Tercera, Cuarta, ... Página

Repite el proceso. Cada ejecución de `python main.py` crea un nuevo JSON sin sobrescribir los anteriores.

---

## 🌐 En Vercel

### Setup

El flujo es exactamente igual:

```bash
# Generar páginas LOCALMENTE
1. Ejecutar python main.py (N veces)
2. Se crean freidoras.json, cafetera.json, tv.json, etc.

# Compilar y subir
3. git add plantilla-astro/src/content/*.json
4. git commit -m "Agregar nuevas páginas"
5. git push

# Vercel automáticamente:
6. Detecta nuevos archivos
7. Ejecuta: cd plantilla-astro && npm run build
8. Lee TODOS los JSON
9. Genera routes dinámicas para cada uno
10. Deploya /freidoras/, /cafetera/, /tv/, etc.
```

---

## 🔧 Cambios en el Código

### Motor Python (main.py)

**Antes:**
```python
astro_content_path = Path(...) / "niche.json"
self.save_output(merged_content, str(astro_content_path))
```

**Ahora:**
```python
self.niche_slug = self._slugify(niche)  # "freidoras de aire" → "freidoras-de-aire"

filename = f"{self.niche_slug}.json"     # "freidoras-de-aire.json"
astro_content_path = content_dir / filename
self.save_output(merged_content, str(astro_content_path))
```

### Astro (Pages)

**Antes:**
- `/src/pages/index.astro` → Una sola página

**Ahora:**
- `/src/pages/index.astro` → **Página principal (índice)**
- `/src/pages/[slug].astro` → **Página dinámica** (genera `/freidoras/`, `/cafetera/`, etc.)

**El archivo `[slug].astro` usa `getStaticPaths()`:**

```typescript
export async function getStaticPaths() {
  // Lee TODOS los JSON en src/content/
  const files = import.meta.glob<{ default: NicheContent }>('../content/**/*.json', { 
    eager: true,
    import: 'default'
  });

  // Crea una ruta para cada uno
  return Object.entries(files).map(([path, module]) => {
    const slug = path.split('/').pop()?.replace('.json', '') || 'index';
    return {
      params: { slug },
      props: { content: module, slug: slug }
    };
  });
}
```

---

## 📊 Ejemplo Real

### Genera esto:

```
Termina python main.py:
✓ freidoras-de-aire.json creado
```

```
Termina python main.py:
✓ cafetera-espresso.json creado
```

```
Termina python main.py:
✓ smartwatch-deportivo.json creado
```

### Astro genera automáticamente:

```
npm run build

Rendering routes...
  ✓ / (index)
  ✓ /freidoras-de-aire/
  ✓ /cafetera-espresso/
  ✓ /smartwatch-deportivo/

4 routes generated
```

### El usuario ve:

**Página principal:** https://tu-dominio.com
- Título "Web Maker"
- 3 tarjetas de nichos
- Clic en "Freidoras de Aire" → /freidoras-de-aire/
- Clic en "Cafetera Espresso" → /cafetera-espresso/
- Clic en "Smartwatch Deportivo" → /smartwatch-deportivo/

---

## ✅ Validar que Funciona

### Local (desarrollo)

```bash
cd plantilla-astro
npm run build

# Deberías ver:
# ✓ / (index)
# ✓ /[nombre-del-nicho]/ (por cada JSON)
```

### Vercel

1. Crea varios nichos
2. Súbelos a GitHub
3. Vercel genera las rutas automáticamente
4. Visita: https://tu-proyecto.vercel.app/
5. Verás el índice con todos los nichos
6. Haz clic en uno → Va a `/nicho-1/`, `/nicho-2/`, etc.

---

## 🎁 Ventajas

✅ **Múltiples nichos en un sitio**  
✅ **Sin sobrescribir** - Cada nicho es independiente  
✅ **SEO** - Cada página es un sitio SEO completo  
✅ **Escalable** - Genera 100 nichos si quieres  
✅ **Vercel optimizado** - Despliega todas automáticamente  
✅ **Sin conflictos** - Puedes generar en paralelo (si quieres)

---

## 💡 Próximos Pasos

1. **Probar localmente:**
   ```bash
   python main.py  # Nicho 1
   python main.py  # Nicho 2
   npm run build
   npm run preview
   # Deberías ver múltiples rutas
   ```

2. **Subir a Vercel:**
   ```bash
   git add .
   git commit -m "Sistema multi-página implementado"
   git push
   # Vercel despliega automáticamente
   ```

3. **Crear más nichos:**
   - Ejecuta `python main.py` tantas veces como nichos quieras
   - Cada uno es independiente
   - Cada uno su propia URL

---

## 🐛 Troubleshooting

### "No se genera la ruta"
- Verifica que el JSON está en `plantilla-astro/src/content/`
- El nombre debe ser `[slug].json` (sin espacios ni caracteres especiales)
- Ejecuta `npm run build` para regenerar

### "Sobrescribió mi página anterior"
- Eso no sucede más, cada nicho tiene su archivo
- Revisa que el nombre sea diferente (slugs diferentes)

### "¿Cómo cambio la URL de la página?"
- La URL se genera del nombre del JSON
- `freidoras-aire.json` → `/freidoras-aire/`
- Para cambiarla, renombra el JSON

---

**¡Ahora tienes un sistema de múltiples páginas escalable!** 🎉

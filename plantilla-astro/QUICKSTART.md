# 🚀 QUICK START - Web Maker

## Paso 1: Instalar Dependencias

```bash
cd plantilla-astro
npm install
# o
pnpm install
```

## Paso 2: Iniciar Servidor de Desarrollo

```bash
npm run dev
```

Abre tu navegador en: **http://localhost:3000**

Ahora deberías ver:
- ✅ Estilos Tailwind CSS aplicados
- ✅ Colores profesionales (Indigo/Purple)
- ✅ Tipografía escalable
- ✅ Cards con sombra y hover
- ✅ Diseño responsive

## Paso 3: Verificar que Funciona

1. **Index (Home)** - Verifica que veas:
   - ✅ Hero con gradiente azul-púrpura
   - ✅ Estadísticas con números grandes
   - ✅ Grid de categorías
   - ✅ Footer profesional

2. **Página de Comparación** (si tienes JSON en content/niches/)
   - ✅ Hero dinámico
   - ✅ Disclaimer banner
   - ✅ Best product section con badge 🏆
   - ✅ Grid de productos
   - ✅ Tabla comparativa

3. **Páginas Legales** (/aviso-legal, /politica-de-privacidad, etc.)
   - ✅ Diseño profesional
   - ✅ Tipografía clara
   - ✅ Espaciado consistente

## Paso 4: Generar Contenido

Si tienes datos JSON, genera páginas:

```bash
cd ..
python motor/main.py
# Esto crea archivos en plantilla-astro/src/content/niches/
```

## Paso 5: Build para Producción

```bash
cd plantilla-astro
npm run build
```

Esto genera archivos listos en `dist/`

## Troubleshooting

### "No veo estilos"

1. **Reinstala dependencias:**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Limpia caché:**
   ```bash
   npm run dev -- --force
   ```

3. **Verifica que globals.css exista:**
   ```bash
   ls src/styles/globals.css
   ```

### "Error en Tailwind"

Asegúrate de que tienes:
- ✅ `@astrojs/tailwind` en package.json
- ✅ `tailwind.config.mjs` (no .js)
- ✅ `postcss.config.cjs`
- ✅ `astro.config.mjs` con `integrations: [tailwind()]`

## 🎨 Design Tokens Disponibles

En Tailwind/CSS puedes usar:

```html
<!-- Colores -->
<div class="bg-primary text-white">Indigo (Primary)</div>
<div class="bg-accent">Amber (Accent)</div>
<div class="bg-background">Claro (Background)</div>

<!-- Espaciado -->
<div class="p-lg">Padding large (40px)</div>
<div class="gap-md">Gap medium (24px)</div>

<!-- Tipografía -->
<h1 class="text-h1">56px Bold</h1>
<h2 class="text-h2">34px Bold</h2>
<p class="text-body">18px Normal</p>

<!-- Cards -->
<div class="card">Card premium con sombra</div>

<!-- Botones -->
<button class="btn btn-primary">Azul principal</button>
<button class="btn btn-outline">Outline</button>
```

## 📚 Estructura de Carpetas

```
plantilla-astro/
├── src/
│   ├── styles/
│   │   └── globals.css (estilos globales con Tailwind)
│   ├── layouts/
│   │   └── BaseLayout.astro (base de todas las páginas)
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Hero.astro
│   │   ├── BestProductSection.astro
│   │   ├── ProductCard.astro
│   │   ├── ComparisonTable.astro
│   │   ├── BuyingCriteria.astro
│   │   ├── FAQ.astro
│   │   ├── DisclaimerBanner.astro
│   │   └── Footer.astro
│   ├── pages/
│   │   ├── index.astro (home)
│   │   ├── [slug].astro (comparativas dinámicas)
│   │   ├── aviso-legal.astro
│   │   ├── politica-de-privacidad.astro
│   │   ├── politica-de-cookies.astro
│   │   └── disclaimer-afiliados.astro
│   └── content/
│       └── niches/
│           └── (tus JSON de productos aquí)
├── tailwind.config.mjs
├── astro.config.mjs
├── postcss.config.cjs
└── package.json
```

## 🔧 Comandos Útiles

```bash
# Desarrollo con hot-reload
npm run dev

# Build para producción
npm run build

# Ver build localmente
npm run preview

# Sincronizar tipos Astro
npm run sync

# Limpiar caché
npm run dev -- --force
```

## ✅ Checklist Final

- [ ] `npm install` ejecutado sin errores
- [ ] `npm run dev` está corriendo
- [ ] Abres http://localhost:3000 y ves estilos
- [ ] Hero tiene gradiente azul-púrpura
- [ ] Cards tienen sombra y hover
- [ ] Footer está presente
- [ ] Responsive funciona (abre DevTools mobile)
- [ ] No hay errores en consola

**Si todo funciona = ¡Listo para producción! 🚀**

---

## 📖 Documentación Completa

Ver: [IMPROVEMENTS.md](IMPROVEMENTS.md) para documentación técnica detallada.

---

**¡Disfruta tu web Web Maker profesional! 🎉**

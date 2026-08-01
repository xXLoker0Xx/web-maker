# 📋 Páginas Legales - Los Mejores 5

## Páginas Implementadas

Tu sitio ahora incluye **3 páginas legales críticas** requeridas por Amazon para pasar la revisión de afiliados:

### 1. `/politica-de-privacidad` 
Política que explica cómo se recopilan, usan y protegen los datos de los usuarios.

**Contenido:**
- Información recopilada (automática y voluntaria)
- Uso de datos
- Divulgación de información
- Seguridad
- Cookies
- Derechos del usuario

### 2. `/aviso-legal`
Términos y condiciones generales del sitio, incluyendo disclaimers importantes.

**Contenido:**
- Propósito del sitio
- Naturaleza del contenido
- Disclaimer de responsabilidad
- Información sobre enlaces de afiliados
- Independencia editorial
- Limitación de responsabilidad
- Uso aceptable

### 3. `/afiliados` ⭐ **CRÍTICA**
Página específica sobre el programa de afiliados de Amazon con el disclaimer obligatorio.

**Disclaimer Obligatorio de Amazon:**
```
"Como afiliado de Amazon, obtengo ingresos por las compras adscritas 
que cumplen los requisitos aplicables."
```

Este texto aparece en un cuadro destacado en la página y es **OBLIGATORIO** para pasar la revisión de Amazon.

---

## 📍 Rutas Disponibles

Vercel despliega automáticamente estas URLs:

```
https://tu-dominio.com/politica-de-privacidad/
https://tu-dominio.com/aviso-legal/
https://tu-dominio.com/afiliados/
```

---

## ✅ Cumplimiento con Amazon

Estas páginas cumplen con los requisitos de Amazon Associates:

✓ **Disclaimer claro y visible** - El texto obligatorio está en un cuadro destacado  
✓ **Información sobre afiliación** - Explica que ganamos comisiones  
✓ **Transparencia** - Aclara que el precio no cambia para el usuario  
✓ **Política de privacidad** - Cumple RGPD y CCPA  
✓ **Aviso legal** - Protege derechos de Amazon  

---

## 🔧 Personalización

### Cambiar el nombre del sitio

Busca "Los Mejores 5" en las 3 páginas y cámbialo por tu nombre:

**En `/politica-de-privacidad.astro`:**
```html
<p>En Los Mejores 5 ("nosotros"...
<!-- Cambia a tu nombre -->
<p>En Tu Sitio ("nosotros"...
```

**En `/aviso-legal.astro`:**
```html
<p>Los Mejores 5 (losmejores5.com) es un sitio web...
<!-- Cambia a tu nombre y dominio -->
<p>Tu Sitio (tu-dominio.com) es un sitio web...
```

**En `/afiliados.astro`:**
```html
<p>Los Mejores 5 (losmejores5.com) es un sitio independiente...
<!-- Cambia a tu nombre y dominio -->
```

### Cambiar email de contacto

Cada página dice "puedes contactarnos a través del formulario de contacto". Si tienes un email, reemplaza:

```html
<p>Para preguntas, puedes contactarnos a través del formulario de contacto en el sitio.</p>
```

Con:

```html
<p>Para preguntas, puedes contactarnos a través de:
<a href="mailto:tu-email@ejemplo.com">tu-email@ejemplo.com</a></p>
```

### Agregar más secciones

Todas las páginas usan HTML simple dentro de Astro. Puedes agregar más secciones `<h2>` y `<h3>` según necesites.

---

## 📝 Checklist antes de publicar

Antes de lanzar al público, verifica:

- [ ] Cambia "Los Mejores 5" por tu nombre en las 3 páginas
- [ ] Cambia "losmejores5.com" por tu dominio
- [ ] Agrega tu email de contacto
- [ ] Revisa que el disclaimer de Amazon esté visible en `/afiliados/`
- [ ] Prueba las rutas en local: `npm run dev`
- [ ] Verifica que los enlaces de navegación funcionan
- [ ] Hace un `git push` para actualizar Vercel

---

## 🔍 Estructura de Archivos

```
plantilla-astro/src/pages/
├── index.astro                      (Página principal)
├── [slug].astro                     (Rutas dinámicas de nichos)
├── politica-de-privacidad.astro     (Nueva)
├── aviso-legal.astro                (Nueva)
└── afiliados.astro                  (Nueva - CRÍTICA)
```

---

## 🎯 URLs en Footer

Cada página legal tiene links a las otras dos. Asegúrate de mantener estos links en el footer:

```html
<div class="nav-footer">
  <a href="/">← Volver al inicio</a>
  <a href="/politica-de-privacidad">Política de Privacidad</a>
  <a href="/aviso-legal">Aviso Legal</a>
  <a href="/afiliados">Política de Afiliados</a>
</div>
```

---

## ⚠️ Importante: Descargo de Responsabilidad

Estas páginas fueron creadas como referencia general. Dependiendo de tu:
- País de operación
- Tipo de productos
- Audiencia objetivo
- Leyes locales (RGPD, CCPA, LSSI-CE, etc.)

Puedes necesitar:
- Consultar con un abogado
- Agregar cláusulas adicionales
- Ajustar el contenido a tu jurisdicción
- Cumplir leyes específicas de tu país

**Este es contenido de referencia, no asesoramiento legal.**

---

## 📚 Recursos Útiles

- **Amazon Associates:** https://associates.amazon.com/legal
- **RGPD (Europa):** https://www.gdpr.eu/
- **CCPA (California):** https://www.ccpa.org/
- **Ley LSSI-CE (España):** https://www.boe.es/

---

## 🚀 Próximos Pasos

1. ✅ Páginas legales creadas
2. ⬜ Personalizar con tu nombre/dominio
3. ⬜ Hacer push a GitHub
4. ⬜ Vercel redeploya automáticamente
5. ⬜ Verificar en producción

**¡Tu sitio ahora está listo para solicitar a Amazon!**

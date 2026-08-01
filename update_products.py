#!/usr/bin/env python3
"""Agrega pros/contras de prueba a los niches para demostrar la comparativa."""

import json
from pathlib import Path

niches_dir = Path("plantilla-astro/src/content/niches")
json_file = niches_dir / "freidoras-de-aire.json"

with open(json_file, 'r', encoding='utf-8') as f:
    content = json.load(f)

# Pros/cons data for air fryers
pros_cons_data = [
    {
        'badge': 'Mejor Calidad',
        'pros': [
            'Capacidad de 6,5L ideal para familias',
            'Doble resistencia para dorado perfecto',
            'Potencia de 2200W muy eficiente',
            'Versátil: aire y grill integrado',
            'Tecnología de calentamiento rápido'
        ],
        'cons': [
            'Precio medio-alto',
            'Requiere espacio considerable en la cocina',
            'Tiempos de calentamiento: 3-5 minutos'
        ]
    },
    {
        'badge': 'Mejor Precio',
        'pros': [
            'Precio muy competitivo del mercado',
            'Panel táctil digital intuitivo',
            'Acabados en acero inoxidable premium',
            'Tecnología PerfectCook patentada',
            '8 modos de cocción diferentes'
        ],
        'cons': [
            'Capacidad algo reducida (5,5L)',
            'Menos potencia que modelos premium',
            'Mantenimiento regular de accesorios'
        ]
    },
    {
        'badge': 'Mejor Rendimiento',
        'pros': [
            'Capacidad generosa de 8L',
            'Grill doble integrado profesional',
            'Control fino de temperatura (80-200°C)',
            'Perfecto para cocina completa',
            '8 menús pre-programados automáticos'
        ],
        'cons': [
            'Precio elevado en comparación',
            'Consumo eléctrico más alto',
            'Requiere muy buen ventilado'
        ]
    },
    {
        'badge': 'Mejor Versátil',
        'pros': [
            'Excelente relación precio-capacidad',
            'Rápido tiempo de cocción',
            'Acabado moderno y compacto',
            'Bajo consumo de energía',
            'Garantía extendida de 3 años'
        ],
        'cons': [
            'Capacidad más pequeña (4,5L)',
            'Una sola resistencia térmica',
            'Menor número de funciones'
        ]
    },
    {
        'badge': 'Alternativa Recomendada',
        'pros': [
            'Precio muy accesible',
            'Fácil de limpiar y mantener',
            'Tamaño portable y versátil',
            'Buena opinión de usuarios verificados',
            'Entrega rápida disponible'
        ],
        'cons': [
            'Menos características premium',
            'Capacidad limitada para familias',
            'Mantenimiento más frecuente requerido'
        ]
    }
]

# Update products
for i, product in enumerate(content['products'][:5]):
    # Extract title from summary if not present
    if 'title' not in product:
        summary = product.get('summary', '')
        # Extract title from first part of summary
        title = summary.split(' - ')[0] if ' - ' in summary else summary[:60]
        product['title'] = title
    
    if i < len(pros_cons_data):
        data = pros_cons_data[i]
        product['badge'] = data['badge']
        product['pros'] = data['pros']
        product['cons'] = data['cons']
    
    # Improve summary
    title = product.get('title', 'Producto')
    price_str = product.get('price', 'N/A')
    reviews = product.get('reviews_count', 0)
    rating = product.get('rating', 0)
    review_text = f"Con {reviews} reseñas" if reviews > 0 else "Sin reseñas aún"
    rating_text = f"valoración de {rating}/5 estrellas" if rating > 0 else "sin valoración aún"
    
    product['summary'] = f"{title} - Precio: {price_str}€. {review_text} y {rating_text}."

# Save updated JSON
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(content, f, ensure_ascii=False, indent=2)

print(f'✓ Actualizado: {json_file}')
print(f'✓ Productos con pros/contras: {sum(1 for p in content["products"][:5] if p.get("pros"))}')

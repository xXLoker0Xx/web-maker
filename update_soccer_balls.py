#!/usr/bin/env python3
"""Agrega pros/contras a balones de fútbol."""

import json
from pathlib import Path

niches_dir = Path("plantilla-astro/src/content/niches")
json_file = niches_dir / "balon-de-futbol.json"

with open(json_file, 'r', encoding='utf-8') as f:
    content = json.load(f)

# Pros/cons data for soccer balls
pros_cons_data = [
    {
        'badge': 'Mejor Profesional',
        'pros': [
            'Balón oficial de competiciones',
            'Construcción de paneles térmicos',
            'Excelente control y trayectoria',
            'Cámara de butilo de calidad',
            'Certificación FIFA aprobado'
        ],
        'cons': [
            'Precio premium',
            'Requiere mantenimiento específico',
            'Menos duradero en pistas de asfalto'
        ]
    },
    {
        'badge': 'Mejor Precio',
        'pros': [
            'Precio muy accesible',
            'Buena calidad por el valor',
            'Resistente y duradero',
            'Apto para entrenamientos',
            'Disponible en varios colores'
        ],
        'cons': [
            'No certificado para competición oficial',
            'Control inferior a modelos premium',
            'Inflado menos consistente'
        ]
    },
    {
        'badge': 'Mejor Durabilidad',
        'pros': [
            'Construcción reforzada extrema',
            'Costura de triple hilo',
            'Resiste superficies abrasivas',
            'Larga vida útil garantizada',
            'Ideal para uso intenso'
        ],
        'cons': [
            'Peso ligeramente superior',
            'Control de balón más difícil',
            'Precio medio-alto'
        ]
    },
    {
        'badge': 'Mejor Control',
        'pros': [
            'Superficie optimizada para toque',
            'Panel de goma espuma especial',
            'Excelente ajuste de vuelo',
            'Ideal para técnica perfecta',
            'Usado en ligas profesionales'
        ],
        'cons': [
            'Desgaste más rápido en competición',
            'Precio elevado',
            'Requiere cancha de calidad'
        ]
    },
    {
        'badge': 'Alternativa Recomendada',
        'pros': [
            'Buena relación calidad-precio',
            'Versátil para todo tipo de uso',
            'Fácil de mantener',
            'Aceptable en semiprofesional',
            'Entrega inmediata disponible'
        ],
        'cons': [
            'Rendimiento medio',
            'Durabilidad moderada',
            'Sin certificación oficial'
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

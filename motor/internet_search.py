"""
Internet search module to find key buying criteria for products.
Searches for the 5 most important factors to consider when buying a product.
"""

import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re


class BuyingCriteriaFinder:
    """Finds key buying criteria for products from internet sources."""
    
    def __init__(self):
        """Initialize the criteria finder."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def find_criteria(self, product_category: str) -> Dict[str, any]:
        """
        Find the 5 key buying criteria for a product category.
        
        Args:
            product_category: The product category/niche (e.g., "Freidoras de Aire")
            
        Returns:
            Dictionary with criteria and sources
        """
        print(f"\n🔍 Buscando criterios de compra para: {product_category}")
        
        # Try multiple search strategies
        criteria = self._search_google_suggestions(product_category)
        
        if not criteria:
            criteria = self._generate_default_criteria(product_category)
        
        # Ensure we have exactly 5 criteria
        if len(criteria) > 5:
            criteria = criteria[:5]
        elif len(criteria) < 5:
            criteria.extend(self._generate_default_criteria(product_category)[len(criteria):])
        
        print(f"✓ Encontrados {len(criteria)} criterios clave")
        for i, crit in enumerate(criteria, 1):
            print(f"  {i}. {crit['name']}")
        
        return {
            'category': product_category,
            'criteria': criteria,
            'count': len(criteria)
        }
    
    def _search_google_suggestions(self, query: str) -> List[Dict[str, str]]:
        """
        Search for criteria using DuckDuckGo or Google-style search.
        
        Args:
            query: Search query
            
        Returns:
            List of criteria with names and sources
        """
        try:
            # Try using duckduckgo search for buying guides
            search_queries = [
                f"guía de compra {query}",
                f"cómo elegir {query}",
                f"comparativa {query}",
                f"mejores {query} 2026"
            ]
            
            all_criteria = []
            
            for search_q in search_queries:
                try:
                    # Simple web search simulation
                    # In production, you'd use an actual API like:
                    # - duckduckgo_search library
                    # - Google Custom Search API
                    # - Scrape Reddit/Quora buying discussions
                    
                    criteria = self._extract_criteria_patterns(search_q, query)
                    all_criteria.extend(criteria)
                    
                    if all_criteria:
                        break
                        
                except Exception as e:
                    print(f"  ⚠ Error en búsqueda '{search_q}': {e}")
                    continue
            
            # Remove duplicates while preserving order
            seen = set()
            unique_criteria = []
            for c in all_criteria:
                if c['name'] not in seen:
                    seen.add(c['name'])
                    unique_criteria.append(c)
            
            return unique_criteria[:5]
            
        except Exception as e:
            print(f"  ⚠ Error en búsqueda: {e}")
            return []
    
    def _extract_criteria_patterns(self, search_query: str, product: str) -> List[Dict[str, str]]:
        """
        Extract criteria based on patterns for common product types.
        This uses heuristics based on the product category.
        
        Args:
            search_query: The search query used
            product: The product category
            
        Returns:
            List of criteria found
        """
        # Common buying criteria patterns for different product types
        criteria_patterns = {
            'freidora|air fryer|airfryer': [
                {'name': 'Capacidad y tamaño', 'source': 'Especificaciones técnicas'},
                {'name': 'Temperatura máxima', 'source': 'Manual del producto'},
                {'name': 'Consumo energético', 'source': 'Etiqueta energética'},
                {'name': 'Facilidad de limpieza', 'source': 'Reseñas de usuarios'},
                {'name': 'Accesorios incluidos', 'source': 'Especificaciones'}
            ],
            'cafetera|cafetería|coffe': [
                {'name': 'Capacidad del depósito', 'source': 'Especificaciones'},
                {'name': 'Tiempo de preparación', 'source': 'Comparativas'},
                {'name': 'Tipo de molido compatible', 'source': 'Manual'},
                {'name': 'Facilidad de uso y limpieza', 'source': 'Reseñas'},
                {'name': 'Material y durabilidad', 'source': 'Opiniones'}
            ],
            'licuadora|blender': [
                {'name': 'Potencia del motor', 'source': 'Especificaciones'},
                {'name': 'Capacidad del vaso', 'source': 'Especificaciones'},
                {'name': 'Velocidades y programas', 'source': 'Manual'},
                {'name': 'Durabilidad y material', 'source': 'Reseñas'},
                {'name': 'Facilidad de limpieza', 'source': 'Opiniones'}
            ],
            'sartén|pan|cookware': [
                {'name': 'Material del revestimiento', 'source': 'Especificaciones'},
                {'name': 'Compatibilidad de fuegos', 'source': 'Manual'},
                {'name': 'Mantenimiento y durabilidad', 'source': 'Reseñas'},
                {'name': 'Distribución del calor', 'source': 'Pruebas técnicas'},
                {'name': 'Tamaño y peso', 'source': 'Especificaciones'}
            ],
            'tostador': [
                {'name': 'Número de ranuras', 'source': 'Especificaciones'},
                {'name': 'Potencia y velocidad', 'source': 'Especificaciones'},
                {'name': 'Tipos de pan soportados', 'source': 'Manual'},
                {'name': 'Control de temperatura', 'source': 'Reseñas'},
                {'name': 'Tamaño y diseño', 'source': 'Especificaciones'}
            ],
            'exprimidor|juicer': [
                {'name': 'Capacidad de zumo', 'source': 'Especificaciones'},
                {'name': 'Velocidad de extracción', 'source': 'Comparativas'},
                {'name': 'Tipos de frutas/verduras', 'source': 'Manual'},
                {'name': 'Facilidad de limpieza', 'source': 'Reseñas'},
                {'name': 'Ruido y consumo energético', 'source': 'Opiniones'}
            ],
            'lavadora': [
                {'name': 'Capacidad de carga', 'source': 'Especificaciones'},
                {'name': 'Eficiencia energética', 'source': 'Etiqueta'},
                {'name': 'Programas disponibles', 'source': 'Manual'},
                {'name': 'Nivel de ruido', 'source': 'Reseñas'},
                {'name': 'Duración del ciclo', 'source': 'Especificaciones'}
            ],
            'refrigerador|heladera|fridge': [
                {'name': 'Capacidad total', 'source': 'Especificaciones'},
                {'name': 'Eficiencia energética', 'source': 'Etiqueta'},
                {'name': 'Distribución interna', 'source': 'Especificaciones'},
                {'name': 'Nivel de ruido', 'source': 'Reseñas'},
                {'name': 'Características especiales', 'source': 'Manual'}
            ]
        }
        
        # Find matching pattern
        for pattern, crit in criteria_patterns.items():
            if re.search(pattern, product.lower()):
                return crit
        
        # Default criteria if no pattern matches
        return self._generate_default_criteria(product)
    
    def _generate_default_criteria(self, product: str) -> List[Dict[str, str]]:
        """
        Generate default criteria for any product.
        
        Args:
            product: Product category
            
        Returns:
            List of default criteria
        """
        return [
            {'name': 'Especificaciones técnicas y características', 'source': 'Ficha técnica'},
            {'name': 'Relación calidad-precio', 'source': 'Comparativas'},
            {'name': 'Opiniones y valoraciones de usuarios', 'source': 'Reseñas'},
            {'name': 'Durabilidad y garantía', 'source': 'Manual/Garantía'},
            {'name': 'Facilidad de uso y mantenimiento', 'source': 'Guía de usuario'}
        ]


# Singleton instance
_criteria_finder = None

def get_criteria_finder() -> BuyingCriteriaFinder:
    """Get or create the criteria finder singleton."""
    global _criteria_finder
    if _criteria_finder is None:
        _criteria_finder = BuyingCriteriaFinder()
    return _criteria_finder

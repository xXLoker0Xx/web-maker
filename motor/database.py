"""
Database module for managing SQLite local cache of Amazon products.
Handles creation and management of the products table with CRUD operations.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class ProductDatabase:
    """Manages SQLite database for caching Amazon products data."""

    def __init__(self, db_path: str = "local_cache.db"):
        """
        Initialize database connection and create tables if they don't exist.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self.connection = None
        self._connect()
        self._create_tables()

    def _connect(self) -> None:
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            print(f"✓ Conexión a base de datos: {self.db_path}")
        except sqlite3.Error as e:
            print(f"✗ Error al conectar a la base de datos: {e}")
            raise

    def _create_tables(self) -> None:
        """Create products table with required schema."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    asin TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    price TEXT,
                    rating REAL,
                    reviews_count INTEGER,
                    features TEXT,
                    image_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.connection.commit()
            print("✓ Tablas de base de datos inicializadas")
        except sqlite3.Error as e:
            print(f"✗ Error al crear tablas: {e}")
            raise

    def product_exists(self, asin: str) -> bool:
        """
        Check if a product with given ASIN already exists in the database.
        
        Args:
            asin: Amazon Standard Identification Number
            
        Returns:
            True if product exists, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1 FROM products WHERE asin = ?", (asin,))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"✗ Error al verificar producto: {e}")
            return False

    def insert_product(self, product_data: Dict[str, Any]) -> bool:
        """
        Insert or update a product in the database.
        
        Args:
            product_data: Dictionary with product information
                {
                    'asin': str,
                    'title': str,
                    'price': str,
                    'rating': float,
                    'reviews_count': int,
                    'features': list,
                    'image_url': str
                }
                
        Returns:
            True if insertion successful, False otherwise
        """
        try:
            # Convert features list to JSON string
            features_json = json.dumps(product_data.get('features', []))
            
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO products 
                (asin, title, price, rating, reviews_count, features, image_url, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product_data.get('asin'),
                product_data.get('title'),
                product_data.get('price'),
                product_data.get('rating'),
                product_data.get('reviews_count'),
                features_json,
                product_data.get('image_url'),
                datetime.now().isoformat()
            ))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ Error al insertar producto {product_data.get('asin')}: {e}")
            return False

    def insert_products_batch(self, products: List[Dict[str, Any]]) -> int:
        """
        Insert multiple products in batch mode.
        
        Args:
            products: List of product dictionaries
            
        Returns:
            Number of products successfully inserted
        """
        inserted_count = 0
        for product in products:
            if self.insert_product(product):
                inserted_count += 1
        return inserted_count

    def get_product(self, asin: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a product by ASIN.
        
        Args:
            asin: Amazon Standard Identification Number
            
        Returns:
            Product dictionary or None if not found
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products WHERE asin = ?", (asin,))
            row = cursor.fetchone()
            if row:
                product = dict(row)
                # Parse features JSON back to list
                product['features'] = json.loads(product.get('features', '[]'))
                return product
            return None
        except sqlite3.Error as e:
            print(f"✗ Error al obtener producto: {e}")
            return None

    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Retrieve all products from database.
        
        Returns:
            List of product dictionaries
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
            rows = cursor.fetchall()
            products = []
            for row in rows:
                product = dict(row)
                product['features'] = json.loads(product.get('features', '[]'))
                products.append(product)
            return products
        except sqlite3.Error as e:
            print(f"✗ Error al obtener productos: {e}")
            return []

    def get_products_by_asins(self, asins: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieve products by list of ASINs.
        
        Args:
            asins: List of Amazon Standard Identification Numbers
            
        Returns:
            List of product dictionaries
        """
        try:
            placeholders = ','.join('?' * len(asins))
            cursor = self.connection.cursor()
            cursor.execute(
                f"SELECT * FROM products WHERE asin IN ({placeholders}) ORDER BY created_at DESC",
                asins
            )
            rows = cursor.fetchall()
            products = []
            for row in rows:
                product = dict(row)
                product['features'] = json.loads(product.get('features', '[]'))
                products.append(product)
            return products
        except sqlite3.Error as e:
            print(f"✗ Error al obtener productos por ASINs: {e}")
            return []

    def delete_product(self, asin: str) -> bool:
        """
        Delete a product from the database.
        
        Args:
            asin: Amazon Standard Identification Number
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM products WHERE asin = ?", (asin,))
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"✗ Error al eliminar producto: {e}")
            return False

    def clear_all(self) -> bool:
        """
        Clear all products from database.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM products")
            self.connection.commit()
            print("✓ Base de datos limpiada")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error al limpiar base de datos: {e}")
            return False

    def get_stats(self) -> Dict[str, int]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with database statistics
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM products")
            total = cursor.fetchone()['total']
            return {'total_products': total}
        except sqlite3.Error as e:
            print(f"✗ Error al obtener estadísticas: {e}")
            return {'total_products': 0}

    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            print("✓ Conexión a base de datos cerrada")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

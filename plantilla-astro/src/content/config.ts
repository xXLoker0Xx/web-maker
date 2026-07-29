// Archivo de configuración para el contenido dinámico de nicho
// Este archivo es opcional, principalmente para validación de tipos en TypeScript

export interface NicheContent {
  title: string;
  description: string;
  intro: string;
  verdict: string;
  products: Product[];
}

export interface Product {
  asin: string;
  badge: string;
  pros: string[];
  cons: string[];
  summary: string;
  image_url?: string;
  price?: string;
  rating?: number;
  reviews_count?: number;
  affiliate_url?: string;
}

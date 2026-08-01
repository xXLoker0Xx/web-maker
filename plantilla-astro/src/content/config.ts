import { defineCollection, z } from 'astro:content';

// Definir la colección 'niches'
const nichesCollection = defineCollection({
  type: 'data',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    intro: z.string(),
    verdict: z.string(),
    products: z.array(z.object({
      asin: z.string(),
      badge: z.string(),
      pros: z.array(z.string()).optional(),
      cons: z.array(z.string()).optional(),
      summary: z.string(),
      image_url: z.string().optional(),
      price: z.string().optional(),
      rating: z.number().optional(),
      reviews_count: z.number().optional(),
      affiliate_url: z.string().optional(),
    })),
  }),
});

// Exportar colecciones
export const collections = {
  niches: nichesCollection,
};

// Tipos TypeScript para referencia
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

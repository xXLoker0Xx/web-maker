import { defineCollection, z } from 'astro:content';

// Definir la colección 'niches'
const nichesCollection = defineCollection({
  type: 'data',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    intro: z.string().optional(),
    verdict: z.string().optional(),
    executive_summary: z.string().optional(),
    key_takeaways: z.array(z.string()).optional(),
    buying_guide: z.string().optional(),
    buying_criteria: z.array(z.string()).optional(),
    faq: z.array(z.object({
      question: z.string(),
      answer: z.string(),
    })).optional(),
    products: z.array(z.object({
      asin: z.string(),
      title: z.string(),
      short_title: z.string().optional(),
      badge: z.string().optional(),
      pros: z.array(z.string()).optional(),
      cons: z.array(z.string()).optional(),
      summary: z.string().optional(),
      highlights: z.array(z.string()).optional(),
      image_url: z.string().optional(),
      price: z.string().optional(),
      rating: z.number().optional(),
      reviews_count: z.number().optional(),
      affiliate_url: z.string().optional(),
      ideal_for: z.string().optional(),
      avoid_if: z.string().optional(),
      best_use_case: z.string().optional(),
      key_features: z.array(z.string()).optional(),
      score: z.number().optional(),
      value_score: z.number().optional(),
      performance_score: z.number().optional(),
      expert_tip: z.string().optional(),
    })).optional(),
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
  intro?: string;
  verdict?: string;
  executive_summary?: string;
  key_takeaways?: string[];
  buying_guide?: string;
  buying_criteria?: string[];
  faq?: Array<{ question: string; answer: string }>;
  products?: Product[];
}

export interface Product {
  asin: string;
  title: string;
  short_title?: string;
  badge?: string;
  pros?: string[];
  cons?: string[];
  summary?: string;
  highlights?: string[];
  image_url?: string;
  price?: string;
  rating?: number;
  reviews_count?: number;
  affiliate_url?: string;
  ideal_for?: string;
  avoid_if?: string;
  best_use_case?: string;
  key_features?: string[];
  score?: number;
  value_score?: number;
  performance_score?: number;
  expert_tip?: string;
}

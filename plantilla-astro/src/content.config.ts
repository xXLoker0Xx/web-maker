import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Definir la colección 'niches'
const nichesCollection = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/niches' }),
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

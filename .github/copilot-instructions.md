# PROJECT CONTEXT — AI Affiliate Website (Amazon Associates)

## Project Overview

I am building a modern affiliate website focused on **product comparisons and recommendations** to monetize through the **Amazon Associates Program**.

The ecosystem of search has shifted from traditional keyword retrieval to **Generative Engine Optimization (GEO)**. Therefore, this platform must not only rank in traditional Google Search (SEO) but also serve as a highly structured, trustworthy data source that Large Language Models (LLMs like ChatGPT, Claude, Perplexity, and Google AI Overviews) actively cite and recommend.

The objective is to build a **high-quality editorial website** that looks handcrafted, trustworthy, and professional (similar to Wirecutter or RTINGS), while being built on a scalable, programmatic SEO (pSEO) foundation.

---

# Current Goal (MVP)

The current objective is to build a **Minimum Viable Product (MVP)** that fully complies with Amazon Associates' strict manual review requirements. 

**Crucial API Status:** Amazon has deprecated PA-API 5.0. All programmatic architecture must be designed to eventually integrate with the **Amazon Creators API** (REST architecture). 

Current MVP status:
* Product scraping and automated data structuring are advanced.
* The public frontend needs to be built.
* Temporary affiliate links will be used initially.
* The first milestone is generating the 3 qualified sales required to unlock permanent Creators API access.

This MVP prioritizes:
* **E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)** above all.
* Flawless GEO (structured data for AI extraction).
* Excellent UX/UI and Core Web Vitals.
* Clean, scalable, component-based architecture.

---

# Technology Stack

Unless explicitly instructed otherwise, prioritize:
* **Astro** (for unparalleled SSG performance and zero JS by default)
* **Tailwind CSS** (for styling and design tokens)
* **TypeScript** (for strict type safety and data structuring)
* **Static Site Generation (SSG)** (SSR only when strictly justified)

Avoid unnecessary JavaScript. Prefer CSS-only solutions for interactivity (hover states, simple toggles) whenever possible.

---

# GEO & Content Strategy (Anti-SpamBrain)

AI-generated content risks being penalized by Google's SpamBrain if it merely rewrites manufacturer descriptions. Every component and page must be structured to avoid "thin affiliate" classification.

When generating layouts or content structures, enforce:
* **Empirical Signals:** Include sections for quantitative data, long-term testing results, and aggregated user sentiment.
* **Extraction-Friendly Formatting:** Use pure HTML tables for comparisons, definition lists for specs, and concise, one-fact-per-paragraph structures.
* **Entity Clarity:** Use exact brand names, model numbers, and technical terminology. 
* **Data Density:** UI components must support rich data (minimum 15-20 data points per product).
* **Above-the-Fold Delivery:** The top 200 words/pixels must answer the core user intent directly.

---

# Website Structure

The website represents a professional editorial publication. 

## Main Sections

### Home
Purpose: Establish immediate E-E-A-T and guide users to topic clusters (Silos).
* Hero (Value proposition)
* Topic Clusters / Categories (Hubs)
* Featured & Latest Comparisons (Spokes)
* Trust Signals (Methodology, Why trust us, Editorial guidelines)
* FAQ

### Comparison Articles (Hub-and-Spoke Model)
Route: `/comparativas/[slug]`
Example: `los-5-mejores-aspiradores-sin-cable-de-2026`

Each article must contain:
1. Hero
2. Top Pick (Best Overall Product)
3. Executive Summary (GEO-optimized for AI summaries)
4. Quick Comparison Table (HTML/Semantic)
5. Individual Product Reviews (Pros, Cons, Data points, Historical context)
6. Buying Guide
7. Buying Criteria (Iconography over numbers)
8. FAQ (Semantic structures)
9. Final Verdict

### Legal & Trust Pages
Mandatory for manual review and E-E-A-T:
* `/aviso-legal`
* `/politica-de-privacidad`
* `/politica-de-cookies`
* `/terminos-y-condiciones`
* `/disclaimer-afiliados`

The affiliate disclaimer must include the required Amazon statement:
> "Como afiliado de Amazon, obtengo ingresos por las compras adscritas que cumplen los requisitos aplicables."

---

# UI / UX DESIGN SYSTEM

Build a premium experience similar to Wirecutter, TechRadar, or The Verge. Optimize for readability, visual hierarchy, and zero-click extraction.

## General Philosophy
* The user (and AI bot) must instantly know: What is the best? Why? How do they compare?
* Never look like an automated thin-affiliate site.

## Visual Hierarchy
1. Hero (Gradient background)
2. Top Pick (Immediate conversion point)
3. Comparison Table
4. Product Cards
5. Editorial content (Guide/FAQ)

## Typography & Spacing
Recommended scale:
* H1: 56px
* H2: 34px
* H3: 24px
* Paragraph: 18px (Line-height: 1.7–1.9)

Use a strict spacing system (CSS Variables):
* `--space-xs`: 8px
* `--space-sm`: 16px
* `--space-md`: 24px
* `--space-lg`: 40px
* `--space-xl`: 64px
* `--space-2xl`: 96px

## Design Tokens (CSS Variables)
Always use CSS variables for theming:
```css
:root {
  --primary: #6366F1;
  --primary-dark: #4F46E5;
  --accent: #F59E0B;
  --background: #F8FAFC;
  --surface: #FFFFFF;
  --text: #111827;
  --text-muted: #6B7280;
  --border: #E5E7EB;
  --success: #10B981;
  --shadow: 0 12px 40px rgba(15,23,42,.08);
  --radius: 20px;
}
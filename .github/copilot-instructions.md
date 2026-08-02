# PROJECT CONTEXT — AI Affiliate Website (Amazon Associates)

## Project Overview

I am building a modern affiliate website focused on **product comparisons and recommendations** to monetize through the **Amazon Associates Program**.

The objective is not simply to generate pages, but to build a **high-quality editorial website** that looks handcrafted, trustworthy and professional, similar to leading review websites.

The project must be scalable, maintainable and production-ready.

---

# Current Goal (MVP)

The current objective is to build a **Minimum Viable Product (MVP)** that fully complies with Amazon Associates' manual review requirements in order to obtain access to the official **Amazon Product Advertising API (PA-API)**.

Current status:

* Product scraping and automation are already well advanced.
* The missing part is the public website.
* The site must be indexable by search engines.
* Temporary affiliate links will be used initially.
* The first objective is to obtain the first three qualified Amazon sales and unlock permanent PA-API access.

This MVP should prioritize:

* Quality over quantity
* Excellent UX/UI
* SEO
* Performance
* Clean architecture
* Fast implementation

---

# Technology Stack

Unless explicitly instructed otherwise, always prioritize:

* Astro
* Tailwind CSS
* TypeScript
* Static Site Generation (SSG)
* Server Side Rendering (SSR) only when justified

The website should achieve excellent Core Web Vitals.

Avoid unnecessary JavaScript.

Prefer CSS whenever possible.

---

# Website Structure

The website represents a professional editorial publication specialized in product recommendations.

Main sections:

## Home

Purpose:

Present the website as a premium destination to discover the best products in every category.

Should include:

* Hero
* Featured comparisons
* Latest comparisons
* Popular categories
* Why trust us
* FAQ
* CTA sections

---

## Comparison Articles

Route:

/comparativas/[slug]

Example:

Los 5 Mejores Aspiradores Sin Cable de 2026

Each article must contain:

1. Hero
2. Top Pick (Best Product)
3. Executive Summary
4. Quick Comparison Table
5. Individual Product Reviews
6. Buying Guide
7. Buying Criteria
8. FAQ
9. Final Verdict

Every article should read like an expert editorial review.

---

## Product Reviews

Each product must include:

* Image
* Product Name
* Rating
* Main Features
* Pros
* Cons
* Key Specifications
* Price (if available)
* CTA
* Amazon Affiliate Link

The recommended product should be visually highlighted.

---

## Legal Pages

Generate all mandatory legal pages:

* /aviso-legal
* /politica-de-privacidad
* /politica-de-cookies
* /terminos-y-condiciones
* /disclaimer-afiliados

The affiliate disclaimer must include the required Amazon Associates statement:

> "Como afiliado de Amazon, obtengo ingresos por las compras adscritas que cumplen los requisitos aplicables."

---

# SEO Requirements

Every page must include:

* Dynamic Title
* Dynamic Description
* Canonical URL
* Open Graph
* Twitter Cards
* Sitemap
* robots.txt

Structured Data:

* Article Schema
* Product Schema
* FAQ Schema
* Breadcrumb Schema
* Organization Schema where appropriate

Semantic HTML is mandatory.

---

# Performance Requirements

Always optimize for:

* Lighthouse
* Core Web Vitals
* Accessibility
* SEO

Requirements:

* Lazy images
* Responsive images
* WebP / AVIF
* No layout shifts
* Minimal JavaScript
* Optimized CSS
* Fast rendering

---

# Accessibility

Always follow accessibility best practices.

Requirements:

* Semantic HTML
* Proper heading hierarchy
* Keyboard navigation
* Focus states
* ARIA labels where needed
* High color contrast
* Alt text
* Respect prefers-reduced-motion

---

# UI / UX DESIGN SYSTEM

Every page, component and layout must follow these principles.

These rules have priority over any default implementation.

---

## General Philosophy

The objective is to build a premium experience similar to:

* Wirecutter
* TechRadar
* Tom's Guide
* The Verge Reviews
* Apple Product Pages

The user should immediately understand:

* Which product is the best.
* Why it is recommended.
* How products compare.
* Where to buy them.

Optimize every interface for:

* Readability
* Trust
* Visual hierarchy
* Conversion
* SEO
* Accessibility
* Mobile usability

The website must never look like an automatically generated affiliate site.

---

# Visual Hierarchy

Every comparison page should follow this order:

1. Hero
2. Top Pick
3. Quick Comparison Table
4. Product Cards
5. Buying Guide
6. Buying Criteria
7. FAQ
8. Final Verdict
9. Footer

Avoid long introductions before useful information.

---

# Hero

Only the Hero section should use a colorful gradient.

Characteristics:

* Rounded corners
* Large spacing
* Strong headline
* Short subtitle
* CTA
* Optional product image

Body background:

#F8FAFC

Hero gradient:

linear-gradient(135deg,#5B7CFF,#7F5AF0)

---

# Layout

Maximum widths:

Reading content:

780–850px

Comparison tables:

1100–1200px

Always center the content.

---

# Typography

Recommended scale:

H1

56px

H2

34px

H3

24px

Paragraph

18px

Line-height

1.7–1.9

Avoid small fonts.

---

# Spacing System

Use a consistent spacing scale.

Example:

--space-xs:8px

--space-sm:16px

--space-md:24px

--space-lg:40px

--space-xl:64px

--space-2xl:96px

Never use arbitrary spacing values.

---

# Design Tokens

Always use CSS variables.

Example:

:root{

--primary:#6366F1;

--primary-dark:#4F46E5;

--accent:#F59E0B;

--background:#F8FAFC;

--surface:#FFFFFF;

--text:#111827;

--text-muted:#6B7280;

--border:#E5E7EB;

--success:#10B981;

--shadow:0 12px 40px rgba(15,23,42,.08);

--radius:20px;

}

---

# Cards

All cards should look premium.

Requirements:

* White background
* Large border radius
* Soft shadow
* Hover animation
* Smooth transitions
* Spacious padding

---

# Best Product Section

Immediately after the Hero.

Include:

🏆 Badge

Large image

Product name

Rating

Main advantages

CTA

Price

Why it is our recommendation

This is the primary conversion section.

---

# Product Cards

Every card should include:

* Image
* Ranking Badge
* Rating
* Pros
* Cons
* Specifications
* CTA
* Price
* Hover effects

Highlight the recommended product.

---

# Comparison Table

Columns:

Image

Product

Rating

Price

Main Feature

CTA

Requirements:

* Sticky header
* Highlight first row
* Responsive
* Easy to scan

---

# Buying Guide

Always include:

* How to choose
* Common mistakes
* Important features
* Who should buy
* Who should avoid

This section improves trust and SEO.

---

# Buying Criteria

Use icons instead of numbers.

Examples:

⚡ Performance

🔋 Battery

💰 Price

🛡 Warranty

⭐ Reviews

Each criterion should include:

* Icon
* Title
* Short explanation

---

# FAQ

Every article must include FAQs.

Prefer semantic HTML:

<details>

<summary>

Examples:

* Which is the best product?
* Which is the cheapest?
* Which offers the best value?
* Is it worth buying?

---

# CTA Strategy

Each major section should contain a CTA.

Examples:

View on Amazon

Check Price

See Best Deal

Never rely on a single CTA.

---

# Sticky CTA

Desktop:

Floating recommendation card.

Mobile:

Sticky bottom CTA.

---

# Scroll Progress

Include a thin reading progress bar fixed at the top.

---

# Navigation

Desktop:

Sticky table of contents.

Example:

* Introduction
* Comparison
* Products
* Buying Guide
* FAQ
* Verdict

---

# Affiliate Disclaimer

Do not place a huge disclaimer at the top.

Instead use a compact information banner.

Example:

ⓘ Transparency

We may earn a commission from qualifying purchases at no additional cost to you.

---

# Footer

Professional footer including:

* About
* Contact
* Privacy Policy
* Affiliate Disclosure
* Copyright

Avoid placeholder text.

---

# Animations

Only subtle animations.

Examples:

* Fade-in
* TranslateY
* Hover elevation

Avoid excessive motion.

---

# Code Quality

Generate production-ready code.

Requirements:

* TypeScript
* Reusable components
* No duplicated CSS
* Clean architecture
* Semantic HTML
* Maintainable code
* Consistent naming
* CSS variables
* No magic numbers
* No unnecessary wrappers
* Avoid inline styles unless absolutely necessary

---

# General Rules for Code Generation

Whenever generating new pages or components:

* Think as a senior frontend engineer.
* Think as a UX designer.
* Think as an SEO specialist.
* Think as an accessibility expert.
* Think as a conversion rate optimization (CRO) specialist.

Do not generate the simplest solution.

Generate the solution that best balances:

* Performance
* Maintainability
* User Experience
* Conversion
* SEO
* Accessibility
* Scalability

Every page should feel like it belongs to a premium editorial publication rather than an automatically generated affiliate website.

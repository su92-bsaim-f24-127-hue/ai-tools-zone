# Phase 3.1.3 — Group B Noindex & Informational Governance Report

**Project:** AI Tools Zone  
**Website:** https://aitoolszone.tech/  
**Audit Date:** 12 November 2026  
**Target Staging Directory:** `staging/catalog-expansion/products/`  

---

## 1. Executive Summary

This report documents the implementation of the `noindex, follow` search engine directive across all 37 Group B informational software pages.
The objective is to allow AI Tools Zone to publish useful software reviews, model comparisons, and technical feature breakdowns without saturating search engine crawl budgets or creating thin index bloat before wholesale suppliers are verified.

### Key Audit Verifications:
- **Total Group B Pages:** Exactly 37 pages in `staging/catalog-expansion/products/`.
- **Robots Meta Tag Verified:** 100% of the 37 pages contain `<meta name="robots" content="noindex,follow">`.
- **Production Sitemap Exclusion:** All 37 pages are **strictly excluded** from the production sitemap (`sitemap.xml`, which contains only the 83 verified canonical pages).
- **No Pre-Order or Deposit CTAs:** Zero pages feature shopping carts, advance checkout forms, or payment requests.
- **COMING_SOON Status Badge:** Every page clearly displays the `COMING_SOON` badge in the header eyebrow.

---

## 2. Master Verification Table (All 37 Group B Pages)

| # | Product Name | Unique Slug | Category | Word Count | Robots Meta Directive | Production Sitemap Status | Pre-Order Check | Commercial Status |
|---|---|---|---|:---:|:---:|:---:|:---:|:---:|
| 1 | **Ahrefs Starter** | `ahrefs-starter` | SEO & Marketing | 663 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 2 | **ChatPRD AI** | `chatprd-ai` | Productivity Software | 651 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 3 | **DaVinci Resolve Studio** | `davinci-resolve-studio` | AI Video | 695 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 4 | **Domo AI** | `domo-ai` | AI Video | 652 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 5 | **Dzine Master** | `dzine-master` | AI Design | 642 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 6 | **Firecrawl Starter** | `firecrawl-starter` | Development | 664 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 7 | **Freepik Premium** | `freepik-premium` | AI Design | 640 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 8 | **Genspark AI** | `genspark-ai` | AI Assistants | 654 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 9 | **Grok / SuperGrok** | `grok-supergrok` | AI Assistants | 670 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 10 | **MiniMax Hailuo AI** | `minimax-hailuo-ai` | AI Video | 668 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 11 | **Helium 10** | `helium-10` | SEO & Marketing | 683 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 12 | **HeyGen AI Avatar Pro** | `heygen-ai-avatar-pro` | AI Video | 699 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 13 | **Higgsfield AI** | `higgsfield-ai` | AI Video | 630 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 14 | **Ideogram AI Plus** | `ideogram-ai-plus` | AI Image Generation | 678 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 15 | **InVideo AI** | `invideo-ai` | AI Video | 661 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 16 | **Jasper AI** | `jasper-ai` | AI Writing | 665 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 17 | **Kling AI Pro** | `kling-ai-pro` | AI Video | 683 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 18 | **Make (Integromat) Pro** | `make-integromat-pro` | Automation | 706 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 19 | **Manus AI** | `manus-ai` | AI Assistants | 658 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 20 | **Morphic AI** | `morphic-ai` | AI Assistants | 647 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 21 | **OpusClip Pro** | `opus-clip-pro` | AI Video | 667 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 22 | **Play.ht** | `playht-voice-ai` | AI Voice | 630 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 23 | **Prime Video** | `prime-video` | Entertainment | 674 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 24 | **Quizlet Plus** | `quizlet-plus` | Education & Learning | 661 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 25 | **Qwen AI** | `qwen-ai` | AI Assistants | 661 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 26 | **Railway Pro** | `railway-pro` | Development | 631 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 27 | **Skillshare Premium** | `skillshare-premium` | Education & Learning | 642 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 28 | **Storyblocks Unlimited** | `storyblocks-unlimited` | AI Video | 662 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 29 | **Success.ai Starter Leads** | `success-ai-leads` | SEO & Marketing | 670 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 30 | **Suno AI** | `suno-ai` | AI Voice | 680 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 31 | **Supabase Pro** | `supabase-pro` | Development | 655 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 32 | **TradingView Pro** | `tradingview-pro` | Research Tools | 676 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 33 | **Udemy Personal Plan** | `udemy-personal-plan` | Education & Learning | 670 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 34 | **v0 by Vercel** | `v0-by-vercel` | AI Coding | 698 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 35 | **vidIQ Pro** | `vidiq-pro` | SEO & Marketing | 687 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 36 | **Windsurf Editor** | `windsurf-editor` | AI Coding | 665 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
| 37 | **WordAI** | `wordai-rewriter` | AI Writing | 610 | `noindex,follow` | `EXCLUDED` | Zero Deposits | `COMING_SOON` |
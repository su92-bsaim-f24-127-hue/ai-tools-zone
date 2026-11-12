# Phase 3.1.1 — Product Identity & Duplicate Final Reconciliation

**Project:** AI Tools Zone  
**Website:** https://aitoolszone.tech/  
**Reconciliation Date:** 12 November 2026  

---

## 1. Executive Summary

This report resolves product identity across official plan names, features, and target query intent for the 6 high-focus brands.

---

## 2. In-Depth Brand & Plan Reconciliations

### A. Grammarly (Grammarly Free vs Grammarly Premium vs Business)
- **Official Offering:** Grammarly provides Free (grammar checks), Premium ($12/mo, tone adjustment, full sentence rewrites, plagiarism checker), and Business ($15/member/mo).
- **Pakistani Market Demand:** Pakistani university students, academic researchers, and content freelancers almost exclusively search for 'Grammarly Premium' to unlock plagiarism and advanced stylistic corrections.
- **AI Tools Zone Resolution:** Single candidate record `grammarly-premium` (ID: `grammarly`, slug: `grammarly-premium`).
- **Cannibalization Risk:** 0%. No other Grammarly pages exist in production or staging.
- **Canonical Destination:** `https://aitoolszone.tech/products/grammarly-premium/`

### B. QuillBot (QuillBot Free vs QuillBot Premium)
- **Official Offering:** QuillBot Free (125 words paraphraser limit) vs QuillBot Premium ($9.95/mo, unlimited paraphraser, 6,000 words summarizer, 20 pages plagiarism checker).
- **Pakistani Market Demand:** Freelancers and thesis writers seek QuillBot Premium to bypass the 125-word limit.
- **AI Tools Zone Resolution:** Single candidate record `quillbot-premium` (ID: `quillbot`, slug: `quillbot-premium`).
- **Cannibalization Risk:** 0%.
- **Canonical Destination:** `https://aitoolszone.tech/products/quillbot-premium/`

### C. Perplexity (Perplexity Free vs Perplexity Pro)
- **Official Offering:** Perplexity Free (standard search) vs Perplexity Pro ($20/mo, 300+ Pro searches/day, model selection: Claude 3.5 Sonnet, GPT-4o, Sonar Large, file uploads).
- **Pakistani Market Demand:** Searches for 'Perplexity Pakistan' and 'Perplexity Pro Pakistan' target the Pro subscription features.
- **AI Tools Zone Resolution:** Single candidate record `perplexity-pro` (ID: `perplexity`, slug: `perplexity-pro`). The landing page H1 and meta title address both general 'Perplexity AI' and 'Perplexity Pro' intent.
- **Cannibalization Risk:** 0%.
- **Canonical Destination:** `https://aitoolszone.tech/products/perplexity-pro/`

### D. Replit (Replit Starter vs Replit Core)
- **Official Offering:** Replit transitioned its individual developer plan to 'Replit Core' ($20/mo, unlimited cloud workspaces, 4 vCPUs, AI Agent credits).
- **AI Tools Zone Resolution:** Replit Core is **already an active production product** at `a09b8c4` (`data/catalog.json`, ID: `replit`, slug: `replit-core`, price: PKR 3,200).
- **Audit Finding:** Do NOT create a new `/products/replit/` page. Replit Core is the authoritative product satisfying all Replit queries.
- **Canonical Destination:** `https://aitoolszone.tech/products/replit-core.html`

### E. DeepSeek (DeepSeek Web Chat vs DeepSeek R1 vs API)
- **Official Offering:** DeepSeek offers free web chat, an open-weights reasoning model (DeepSeek-R1), and pay-as-you-go API tokens.
- **Pakistani Market Demand:** Users seek stable access and assistance overcoming server capacity errors during peak hours.
- **AI Tools Zone Resolution:** Single candidate record `deepseek-unlimited` (ID: `deepseek`, slug: `deepseek-unlimited`).
- **Content Architecture:** Dedicated technical comparisons (e.g. 'DeepSeek R1 vs ChatGPT Plus in Pakistan') are mapped to `/blog/` and `/compare/`, keeping the product listing clean.
- **Canonical Destination:** `https://aitoolszone.tech/products/deepseek-unlimited/`

### F. GitHub Copilot (GitHub Copilot vs Microsoft 365 Copilot)
- **Official Offering:** GitHub Copilot ($10/mo, IDE code completion) is an entirely different product from Microsoft 365 Copilot ($30/user/mo, Office document automation).
- **AI Tools Zone Resolution:**
  - GitHub Copilot is cataloged under Development: `github-copilot` (`/products/github-copilot/`).
  - Microsoft 365 Copilot is cataloged under Office Software: `microsoft-office-365` (`/products/microsoft-office-365/`).
- **Cannibalization Risk:** 0%. Target completely different user personas (software developers vs corporate office workers).
- **Canonical Destination:** `https://aitoolszone.tech/products/github-copilot/`
# Phase 3.1 — Independent Catalog Reconciliation Report

**Project:** AI Tools Zone  
**Website:** https://aitoolszone.tech/  
**Audit Date:** 12 November 2026  
**Auditor:** Independent Technical SEO & Catalog Quality Gate  
**Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  

---

## 1. Executive Reconciliation Summary

This independent audit reconciles the complete product catalog across all project repositories, data stores, CSV registers, and staging directories.

### Key Audit Verifications:
- **Total Tracked Products:** Exactly **77 records**.
- **Existing Active Products (`AVAILABLE`):** Exactly **20 records** in `data/catalog.json`. Production baseline is 100% preserved.
- **Newly Discovered Candidates:** Exactly **57 records** in `data/draft-catalog-recommendations.json`.
- **Breakdown of 57 Candidates:**
  - `ENQUIRE`: **12 products** (High-priority Pakistani search demand, staged with WhatsApp lead capture).
  - `COMING_SOON`: **40 products** (SaaS and AI pipeline discovery, staged as informational hubs).
  - `REJECTED`: **5 products** (`allinone`, `turnitin`, `midjourney`, `semrush`, `spotify`) strictly excluded from public offers.
- **Eligible Staged HTML Pages:** Exactly **52 product pages** (`12 ENQUIRE + 40 COMING_SOON`).
- **Staged Category Hubs:** Exactly **20 category pages**.
- **Mathematical Equality:** `20 Active + 57 Candidates = 77 Master Records`. Exactly **0 missing**, **0 unaccounted for**.

---

## 2. Master 77-Product Reconciliation Register

| # | Product ID | Product Name | Brand | Slug | Type | Category | Status | Access Model | Price Benchmark | Page Path | Overlap Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `chatgpt` | **ChatGPT Plus** | OpenAI | `chatgpt-plus` | Active Production | AI Assistants | `AVAILABLE` | Private | PKR PKR 2,300 | `/products/chatgpt-plus.html` | Active Baseline |
| 2 | `gemini` | **Gemini Pro** | Google | `gemini-pro` | Active Production | AI Assistants | `AVAILABLE` | Private | PKR PKR 2,000 | `/products/gemini-pro.html` | Active Baseline |
| 3 | `veo` | **Veo 3 Ultra** | Google | `veo-3-ultra` | Active Production | AI Video | `AVAILABLE` | Shared | PKR PKR 2,100 | `/products/veo-3-ultra.html` | Active Baseline |
| 4 | `leonardo` | **Leonardo AI Essential** | Leonardo.Ai | `leonardo-ai-essential` | Active Production | Design | `AVAILABLE` | Private | PKR PKR 1,900 | `/products/leonardo-ai-essential.html` | Active Baseline |
| 5 | `elevenlabs` | **ElevenLabs** | ElevenLabs | `elevenlabs` | Active Production | AI Voice | `AVAILABLE` | Private | PKR PKR 3,300 | `/products/elevenlabs.html` | Active Baseline |
| 6 | `canva` | **Canva Pro Edu** | Canva | `canva-pro-edu` | Active Production | Design | `AVAILABLE` | Invitation | PKR PKR 900 | `/products/canva-pro-edu.html` | Active Baseline |
| 7 | `figma` | **Figma Pro Private** | Figma | `figma-pro-private` | Active Production | Design | `AVAILABLE` | Private | PKR PKR 3,000 | `/products/figma-pro-private.html` | Active Baseline |
| 8 | `capcut` | **CapCut Pro** | CapCut | `capcut-pro` | Active Production | AI Video | `AVAILABLE` | Private | PKR PKR 900 | `/products/capcut-pro.html` | Active Baseline |
| 9 | `adobe` | **Adobe Creative Cloud** | Adobe | `adobe-creative-cloud` | Active Production | Design | `AVAILABLE` | Private | PKR PKR 1,700 | `/products/adobe-creative-cloud.html` | Active Baseline |
| 10 | `lovable` | **Lovable Pro** | Lovable | `lovable-pro` | Active Production | Development | `AVAILABLE` | Private | PKR PKR 1,600 | `/products/lovable-pro.html` | Active Baseline |
| 11 | `gamma` | **Gamma Pro** | Gamma | `gamma-pro` | Active Production | Productivity | `AVAILABLE` | Private | PKR PKR 23,000 | `/products/gamma-pro.html` | Active Baseline |
| 12 | `replit` | **Replit Core** | Replit | `replit-core` | Active Production | Development | `AVAILABLE` | Private | PKR PKR 3,200 | `/products/replit-core.html` | Active Baseline |
| 13 | `n8n` | **n8n Starter** | n8n | `n8n-starter` | Active Production | Development | `AVAILABLE` | Private | PKR PKR 7,000 | `/products/n8n-starter.html` | Active Baseline |
| 14 | `notion` | **Notion Business** | Notion | `notion-business` | Active Production | Productivity | `AVAILABLE` | Invitation | PKR PKR 2,200 | `/products/notion-business.html` | Active Baseline |
| 15 | `nordvpn` | **NordVPN** | NordVPN | `nordvpn` | Active Production | VPN & Security | `AVAILABLE` | Private | PKR PKR 1,800 | `/products/nordvpn.html` | Active Baseline |
| 16 | `surfshark` | **Surfshark VPN** | Surfshark | `surfshark-vpn` | Active Production | VPN & Security | `AVAILABLE` | Shared | PKR PKR 800 | `/products/surfshark-vpn.html` | Active Baseline |
| 17 | `youtube` | **YouTube Premium** | YouTube | `youtube-premium` | Active Production | Entertainment | `AVAILABLE` | Invitation | PKR PKR 1,200 | `/products/youtube-premium.html` | Active Baseline |
| 18 | `netflix` | **Netflix Premium 4K** | Netflix | `netflix-premium-4k` | Active Production | Entertainment | `AVAILABLE` | Shared | PKR PKR 400 | `/products/netflix-premium-4k.html` | Active Baseline |
| 19 | `linkedin` | **LinkedIn Premium** | LinkedIn | `linkedin-premium` | Active Production | Business | `AVAILABLE` | Invitation | PKR PKR 1,500 | `/products/linkedin-premium.html` | Active Baseline |
| 20 | `windows` | **Windows 11 Pro Key** | Microsoft | `windows-11-pro-key` | Active Production | Software | `AVAILABLE` | License Key | PKR PKR 1,900 | `/products/windows-11-pro-key.html` | Active Baseline |
| 21 | `claude` | **Claude Pro** | Anthropic | `claude-pro` | New Candidate | AI Assistants | `ENQUIRE` | Concierge Payment Facilitation (Customer Account) | $20.00 / month (Price on Enquiry) | `/products/claude-pro/` | Unique Candidate |
| 22 | `cursor` | **Cursor AI Pro** | Anysphere | `cursor-ai-pro` | New Candidate | Development | `ENQUIRE` | Developer Workspace License / Concierge Payment | $20.00 / month (Price on Enquiry) | `/products/cursor-ai-pro/` | Unique Candidate |
| 23 | `office365` | **Microsoft Office 365** | Microsoft | `microsoft-office-365` | New Candidate | Office Software | `ENQUIRE` | Personal Microsoft Account Invitation / License | $99.99 / year (Family Retail) (Price on Enquiry) | `/products/microsoft-office-365/` | Unique Candidate |
| 24 | `grammarly` | **Grammarly Premium** | Grammarly | `grammarly-premium` | New Candidate | AI Writing | `ENQUIRE` | Personal Email Invitation / Workspace Seat | $30.00 / month (Retail) (Price on Enquiry) | `/products/grammarly-premium/` | Unique Candidate |
| 25 | `perplexity` | **Perplexity Pro** | Perplexity AI | `perplexity-pro` | New Candidate | AI Assistants | `ENQUIRE` | Personal Account Upgrade / Voucher | $20.00 / month (Price on Enquiry) | `/products/perplexity-pro/` | Unique Candidate |
| 26 | `copilot` | **GitHub Copilot** | GitHub (Microsoft) | `github-copilot` | New Candidate | Development | `ENQUIRE` | GitHub Account Provisioning / Organization Seat | $10.00 / mo (Individual) / $19.00 / mo (Business) (Price on Enquiry) | `/products/github-copilot/` | Unique Candidate |
| 27 | `quillbot` | **QuillBot Premium** | Learneo | `quillbot-premium` | New Candidate | AI Writing | `ENQUIRE` | Direct Account Upgrade / Team Seat | $9.95 / month (Price on Enquiry) | `/products/quillbot-premium/` | Unique Candidate |
| 28 | `coursera-plus` | **Coursera Plus** | Coursera | `coursera-plus-premium` | New Candidate | Education & Learning | `ENQUIRE` | Verified Learning Seat / Personal Account Invitation | $59.00 / month ($399 / year) (Price on Enquiry) | `/products/coursera-plus-premium/` | Unique Candidate |
| 29 | `runway` | **Runway ML Gen-3** | Runway AI | `runway-ml-gen-3` | New Candidate | AI Video | `ENQUIRE` | Dedicated Account Allocation / Managed Credits | $15.00 / mo (Standard) / $35.00 / mo (Pro) (Price on Enquiry) | `/products/runway-ml-gen-3/` | Unique Candidate |
| 30 | `deepseek` | **DeepSeek Unlimited** | DeepSeek | `deepseek-unlimited` | New Candidate | AI Assistants | `ENQUIRE` | Dedicated Developer API / Web Workspace | $15.00 / month (Price on Enquiry) | `/products/deepseek-unlimited/` | Unique Candidate |
| 31 | `ahrefs` | **Ahrefs Starter** | Ahrefs | `ahrefs-starter` | New Candidate | SEO & Marketing | `COMING_SOON` | Direct Account / Workspace Seat | $29.00 / month (Price on Enquiry) | `/products/ahrefs-starter/` | Unique Candidate |
| 32 | `allinone` | **All-in-One Mega AI Portal** | Multi-Vendor Cookie Sharing Panel | `all-in-one-mega-ai-portal` | New Candidate | AI Assistants | `REJECTED` | Cracked Browser Cookie Injection | N/A (Unauthorized Grey-Market Service) (Price on Enquiry) | None (Excluded) | Excluded High Risk |
| 33 | `bolt-new` | **Bolt.new Pro** | StackBlitz | `bolt-new-pro` | New Candidate | AI Coding | `ENQUIRE` | Personal Account Upgrade / Workspace Seat | $20.00 / month (Price on Enquiry) | `/products/bolt-new-pro/` | Unique Candidate |
| 34 | `chatprd` | **ChatPRD AI** | ChatPRD | `chatprd-ai` | New Candidate | Productivity Software | `COMING_SOON` | Direct Workspace Seat | $20.00 / month (Price on Enquiry) | `/products/chatprd-ai/` | Unique Candidate |
| 35 | `davinci-resolve` | **DaVinci Resolve Studio** | Blackmagic Design | `davinci-resolve-studio` | New Candidate | AI Video | `COMING_SOON` | Official Activation License Key | $295.00 (Lifetime License) (Price on Enquiry) | `/products/davinci-resolve-studio/` | Unique Candidate |
| 36 | `descript` | **Descript Creator** | Descript | `descript-creator` | New Candidate | AI Video | `ENQUIRE` | Personal Account Upgrade / Workspace Seat | $15.00 / month (Price on Enquiry) | `/products/descript-creator/` | Unique Candidate |
| 37 | `domo-ai` | **Domo AI** | Domo AI | `domo-ai` | New Candidate | AI Video | `COMING_SOON` | Discord Workspace / Web Platform Seat | $16.00 / month (Price on Enquiry) | `/products/domo-ai/` | Unique Candidate |
| 38 | `dzine` | **Dzine Master** | Dzine AI | `dzine-master` | New Candidate | AI Design | `COMING_SOON` | Personal Account Upgrade | $19.00 / month (Price on Enquiry) | `/products/dzine-master/` | Unique Candidate |
| 39 | `enterprise-api` | **Enterprise AI API Credits** | Independent Software / Multi-Provider | `enterprise-ai-api-credits` | New Candidate | Development | `COMING_SOON` | Direct API Key / Developer Account Provisioning | Custom API Pricing (Price on Enquiry) | `/products/enterprise-ai-api-credits/` | Unique Candidate |
| 40 | `firecrawl` | **Firecrawl Starter** | Mendable / Firecrawl | `firecrawl-starter` | New Candidate | Development | `COMING_SOON` | Developer API Key / Cloud Workspace | $20.00 / month (Price on Enquiry) | `/products/firecrawl-starter/` | Unique Candidate |
| 41 | `freepik` | **Freepik Premium** | Freepik Company | `freepik-premium` | New Candidate | AI Design | `COMING_SOON` | Direct Account / Team Invitation | $15.00 / month (Price on Enquiry) | `/products/freepik-premium/` | Unique Candidate |
| 42 | `genspark` | **Genspark AI** | MainFunc / Genspark | `genspark-ai` | New Candidate | AI Assistants | `COMING_SOON` | Personal Account Upgrade | $20.00 / month (Price on Enquiry) | `/products/genspark-ai/` | Unique Candidate |
| 43 | `google-ultra` | **Google AI Ultra** | Google | `google-ai-ultra` | New Candidate | AI Assistants | `COMING_SOON` | Google Workspace / Personal Account Upgrade | $20.00 / month (Price on Enquiry) | `/products/google-ai-ultra/` | Unique Candidate |
| 44 | `grok` | **Grok / SuperGrok** | xAI | `grok-supergrok` | New Candidate | AI Assistants | `COMING_SOON` | X (Twitter) Account Upgrade / Premium+ Activation | $16.00 / month (X Premium+) (Price on Enquiry) | `/products/grok-supergrok/` | Unique Candidate |
| 45 | `hailuo-ai` | **MiniMax Hailuo AI** | MiniMax | `minimax-hailuo-ai` | New Candidate | AI Video | `COMING_SOON` | Direct Web Account / API Seat | $20.00 / month (Price on Enquiry) | `/products/minimax-hailuo-ai/` | Unique Candidate |
| 46 | `helium-10` | **Helium 10** | Helium 10 | `helium-10` | New Candidate | SEO & Marketing | `COMING_SOON` | Direct Account / Sub-User Seat | $39.00 / month (Starter) / $99.00 / mo (Platinum) (Price on Enquiry) | `/products/helium-10/` | Unique Candidate |
| 47 | `heygen` | **HeyGen AI Avatar Pro** | HeyGen | `heygen-ai-avatar-pro` | New Candidate | AI Video | `COMING_SOON` | Direct Account / Creator Seat | $29.00 / month (Price on Enquiry) | `/products/heygen-ai-avatar-pro/` | Unique Candidate |
| 48 | `higgsfield` | **Higgsfield AI** | Higgsfield AI | `higgsfield-ai` | New Candidate | AI Video | `COMING_SOON` | Direct Account / Mobile Platform Seat | $20.00 / month (Price on Enquiry) | `/products/higgsfield-ai/` | Unique Candidate |
| 49 | `ideogram` | **Ideogram AI Plus** | Ideogram AI | `ideogram-ai-plus` | New Candidate | AI Image Generation | `COMING_SOON` | Personal Account Upgrade | $20.00 / month (Price on Enquiry) | `/products/ideogram-ai-plus/` | Unique Candidate |
| 50 | `invideo-ai` | **InVideo AI** | InVideo | `invideo-ai` | New Candidate | AI Video | `COMING_SOON` | Personal Account Upgrade / Workspace Seat | $25.00 / month (Plus Tier) (Price on Enquiry) | `/products/invideo-ai/` | Unique Candidate |
| 51 | `jasper` | **Jasper AI** | Jasper AI | `jasper-ai` | New Candidate | AI Writing | `COMING_SOON` | Direct Account / Team Workspace Seat | $49.00 / month (Creator) (Price on Enquiry) | `/products/jasper-ai/` | Unique Candidate |
| 52 | `kling` | **Kling AI Pro** | Kuaishou Technology | `kling-ai-pro` | New Candidate | AI Video | `COMING_SOON` | Direct Web Account / Credit Allocation | $30.00 / month (Price on Enquiry) | `/products/kling-ai-pro/` | Unique Candidate |
| 53 | `make` | **Make (Integromat) Pro** | Celonis / Make | `make-integromat-pro` | New Candidate | Automation | `COMING_SOON` | Direct Account / Organization Workspace | $16.00 / month (Pro) (Price on Enquiry) | `/products/make-integromat-pro/` | Unique Candidate |
| 54 | `manus-ai` | **Manus AI** | Manus AI | `manus-ai` | New Candidate | AI Assistants | `COMING_SOON` | Personal Account Upgrade / Beta Seat | $20.00 / month (Price on Enquiry) | `/products/manus-ai/` | Unique Candidate |
| 55 | `midjourney` | **Midjourney Pro** | Midjourney, Inc. | `midjourney-pro` | New Candidate | AI Image Generation | `REJECTED` | Discord Shared Account | $30.00 / mo (Standard) / $60.00 / mo (Pro) (Price on Enquiry) | None (Excluded) | Excluded High Risk |
| 56 | `morphic` | **Morphic AI** | Morphic | `morphic-ai` | New Candidate | AI Assistants | `COMING_SOON` | Personal Account Upgrade | $15.00 / month (Price on Enquiry) | `/products/morphic-ai/` | Unique Candidate |
| 57 | `notebooklm` | **Google NotebookLM Pro** | Google | `google-notebooklm-pro` | New Candidate | Research Tools | `COMING_SOON` | Google Workspace / Enterprise Activation | $20.00 / month (Workspace Tier) (Price on Enquiry) | `/products/google-notebooklm-pro/` | Unique Candidate |
| 58 | `opus-clip` | **OpusClip Pro** | OpusClip | `opus-clip-pro` | New Candidate | AI Video | `COMING_SOON` | Personal Account Upgrade / Workspace Seat | $19.00 / month (Price on Enquiry) | `/products/opus-clip-pro/` | Unique Candidate |
| 59 | `playht` | **Play.ht** | Play.ht | `playht-voice-ai` | New Candidate | AI Voice | `COMING_SOON` | Direct Account / Studio Seat | $39.00 / month (Creator) (Price on Enquiry) | `/products/playht-voice-ai/` | Unique Candidate |
| 60 | `prime-video` | **Prime Video** | Amazon | `prime-video` | New Candidate | Entertainment | `COMING_SOON` | Direct Account / Profile Activation | $8.99 / month (Direct Retail) (Price on Enquiry) | `/products/prime-video/` | Unique Candidate |
| 61 | `quizlet` | **Quizlet Plus** | Quizlet | `quizlet-plus` | New Candidate | Education & Learning | `COMING_SOON` | Personal Account Upgrade | $35.99 / year (Price on Enquiry) | `/products/quizlet-plus/` | Unique Candidate |
| 62 | `qwen` | **Qwen AI** | Alibaba Cloud | `qwen-ai` | New Candidate | AI Assistants | `COMING_SOON` | Direct Account / API Provisioning | Usage-Based API Pricing (Price on Enquiry) | `/products/qwen-ai/` | Unique Candidate |
| 63 | `railway` | **Railway Pro** | Railway | `railway-pro` | New Candidate | Development | `COMING_SOON` | Developer Team Workspace / Account Upgrade | $20.00 / month (Price on Enquiry) | `/products/railway-pro/` | Unique Candidate |
| 64 | `semrush` | **SEMrush Pro** | Semrush Inc. | `semrush-pro` | New Candidate | SEO & Marketing | `REJECTED` | Shared Browser Proxy Panel | $139.95 / month (Price on Enquiry) | None (Excluded) | Excluded High Risk |
| 65 | `skillshare` | **Skillshare Premium** | Skillshare | `skillshare-premium` | New Candidate | Education & Learning | `COMING_SOON` | Personal Account Upgrade / Team Member | $32.00 / month (or $168 / year) (Price on Enquiry) | `/products/skillshare-premium/` | Unique Candidate |
| 66 | `spotify` | **Spotify Premium** | Spotify AB | `spotify-premium` | New Candidate | Entertainment | `REJECTED` | Family Link Sharing | $10.99 / mo (Individual) / $16.99 / mo (Family) (Price on Enquiry) | None (Excluded) | Excluded High Risk |
| 67 | `storyblocks` | **Storyblocks Unlimited** | Storyblocks | `storyblocks-unlimited` | New Candidate | AI Video | `COMING_SOON` | Direct Account / Creator Seat | $30.00 / month (Price on Enquiry) | `/products/storyblocks-unlimited/` | Unique Candidate |
| 68 | `success-ai` | **Success.ai Starter Leads** | Success.ai | `success-ai-leads` | New Candidate | SEO & Marketing | `COMING_SOON` | Direct Account / Growth Seat | $23.00 / month (Price on Enquiry) | `/products/success-ai-leads/` | Unique Candidate |
| 69 | `suno` | **Suno AI** | Suno AI | `suno-ai` | New Candidate | AI Voice | `COMING_SOON` | Personal Account Upgrade | $10.00 / mo (Pro) / $30.00 / mo (Premier) (Price on Enquiry) | `/products/suno-ai/` | Unique Candidate |
| 70 | `supabase` | **Supabase Pro** | Supabase | `supabase-pro` | New Candidate | Development | `COMING_SOON` | Developer Organization Seat / Account Upgrade | $25.00 / month (Price on Enquiry) | `/products/supabase-pro/` | Unique Candidate |
| 71 | `tradingview` | **TradingView Pro** | TradingView | `tradingview-pro` | New Candidate | Research Tools | `COMING_SOON` | Personal Account Upgrade | $14.95 / mo (Essential) / $29.95 / mo (Plus) (Price on Enquiry) | `/products/tradingview-pro/` | Unique Candidate |
| 72 | `turnitin` | **Turnitin Student / Instructor** | Turnitin LLC | `turnitin-plagiarism-checker` | New Candidate | Education & Learning | `REJECTED` | Compromised University Instructor Account | Institutional Licensing Only (Not Sold to Consumers) (Price on Enquiry) | None (Excluded) | Excluded High Risk |
| 73 | `udemy-personal` | **Udemy Personal Plan** | Udemy | `udemy-personal-plan` | New Candidate | Education & Learning | `COMING_SOON` | Personal Account Upgrade | $20.00 / month (Price on Enquiry) | `/products/udemy-personal-plan/` | Unique Candidate |
| 74 | `v0` | **v0 by Vercel** | Vercel | `v0-by-vercel` | New Candidate | AI Coding | `COMING_SOON` | Personal Account Upgrade / Team Workspace Seat | $20.00 / month (Price on Enquiry) | `/products/v0-by-vercel/` | Unique Candidate |
| 75 | `vidiq` | **vidIQ Pro** | vidIQ | `vidiq-pro` | New Candidate | SEO & Marketing | `COMING_SOON` | Direct Account / Channel Integration | $10.00 / month (Price on Enquiry) | `/products/vidiq-pro/` | Unique Candidate |
| 76 | `windsurf` | **Windsurf Editor** | Codeium | `windsurf-editor` | New Candidate | AI Coding | `COMING_SOON` | Developer Workspace Seat / Account Upgrade | $15.00 / month (Price on Enquiry) | `/products/windsurf-editor/` | Unique Candidate |
| 77 | `wordai` | **WordAI** | WordAI | `wordai-rewriter` | New Candidate | AI Writing | `COMING_SOON` | Direct Account / Studio Seat | $27.00 / month (Price on Enquiry) | `/products/wordai-rewriter/` | Unique Candidate |

---

## 3. Discrepancy Analysis vs Prior Reports

During the independent audit, the following historical narrative inconsistencies from Phase 2 and Phase 3 report summaries were identified and resolved:
1. **Grammarly & QuillBot Status:** Prior narrative summaries mentioned `grammarly-active` and `quillbot-active`. Audit confirmation: Neither product exists in the production `data/catalog.json`. Both are newly discovered candidates assigned to `ENQUIRE` status (`grammarly-premium` and `quillbot-premium`).
2. **Replit Core Status:** In competitor scans, Replit Core was extracted. However, Replit Core (`replit-core`) was already an active production product in `data/catalog.json` (PKR 3,200). It is correctly classified as an existing active product, not duplicated as a candidate.
3. **ElevenLabs & HeyGen Status:** Report 64's ASCII diagram listed `elevenlabs` in ENQUIRE, whereas ElevenLabs is already an active production product (`elevenlabs`, PKR 3,300). HeyGen is classified as `COMING_SOON`. The 12 ENQUIRE products are confirmed as: `claude-pro`, `cursor-ai-pro`, `microsoft-office-365`, `grammarly-premium`, `perplexity-pro`, `github-copilot`, `quillbot-premium`, `coursera-plus-premium`, `runway-ml-gen-3`, `deepseek-unlimited`, `bolt-new-pro`, and `descript-creator`.
4. **Zero Count Drift:** The final inventory matches the mathematical identity across all files: `20 + 57 = 77`.
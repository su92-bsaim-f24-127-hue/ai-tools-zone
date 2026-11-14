# Deliverable 00: Repository and Website URL Inventory

## 1. Project & Repository Verification

- **Project Name:** AI Tools Zone
- **Website URL:** `https://aitoolszone.tech/`
- **Active Git Branch:** `feature/competitor-product-keyword-growth`
- **HEAD Commit:** `7f21b78c16a1ca5a67627d373796087b0e35187b`
- **Expected Baseline Commit:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`
- **Merge Base with Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a` (Baseline is direct ancestor)
- **Working Tree Status:** Clean (0 unstaged changes, 0 uncommitted modifications)
- **Market / Target Audience:** Pakistan (`en-PK`)
- **Primary Currency:** Pakistani Rupee (`PKR`)
- **Production Authorization:** **NOT GRANTED** (All implementation strictly confined to feature branch)

## 2. Project Architecture Source Files

The static website generation and internal linking structure is controlled by deterministic Python and JSON data sources:

| Architectural Role | Primary Source File | Description |
| :--- | :--- | :--- |
| **Core Build Engine** | `build_site.py` | Generates homepage, product pages, legal pages, FAQ page, manifest, and coordinates overall build |
| **Editorial & Hub Builder** | `seo_pages.py` | Builds category pages, use cases, comparison pages, alternatives, guides, blog articles, and hubs |
| **Catalog Database** | `data/catalog.json` | Canonical structured data for all 32 live products (prices, durations, features, access) |
| **Product Editorial Content**| `data/product-content.json` | Deep overviews, FAQs, capability bullets, and target intent for individual products |
| **SEO Page Content** | `data/seo-content.json` | Editorial text, category descriptions, comparisons, and use-case recommendations |
| **Blog Content Hub** | `data/blog-content.json` | 20 informational guides addressing long-tail Pakistani search intent |
| **Brand Logos Registry** | `assets/product-logo-sources.json`| Sourced 128x128 official brand marks for all 32 products |
| **State & Freshness Hash** | `data/page-state.json` | Content-based SHA256 hashes and deterministic lastmod timestamps for all 95 routes |
| **SEO Audit Test Suite** | `audit_seo.py` | Crawls all local pages, verifies canonical tags, meta tags, image tags, and broken links |
| **Growth Engine Audit** | `audit_growth.py` | Validates 95 indexable pages, product offers, incoming link graphs, and contract parity |
| **Security Validator** | `scripts/test_render_text_security.py` | Validates markdown link sanitization and XSS/scheme protection |
| **Packaging Pipeline** | `package_site.py` | Validates production package integrity (165 production files in `ai-tools-zone.zip`) |

## 3. Comprehensive URL Inventory (95 Canonical Pages)

| # | Canonical Path | Page Type | H1 Heading | Indexable | In-Links | Out-Links | Primary Search Intent |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | `/` | home | AI Subscriptions in Pakistan.Clear PKR p | Yes | 202 | 115 | Commercial Discovery & Marketplace Overview |
| 2 | `/about/` | legal_info | About AI Tools Zone | Yes | 102 | 30 | Trust, Transparency & Compliance |
| 3 | `/alternatives/` | alternatives_hub | AI Tool Alternatives for Specific Tasks | Yes | 3 | 33 | Trust, Transparency & Compliance |
| 4 | `/alternatives/canva/` | alternatives | Canva Alternatives for Design Work in Pa | Yes | 8 | 36 | Commercial Alternative Evaluation |
| 5 | `/alternatives/chatgpt/` | alternatives | ChatGPT Alternatives: Choose by Task in  | Yes | 10 | 37 | Commercial Alternative Evaluation |
| 6 | `/blog/` | blog_hub | AI Tools Zone Blog | Yes | 211 | 82 | Trust, Transparency & Compliance |
| 7 | `/blog/ai-agency-automation-pakistan-n8n-make/` | blog | AI Agency Automation in Pakistan: Build  | Yes | 5 | 32 | Informational / Long-Tail Organic Query Resol |
| 8 | `/blog/ai-phone-agents-whatsapp-bots-pakistan/` | blog | AI Phone Agents & WhatsApp Bots for Paki | Yes | 194 | 31 | Informational / Long-Tail Organic Query Resol |
| 9 | `/blog/ai-subscription-vs-api-credits-pakistan/` | blog | AI Subscription vs API Credits in Pakist | Yes | 5 | 32 | Informational / Long-Tail Organic Query Resol |
| 10 | `/blog/ai-tools-for-content-creators-pakistan/` | blog | AI Tools for Pakistani Content Creators: | Yes | 3 | 32 | Informational / Long-Tail Organic Query Resol |
| 11 | `/blog/ai-tools-for-pakistani-freelancers/` | blog | AI Tools for Freelancers in Pakistan: ch | Yes | 5 | 31 | Informational / Long-Tail Organic Query Resol |
| 12 | `/blog/ai-tools-for-pakistani-students-research-thesis/` | blog | AI Tools for Pakistani Students: Researc | Yes | 6 | 34 | Informational / Long-Tail Organic Query Resol |
| 13 | `/blog/ai-tools-for-teachers-pakistan/` | blog | AI Tools for Teachers in Pakistan: a saf | Yes | 7 | 31 | Informational / Long-Tail Organic Query Resol |
| 14 | `/blog/avoiding-account-bans-shared-ai-tools-pakistan/` | blog | How to Avoid Account Bans on Shared AI T | Yes | 6 | 33 | Informational / Long-Tail Organic Query Resol |
| 15 | `/blog/best-ai-image-generators-pakistan/` | blog | Best AI Image Generators in Pakistan (20 | Yes | 6 | 32 | Informational / Long-Tail Organic Query Resol |
| 16 | `/blog/best-ai-video-generators-pakistan/` | blog | Best AI Video Generators in Pakistan (20 | Yes | 5 | 32 | Informational / Long-Tail Organic Query Resol |
| 17 | `/blog/canva-pro-vs-adobe-creative-cloud-pakistan-freelancers/` | blog | Canva Pro vs Adobe Creative Cloud in Pak | Yes | 6 | 32 | Informational / Long-Tail Organic Query Resol |
| 18 | `/blog/chatgpt-plus-vs-gemini-pro-pakistan/` | blog | ChatGPT Plus vs Gemini Pro for Pakistan  | Yes | 5 | 32 | Informational / Long-Tail Organic Query Resol |
| 19 | `/blog/cheap-ai-subscriptions-pakistan/` | blog | Cheap AI Subscriptions in Pakistan: PKR  | Yes | 7 | 32 | Informational / Long-Tail Organic Query Resol |
| 20 | `/blog/cursor-vs-copilot-pakistan/` | blog | Cursor AI vs GitHub Copilot in Pakistan: | Yes | 5 | 32 | Informational / Long-Tail Organic Query Resol |
| 21 | `/blog/faceless-youtube-automation-ai-tools-pakistan/` | blog | Faceless YouTube Channel Automation with | Yes | 8 | 34 | Informational / Long-Tail Organic Query Resol |
| 22 | `/blog/free-ai-tools-pakistan/` | blog | Free AI Tools in Pakistan: a practical s | Yes | 99 | 32 | Informational / Long-Tail Organic Query Resol |
| 23 | `/blog/how-to-earn-money-with-ai-pakistan/` | blog | How to Earn Money with AI Tools in Pakis | Yes | 6 | 32 | Informational / Long-Tail Organic Query Resol |
| 24 | `/blog/how-to-pay-for-chatgpt-plus-pakistan/` | blog | How to Pay for ChatGPT Plus in Pakistan: | Yes | 5 | 32 | Informational / Long-Tail Organic Query Resol |
| 25 | `/blog/jazzcash-easypaisa-ai-tools-pakistan/` | blog | How to Buy AI Subscriptions with JazzCas | Yes | 6 | 33 | Informational / Long-Tail Organic Query Resol |
| 26 | `/blog/where-to-buy-ai-tools-pakistan/` | blog | Where to Buy AI Tools in Pakistan: Safe  | Yes | 5 | 32 | Informational / Long-Tail Organic Query Resol |
| 27 | `/categories/` | categories_hub | Browse AI Tools & Subscription Categorie | Yes | 201 | 46 | Trust, Transparency & Compliance |
| 28 | `/categories/ai-assistants/` | category | AI assistants and writing tools in Pakis | Yes | 24 | 39 | Category-Level Commercial & Informational Eva |
| 29 | `/categories/ai-video/` | category | AI Video Generation & Editing Tools in P | Yes | 24 | 36 | Category-Level Commercial & Informational Eva |
| 30 | `/categories/ai-voice/` | category | AI voice tools and narration plans in Pa | Yes | 12 | 34 | Category-Level Commercial & Informational Eva |
| 31 | `/categories/business/` | category | Business and professional subscription p | Yes | 11 | 34 | Category-Level Commercial & Informational Eva |
| 32 | `/categories/design/` | category | Graphic Design & AI Image Tools in Pakis | Yes | 24 | 37 | Category-Level Commercial & Informational Eva |
| 33 | `/categories/development/` | category | AI coding, app building and automation t | Yes | 23 | 38 | Category-Level Commercial & Informational Eva |
| 34 | `/categories/entertainment/` | category | Entertainment subscription plans in Paki | Yes | 11 | 34 | Category-Level Commercial & Informational Eva |
| 35 | `/categories/productivity/` | category | AI productivity and presentation tools i | Yes | 18 | 37 | Category-Level Commercial & Informational Eva |
| 36 | `/categories/software/` | category | Software license listings in Pakistan | Yes | 11 | 35 | Category-Level Commercial & Informational Eva |
| 37 | `/categories/vpn-security/` | category | VPN subscription plans in Pakistan | Yes | 12 | 34 | Category-Level Commercial & Informational Eva |
| 38 | `/compare/` | compare_hub | Compare AI Tools in Pakistan | Yes | 207 | 51 | Trust, Transparency & Compliance |
| 39 | `/compare/canva-vs-adobe/` | comparison | Canva vs Adobe: Design Workflow & PKR Pl | Yes | 108 | 38 | Commercial Investigation & Tool Evaluation |
| 40 | `/compare/capcut-vs-canva/` | comparison | CapCut vs Canva: Creator Workflow & PKR  | Yes | 8 | 34 | Commercial Investigation & Tool Evaluation |
| 41 | `/compare/capcut-vs-runway/` | comparison | CapCut vs Runway: editing and AI video w | Yes | 106 | 37 | Commercial Investigation & Tool Evaluation |
| 42 | `/compare/chatgpt-vs-claude/` | comparison | ChatGPT Plus vs Claude Pro for Pakistan  | Yes | 106 | 36 | Commercial Investigation & Tool Evaluation |
| 43 | `/compare/chatgpt-vs-gemini/` | comparison | ChatGPT vs Gemini: PKR Plans & Access | Yes | 110 | 37 | Commercial Investigation & Tool Evaluation |
| 44 | `/compare/claude-vs-gemini/` | comparison | Claude Pro vs Gemini: a practical plan c | Yes | 6 | 36 | Commercial Investigation & Tool Evaluation |
| 45 | `/compare/elevenlabs-vs-playht/` | comparison | ElevenLabs vs PlayHT: test voice tools f | Yes | 7 | 36 | Commercial Investigation & Tool Evaluation |
| 46 | `/compare/grammarly-vs-quillbot-vs-wordai/` | comparison | Grammarly vs QuillBot vs WordAI: choose  | Yes | 9 | 32 | Commercial Investigation & Tool Evaluation |
| 47 | `/compare/helium10-vs-semrush-vs-vidiq/` | comparison | Helium 10 vs Semrush vs vidIQ: choose by | Yes | 8 | 32 | Commercial Investigation & Tool Evaluation |
| 48 | `/compare/leonardo-vs-midjourney/` | comparison | Leonardo AI vs Midjourney: Image Generat | Yes | 104 | 36 | Commercial Investigation & Tool Evaluation |
| 49 | `/compare/replit-vs-lovable/` | comparison | Replit Core vs Lovable Pro: AI Coding &  | Yes | 10 | 37 | Commercial Investigation & Tool Evaluation |
| 50 | `/faq/` | faq | Frequently Asked Questions (FAQs) | Yes | 107 | 130 | Transactional Assurance & FAQ Resolution |
| 51 | `/guides/` | guides_hub | Practical AI tool guides & blog for Paki | Yes | 103 | 148 | Trust, Transparency & Compliance |
| 52 | `/guides/catalog-methodology/` | guide | How We List and Compare AI Subscription  | Yes | 34 | 31 | Informational / Buying Decision Support |
| 53 | `/guides/choose-ai-subscription/` | guide | How to Choose an AI Subscription in Paki | Yes | 46 | 31 | Informational / Buying Decision Support |
| 54 | `/guides/private-vs-shared-access/` | guide | Private vs Shared AI Access: Invitations | Yes | 56 | 31 | Informational / Buying Decision Support |
| 55 | `/pricing/` | pricing | AI Tools Pricing in Pakistan: Compare PK | Yes | 220 | 78 | Commercial Comparison / Price Evaluation |
| 56 | `/privacy/` | legal_info | Your privacy matters. | Yes | 98 | 26 | Trust, Transparency & Compliance |
| 57 | `/products/` | products_hub | All AI Tools & Digital Subscriptions in  | Yes | 139 | 73 | Commercial Exploration / Tool Catalog |
| 58 | `/products/adobe-creative-cloud/` | product | Adobe Creative Cloud | Yes | 19 | 38 | Commercial Purchase / Transactional Intent |
| 59 | `/products/bolt-new-pro/` | product | Bolt.new Pro | Yes | 6 | 34 | Commercial Purchase / Transactional Intent |
| 60 | `/products/canva-pro-edu/` | product | Canva Pro Edu | Yes | 36 | 39 | Commercial Purchase / Transactional Intent |
| 61 | `/products/capcut-pro/` | product | CapCut Pro | Yes | 27 | 39 | Commercial Purchase / Transactional Intent |
| 62 | `/products/chatgpt-plus/` | product | ChatGPT Plus | Yes | 33 | 38 | Commercial Purchase / Transactional Intent |
| 63 | `/products/claude-pro/` | product | Claude Pro | Yes | 10 | 34 | Commercial Purchase / Transactional Intent |
| 64 | `/products/coursera-plus-premium/` | product | Coursera Plus | Yes | 7 | 32 | Commercial Purchase / Transactional Intent |
| 65 | `/products/cursor-ai-pro/` | product | Cursor AI Pro | Yes | 9 | 34 | Commercial Purchase / Transactional Intent |
| 66 | `/products/deepseek-unlimited/` | product | DeepSeek Unlimited | Yes | 10 | 34 | Commercial Purchase / Transactional Intent |
| 67 | `/products/descript-creator/` | product | Descript Creator | Yes | 9 | 34 | Commercial Purchase / Transactional Intent |
| 68 | `/products/elevenlabs/` | product | ElevenLabs | Yes | 20 | 35 | Commercial Purchase / Transactional Intent |
| 69 | `/products/figma-pro-private/` | product | Figma Pro Private | Yes | 15 | 37 | Commercial Purchase / Transactional Intent |
| 70 | `/products/gamma-pro/` | product | Gamma Pro | Yes | 17 | 36 | Commercial Purchase / Transactional Intent |
| 71 | `/products/gemini-pro/` | product | Gemini Pro | Yes | 28 | 38 | Commercial Purchase / Transactional Intent |
| 72 | `/products/github-copilot/` | product | GitHub Copilot | Yes | 6 | 34 | Commercial Purchase / Transactional Intent |
| 73 | `/products/grammarly-premium/` | product | Grammarly Premium | Yes | 11 | 34 | Commercial Purchase / Transactional Intent |
| 74 | `/products/leonardo-ai-essential/` | product | Leonardo AI Essential | Yes | 23 | 39 | Commercial Purchase / Transactional Intent |
| 75 | `/products/linkedin-premium/` | product | LinkedIn Premium | Yes | 11 | 34 | Commercial Purchase / Transactional Intent |
| 76 | `/products/lovable-pro/` | product | Lovable Pro | Yes | 20 | 38 | Commercial Purchase / Transactional Intent |
| 77 | `/products/microsoft-office-365/` | product | Microsoft Office 365 | Yes | 7 | 32 | Commercial Purchase / Transactional Intent |
| 78 | `/products/n8n-starter/` | product | n8n Starter | Yes | 23 | 38 | Commercial Purchase / Transactional Intent |
| 79 | `/products/netflix-premium-4k/` | product | Netflix Premium 4K | Yes | 12 | 34 | Commercial Purchase / Transactional Intent |
| 80 | `/products/nordvpn/` | product | NordVPN | Yes | 12 | 34 | Commercial Purchase / Transactional Intent |
| 81 | `/products/notion-business/` | product | Notion Business | Yes | 21 | 37 | Commercial Purchase / Transactional Intent |
| 82 | `/products/perplexity-pro/` | product | Perplexity Pro | Yes | 7 | 34 | Commercial Purchase / Transactional Intent |
| 83 | `/products/quillbot-premium/` | product | QuillBot Premium | Yes | 11 | 34 | Commercial Purchase / Transactional Intent |
| 84 | `/products/replit-core/` | product | Replit Core | Yes | 22 | 39 | Commercial Purchase / Transactional Intent |
| 85 | `/products/runway-ml-gen-3/` | product | Runway ML Gen-3 | Yes | 9 | 34 | Commercial Purchase / Transactional Intent |
| 86 | `/products/surfshark-vpn/` | product | Surfshark VPN | Yes | 11 | 34 | Commercial Purchase / Transactional Intent |
| 87 | `/products/veo-3-ultra/` | product | Veo 3 Ultra | Yes | 15 | 35 | Commercial Purchase / Transactional Intent |
| 88 | `/products/windows-11-pro-key/` | product | Windows 11 Pro Key | Yes | 12 | 34 | Commercial Purchase / Transactional Intent |
| 89 | `/products/youtube-premium/` | product | YouTube Premium | Yes | 13 | 34 | Commercial Purchase / Transactional Intent |
| 90 | `/terms/` | legal_info | Clear plans. Clear next steps. | Yes | 148 | 26 | Trust, Transparency & Compliance |
| 91 | `/use-cases/` | use_cases_hub | Choose AI Tools by Your Workflow | Yes | 7 | 37 | Trust, Transparency & Compliance |
| 92 | `/use-cases/ai-tools-for-business/` | use_case | AI Tools for Business Teams in Pakistan | Yes | 18 | 38 | Workflow-Specific Informational & Tool Adopti |
| 93 | `/use-cases/ai-tools-for-creators/` | use_case | AI Tools for Creators & Freelancers in P | Yes | 24 | 38 | Workflow-Specific Informational & Tool Adopti |
| 94 | `/use-cases/ai-tools-for-developers/` | use_case | AI Tools for Developers in Pakistan | Yes | 20 | 36 | Workflow-Specific Informational & Tool Adopti |
| 95 | `/use-cases/ai-tools-for-students/` | use_case | AI Tools for Students in Pakistan | Yes | 115 | 38 | Workflow-Specific Informational & Tool Adopti |
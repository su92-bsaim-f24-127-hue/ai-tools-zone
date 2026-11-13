# Deliverable 04: Phase 2 — Category & Product Level Cross-Linking

## 1. Executive Summary & Architecture

Phase 2 established strong bidirectional internal linking between:
1. **Vertical Category Hubs** (`/categories/ai-video/`, `/categories/design/`)
2. **Audience Use-Case Hub** (`/use-cases/ai-tools-for-students/`)
3. **Specific Product Detail Pages** (`/products/chatgpt-plus/`, `/products/capcut-pro/`, `/products/leonardo-ai-essential/`, `/products/runway-ml-gen-3/`)
4. **Commercial Tool Comparisons** (`/compare/capcut-vs-runway/`, `/compare/leonardo-vs-midjourney/`)

Prior to this phase, category pages listed product cards but lacked in-text semantic citations connecting tools to specific workflows. Product pages also suffered from isolated overviews without pathways to relevant buying guides or comparison matrices.

---

## 2. Category Hub Enhancements

### 2.1 AI Video Category (`/categories/ai-video/`)
- **Target Keyword:** Cluster D (`AI video editing tools Pakistan`)
- **Key Enhancements in `data/seo-content.json`:**
  - Injected contextual links to timeline editing tools: `[CapCut Pro](/products/capcut-pro/)`.
  - Injected contextual links to generative cinematic engines: `[Veo 3 Ultra](/products/veo-3-ultra/)` and `[Runway ML Gen-3](/products/runway-ml-gen-3/)`.
  - Injected contextual link to podcast/transcript editor: `[Descript Creator](/products/descript-creator/)`.
  - Embedded direct editorial links to the comparative workflow guide: `[CapCut vs Runway comparison guide](/compare/capcut-vs-runway/)` and informational guide: `[best AI video generators guide](/blog/best-ai-video-generators-pakistan/)`.
  - In FAQ answers, established explicit recommendations for beginners vs VFX artists with links to CapCut Pro, Descript Creator, Runway ML, and Veo 3 Ultra.
  - Added related links to `/pricing/` and creator use cases.

### 2.2 Design Category (`/categories/design/`)
- **Target Keyword:** Cluster E (`AI image generator subscription Pakistan`)
- **Key Enhancements in `data/seo-content.json`:**
  - Contextually cited layout tools: `[Canva Pro Edu](/products/canva-pro-edu/)`.
  - Contextually cited generative image creation: `[Leonardo AI Essential](/products/leonardo-ai-essential/)`.
  - Contextually cited UI/UX prototyping: `[Figma Pro Private](/products/figma-pro-private/)`.
  - Contextually cited vector/photo suites: `[Adobe Creative Cloud](/products/adobe-creative-cloud/)`.
  - Embedded editorial guidance linking to `[Leonardo vs Midjourney comparison](/compare/leonardo-vs-midjourney/)`, `[Canva vs Adobe guide](/compare/canva-vs-adobe/)`, and `[best AI image generators guide](/blog/best-ai-image-generators-pakistan/)`.
  - Linked to the PKR pricing hub: `[pricing page](/pricing/)`.

---

## 3. Student Use-Case Hub Optimization (`/use-cases/ai-tools-for-students/`)

### 3.1 Search Intent & Scope
- **Target Keywords:** Cluster C (`cheap AI tools for students Pakistan`, `best AI productivity tools for students Pakistan`)
- **Catalog Integration:** Expanded the product grid from 4 basic tools to 8 comprehensive academic tools:
  - `chatgpt`, `gemini`, `quillbot`, `grammarly`, `notion`, `canva`, `coursera-plus`, `perplexity`

### 3.2 In-Content Editorial Workflow Sections
1. **Academic Study and Thesis Workflow:**
   > *"Try explaining complex course concepts with [ChatGPT Plus](/products/chatgpt-plus/) or [Gemini Pro](/products/gemini-pro/), then refine and verify academic phrasing using [QuillBot Premium](/products/quillbot-premium/) and [Grammarly Premium](/products/grammarly-premium/). For literature reviews and cited research papers, use [Perplexity Pro](/products/perplexity-pro/) to retrieve real academic sources. For university lecture organization and revision notes, structure your notes in [Notion Business](/products/notion-business/). For thesis defense presentations and visual projects, design clear slides with [Canva Pro Edu](/products/canva-pro-edu/)."*
2. **Professional Upskilling and Certification:**
   > *"Beyond daily semester coursework, Pakistani university students and career starters can build verified job skills using [Coursera Plus](/products/coursera-plus-premium/), which provides access to over 7,000 professional certificate programs from Google, IBM, and top global universities."*
3. **Faculty & Researcher Guidance:**
   > Connected directly to the informational thesis guide: `[playbook for student research and thesis writing](/blog/ai-tools-for-pakistani-students-research-thesis/)` and `[guide for teachers in Pakistan](/blog/ai-tools-for-teachers-pakistan/)`.
4. **Student Budget & Pricing Guidance:**
   > *"Balancing software costs on a student allowance requires comparing PKR prices. Explore our [PKR pricing guide](/pricing/) to find [affordable AI subscriptions](/pricing/#under-1000) under PKR 1,000 per month, including student-friendly writing tools like QuillBot (PKR 450) and Grammarly (PKR 750). Compare the complete [AI tools catalog](/products/) before ordering."*

---

## 4. Product Detail Page Enhancements (`data/product-content.json`)

### 4.1 ChatGPT Plus (`/products/chatgpt-plus/`)
- **Overview Editorial Injection:**
  - Added direct link to payment resolution guide: `[how to pay for ChatGPT Plus in Pakistan guide](/blog/how-to-pay-for-chatgpt-plus-pakistan/)`.
  - Added direct link to student use-case: `[AI tools for students playbook](/use-cases/ai-tools-for-students/)`.
  - Added link to budget catalog: `[PKR pricing catalog](/pricing/)`.
  - Injected comparison links: `[ChatGPT vs Claude](/compare/chatgpt-vs-claude/)` and `[ChatGPT vs Gemini](/compare/chatgpt-vs-gemini/)`.

### 4.2 CapCut Pro (`/products/capcut-pro/`)
- **Overview Editorial Injection:**
  - Added link to parent category: `[AI Video editing category](/categories/ai-video/)`.
  - Added link to workflow comparison: `[CapCut vs Runway](/compare/capcut-vs-runway/)`.
  - Added cross-links to companion generative video tools: `[Runway ML Gen-3](/products/runway-ml-gen-3/)` and `[Veo 3 Ultra](/products/veo-3-ultra/)`.
  - Added pricing hub anchor: `[pricing page](/pricing/)`.

### 4.3 Leonardo AI Essential (`/products/leonardo-ai-essential/`)
- **Overview Editorial Injection:**
  - Added workflow export links: `[Canva Pro](/products/canva-pro-edu/)` and `[Adobe Creative Cloud](/products/adobe-creative-cloud/)`.
  - Added category link: `[Design & AI Image tools category](/categories/design/)`.
  - Added comparison guide link: `[Leonardo vs Midjourney guide](/compare/leonardo-vs-midjourney/)`.
  - Added pricing link: `[PKR pricing page](/pricing/)`.

---

## 5. Comparison Page Upgrades

### 5.1 CapCut vs Runway (`/compare/capcut-vs-runway/`)
- **Catalog Status Reconciliation:**
  - Previously, this comparison contained a disclaimer that "AI Tools Zone currently lists a CapCut offer, but not Runway".
  - With the addition of **Runway ML Gen-3 (PKR 3,500)** to the active catalog, this section was updated to accurately reflect local availability:
    > *"AI Tools Zone now lists both [CapCut Pro](/products/capcut-pro/) for timeline editing and [Runway ML Gen-3](/products/runway-ml-gen-3/) for generative video in our [AI Video tools category](/categories/ai-video/) with local PKR pricing. Compare all plans on our [PKR pricing page](/pricing/)."*
  - Connected comparison table card directly to `/products/runway-ml-gen-3/`.
  - Added related links to `/blog/best-ai-video-generators-pakistan/` and `/pricing/`.

### 5.2 Leonardo vs Midjourney (`/compare/leonardo-vs-midjourney/`)
- Updated related links to connect directly to `/products/leonardo-ai-essential/`, `/categories/design/`, `/compare/canva-vs-adobe/`, `/blog/best-ai-image-generators-pakistan/`, and `/pricing/`.

---

## 6. Topical Equity Impact

| Destination Target | Incoming Links Before | Incoming Links After | Net Change | Qualitative Assessment |
| :--- | :---: | :---: | :---: | :--- |
| `/categories/ai-video/` | 18 | 24 | **+6** | Strong category authority with bidirectional product signals |
| `/categories/design/` | 24 | 30 | **+6** | Comprehensive design & generative image cluster hub |
| `/use-cases/ai-tools-for-students/` | 115 | 119 | **+4** | Strengthened hub connecting 8 student tools & pricing |
| `/products/chatgpt-plus/` | 36 | 39 | **+3** | Contextual links from student hub, guide, and comparison |
| `/products/capcut-pro/` | 20 | 23 | **+3** | Contextual links from AI video category & comparison |
| `/products/runway-ml-gen-3/` | 6 | 10 | **+4** | Fully integrated into video cluster & comparison guide |
| `/products/leonardo-ai-essential/` | 15 | 17 | **+2** | Connected to design category and Midjourney comparison |

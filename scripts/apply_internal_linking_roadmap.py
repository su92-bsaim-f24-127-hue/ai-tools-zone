"""
apply_internal_linking_roadmap.py
Implements the 4-phase internal linking roadmap across:
- templates/home.html & build_site.py (Homepage)
- seo_pages.py (/products/ & /pricing/ hubs, home_discovery)
- data/seo-content.json (Student use case, AI Video category, Design category, comparisons)
- data/product-content.json (ChatGPT Plus, CapCut Pro, Leonardo AI)
- data/blog-content.json (Where to Buy guide, How to Pay guide, Student Research guide)
"""

import os
import json
import re

REPO_DIR = r"C:\Users\ELITEBOOK\projects\ai-tools-zone"
SEO_CONTENT_FILE = os.path.join(REPO_DIR, "data", "seo-content.json")
PRODUCT_CONTENT_FILE = os.path.join(REPO_DIR, "data", "product-content.json")
BLOG_CONTENT_FILE = os.path.join(REPO_DIR, "data", "blog-content.json")
SEO_PAGES_FILE = os.path.join(REPO_DIR, "seo_pages.py")
BUILD_SITE_FILE = os.path.join(REPO_DIR, "build_site.py")
HOME_TEMPLATE_FILE = os.path.join(REPO_DIR, "templates", "home.html")

def update_seo_content():
    with open(SEO_CONTENT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Update Student Use-Case (/use-cases/ai-tools-for-students/)
    for page in data.get("pages", []):
        if page.get("path") == "/use-cases/ai-tools-for-students/":
            page["products"] = [
                "chatgpt", "gemini", "quillbot", "grammarly", "notion", "canva", "coursera-plus", "perplexity"
            ]
            page["sections"] = [
                [
                    "Build an academic study and thesis workflow",
                    "Try explaining complex course concepts with [ChatGPT Plus](/products/chatgpt-plus/) or [Gemini Pro](/products/gemini-pro/), then refine and verify academic phrasing using [QuillBot Premium](/products/quillbot-premium/) and [Grammarly Premium](/products/grammarly-premium/). For literature reviews and cited research papers, use [Perplexity Pro](/products/perplexity-pro/) to retrieve real academic sources. For university lecture organization and revision notes, structure your notes in [Notion Business](/products/notion-business/). For thesis defense presentations and visual projects, design clear slides with [Canva Pro Edu](/products/canva-pro-edu/)."
                ],
                [
                    "Professional upskilling and certification",
                    "Beyond daily semester coursework, Pakistani university students and career starters can build verified job skills using [Coursera Plus](/products/coursera-plus-premium/), which provides access to over 7,000 professional certificate programs from Google, IBM, and top global universities."
                ],
                [
                    "For teachers, researchers and thesis supervisors",
                    "Faculty and thesis advisors can use the same workflow to draft practice exercises or organize reading lists. Independently verify references and quotations; generated citations must always be cross-checked. Check out our dedicated [playbook for student research and thesis writing](/blog/ai-tools-for-pakistani-students-research-thesis/) and our [guide for teachers in Pakistan](/blog/ai-tools-for-teachers-pakistan/)."
                ],
                [
                    "Choose within a student budget in PKR",
                    "Balancing software costs on a student allowance requires comparing PKR prices. Explore our [PKR pricing guide](/pricing/) to find [affordable AI subscriptions](/pricing/#under-1000) under PKR 1,000 per month, including student-friendly writing tools like QuillBot (PKR 450) and Grammarly (PKR 750). Compare the complete [AI tools catalog](/products/) before ordering."
                ]
            ]
            page["related"] = [
                "/categories/ai-assistants/",
                "/pricing/",
                "/products/",
                "/blog/ai-tools-for-pakistani-students-research-thesis/",
                "/compare/grammarly-vs-quillbot-vs-wordai/",
                "/compare/chatgpt-vs-gemini/",
                "/guides/choose-ai-subscription/"
            ]

        # 2. Update CapCut vs Runway comparison
        if page.get("path") == "/compare/capcut-vs-runway/":
            page["products"] = ["capcut", "runway"]
            for comp in page.get("comparison", []):
                if comp.get("name") == "Runway":
                    comp["product"] = "runway"
            page["sections"][2] = [
                "Check rights, credits and current access in Pakistan",
                "Read the provider's current pricing and terms for export limits, model access, commercial use and credit behavior. AI Tools Zone now lists both [CapCut Pro](/products/capcut-pro/) for timeline editing and [Runway ML Gen-3](/products/runway-ml-gen-3/) for generative video in our [AI Video tools category](/categories/ai-video/) with local PKR pricing. Compare all plans on our [PKR pricing page](/pricing/)."
            ]
            page["related"] = [
                "/products/capcut-pro/",
                "/products/runway-ml-gen-3/",
                "/products/veo-3-ultra/",
                "/categories/ai-video/",
                "/compare/capcut-vs-canva/",
                "/blog/best-ai-video-generators-pakistan/",
                "/pricing/"
            ]

        # 3. Update Leonardo vs Midjourney comparison
        if page.get("path") == "/compare/leonardo-vs-midjourney/":
            page["related"] = [
                "/products/leonardo-ai-essential/",
                "/categories/design/",
                "/compare/canva-vs-adobe/",
                "/blog/best-ai-image-generators-pakistan/",
                "/use-cases/ai-tools-for-creators/",
                "/pricing/"
            ]

    # 4. Update Categories (AI Video & Design)
    for cat in data.get("categories", []):
        if cat.get("name") == "AI Video":
            cat["intro"] = [
                "Choose video tools by the stage of production you need help with. Edit short-form vertical content for TikTok, Reels, and YouTube Shorts with [CapCut Pro](/products/capcut-pro/). For cinematic AI video generation from text or image prompts, use [Veo 3 Ultra](/products/veo-3-ultra/) or [Runway ML Gen-3](/products/runway-ml-gen-3/). For text-based transcript editing and podcast audio cleanup, evaluate [Descript Creator](/products/descript-creator/).",
                "Before choosing a plan, compare features using our [CapCut vs Runway comparison guide](/compare/capcut-vs-runway/) and check our curated [best AI video generators guide](/blog/best-ai-video-generators-pakistan/). Review the seller-listed plan's export settings, watermark conditions, and duration before payment."
            ]
            cat["choose"] = "For footage you already have, start by testing your editing workflow in [CapCut Pro](/products/capcut-pro/). For generative B-roll and cinematic VFX, evaluate [Runway ML Gen-3](/products/runway-ml-gen-3/) or [Veo 3 Ultra](/products/veo-3-ultra/). Compare all listed plans and PKR pricing in our [pricing guide](/pricing/)."
            cat["faq"][0] = [
                "Which tool should I use for video editing?",
                "Start with [CapCut Pro](/products/capcut-pro/) when you need timeline editing, automated captions, and transitions for social media. For text-based audio/video editing, choose [Descript Creator](/products/descript-creator/)."
            ]
            cat["faq"][1] = [
                "Does a video generation plan replace an editor?",
                "Not necessarily. Even when generating clips with [Runway ML Gen-3](/products/runway-ml-gen-3/) or [Veo 3 Ultra](/products/veo-3-ultra/), you typically assemble clips, adjust pacing, and add sound effects in an editor like CapCut Pro."
            ]
            cat["related"] = [
                "/products/capcut-pro/",
                "/products/runway-ml-gen-3/",
                "/products/descript-creator/",
                "/products/veo-3-ultra/",
                "/compare/capcut-vs-runway/",
                "/blog/best-ai-video-generators-pakistan/",
                "/use-cases/ai-tools-for-creators/",
                "/pricing/"
            ]

        if cat.get("name") == "Design":
            cat["intro"] = [
                "Design work can mean social media templates, original generative illustrations, user interface prototypes, or multi-app creative projects. We list [Canva Pro Edu](/products/canva-pro-edu/) for layouts, [Leonardo AI Essential](/products/leonardo-ai-essential/) for custom image generation, [Figma Pro Private](/products/figma-pro-private/) for UI/UX collaboration, and [Adobe Creative Cloud](/products/adobe-creative-cloud/) for industry-standard design suites.",
                "Start with your final deliverable. Compare web-based AI image generation with Discord pipelines in our [Leonardo vs Midjourney comparison](/compare/leonardo-vs-midjourney/), or compare template tools in our [Canva vs Adobe guide](/compare/canva-vs-adobe/). Learn more in our [best AI image generators guide](/blog/best-ai-image-generators-pakistan/)."
            ]
            cat["choose"] = "Shortlist [Canva Pro](/products/canva-pro-edu/) for rapid marketing graphics, [Leonardo AI](/products/leonardo-ai-essential/) for fine-tuned asset generation, [Figma Pro](/products/figma-pro-private/) for interfaces, or [Adobe Creative Cloud](/products/adobe-creative-cloud/) for professional vector and photo editing. Compare all options on our [pricing page](/pricing/)."
            cat["related"] = [
                "/products/leonardo-ai-essential/",
                "/products/canva-pro-edu/",
                "/products/adobe-creative-cloud/",
                "/products/figma-pro-private/",
                "/compare/leonardo-vs-midjourney/",
                "/compare/canva-vs-adobe/",
                "/blog/best-ai-image-generators-pakistan/",
                "/pricing/"
            ]

    with open(SEO_CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Updated data/seo-content.json successfully.")

def update_product_content():
    with open(PRODUCT_CONTENT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ChatGPT Plus
    if "chatgpt" in data:
        data["chatgpt"]["overview"] = (
            "ChatGPT Plus provides high-priority access to OpenAI's most capable models, custom GPTs, and advanced data analysis tools. "
            "Pakistani professionals, students, and freelancers can activate their subscription domestically without international credit card declines. "
            "For detailed payment troubleshooting and official vs local alternatives, read our [how to pay for ChatGPT Plus in Pakistan guide](/blog/how-to-pay-for-chatgpt-plus-pakistan/). "
            "Students using ChatGPT for coursework should review our [AI tools for students playbook](/use-cases/ai-tools-for-students/), or explore budget options in our [PKR pricing catalog](/pricing/). "
            "You can also compare performance in [ChatGPT vs Claude](/compare/chatgpt-vs-claude/) and [ChatGPT vs Gemini](/compare/chatgpt-vs-gemini/)."
        )

    # CapCut Pro
    if "capcut" in data:
        data["capcut"]["overview"] = (
            "CapCut Pro is the essential editing suite for TikTok, YouTube Shorts, and Instagram Reels creators in Pakistan. "
            "Unlock 4K 60fps exports, automated bilingual speech-to-text subtitles, and pro aesthetic transitions. "
            "Explore our full [AI Video editing category](/categories/ai-video/) or compare editing vs generative workflows in [CapCut vs Runway](/compare/capcut-vs-runway/). "
            "To combine video editing with generative B-roll, check out [Runway ML Gen-3](/products/runway-ml-gen-3/) and [Veo 3 Ultra](/products/veo-3-ultra/), or view all video rates on our [pricing page](/pricing/)."
        )

    # Leonardo AI
    if "leonardo" in data:
        data["leonardo"]["overview"] = (
            "Leonardo AI combines versatile fine-tuned visual models with canvas editing, inpainting, and motion generation. "
            "Export your marketing graphics and character portraits into [Canva Pro](/products/canva-pro-edu/) or [Adobe Creative Cloud](/products/adobe-creative-cloud/) for final delivery. "
            "Explore our complete [Design & AI Image tools category](/categories/design/) or compare web canvas capabilities against Discord in our [Leonardo vs Midjourney guide](/compare/leonardo-vs-midjourney/). "
            "Check plan rates and access details on our [PKR pricing page](/pricing/)."
        )

    with open(PRODUCT_CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Updated data/product-content.json successfully.")

def update_blog_content():
    with open(BLOG_CONTENT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for art in data.get("articles", []):
        # 1. Where to Buy AI Tools in Pakistan
        if art.get("path") == "/blog/where-to-buy-ai-tools-pakistan/":
            art["related"] = [
                "/products/",
                "/pricing/",
                "/use-cases/ai-tools-for-students/",
                "/categories/ai-video/",
                "/categories/design/",
                "/blog/cheap-ai-subscriptions-pakistan/",
                "/guides/choose-ai-subscription/"
            ]
            sections = art.get("sections", [])
            if len(sections) > 0 and "paragraphs" in sections[0] and len(sections[0]["paragraphs"]) > 0:
                sections[0]["paragraphs"][0] += " To compare verified seller offers with transparent pricing in Pakistani Rupees, explore our [complete products catalog](/products/) and [PKR pricing guide](/pricing/)."
            if len(sections) > 2 and "paragraphs" in sections[2] and len(sections[2]["paragraphs"]) > 0:
                sections[2]["paragraphs"][0] += " Before ordering, check whether your workflow requires [AI tools for students](/use-cases/ai-tools-for-students/), [AI video editing tools](/categories/ai-video/), or [AI image generator subscriptions](/categories/design/)."

        # 2. How to Pay for ChatGPT Plus in Pakistan
        if art.get("path") == "/blog/how-to-pay-for-chatgpt-plus-pakistan/":
            art["related"] = [
                "/products/chatgpt-plus/",
                "/blog/where-to-buy-ai-tools-pakistan/",
                "/pricing/",
                "/use-cases/ai-tools-for-students/",
                "/compare/chatgpt-vs-claude/",
                "/guides/private-vs-shared-access/"
            ]
            sections = art.get("sections", [])
            if len(sections) > 2 and "paragraphs" in sections[2] and len(sections[2]["paragraphs"]) > 0:
                sections[2]["paragraphs"][0] += " View current local availability and terms on the [ChatGPT Plus product offer page](/products/chatgpt-plus/) or compare costs on our [PKR pricing page](/pricing/)."

        # 3. AI Tools for Pakistani Students
        if art.get("path") == "/blog/ai-tools-for-pakistani-students-research-thesis/":
            art["related"] = [
                "/use-cases/ai-tools-for-students/",
                "/products/quillbot-premium/",
                "/products/grammarly-premium/",
                "/products/coursera-plus-premium/",
                "/products/chatgpt-plus/",
                "/pricing/",
                "/compare/grammarly-vs-quillbot-vs-wordai/"
            ]
            sections = art.get("sections", [])
            if len(sections) > 0 and "paragraphs" in sections[0] and len(sections[0]["paragraphs"]) > 0:
                sections[0]["paragraphs"][0] += " For an overview of recommended student stacks and access guidelines, visit our [AI tools for students hub](/use-cases/ai-tools-for-students/)."

    with open(BLOG_CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Updated data/blog-content.json successfully.")

def update_seo_pages_py():
    with open(SEO_PAGES_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    # Update home_discovery()
    old_discovery = "def home_discovery():\n    return '<section class=\"answer-strip wrap\" aria-labelledby=\"buying-guides\"><h2 id=\"buying-guides\">Choose with a clearer picture.</h2><p>Compare complete plans, explore tools for your work, and understand access before you buy.</p>' + links(['/products/','/categories/','/categories/design/','/use-cases/','/use-cases/ai-tools-for-students/','/compare/','/compare/chatgpt-vs-gemini/','/compare/chatgpt-vs-claude/','/compare/canva-vs-adobe/','/compare/capcut-vs-runway/','/compare/leonardo-vs-midjourney/','/blog/free-ai-tools-pakistan/','/blog/ai-tools-for-pakistani-freelancers/','/pricing/']) + '</section>'"
    
    new_discovery = "def home_discovery():\n    return '<section class=\"answer-strip wrap\" aria-labelledby=\"buying-guides\"><h2 id=\"buying-guides\">Choose with a clearer picture.</h2><p>Compare complete plans, explore tools for your work, and understand access before you buy.</p>' + links(['/products/','/pricing/','/categories/','/categories/ai-video/','/categories/design/','/use-cases/','/use-cases/ai-tools-for-students/','/compare/','/compare/chatgpt-vs-gemini/','/compare/chatgpt-vs-claude/','/compare/canva-vs-adobe/','/compare/capcut-vs-runway/','/compare/leonardo-vs-midjourney/','/blog/where-to-buy-ai-tools-pakistan/','/blog/how-to-pay-for-chatgpt-plus-pakistan/','/blog/free-ai-tools-pakistan/','/blog/ai-tools-for-pakistani-freelancers/']) + '</section>'"

    if old_discovery in code:
        code = code.replace(old_discovery, new_discovery)
        print("Replaced home_discovery in seo_pages.py")
    else:
        print("Warning: old_discovery pattern not matched exactly.")

    # Update products hub & pricing hub content
    old_products_hub = """        if hub == 'products':
            selected=products
            content += plan_table(products)+disclaimer+'<h2>Browse by category</h2>'+links([category_path(c['name']) for c in CONTENT['categories']])
            content += '<h2>Find the right starting point</h2>'+links(['/use-cases/','/compare/','/pricing/'])"""

    new_products_hub = """        if hub == 'products':
            selected=products
            content += '<p class="lead-text">Browse our verified catalog of premium AI accounts and digital tools in Pakistan. Compare seller-listed PKR prices, subscription durations, and access types before ordering on WhatsApp. For budget breakdowns, <a href="/pricing/">compare AI subscription prices in PKR</a> across all categories. Students can explore our curated <a href="/use-cases/ai-tools-for-students/">student-friendly AI tools and thesis software</a>, video creators can browse dedicated <a href="/categories/ai-video/">AI video editing tools and generators</a>, and designers can view <a href="/categories/design/">AI image generator subscriptions and design tools</a>. Before ordering, read our comprehensive guide on <a href="/blog/where-to-buy-ai-tools-pakistan/">where to buy AI tools in Pakistan</a>.</p>'
            content += plan_table(products)+disclaimer+'<h2>Browse by category</h2>'+links([category_path(c['name']) for c in CONTENT['categories']])
            content += '<h2>Popular tool comparisons</h2>'+links(['/compare/chatgpt-vs-gemini/','/compare/chatgpt-vs-claude/','/compare/canva-vs-adobe/','/compare/capcut-vs-runway/','/compare/leonardo-vs-midjourney/'])
            content += '<h2>Find the right starting point</h2>'+links(['/use-cases/','/use-cases/ai-tools-for-students/','/compare/','/pricing/','/blog/where-to-buy-ai-tools-pakistan/'])"""

    if old_products_hub in code:
        code = code.replace(old_products_hub, new_products_hub)
        print("Replaced products hub content in seo_pages.py")
    else:
        print("Warning: old_products_hub pattern not matched exactly.")

    # Update pricing hub
    old_pricing_lead = """        elif hub == 'pricing':
            selected=products
            content += '<nav aria-label="Price ranges">'+links(['/pricing/#under-1000','/pricing/#under-2000','/pricing/#all-prices']).replace('/pricing/#under-1000</a>','Under PKR 1,000</a>').replace('/pricing/#under-2000</a>','Under PKR 2,000</a>').replace('/pricing/#all-prices</a>','All listed prices</a>')+'</nav>'"""

    new_pricing_lead = """        elif hub == 'pricing':
            selected=products
            content += '<p class="lead-text">Find affordable AI subscriptions in Pakistan with listed PKR prices and local payment methods via JazzCash, Easypaisa, or bank transfer. If you want to explore the complete catalog, visit the <a href="/products/">all tools directory</a>. Looking for academic and thesis discounts? Explore <a href="/use-cases/ai-tools-for-students/">budget-friendly AI tools for students</a>. For specialized creator workflows, check our <a href="/categories/ai-video/">AI video editing subscriptions</a> and <a href="/categories/design/">AI image generation software</a>.</p>'
            content += '<nav aria-label="Price ranges">'+links(['/pricing/#under-1000','/pricing/#under-2000','/pricing/#all-prices']).replace('/pricing/#under-1000</a>','Under PKR 1,000</a>').replace('/pricing/#under-2000</a>','Under PKR 2,000</a>').replace('/pricing/#all-prices</a>','All listed prices</a>')+'</nav>'"""

    if old_pricing_lead in code:
        code = code.replace(old_pricing_lead, new_pricing_lead)
        print("Replaced pricing hub lead in seo_pages.py")
    else:
        print("Warning: old_pricing_lead pattern not matched exactly.")

    with open(SEO_PAGES_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("Updated seo_pages.py successfully.")

def update_build_site_py():
    with open(BUILD_SITE_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    old_answer_strip = """home=home.replace('    <section id="categories"','    <section class="answer-strip wrap" aria-labelledby="about-store"><h2 id="about-store">AI subscriptions in Pakistan, with a person to help.</h2><p>AI Tools Zone is an independent digital marketplace for creators, students and businesses in Pakistan. Compare seller-listed prices in PKR, read each plan’s access type and duration, and select Order on WhatsApp to discuss your order on WhatsApp. Availability and plan limits are confirmed before payment.</p><a class="inline-link" href="about/">About AI Tools Zone & contact ↗</a></section>\\n    <section id="categories"')"""

    new_answer_strip = """home=home.replace('    <section id="categories"','    <section class="answer-strip wrap" aria-labelledby="about-store"><h2 id="about-store">AI subscriptions in Pakistan, with a person to help.</h2><p>AI Tools Zone is an independent digital marketplace for creators, students and businesses in Pakistan. Whether you need <a href="products/">premium AI accounts in Pakistan</a> for engineering, <a href="pricing/">affordable AI subscriptions</a> for startups, <a href="use-cases/ai-tools-for-students/">AI tools for students</a> and academic research, <a href="categories/ai-video/">AI video editing tools</a>, or <a href="categories/design/">AI image generation tools</a>, compare seller-listed prices in PKR, read each plan’s access type and duration, and select Order on WhatsApp to discuss your order on WhatsApp. Availability and plan limits are confirmed before payment. Read our guide on <a href="blog/where-to-buy-ai-tools-pakistan/">where to buy AI tools in Pakistan</a>.</p><a class="inline-link" href="about/">About AI Tools Zone & contact ↗</a></section>\\n    <section id="categories"')"""

    if old_answer_strip in code:
        code = code.replace(old_answer_strip, new_answer_strip)
        print("Replaced answer strip in build_site.py")
    else:
        print("Warning: old_answer_strip pattern not matched exactly.")

    with open(BUILD_SITE_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print("Updated build_site.py successfully.")

def main():
    update_seo_content()
    update_product_content()
    update_blog_content()
    update_seo_pages_py()
    update_build_site_py()
    print("All internal linking updates staged successfully.")

if __name__ == "__main__":
    main()

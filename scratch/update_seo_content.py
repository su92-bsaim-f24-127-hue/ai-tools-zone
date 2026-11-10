import json
from pathlib import Path

path = Path('data/seo-content.json')
data = json.loads(path.read_text(encoding='utf-8'))

# 1. Update canva-vs-adobe
for p in data['pages']:
    if p['path'] == '/compare/canva-vs-adobe/':
        p['comparison'] = [
            {
                "name": "Canva Pro Edu",
                "officialUrl": "https://www.canva.com/pricing/",
                "product": "canva",
                "test": "Create a multi-slide Instagram carousel or presentation and test 1-click Magic Studio background removal and brand kit export."
            },
            {
                "name": "Adobe Creative Cloud",
                "officialUrl": "https://www.adobe.com/creativecloud.html",
                "product": "adobe",
                "test": "Open complex vector artwork in Illustrator or edit 4K timeline footage in Premiere Pro with Adobe Firefly generative fill."
            }
        ]
        p['related'] = [
            "/categories/design/",
            "/alternatives/canva/",
            "/use-cases/ai-tools-for-creators/",
            "/compare/leonardo-vs-midjourney/",
            "/blog/canva-pro-vs-adobe-creative-cloud-pakistan-freelancers/"
        ]

# 2. Add /compare/leonardo-vs-midjourney/
leonardo_page = {
    "path": "/compare/leonardo-vs-midjourney/",
    "type": "compare",
    "title": "Leonardo AI vs Midjourney: Image Generator Workflow & PKR Plans",
    "description": "Compare Leonardo AI and Midjourney for Pakistani designers and creators. Review web canvas vs Discord interface, fine-tuned models, and listed PKR plans.",
    "answer": "Leonardo AI and Midjourney represent two distinct image generation workflows. In this catalog, Leonardo AI is listed with transparent PKR pricing and private access, while Midjourney operates via Discord with USD subscription tiers. Compare prompt control, canvas editing, and local payment convenience before deciding.",
    "products": [
        "leonardo"
    ],
    "comparison": [
        {
            "name": "Leonardo AI Essential",
            "officialUrl": "https://leonardo.ai/pricing/",
            "product": "leonardo",
            "test": "Generate game assets or commercial marketing graphics using the Phoenix model with Alchemy upscaler, negative prompts, and transparent PNG export."
        },
        {
            "name": "Midjourney v6",
            "officialUrl": "https://www.midjourney.com/",
            "test": "Prompt cinematic portrait photography inside Discord; test aesthetic quality, style referencing, and regional card payment acceptance."
        }
    ],
    "sections": [
        [
            "Web Canvas Studio vs Discord Interface",
            "Leonardo AI provides a comprehensive web application with visual canvas editing, real-time generation, layer controls, and fine-tuned community models. Midjourney generates imagery through Discord commands or its web portal. Creators who prefer point-and-click image manipulation and in-painting often prefer Leonardo's interface, while those seeking raw cinematic realism explore Midjourney."
        ],
        [
            "Prompt Controls, Negative Prompts and Custom Models",
            "Leonardo AI allows direct control over dimensions, guidance scale, negative prompting, and custom LoRA models. Midjourney uses text parameter flags (--ar, --s, --stylize). For production consistency in e-commerce, logos, and UI illustration, fine-tuned controls provide repeatable results."
        ],
        [
            "Payment and Access in Pakistan",
            "Subscribing to international AI services directly can result in credit card declines due to Pakistani banking forex restrictions. AI Tools Zone lists Leonardo AI Essential with flat PKR pricing and instant WhatsApp activation via JazzCash, EasyPaisa, or local bank transfer. Midjourney is not currently listed in our local catalog and requires an international payment method."
        ]
    ],
    "faq": [
        [
            "Which tool is easier for beginners in Pakistan?",
            "Leonardo AI is generally easier for beginners because of its straightforward web interface, pre-set style presets, and transparent PKR payment without needing Discord setup."
        ],
        [
            "Does AI Tools Zone list Midjourney?",
            "Midjourney is not currently listed in the AI Tools Zone catalog. We provide this comparison to help creators understand workflow differences between web-based generation and Discord-based tools."
        ],
        [
            "Can I use Leonardo AI generated images commercially?",
            "Paid plans on Leonardo AI generally include commercial rights for generated images. Confirm the exact licensing and current usage terms on the official Leonardo.ai website before using outputs in client work."
        ]
    ],
    "related": [
        "/products/leonardo-ai-essential/",
        "/categories/design/",
        "/blog/best-ai-image-generators-pakistan/",
        "/use-cases/ai-tools-for-creators/",
        "/compare/canva-vs-adobe/"
    ],
    "sources": [
        [
            "Leonardo.ai pricing and features",
            "https://leonardo.ai/pricing/"
        ],
        [
            "Midjourney documentation",
            "https://docs.midjourney.com/"
        ]
    ]
}

# Check if leonardo-vs-midjourney already in pages
if not any(p['path'] == leonardo_page['path'] for p in data['pages']):
    data['pages'].append(leonardo_page)

# 3. Enhance internal cross-links for other low-link comparison pages
for p in data['pages']:
    if p['path'] == '/compare/claude-vs-gemini/':
        p['related'] = [
            "/compare/chatgpt-vs-claude/",
            "/compare/chatgpt-vs-gemini/",
            "/categories/ai-assistants/",
            "/products/gemini-pro/",
            "/use-cases/ai-tools-for-students/"
        ]
    elif p['path'] == '/compare/elevenlabs-vs-playht/':
        p['related'] = [
            "/products/elevenlabs/",
            "/categories/ai-voice/",
            "/compare/capcut-vs-runway/",
            "/use-cases/ai-tools-for-creators/",
            "/blog/faceless-youtube-automation-ai-tools-pakistan/"
        ]
    elif p['path'] == '/compare/grammarly-vs-quillbot-vs-wordai/':
        p['related'] = [
            "/use-cases/ai-tools-for-students/",
            "/categories/productivity/",
            "/blog/ai-tools-for-pakistani-students-research-thesis/",
            "/blog/ai-tools-for-teachers-pakistan/",
            "/compare/helium10-vs-semrush-vs-vidiq/"
        ]
    elif p['path'] == '/compare/helium10-vs-semrush-vs-vidiq/':
        p['related'] = [
            "/categories/software/",
            "/products/n8n-starter/",
            "/blog/how-to-earn-money-with-ai-pakistan/",
            "/compare/grammarly-vs-quillbot-vs-wordai/",
            "/blog/faceless-youtube-automation-ai-tools-pakistan/"
        ]
    elif p['path'] == '/compare/chatgpt-vs-claude/':
        p['related'] = [
            "/compare/chatgpt-vs-gemini/",
            "/compare/claude-vs-gemini/",
            "/products/chatgpt-plus/",
            "/guides/choose-ai-subscription/",
            "/use-cases/ai-tools-for-students/"
        ]
    elif p['path'] == '/compare/capcut-vs-runway/':
        p['related'] = [
            "/compare/capcut-vs-canva/",
            "/products/capcut-pro/",
            "/products/veo-3-ultra/",
            "/categories/ai-video/",
            "/use-cases/ai-tools-for-creators/",
            "/blog/faceless-youtube-automation-ai-tools-pakistan/"
        ]

path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('Updated data/seo-content.json successfully. Total pages in seo-content:', len(data['pages']))

"""Structured FAQ content for the dedicated /faq/ hub on AI Tools Zone."""

CATEGORIES = [
    {
        "id": "ordering",
        "title": "A. Ordering and Purchasing",
        "intro": "How orders work on AI Tools Zone, from catalog selection to WhatsApp confirmation.",
        "faqs": [
            (
                "How do I place an order for an AI subscription on AI Tools Zone?",
                'To place an order, browse our <a href="/products/">catalog of 20 digital tools</a>, select the tool you need, and click <strong>Order on WhatsApp</strong>. Your WhatsApp app opens automatically with a pre-formatted message detailing the product name, listed PKR price, duration, and access type. You review and send the message to our support line at <a href="https://wa.me/923430173923">+92 343 0173923</a>. Our team confirms current stock availability, payment details, and fulfillment steps before any payment is transferred. Read our <a href="/terms/">ordering guide and terms</a> for full process details.'
            ),
            (
                "Is ordering done through an online shopping cart or directly on WhatsApp?",
                "AI Tools Zone operates with direct human WhatsApp ordering rather than an automated shopping cart checkout. Because international subscription entitlements, team seat availability, and server quotas change frequently, a real person confirms that the exact plan meets your technical requirements before collecting payment. No credit card information is entered on this website."
            ),
            (
                "What details should I confirm with support before making a payment?",
                'Before transferring funds, always ask our WhatsApp agent to confirm four key points: 1) Current account availability and stock status; 2) The exact access type (<a href="/guides/private-vs-shared-access/">Private, Shared, Invitation, or License Key</a>); 3) Plan allowances (such as character limits on <a href="/products/elevenlabs/">ElevenLabs</a> or message quotas on <a href="/products/chatgpt-plus/">ChatGPT Plus</a>); and 4) The applicable replacement warranty period (typically 7 or 30 days).'
            ),
            (
                "Can I customize or bundle multiple subscriptions in a single order?",
                'Yes. Many Pakistani content creators, students, and agencies combine tools into custom stacks (for example, pairing <a href="/products/chatgpt-plus/">ChatGPT Plus</a>, <a href="/products/elevenlabs/">ElevenLabs</a>, and <a href="/products/capcut-pro/">CapCut Pro</a> for YouTube automation, or <a href="/products/canva-pro-edu/">Canva Pro</a> and <a href="/products/leonardo-ai-essential/">Leonardo AI</a> for graphic design). Mention your desired stack on WhatsApp, and our team will provide a consolidated PKR quote and single payment transfer instructions.'
            )
        ]
    },
    {
        "id": "payment",
        "title": "B. Pakistani Payment Methods",
        "intro": "Transparent PKR pricing without international forex taxes or credit card barriers.",
        "faqs": [
            (
                "Which local Pakistani payment methods are accepted?",
                'We accept standard Pakistani mobile wallets and interbank electronic fund transfers: <strong>JazzCash</strong> direct mobile transfer, <strong>Easypaisa</strong> direct mobile transfer, and <strong>Bank Transfer (IBFT / Raast)</strong> from any Pakistani banking app (HBL, Meezan Bank, Bank Alfalah, Standard Chartered, UBL, MCB, Faysal Bank, etc.), as well as <strong>SadaPay</strong> and <strong>NayaPay</strong>. All payment instructions are shared 1-on-1 on WhatsApp after confirming order availability. See our <a href="/blog/jazzcash-easypaisa-ai-tools-pakistan/">guide to paying for AI tools with JazzCash and Easypaisa</a>.'
            ),
            (
                "Why do local Pakistani debit cards get declined on official AI platforms?",
                'Most Pakistani commercial bank cards decline international software subscriptions (such as OpenAI, Adobe, Midjourney, or Claude) due to State Bank of Pakistan (SBP) foreign exchange regulations, mandatory 3D-Secure OTP mismatches on recurring subscriptions, international transaction withholding taxes (often adding 10%–16% extra charges), or default international eCommerce restrictions on standard debit cards. AI Tools Zone solves this payment friction by accepting domestic PKR payments without international card requirements. Read our <a href="/blog/how-to-pay-for-chatgpt-plus-pakistan/">ChatGPT Plus Pakistan payment guide</a>.'
            ),
            (
                "Can I pay using SadaPay or NayaPay?",
                'Yes. SadaPay and NayaPay users can transfer funds seamlessly using Raast instant transfer or regular IBFT directly to our designated business bank account. Simply inform our representative on WhatsApp that you prefer SadaPay or NayaPay, and we will send the matching Raast ID or IBFT account number. Browse our <a href="/pricing/">PKR pricing directory</a>.'
            ),
            (
                "Are there any hidden conversion fees, sales taxes, or service charges?",
                'No. All prices listed on our <a href="/pricing/">PKR pricing page</a> and individual product cards are transparent and flat. You pay the exact amount confirmed in your WhatsApp chat in Pakistani Rupees (PKR), with zero foreign currency conversion fees, bank withholding taxes, or unexpected recurring subscription rebills. Read our <a href="/terms/">ordering policies</a>.'
            )
        ]
    },
    {
        "id": "activation",
        "title": "C. Subscription Activation",
        "intro": "What to expect once your payment is verified and confirmed.",
        "faqs": [
            (
                "How does subscription activation work after payment is confirmed?",
                'Activation depends on the specific access category defined in our <a href="/products/">catalog</a>: For <strong>Private Accounts</strong>, dedicated login credentials (email and password) are sent directly to your WhatsApp. For <strong>Workspace Invitations</strong>, an official team invite link is sent to your personal email address. For <strong>Shared Profiles</strong>, login credentials and your designated profile name/PIN are delivered. For <strong>License Keys</strong>, a genuine 25-character digital product key is delivered with step-by-step instructions (e.g., <a href="/products/windows-11-pro-key/">Windows 11 Pro</a>).'
            ),
            (
                "Do I need to share my personal email password to get access?",
                '<strong>Never.</strong> AI Tools Zone will <strong>never</strong> ask for your personal email password, bank PINs, or confidential security credentials. For invitation plans (such as <a href="/products/canva-pro-edu/">Canva Pro Edu</a> or <a href="/products/notion-business/">Notion Business</a>), you provide only your email address to receive the official invitation link. Read our <a href="/privacy/">privacy policy</a> for full security commitments.'
            ),
            (
                "Can activation be completed on my existing email address?",
                'Yes, for all invitation-based subscriptions. Products like <a href="/products/canva-pro-edu/">Canva Pro Edu</a>, <a href="/products/notion-business/">Notion Business</a>, and <a href="/products/youtube-premium/">YouTube Premium</a> attach directly to your existing personal account. Your existing documents, private designs, bookmarks, and watch history remain intact.'
            ),
            (
                "What should I do if an activation link expires or shows an error?",
                'Invitation links typically remain valid for 24–48 hours. If a link expires or displays a browser region error, send a screenshot to our WhatsApp customer support team at <a href="https://wa.me/923430173923">+92 343 0173923</a>. Our agents verify your order reference and generate a fresh replacement invitation link promptly. Full support details are in our <a href="/terms/">ordering terms</a>.'
            )
        ]
    },
    {
        "id": "access-types",
        "title": "D. Account Access and Security",
        "intro": "Understanding Private, Shared, Invitation, and License Key subscriptions.",
        "faqs": [
            (
                "What is the difference between Private, Shared, and Invitation access?",
                '<strong>Private</strong> means you receive dedicated account credentials used exclusively by you. <strong>Invitation</strong> means an official invite is sent to your email to join a managed workspace while keeping your own password. <strong>Shared</strong> means multiple verified users share access to a single master account with dedicated profiles (like <a href="/products/netflix-premium-4k/">Netflix Premium 4K</a> or <a href="/products/surfshark-vpn/">Surfshark VPN</a>). Review our detailed <a href="/guides/private-vs-shared-access/">Private vs Shared Access Guide</a> before purchasing.'
            ),
            (
                "Can other users see my private documents, chats, or projects on a Shared plan?",
                'On shared accounts with individual user profiles (like streaming or VPN services), profiles are distinct. However, for AI chat assistants (<a href="/products/chatgpt-plus/">ChatGPT Plus</a> or <a href="/products/gemini-pro/">Gemini Pro</a>), AI Tools Zone lists <strong>Private</strong> access so that your prompt history, uploaded PDF files, and client deliverables remain strictly private to you.'
            ),
            (
                "How can I avoid account lockouts or bans on shared subscriptions?",
                'To ensure uninterrupted service on shared plans: 1) Never change the master account email, password, or billing settings; 2) Only stream or log in on your assigned screen/profile; 3) Avoid logging into an excessive number of simultaneous devices. Learn more in our guide on <a href="/blog/avoiding-account-bans-shared-ai-tools-pakistan/">avoiding account bans on shared digital subscriptions</a>.'
            ),
            (
                "Does AI Tools Zone support two-factor authentication (2FA)?",
                'On dedicated <strong>Private</strong> subscriptions (such as private developer or design accounts), you can enable your own authenticator app (Google Authenticator, Microsoft Authenticator) or security keys to secure your login credentials completely.'
            )
        ]
    },
    {
        "id": "delivery",
        "title": "E. Delivery Times",
        "intro": "Fulfillment estimates across our 20 active digital products.",
        "faqs": [
            (
                "How long does delivery take after payment confirmation?",
                'The estimated delivery time is listed on every product page: <strong>Fast Track (15–30 minutes)</strong> for <a href="/products/chatgpt-plus/">ChatGPT Plus</a>, <a href="/products/gemini-pro/">Gemini Pro</a>, <a href="/products/canva-pro-edu/">Canva Pro</a>, <a href="/products/capcut-pro/">CapCut Pro</a>, <a href="/products/nordvpn/">NordVPN</a>, <a href="/products/surfshark-vpn/">Surfshark</a>, <a href="/products/netflix-premium-4k/">Netflix 4K</a>, <a href="/products/youtube-premium/">YouTube Premium</a>, and <a href="/products/windows-11-pro-key/">Windows 11 Pro</a>; <strong>Standard (30–60 minutes)</strong> for <a href="/products/leonardo-ai-essential/">Leonardo AI</a>, <a href="/products/elevenlabs/">ElevenLabs</a>, <a href="/products/lovable-pro/">Lovable Pro</a>, <a href="/products/replit-core/">Replit Core</a>, <a href="/products/notion-business/">Notion Business</a>, and <a href="/products/linkedin-premium/">LinkedIn Premium</a>; and <strong>Specialized (1–2 hours)</strong> for <a href="/products/adobe-creative-cloud/">Adobe Creative Cloud</a>, <a href="/products/figma-pro-private/">Figma Pro</a>, <a href="/products/gamma-pro/">Gamma Pro</a>, and <a href="/products/n8n-starter/">n8n Starter</a>.'
            ),
            (
                "What happens if delivery is delayed beyond the estimated timeframe?",
                'Delivery depends on vendor server provisioning queues and current stock availability. If your delivery exceeds the estimated window, our WhatsApp team will message you with an updated timeline. If a requested plan cannot be activated due to unexpected stock exhaustion, you are entitled to an immediate 100% full refund with zero deductions. Full details are in our <a href="/terms/">terms</a>.'
            ),
            (
                "Are digital orders fulfilled 24/7 or during specific business hours?",
                'Our WhatsApp customer support and fulfillment desk is actively staffed daily between <strong>9:00 AM and 11:00 PM PKT (Pakistan Standard Time)</strong>. Orders submitted outside active hours are queued and fulfilled first thing the following morning. Check our <a href="/about/">about page</a> for operating information.'
            )
        ]
    },
    {
        "id": "warranty",
        "title": "F. Replacement Warranties",
        "intro": "Clear warranty coverage, replacement terms, and claim guidelines.",
        "faqs": [
            (
                "What does the replacement warranty cover?",
                'The replacement warranty protects you against subscription revocation, account lockouts, or plan downtime that occurs within the specified warranty period. If an account stops functioning properly, our team troubleshoots the issue or provisions a brand-new replacement account free of charge. Full terms are detailed on our <a href="/terms/">ordering and warranty page</a>.'
            ),
            (
                "Which products come with a 30-day replacement warranty?",
                'The following subscriptions in our catalog carry a full <strong>30-Day Replacement Warranty</strong>: <a href="/products/canva-pro-edu/">Canva Pro Edu (1 Year)</a>, <a href="/products/figma-pro-private/">Figma Pro Private (2 Years)</a>, <a href="/products/gamma-pro/">Gamma Pro (1 Year)</a>, <a href="/products/n8n-starter/">n8n Starter (1 Year)</a>, <a href="/products/notion-business/">Notion Business (3 Months)</a>, and <a href="/products/youtube-premium/">YouTube Premium (3 Months)</a>.'
            ),
            (
                "Why is Gemini Pro listed with No Warranty?",
                'Our 1-year <a href="/products/gemini-pro/">Gemini Pro</a> subscription is offered at an exceptionally low rate (PKR 2,000 for 12 months) and is marked with <strong>No Warranty</strong> (replacement warranty not applicable). Account credentials and full model access are verified and confirmed functional upon delivery. Once delivered and confirmed, long-term replacements are not provided for this specific listing.'
            ),
            (
                "How do I claim a replacement if my account stops working?",
                'To claim a replacement within your active warranty window: 1) Open your existing WhatsApp order chat with AI Tools Zone; 2) Send a screenshot of the error message or login prompt; 3) Provide your original order reference. Our support desk verifies the report and provides a resolved login or replacement within our standard delivery window.'
            )
        ]
    },
    {
        "id": "refunds",
        "title": "G. Refund and Cancellation Policies",
        "intro": "When refunds apply, how cancellations work, and order exchanges.",
        "faqs": [
            (
                "Can I get a full refund if my subscription cannot be delivered?",
                'Yes. If an ordered tool is temporarily unavailable, out of stock, or cannot be successfully activated on your device, you can request an immediate 100% full refund. Refunds are transferred back directly via JazzCash, Easypaisa, or Raast bank transfer. Read our <a href="/terms/">terms of service</a>.'
            ),
            (
                "Are refunds available after an account has been successfully delivered and verified?",
                'Because digital credentials, workspace invitations, and software product keys are intangible digital assets that cannot be returned once revealed, fulfilled orders are non-refundable after successful activation. All delivered accounts are covered by the stated replacement warranty rather than monetary refunds. Review our <a href="/terms/">ordering policies</a> before payment.'
            ),
            (
                "What should I do if I ordered the wrong product by mistake?",
                'If you realize you selected the wrong subscription, contact our WhatsApp agent immediately before credentials or invitations are issued. We can swap your order to the correct tool (adjusting any price difference). If access credentials have already been generated and dispatched, the order cannot be swapped.'
            )
        ]
    },
    {
        "id": "compatibility",
        "title": "H. Product Compatibility and Technical Requirements",
        "intro": "Device support, Pakistani ISP behavior, and native desktop app details.",
        "faqs": [
            (
                "Do these AI tools work on Windows, Mac, Android, and iOS?",
                'Yes. Cloud-based AI tools (such as <a href="/products/chatgpt-plus/">ChatGPT Plus</a>, <a href="/products/gemini-pro/">Gemini Pro</a>, <a href="/products/canva-pro-edu/">Canva Pro</a>, <a href="/products/gamma-pro/">Gamma Pro</a>, <a href="/products/notion-business/">Notion Business</a>, and <a href="/products/lovable-pro/">Lovable Pro</a>) operate on any modern web browser across Windows, macOS, Linux, ChromeOS, iOS, and Android. Most also feature dedicated mobile apps in Google Play Store and Apple App Store.'
            ),
            (
                "Do I need a VPN to access AI tools in Pakistan?",
                'Most tools listed on AI Tools Zone—including ChatGPT, Gemini, Canva, CapCut, and Replit—connect directly across standard Pakistani internet service providers without requiring a VPN. A VPN is only required for tools with regional geoblocking (such as Claude Pro or specific streaming platforms). For privacy on public Wi-Fi, explore our <a href="/products/nordvpn/">NordVPN</a> and <a href="/products/surfshark-vpn/">Surfshark</a> options in the <a href="/categories/vpn-security/">VPN & Security category</a>.'
            ),
            (
                "Does CapCut Pro work on PC without an emulator in Pakistan?",
                'Yes. Our <a href="/products/capcut-pro/">CapCut Pro</a> subscription activates directly inside the official CapCut desktop application for Windows and macOS. You do not need BlueStacks or any third-party Android emulator. You get native multi-track timeline editing, 4K 60fps export, and pro transitions directly on your PC.'
            ),
            (
                "Can the Windows 11 Pro product key be used on a clean install?",
                'Yes. The genuine digital product key for <a href="/products/windows-11-pro-key/">Windows 11 Pro</a> can be used during a clean installation from official Microsoft USB installation media, or entered directly into Windows Settings (<em>Settings &gt; System &gt; Activation &gt; Change Product Key</em>) to upgrade an existing Windows 11 Home installation without formatting your drive.'
            )
        ]
    },
    {
        "id": "support",
        "title": "I. Customer Support",
        "intro": "Direct human assistance on WhatsApp, resolution procedures, and scope.",
        "faqs": [
            (
                "How can I contact human customer support at AI Tools Zone?",
                'You can speak directly with a human customer support specialist on WhatsApp at <a href="https://wa.me/923430173923"><strong>+92 343 0173923</strong></a>. We do not use automated chatbot loops that prevent you from reaching real assistance. You can ask technical questions, confirm plan limits, request renewal quotes, or resolve warranty claims directly. Visit our <a href="/about/">about and contact page</a> for details.'
            ),
            (
                "What information should I provide when asking for support on an existing order?",
                'To expedite support, please provide: 1) The phone number used to place the original order; 2) The product name and purchase date; and 3) A clear screenshot of the error screen or account issue. Having these details ready allows our team to look up your order record and resolve issues rapidly.'
            ),
            (
                "Does AI Tools Zone provide custom bot development or AI consulting?",
                'No. AI Tools Zone is strictly a software and digital subscription marketplace. We do not provide custom software development, WhatsApp bot coding, or consulting services. For developers building their own automation infrastructure, we recommend our <a href="/products/n8n-starter/">n8n Starter</a>, <a href="/products/lovable-pro/">Lovable Pro</a>, and <a href="/products/replit-core/">Replit Core</a> subscriptions.'
            )
        ]
    },
    {
        "id": "choosing",
        "title": "J. Choosing the Right AI Tool",
        "intro": "Practical tool selection advice for students, creators, developers, and businesses.",
        "faqs": [
            (
                "How do I choose between ChatGPT Plus, Gemini Pro, and specialized tools?",
                'For complex logic, coding, mathematical reasoning, and data analysis, choose <a href="/products/chatgpt-plus/">ChatGPT Plus</a> (read our <a href="/compare/chatgpt-vs-claude/">ChatGPT vs Claude comparison</a>). For ingesting huge academic papers, long textbooks, and 1M+ token research, choose <a href="/products/gemini-pro/">Gemini Pro</a> (read our <a href="/compare/chatgpt-vs-gemini/">ChatGPT vs Gemini comparison</a>). For rapid social media marketing graphics, choose <a href="/products/canva-pro-edu/">Canva Pro Edu</a> (read <a href="/compare/canva-vs-adobe/">Canva vs Adobe</a>). For video creators and TikTok/YouTube Shorts editing, choose <a href="/products/capcut-pro/">CapCut Pro</a> (read <a href="/compare/capcut-vs-runway/">CapCut vs Runway</a>). Browse our targeted guides for <a href="/use-cases/ai-tools-for-students/">Students</a>, <a href="/use-cases/ai-tools-for-creators/">Creators</a>, <a href="/use-cases/ai-tools-for-developers/">Developers</a>, and <a href="/use-cases/ai-tools-for-business/">Businesses</a>.'
            )
        ]
    }
]

def build_faq_html():
    """Generate accessible, crawlable semantic HTML for the /faq/ hub."""
    nav_links = "".join(f'<a href="#{c["id"]}">{c["title"].split(". ")[1]}</a>' for c in CATEGORIES)
    category_nav = f'<nav class="faq-category-nav" aria-label="FAQ Category Navigation">{nav_links}</nav>'
    
    sections = []
    for cat in CATEGORIES:
        faq_items = []
        for q, a in cat["faqs"]:
            faq_items.append(
                f'<details class="faq-accordion">'
                f'<summary class="faq-summary"><h3>{q}</h3><span class="faq-icon" aria-hidden="true">+</span></summary>'
                f'<div class="faq-body"><p>{a}</p></div>'
                f'</details>'
            )
        sections.append(
            f'<section class="content-block" id="{cat["id"]}">'
            f'<h2>{cat["title"]}</h2>'
            f'<p>{cat["intro"]}</p>'
            f'<div class="faq-list">{"".join(faq_items)}</div>'
            f'</section>'
        )
    
    help_strip = (
        '<section class="content-block help-strip">'
        '<h2>Still have a question?</h2>'
        '<p>Our human customer support team is available on WhatsApp daily from 9:00 AM to 11:00 PM PKT. '
        'Contact us directly to confirm stock availability, ask technical questions, or get advice on selecting the right subscription.</p>'
        '<p><a class="button button-lime" href="https://wa.me/923430173923" target="_blank" rel="noopener noreferrer">Ask on WhatsApp ↗</a> '
        '<a class="button button-outline" href="/products/">Explore all 20 tools</a></p>'
        '</section>'
    )
    
    resource_links = (
        '<section class="content-block">'
        '<h2>Explore more resources</h2>'
        '<ul class="reading-links">'
        '<li><a href="/pricing/">AI Tools Pricing in Pakistan: Compare PKR Plans</a></li>'
        '<li><a href="/guides/private-vs-shared-access/">Private vs Shared vs Invitation Access Guide</a></li>'
        '<li><a href="/guides/choose-ai-subscription/">How to Choose an AI Subscription Checklist</a></li>'
        '<li><a href="/terms/">Ordering, Access &amp; Replacement Warranty Terms</a></li>'
        '<li><a href="/about/">About AI Tools Zone &amp; Customer Support</a></li>'
        '</ul>'
        '</section>'
    )
    
    lead_paragraph = (
        '<p class="direct-answer">Clear answers to common questions about buying AI tools and digital subscriptions in Pakistan. '
        'Learn about Pakistani payment methods (JazzCash, Easypaisa, Raast), instant subscription activation, replacement warranties, '
        'account security, and practical advice on choosing the right tools for your work.</p>'
    )
    
    return lead_paragraph + category_nav + "".join(sections) + help_strip + resource_links

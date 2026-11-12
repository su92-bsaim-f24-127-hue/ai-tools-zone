#!/usr/bin/env python3
"""
Apply Phase 4.1.2 Commercial Copy Corrections
AI Tools Zone - Controlled Feature-Branch Corrections
"""

import json
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parent.parent
    content_file = repo_root / 'data' / 'product-content.json'
    content = json.loads(content_file.read_text(encoding='utf-8'))
    
    # 1. chatgpt
    c = content.get('chatgpt', {})
    c['meta_description'] = "Subscribe to ChatGPT Plus in Pakistan without credit card. Pay in PKR via JazzCash or EasyPaisa. Fast 15–30 min setup via WhatsApp upon payment verification."
    if 'benefits' in c and len(c['benefits']) > 0:
        c['benefits'][0] = "Overcome international card decline blocks with local JazzCash, Easypaisa, or direct bank transfer."
        
    # 2. canva
    c = content.get('canva', {})
    c['meta_description'] = "Get Canva Pro access in Pakistan with 100M+ assets, brand kits & background remover. Pay via JazzCash or EasyPaisa. Fast 15–30 minute setup via WhatsApp."
    if 'benefits' in c and len(c['benefits']) > 2:
        c['benefits'][2] = "Fast 15–30 minute WhatsApp workspace invitation upon payment verification with a 30-day replacement warranty."
    if 'faqs' in c and len(c['faqs']) > 0:
        c['faqs'][0]['a'] = "We send an official team workspace invitation link to your email. You log in to your existing Canva account, accept the invite, and your account unlocks Pro features upon accepting the workspace invitation."

    # 3. windows
    c = content.get('windows', {})
    c['headline'] = "Windows 11 Pro Retail Product Key in Pakistan"
    c['meta_description'] = "Buy Windows 11 Pro retail product key in Pakistan. Lifetime online activation on 1 PC. Fast 15–30 minute setup via WhatsApp upon payment verification."
    c['seo_intro'] = "Buy an authentic Windows 11 Pro retail product key in Pakistan with permanent online activation for 1 PC. Unlocks BitLocker encryption and direct Microsoft updates in PKR."
    c['overview'] = "An authentic Windows 11 Pro retail key protects your computer against security vulnerabilities introduced by cracked KMS tools. Equip your clean workstation with [Notion Business](/products/notion-business/) or browse our [Software category](/categories/software/)."
    c['why_buy_local'] = "Receive an authentic retail digital activation key delivered within 15–30 minutes via WhatsApp upon payment verification with step-by-step guidance in PKR."
    if 'benefits' in c and len(c['benefits']) > 2:
        c['benefits'][2] = "Fast 15–30 minute WhatsApp delivery of your digital license key upon payment verification with a 30-day replacement warranty."
    if 'faqs' in c and len(c['faqs']) > 0:
        c['faqs'][0]['q'] = "Is this Windows 11 Pro license key permanent and authentic?"
        c['faqs'][0]['a'] = "Yes. This 25-character digital retail product key provides permanent online activation for 1 PC via Microsoft activation servers. AI Tools Zone is an independent software reseller and is not an authorized OEM partner or direct affiliate of Microsoft Corporation."

    # 4. netflix
    c = content.get('netflix', {})
    c['headline'] = "Netflix Premium 4K Profile Screen in Pakistan"
    c['meta_description'] = "Dedicated private profile screen with personal PIN on a shared 4K UHD family plan. Pay in PKR via JazzCash or EasyPaisa. Fast 15–30 minute WhatsApp setup."
    c['why_buy_local'] = "Dedicated private profile screen with a personal PIN on a shared 4K UHD family plan. Supported via WhatsApp in PKR with household verification guidance."
    if 'benefits' in c and len(c['benefits']) > 2:
        c['benefits'][2] = "Fast 15–30 minute WhatsApp delivery upon payment verification with 7-day replacement warranty."
    if 'faqs' in c:
        if len(c['faqs']) > 0:
            c['faqs'][0]['a'] = "Yes. You are assigned a dedicated private profile screen with a personal PIN on a shared 4K UHD family plan. You set your own 4-digit Profile Lock PIN in Netflix Account Settings."
        if len(c['faqs']) > 1:
            c['faqs'][1]['a'] = "This listing is strictly for 1 private profile screen on a shared 4K family account. It does not provide an individually owned or exclusive master account."
        if len(c['faqs']) > 5:
            c['faqs'][5]['a'] = "Changing account passwords or billing details on a shared subscription violates terms and disrupts access for all screen profiles, voiding your replacement warranty. Access your assigned private profile PIN only."

    # 5. adobe
    c = content.get('adobe', {})
    c['headline'] = "Adobe Creative Cloud All Apps Subscription in Pakistan"
    c['meta_description'] = "Authentic Adobe Creative Cloud in Pakistan. 20+ apps including Photoshop, Illustrator & Premiere. Pay in PKR via JazzCash or EasyPaisa. Fast setup."
    c['seo_intro'] = "Get authentic Adobe Creative Cloud in Pakistan on your personal Adobe ID via independent marketplace activation. Includes 20+ desktop apps with cloud updates."
    c['why_buy_local'] = "Avoid hazardous cracked software and malware risks. Receive authentic retail Adobe Creative Cloud activation via independent marketplace support, paid via JazzCash, EasyPaisa, or local bank transfer."
    if 'faqs' in c and len(c['faqs']) > 2:
        c['faqs'][2]['a'] = "Yes. You download authentic, unmodified software directly through the official Adobe Creative Cloud Desktop application with regular cloud updates. AI Tools Zone is an independent service marketplace and is not an authorized distributor or corporate partner of Adobe Inc."

    # 6. elevenlabs
    c = content.get('elevenlabs', {})
    if 'benefits' in c and len(c['benefits']) > 2:
        c['benefits'][2] = "Private access with fast 15–30 minute WhatsApp setup upon payment verification and 7-day warranty."

    # 7. capcut
    c = content.get('capcut', {})
    if 'benefits' in c and len(c['benefits']) > 2:
        c['benefits'][2] = "Fast 15–30 minute WhatsApp delivery of private access upon payment verification with 7-day replacement warranty."

    # 8. nordvpn
    c = content.get('nordvpn', {})
    c['seo_intro'] = "Get a NordVPN 2-year subscription in Pakistan via independent marketplace activation. Protect up to 10 devices simultaneously with high-speed NordLynx servers in PKR."
    c['why_buy_local'] = "VPN provider websites frequently block Pakistani debit cards. Pay easily in PKR via JazzCash, EasyPaisa, or bank transfer with 15–30 minute credential delivery upon payment verification."

    content_file.write_text(json.dumps(content, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print("Successfully applied Phase 4.1.2 commercial copy corrections to data/product-content.json!")

if __name__ == '__main__':
    main()

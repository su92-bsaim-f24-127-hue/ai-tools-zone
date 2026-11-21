import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(".")
FOLDERS = ('products','categories','use-cases','compare','alternatives','guides','pricing','blog','about','privacy','terms','faq','buy-ai-tools-in-pakistan','how-to-buy-chatgpt-plus-in-pakistan','best-ai-tools-for-students-pakistan','ai-video-editing-tools-pakistan','ai-image-generator-subscriptions-pakistan')

built_files = [ROOT / 'index.html', ROOT / '404.html']
for folder in FOLDERS:
    p = ROOT / folder
    if p.exists():
        built_files.extend(sorted(p.rglob("*.html")))

ALLOWED_PREMIUM_PRODUCTS = [
    r"ChatGPT\s+Plus",
    r"Grammarly\s+Premium",
    r"QuillBot\s+Premium",
    r"Netflix\s+Premium\s+4K",
    r"Netflix\s+Premium",
    r"YouTube(?:\s+Music)?\s+Premium",
    r"LinkedIn\s+Premium"
]

TERMS = [
    ("unlock", re.compile(r"\bunlock(?:s|ed|ing)?\b", re.I)),
    ("most popular", re.compile(r"\bmost\s+popular\b", re.I)),
    ("leading", re.compile(r"\bleading\b", re.I)),
    ("top-rated", re.compile(r"\btop[- ]rated\b", re.I)),
    ("best-selling", re.compile(r"\bbest[- ]selling\b", re.I)),
    ("#1", re.compile(r"#1\b", re.I)),
    ("number one", re.compile(r"\bnumber\s+one\b", re.I)),
    ("trusted", re.compile(r"\btrusted\b", re.I)),
    ("proven", re.compile(r"\bproven\b", re.I)),
    ("widely used", re.compile(r"\bwidely\s+used\b", re.I)),
    ("industry standard", re.compile(r"\bindustry\s+standard\b", re.I)),
    ("industry-standard", re.compile(r"\bindustry-standard\b", re.I)),
    ("world-class", re.compile(r"\bworld[- ]class\b", re.I)),
    ("state-of-the-art", re.compile(r"\bstate[- ]of[- ]the[- ]art\b", re.I)),
    ("cutting-edge", re.compile(r"\bcutting[- ]edge\b", re.I)),
    ("powerful", re.compile(r"\bpowerful\b", re.I)),
    ("stunning", re.compile(r"\bstunning\b", re.I)),
    ("unbeatable", re.compile(r"\bunbeatable\b", re.I)),
    ("unmatched", re.compile(r"\bunmatched\b", re.I)),
    ("VIP", re.compile(r"\bVIP\b", re.I)),
]

def mask_allowed(text):
    masked = text
    for pat in ALLOWED_PREMIUM_PRODUCTS:
        masked = re.sub(pat, "ALLOWED_PROD", masked, flags=re.I)
    masked = re.sub(r'/(?:grammarly-premium|quillbot-premium|netflix-premium-4k|youtube-premium|linkedin-premium)/?', '/', masked, flags=re.I)
    masked = re.sub(r'\b(?:grammarly-premium|quillbot-premium|netflix-premium-4k|youtube-premium|linkedin-premium)\b', 'ALLOWED_SLUG', masked, flags=re.I)
    return masked

def extract_sentence(text, start, end):
    s = start
    while s > 0 and text[s-1] not in '.!?\n\r':
        s -= 1
    e = end
    while e < len(text) and text[e] not in '.!?\n\r':
        e += 1
    if e < len(text) and text[e] in '.!?':
        e += 1
    return ' '.join(text[s:e].split())

def get_line_num(raw_text, needle):
    idx = raw_text.find(needle)
    if idx == -1:
        idx = raw_text.lower().find(needle.lower())
    if idx == -1:
        return 1
    return raw_text.count('\n', 0, idx) + 1

hits = []

for fpath in built_files:
    rel = fpath.as_posix()
    with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
        raw_html = fh.read()
    
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # 1. <title>
    if soup.title and soup.title.string:
        t_str = soup.title.string.strip()
        t_masked = mask_allowed(t_str)
        if re.search(r'\bpremium\b', t_masked, re.I):
            hits.append((rel, get_line_num(raw_html, t_str), t_str))
        for lbl, rgx in TERMS:
            if rgx.search(t_str):
                hits.append((rel, get_line_num(raw_html, t_str), t_str))
                
    # 2. Meta tags
    for meta in soup.find_all("meta"):
        n = meta.get("name", "").lower()
        p = meta.get("property", "").lower()
        val = meta.get("content", "").strip()
        if not val:
            continue
        if n in ["description", "twitter:description", "twitter:title"] or p in ["og:description", "og:title"]:
            val_masked = mask_allowed(val)
            if re.search(r'\bpremium\b', val_masked, re.I):
                hits.append((rel, get_line_num(raw_html, val[:40]), val))
            for lbl, rgx in TERMS:
                if rgx.search(val):
                    hits.append((rel, get_line_num(raw_html, val[:40]), val))
                    
    # 3. JSON-LD descriptions
    for script in soup.find_all("script", type="application/ld+json"):
        if script.string:
            try:
                data = json.loads(script.string)
                def parse_ld(obj):
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if k.lower() == "description" and isinstance(v, str):
                                v_clean = ' '.join(v.split())
                                v_masked = mask_allowed(v_clean)
                                if re.search(r'\bpremium\b', v_masked, re.I):
                                    hits.append((rel, get_line_num(raw_html, v[:30]), v_clean))
                                for lbl, rgx in TERMS:
                                    if rgx.search(v_clean):
                                        hits.append((rel, get_line_num(raw_html, v[:30]), v_clean))
                            else:
                                parse_ld(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            parse_ld(item)
                parse_ld(data)
            except Exception:
                pass
                
    # 4. Visible text
    for s in soup(["script", "style", "noscript"]):
        s.extract()
    for tnode in soup.find_all(string=True):
        parent = tnode.parent
        if parent and parent.name in ['script', 'style', 'noscript']:
            continue
        t_str = str(tnode).strip()
        if not t_str:
            continue
        t_masked = mask_allowed(t_str)
        if re.search(r'\bpremium\b', t_masked, re.I):
            sent = extract_sentence(t_str, 0, len(t_str)) or t_str
            hits.append((rel, get_line_num(raw_html, t_str[:30]), sent))
        for lbl, rgx in TERMS:
            for m in rgx.finditer(t_str):
                sent = extract_sentence(t_str, m.start(), m.end()) or t_str
                hits.append((rel, get_line_num(raw_html, t_str[:30]), sent))

# Deduplicate
seen = set()
dedup = []
for rel, lno, sent in hits:
    key = (rel, lno, sent)
    if key not in seen:
        seen.add(key)
        dedup.append((rel, lno, sent))

for rel, lno, sent in dedup:
    print(f"{rel}:{lno}: {sent}")

import re
from urllib.parse import urlparse
from html import escape

def is_safe_url(url: str) -> bool:
    if not url:
        return False
    # Reject whitespace and control characters (ASCII 0-31, 127)
    if any(ord(c) <= 32 or ord(c) == 127 for c in url):
        return False
    # Reject quotes, backslashes, angle brackets (attribute breakout / tag injection)
    if any(c in url for c in '<>"\'\\'):
        return False
    # Reject protocol-relative URLs (e.g., //example.com)
    if url.startswith('//'):
        return False
    # Allowed 1: Same-site relative path starting with single '/'
    if url.startswith('/'):
        # Reject scheme-like relative paths such as /javascript:, /data:, /vbscript:
        after_slash = url[1:].lstrip().lower()
        if any(after_slash.startswith(scheme) for scheme in ['javascript:', 'data:', 'vbscript:', 'file:', 'about:']):
            return False
        return True
    # Allowed 2: Explicit HTTPS external URLs
    if url.startswith('https://'):
        try:
            parsed = urlparse(url)
            # Must have https scheme and non-empty valid netloc
            if parsed.scheme == 'https' and parsed.netloc and not parsed.netloc.startswith('.'):
                return True
        except Exception:
            return False
        return False
    # All other schemes rejected (http://, javascript:, data:, etc.)
    return False

def render_text(value: str) -> str:
    if value is None:
        return ""
    text = str(value)
    
    # We find markdown links [text](url) where text has no unescaped brackets and url has no spaces or closing parens
    def link_replacer(match):
        anchor_text = match.group(1)
        url = match.group(2).strip()
        if is_safe_url(url):
            # Safe link: render anchor tag with escaped text and escaped URL attribute
            safe_text = escape(anchor_text, quote=True)
            safe_href = escape(url, quote=True)
            return f'<a href="{safe_href}">{safe_text}</a>'
        else:
            # Unsafe URL: return the escaped raw markdown pattern
            return escape(match.group(0), quote=True)
            
    # Pattern: [anchor_text](url)
    pattern = r'\[([^\]]+)\]\(([^)\s]+)\)'
    
    # We tokenize by markdown link matches so that text outside matches is escaped
    result = []
    last_idx = 0
    for m in re.finditer(pattern, text):
        start, end = m.span()
        # Escape any text before this match
        result.append(escape(text[last_idx:start], quote=True))
        # Process the match
        result.append(link_replacer(m))
        last_idx = end
    # Escape any remaining text
    result.append(escape(text[last_idx:], quote=True))
    
    return "".join(result)

# Test cases
test_cases = [
    ("Ordinary Markdown", "[ChatGPT Plus](/products/chatgpt-plus/)"),
    ("Valid Internal Category", "[VPN](/categories/vpn-security/)"),
    ("Approved External HTTPS", "[OpenAI](https://openai.com)"),
    ("Unapproved HTTP Scheme", "[Insecure](http://example.com)"),
    ("Protocol-Relative URL", "[Bypass](//example.com)"),
    ("javascript: scheme", "[Click](javascript:alert(1))"),
    ("Relative /javascript: scheme", "[Click](/javascript:alert(1))"),
    ("data: URI scheme", "[Data](data:text/html,<script>alert(1)</script>)"),
    ("vbscript: scheme", "[VB](vbscript:msgbox(1))"),
    ("Unsafe HTML tag in anchor", "[<script>alert(1)</script>](/products/)"),
    ("Unsafe HTML tag in URL", "[Click](https://example.com/<script>alert(1)</script>)"),
    ("Attribute breakout double quote", '[Click](/path" onmouseover="alert(1))'),
    ("Attribute breakout single quote", "[Click](/path' onfocus='alert(1))"),
    ("Control characters in URL", "[Click](/path\x00test)"),
    ("Spaces in URL", "[Click](https://example.com/foo bar)"),
    ("Malformed unclosed markdown", "[Click without closing"),
    ("Plain text with special characters", "Text with & < > \" and '."),
]

print("TEST RUN:")
for name, inp in test_cases:
    out = render_text(inp)
    print(f"[{name}]")
    print(f"  Input : {inp}")
    print(f"  Output: {out}")
    print("-" * 50)

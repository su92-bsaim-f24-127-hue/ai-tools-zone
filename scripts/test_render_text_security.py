#!/usr/bin/env python3
"""
Test Suite for Markdown Link Renderer Security and URL Policy
AI Tools Zone - Phase 4.1.2 Hardened Renderer Tests
"""

import sys
import os
from pathlib import Path

# Ensure root is in path
sys.path.insert(0, os.path.abspath("."))
from seo_pages import render_text, is_safe_url

def run_tests():
    test_cases = [
        # Approved URL Cases
        ("Standard internal product link", "[ChatGPT Plus](/products/chatgpt-plus/)", '<a href="/products/chatgpt-plus/">ChatGPT Plus</a>', True),
        ("Standard internal category link", "[VPN Hub](/categories/vpn-security/)", '<a href="/categories/vpn-security/">VPN Hub</a>', True),
        ("Internal query link", "[Filter](/products/?q=ai)", '<a href="/products/?q=ai">Filter</a>', True),
        ("Internal hash link", "[Section](/privacy/#terms)", '<a href="/privacy/#terms">Section</a>', True),
        ("Approved external HTTPS link", "[OpenAI](https://openai.com/chatgpt)", '<a href="https://openai.com/chatgpt">OpenAI</a>', True),
        
        # Rejected URL Cases (Must NOT construct an <a href> anchor)
        ("Insecure HTTP scheme", "[Insecure](http://example.com)", "[Insecure](http://example.com)", False),
        ("Protocol-relative URL", "[Bypass](//example.com/login)", "[Bypass](//example.com/login)", False),
        ("Direct javascript: URI", "[Click](javascript:alert(1))", "[Click](javascript:alert(1))", False),
        ("Relative /javascript: URI", "[Click](/javascript:alert(1))", "[Click](/javascript:alert(1))", False),
        ("Data URI scheme", "[Data](data:text/html,<script>alert(1)</script>)", "[Data](data:text/html,&lt;script&gt;alert(1)&lt;/script&gt;)", False),
        ("VBScript URI scheme", "[VBScript](vbscript:msgbox(1))", "[VBScript](vbscript:msgbox(1))", False),
        ("File URI scheme", "[Local](file:///etc/passwd)", "[Local](file:///etc/passwd)", False),
        ("Relative /data: URI", "[Click](/data:image/svg+xml;base64,PHN2Zz4=)", "[Click](/data:image/svg+xml;base64,PHN2Zz4=)", False),
        
        # Injection and Attribute Breakout Cases
        ("Attribute breakout double quote", '[Click](/path" onmouseover="alert(1))', '[Click](/path&quot; onmouseover=&quot;alert(1))', False),
        ("Attribute breakout single quote", "[Click](/path' onfocus='alert(1))", "[Click](/path&#x27; onfocus=&#x27;alert(1))", False),
        ("Tag breakout angle bracket", "[Click](/path><script>alert(1)</script>)", "[Click](/path&gt;&lt;script&gt;alert(1)&lt;/script&gt;)", False),
        ("Backslash injection", "[Click](/path\\test)", "[Click](/path\\test)", False),
        ("Control character in URL (null byte)", "[Click](/path\x00test)", "[Click](/path\x00test)", False),
        ("Newline in URL", "[Click](/path\ntest)", "[Click](/path\ntest)", False),
        
        # HTML Escaping in Anchor Text & Plain Text
        ("Script tag inside anchor text", "[<script>alert(1)</script>](/products/)", '<a href="/products/">&lt;script&gt;alert(1)&lt;/script&gt;</a>', True),
        ("Plain text HTML escaping", "Text with <script>alert(1)</script> & 'quotes'", "Text with &lt;script&gt;alert(1)&lt;/script&gt; &amp; &#x27;quotes&#x27;", False),
        ("Malformed unclosed markdown", "[Unclosed bracket link", "[Unclosed bracket link", False),
        ("Empty markdown link", "[Click]()", "[Click]()", False),
    ]

    print("HARDENED RENDER_TEXT SECURITY VERIFICATION:")
    print("=" * 60)
    failed = 0
    for idx, (name, inp, expected, should_link) in enumerate(test_cases, 1):
        out = render_text(inp)
        has_anchor = "<a href=" in out
        
        # Check expected output and anchor presence
        is_match = (out == expected) and (has_anchor == should_link)
        status = "PASS" if is_match else "FAIL"
        if not is_match:
            failed += 1
            print(f"[{status}] Case {idx}: {name}")
            print(f"  Input   : {inp}")
            print(f"  Expected: {expected}")
            print(f"  Got     : {out}")
        else:
            print(f"[{status}] Case {idx}: {name}")

    print("=" * 60)
    if failed == 0:
        print(f"ALL {len(test_cases)} SECURITY AND URL POLICY CASES PASSED (0 failures).")
        return 0
    else:
        print(f"FAILED: {failed} / {len(test_cases)} cases failed.")
        return 1

if __name__ == '__main__':
    sys.exit(run_tests())

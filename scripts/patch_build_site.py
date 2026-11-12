"""
Script: patch_build_site.py
Purpose: Enable render_text for product overview_text and FAQs in build_site.py.
"""

with open("build_site.py", "r", encoding="utf-8") as f:
    text = f.read()

target1 = '   faq_items.append(f\'<h3>{e(f["q"])}</h3><p>{e(f["a"])}</p>\')'
repl1 = '   faq_items.append(f\'<h3>{e(f["q"])}</h3><p>{render_text(f["a"])}</p>\')'
assert target1 in text, "target1 not found"
text = text.replace(target1, repl1, 1)

target2 = '<p>{e(overview_text)}</p>'
repl2 = '<p>{render_text(overview_text)}</p>'
assert target2 in text, "target2 not found"
text = text.replace(target2, repl2, 1)

with open("build_site.py", "w", encoding="utf-8") as f:
    f.write(text)

print("build_site.py successfully updated with render_text for faqs and overview_text.")

import json
from pathlib import Path

# 1. Update seo-content.json
seo_path = Path('data/seo-content.json')
seo_data = json.loads(seo_path.read_text(encoding='utf-8'))

for c in seo_data['categories']:
    if c['name'] == 'AI Assistants':
        if '/compare/claude-vs-gemini/' not in c['related']:
            c['related'].append('/compare/claude-vs-gemini/')
        if '/compare/chatgpt-vs-claude/' not in c['related']:
            c['related'].append('/compare/chatgpt-vs-claude/')
    elif c['name'] == 'AI Voice':
        if '/compare/elevenlabs-vs-playht/' not in c['related']:
            c['related'].append('/compare/elevenlabs-vs-playht/')
    elif c['name'] == 'Software':
        if '/compare/helium10-vs-semrush-vs-vidiq/' not in c['related']:
            c['related'].append('/compare/helium10-vs-semrush-vs-vidiq/')
    elif c['name'] == 'Productivity':
        if '/compare/grammarly-vs-quillbot-vs-wordai/' not in c['related']:
            c['related'].append('/compare/grammarly-vs-quillbot-vs-wordai/')
    elif c['name'] == 'Design':
        if '/compare/leonardo-vs-midjourney/' not in c['related']:
            c['related'].append('/compare/leonardo-vs-midjourney/')

for p in seo_data['pages']:
    if p['path'] == '/use-cases/ai-tools-for-students/':
        for target in ['/blog/ai-tools-for-teachers-pakistan/', '/compare/grammarly-vs-quillbot-vs-wordai/']:
            if target not in p['related']:
                p['related'].append(target)
    elif p['path'] == '/compare/chatgpt-vs-gemini/':
        if '/compare/claude-vs-gemini/' not in p['related']:
            p['related'].append('/compare/claude-vs-gemini/')

seo_path.write_text(json.dumps(seo_data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

# 2. Update blog-content.json
blog_path = Path('data/blog-content.json')
blog_data = json.loads(blog_path.read_text(encoding='utf-8'))

for a in blog_data['articles']:
    if a['path'] == '/blog/ai-tools-for-pakistani-students-research-thesis/':
        if '/blog/ai-tools-for-teachers-pakistan/' not in a['related']:
            a['related'].append('/blog/ai-tools-for-teachers-pakistan/')
        if '/compare/grammarly-vs-quillbot-vs-wordai/' not in a['related']:
            a['related'].append('/compare/grammarly-vs-quillbot-vs-wordai/')
    elif a['path'] == '/blog/free-ai-tools-pakistan/':
        if '/blog/ai-tools-for-teachers-pakistan/' not in a['related']:
            a['related'].append('/blog/ai-tools-for-teachers-pakistan/')
    elif a['path'] == '/blog/faceless-youtube-automation-ai-tools-pakistan/':
        if '/compare/elevenlabs-vs-playht/' not in a['related']:
            a['related'].append('/compare/elevenlabs-vs-playht/')
        if '/compare/helium10-vs-semrush-vs-vidiq/' not in a['related']:
            a['related'].append('/compare/helium10-vs-semrush-vs-vidiq/')

blog_path.write_text(json.dumps(blog_data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('Enriched related links across categories, pages, and blog articles.')

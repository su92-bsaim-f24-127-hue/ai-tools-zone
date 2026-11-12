import json

path = r'C:\Users\ELITEBOOK\.gemini\antigravity-cli\brain\f51d5b49-c221-4e92-8fc9-553ab2fd3b6b\.system_generated\logs\transcript.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line)
        if o.get('type') == 'USER_INPUT':
            content = o.get('content', '')
            print(f"Step {o.get('step_index')}: {content[:100].strip()}")

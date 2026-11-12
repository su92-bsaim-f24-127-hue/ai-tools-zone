import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://api.github.com/repos/su92-bsaim-f24-127-hue/ai-tools-zone/actions/runs?per_page=5'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        for run in data.get('workflow_runs', []):
            print(f"Run #{run.get('run_number')}: {run.get('name')} | Status: {run.get('status')} | Conclusion: {run.get('conclusion')} | Commit: {run.get('head_sha')[:7]} | URL: {run.get('html_url')}")
except Exception as ex:
    print(f"Error checking actions: {ex}")

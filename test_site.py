"""Compatibility entry point for the current direct-WhatsApp storefront audit."""
from pathlib import Path
import runpy
if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).parent / 'audit_site.py'), run_name='__main__')

"""Compatibility entry point. Old shopping-bag tests were superseded by direct Buy Now checks."""
from pathlib import Path
import runpy
if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).parent / 'audit_site.py'), run_name='__main__')

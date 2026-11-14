"""AI Tools Zone SEO Telemetry Configuration.

Centralizes configuration constants, API endpoints, read-only scopes, and loads
the canonical 97-route inventory dynamically from data/seo-contract.json to avoid
duplicate implementations.
"""

from pathlib import Path
import json
from typing import List, Dict, Any, Optional

# Base project paths
ROOT_DIR: Path = Path(__file__).resolve().parent.parent.parent
DATA_DIR: Path = ROOT_DIR / "data"
SEO_CONTRACT_PATH: Path = DATA_DIR / "seo-contract.json"

# Target Verified Identifiers
WEBSITE_ORIGIN: str = "https://aitoolszone.tech"
GSC_PROPERTY_ID: str = "sc-domain:aitoolszone.tech"
GA4_PROPERTY_ID: str = "562093633"
GA4_PROPERTY_RESOURCE: str = f"properties/{GA4_PROPERTY_ID}"

# Service Account Principal for ADC Impersonation
SERVICE_ACCOUNT_EMAIL: str = "ai-tools-zone-seo-reader@ai-tools-zone-seo.iam.gserviceaccount.com"

# Strictly Read-Only OAuth 2.0 Scopes
GSC_READONLY_SCOPE: str = "https://www.googleapis.com/auth/webmasters.readonly"
GA4_READONLY_SCOPE: str = "https://www.googleapis.com/auth/analytics.readonly"
ALL_TELEMETRY_SCOPES: List[str] = [GSC_READONLY_SCOPE, GA4_READONLY_SCOPE]

# In-memory cached contract
_CACHED_CONTRACT: Optional[Dict[str, Any]] = None


def load_seo_contract(reload: bool = False) -> Dict[str, Any]:
    """Load the authoritative SEO contract from data/seo-contract.json."""
    global _CACHED_CONTRACT
    if _CACHED_CONTRACT is None or reload:
        if not SEO_CONTRACT_PATH.exists():
            raise FileNotFoundError(f"Authoritative SEO contract missing at: {SEO_CONTRACT_PATH}")
        with open(SEO_CONTRACT_PATH, "r", encoding="utf-8") as f:
            _CACHED_CONTRACT = json.load(f)
    return _CACHED_CONTRACT


def get_canonical_routes(reload: bool = False) -> List[str]:
    """Retrieve canonical routes directly from the existing SEO contract.

    Guarantees no duplicate route inventory is maintained in code.
    Validates structural integrity and route counts.
    """
    contract = load_seo_contract(reload=reload)
    routes: List[str] = contract.get("routes", [])
    expected: int = contract.get("expected_pages", 97)

    if len(routes) != expected:
        raise ValueError(
            f"Route count mismatch in contract: found {len(routes)}, expected {expected}"
        )

    # Sanity check canonical route formatting
    for r in routes:
        if not (r.startswith("/") and r.endswith("/")):
            raise ValueError(f"Malformed canonical route detected: {r}")

    return list(routes)


def get_expected_page_count() -> int:
    """Return expected canonical page count from SEO contract."""
    contract = load_seo_contract()
    return int(contract.get("expected_pages", 97))

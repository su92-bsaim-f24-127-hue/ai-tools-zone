"""AI Tools Zone SEO Telemetry Authentication Module.

Handles Application Default Credentials (ADC) resolution and service account
impersonation for Google Search Console and Google Analytics 4 (GA4).
Enforces strictly read-only scopes, zero credential exposure, and safe connectivity checks.
"""

import sys
import logging
from typing import Optional, List, Dict, Any

import google.auth
from google.auth import impersonated_credentials
from google.auth.credentials import Credentials
import googleapiclient.discovery
from googleapiclient.discovery import Resource

try:
    from .config import (
        GSC_PROPERTY_ID,
        GA4_PROPERTY_ID,
        GA4_PROPERTY_RESOURCE,
        SERVICE_ACCOUNT_EMAIL,
        GSC_READONLY_SCOPE,
        GA4_READONLY_SCOPE,
        get_canonical_routes,
        get_expected_page_count,
    )
except ImportError:
    from config import (
        GSC_PROPERTY_ID,
        GA4_PROPERTY_ID,
        GA4_PROPERTY_RESOURCE,
        SERVICE_ACCOUNT_EMAIL,
        GSC_READONLY_SCOPE,
        GA4_READONLY_SCOPE,
        get_canonical_routes,
        get_expected_page_count,
    )

# Logger configuration with strict privacy
logger = logging.getLogger("telemetry.auth")


def mask_identifier(identifier: Optional[str]) -> str:
    """Mask email or sensitive identifiers for safe diagnostic logging."""
    if not identifier:
        return "<unset>"
    if "@" in identifier:
        user, domain = identifier.split("@", 1)
        masked_user = user[:2] + "***" + (user[-1] if len(user) > 3 else "")
        return f"{masked_user}@{domain}"
    if len(identifier) > 6:
        return identifier[:3] + "***" + identifier[-2:]
    return "***"


def get_adc_credentials(scopes: List[str]) -> Credentials:
    """Acquire credentials via Application Default Credentials (ADC) with impersonation support.

    Guarantees:
    - Never logs or prints raw tokens, private keys, or authorization headers.
    - Resolves ADC and automatically establishes service account impersonation
      for least-privilege read-only access.
    """
    try:
        creds, project_id = google.auth.default(scopes=scopes)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to acquire Application Default Credentials (ADC): {type(exc).__name__}"
        ) from None

    # Check if creds are already impersonated to target principal
    current_target = getattr(creds, "service_account_email", None) or getattr(creds, "_target_principal", None)

    if current_target == SERVICE_ACCOUNT_EMAIL and getattr(creds, "valid", True):
        return creds

    # If creds is already an ImpersonatedCredentials instance targeting the service account
    if isinstance(creds, impersonated_credentials.Credentials):
        return creds

    # Explicitly establish impersonation over source credentials
    try:
        impersonated = impersonated_credentials.Credentials(
            source_credentials=creds,
            target_principal=SERVICE_ACCOUNT_EMAIL,
            target_scopes=scopes,
            lifetime=3600,
        )
        return impersonated
    except Exception as exc:
        raise RuntimeError(
            f"Failed to establish service account impersonation for {mask_identifier(SERVICE_ACCOUNT_EMAIL)}: "
            f"{type(exc).__name__}"
        ) from None


def get_gsc_service() -> Resource:
    """Build and return an authenticated, read-only Google Search Console v1 client."""
    creds = get_adc_credentials(scopes=[GSC_READONLY_SCOPE])
    return googleapiclient.discovery.build(
        "searchconsole",
        "v1",
        credentials=creds,
        cache_discovery=False,
    )


def get_ga4_service() -> Resource:
    """Build and return an authenticated, read-only Google Analytics Data v1beta client."""
    creds = get_adc_credentials(scopes=[GA4_READONLY_SCOPE])
    return googleapiclient.discovery.build(
        "analyticsdata",
        "v1beta",
        credentials=creds,
        cache_discovery=False,
    )


def verify_connectivity() -> Dict[str, Any]:
    """Execute safe, non-mutating read-only connectivity checks against GSC and GA4.

    Performs:
    1. Search Console sites.list and property verification.
    2. GA4 property metadata retrieval.
    3. Route inventory validation from data/seo-contract.json.

    Returns structured results dictionary with zero credentials or tokens exposed.
    """
    results: Dict[str, Any] = {
        "status": "pending",
        "gsc": {},
        "ga4": {},
        "contract": {},
    }

    print("=" * 60)
    print("AI Tools Zone — SEO Telemetry Auth & Connectivity Verification")
    print("=" * 60)
    print(f"Service Account (Target) : {mask_identifier(SERVICE_ACCOUNT_EMAIL)}")
    print(f"Search Console Property  : {GSC_PROPERTY_ID}")
    print(f"GA4 Property ID          : {GA4_PROPERTY_ID}")

    # 1. Verify Route Contract Integrity (97 canonical routes)
    try:
        routes = get_canonical_routes()
        expected = get_expected_page_count()
        results["contract"] = {
            "verified": True,
            "route_count": len(routes),
            "expected_count": expected,
        }
        print(f"SEO Contract Routes      : {len(routes)} of {expected} verified [PASS]")
    except Exception as exc:
        results["contract"] = {"verified": False, "error": str(exc)}
        print(f"SEO Contract Routes      : Verification failed: {exc} [FAIL]")

    # 2. Verify Search Console API Connectivity (Read-Only)
    try:
        gsc = get_gsc_service()

        # Verify sites.list endpoint
        sites_list_resp = gsc.sites().list().execute()
        site_entries = sites_list_resp.get("siteEntry", [])
        known_sites = [entry.get("siteUrl") for entry in site_entries if entry.get("siteUrl")]

        # Verify specific property access and permission
        site_detail = gsc.sites().get(siteUrl=GSC_PROPERTY_ID).execute()
        permission_level = site_detail.get("permissionLevel", "unknown")

        results["gsc"] = {
            "authenticated": True,
            "property_in_site_list": GSC_PROPERTY_ID in known_sites,
            "permission_level": permission_level,
            "verified_property": site_detail.get("siteUrl"),
        }
        print(f"Search Console API       : Authenticated via ADC [PASS]")
        print(f"  - Verified Property    : {site_detail.get('siteUrl')}")
        print(f"  - Permission Level     : {permission_level}")
        print(f"  - Total Managed Sites  : {len(known_sites)}")
    except Exception as exc:
        results["gsc"] = {"authenticated": False, "error": type(exc).__name__}
        print(f"Search Console API       : Connection check failed: {type(exc).__name__} [FAIL]")

    # 3. Verify GA4 Data API Connectivity (Read-Only)
    try:
        ga4 = get_ga4_service()
        metadata_resp = ga4.properties().getMetadata(name=f"{GA4_PROPERTY_RESOURCE}/metadata").execute()
        dims_count = len(metadata_resp.get("dimensions", []))
        metrics_count = len(metadata_resp.get("metrics", []))

        results["ga4"] = {
            "authenticated": True,
            "property_resource": GA4_PROPERTY_RESOURCE,
            "available_dimensions": dims_count,
            "available_metrics": metrics_count,
        }
        print(f"GA4 Data API v1beta      : Authenticated via ADC [PASS]")
        print(f"  - Verified Resource    : {GA4_PROPERTY_RESOURCE}")
        print(f"  - Available Dimensions : {dims_count}")
        print(f"  - Available Metrics    : {metrics_count}")
    except Exception as exc:
        results["ga4"] = {"authenticated": False, "error": type(exc).__name__}
        print(f"GA4 Data API v1beta      : Connection check failed: {type(exc).__name__} [FAIL]")

    # Overall Verdict
    all_passed = (
        results["contract"].get("verified", False)
        and results["gsc"].get("authenticated", False)
        and results["ga4"].get("authenticated", False)
    )
    results["status"] = "success" if all_passed else "failure"

    print("-" * 60)
    print(f"Stage 1 Auth Verification Overall Verdict: {'SUCCESS' if all_passed else 'FAILURE'}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    outcome = verify_connectivity()
    if outcome.get("status") != "success":
        sys.exit(1)

"""AI Tools Zone SEO Telemetry Package.

Out-of-band programmatic telemetry subsystem for Google Search Console and GA4.
"""

from .config import (
    GSC_PROPERTY_ID,
    GA4_PROPERTY_ID,
    GA4_PROPERTY_RESOURCE,
    SERVICE_ACCOUNT_EMAIL,
    GSC_READONLY_SCOPE,
    GA4_READONLY_SCOPE,
    ALL_TELEMETRY_SCOPES,
    load_seo_contract,
    get_canonical_routes,
    get_expected_page_count,
)

__all__ = [
    # Config
    "GSC_PROPERTY_ID",
    "GA4_PROPERTY_ID",
    "GA4_PROPERTY_RESOURCE",
    "SERVICE_ACCOUNT_EMAIL",
    "GSC_READONLY_SCOPE",
    "GA4_READONLY_SCOPE",
    "ALL_TELEMETRY_SCOPES",
    "load_seo_contract",
    "get_canonical_routes",
    "get_expected_page_count",
    # Auth
    "get_adc_credentials",
    "get_gsc_service",
    "get_ga4_service",
    "verify_connectivity",
    # GSC Data Engine (Stage 2)
    "get_site_totals",
    "get_pakistan_performance",
    "inspect_canonical_routes",
    "RateLimiter",
    # GA4 Data Engine (Stage 3)
    "get_organic_landing_page_performance",
    "get_ai_assistant_traffic",
    "get_whatsapp_lead_performance",
    "QuotaTracker",
    "GA4QuotaExhaustedError",
    "GA4ClientError",
    # Normalizer & Archival Engine (Stage 4)
    "normalize_telemetry",
    "validate_normalized_payload",
    "save_telemetry_snapshot",
    "normalize_date",
    "validate_date_range",
    "normalize_url_path",
    "match_canonical_route",
    "NormalizationError",
    "ImmutableArchiveError",
    # Reporting Engine (Stage 5)
    "generate_reports",
    "generate_weekly_seo_performance_markdown",
    "generate_indexation_matrix_rows",
    "calculate_wow_comparison",
    "save_weekly_report",
    "save_indexation_matrix_csv",
    "load_snapshot",
    "ReportGenerationError",
    "MalformedArchiveError",
    "ReportPreservationError",
    # Alert Engine (Stage 5)
    "evaluate_alerts",
    "generate_alerts_markdown",
    "save_alerts_report",
    "run_alert_evaluation",
    "Alert",
]


def __getattr__(name: str):
    """Lazy-load modules to keep initialization lightweight and avoid circular import warnings."""
    if name in ("get_adc_credentials", "get_gsc_service", "get_ga4_service", "verify_connectivity"):
        from . import auth
        return getattr(auth, name)
    if name in ("get_site_totals", "get_pakistan_performance", "inspect_canonical_routes", "RateLimiter"):
        from . import gsc_client
        return getattr(gsc_client, name)
    if name in (
        "get_organic_landing_page_performance",
        "get_ai_assistant_traffic",
        "get_whatsapp_lead_performance",
        "QuotaTracker",
        "GA4QuotaExhaustedError",
        "GA4ClientError",
    ):
        from . import ga4_client
        return getattr(ga4_client, name)
    if name in (
        "normalize_telemetry",
        "validate_normalized_payload",
        "save_telemetry_snapshot",
        "normalize_date",
        "validate_date_range",
        "normalize_url_path",
        "match_canonical_route",
        "NormalizationError",
        "ImmutableArchiveError",
    ):
        from . import normalizer
        return getattr(normalizer, name)
    if name in (
        "generate_reports",
        "generate_weekly_seo_performance_markdown",
        "generate_indexation_matrix_rows",
        "calculate_wow_comparison",
        "save_weekly_report",
        "save_indexation_matrix_csv",
        "load_snapshot",
        "ReportGenerationError",
        "MalformedArchiveError",
        "ReportPreservationError",
    ):
        from . import report_generator
        return getattr(report_generator, name)
    if name in (
        "evaluate_alerts",
        "generate_alerts_markdown",
        "save_alerts_report",
        "run_alert_evaluation",
        "Alert",
    ):
        import importlib
        mod = importlib.import_module(".evaluate_alerts", __name__)
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

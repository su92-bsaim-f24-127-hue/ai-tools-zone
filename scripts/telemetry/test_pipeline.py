"""Unit tests for the Unified SEO Telemetry Pipeline Runner (run_pipeline.py)."""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from scripts.telemetry.run_pipeline import (
    calculate_reporting_window,
    find_latest_prior_snapshot,
    execute_pipeline,
)
from scripts.telemetry.config import ROOT_DIR


class TestPipelineRunner(unittest.TestCase):
    """Test suite for the pipeline execution engine."""

    def setUp(self):
        self.archive_dir = ROOT_DIR / "scratch" / "telemetry_archive"
        self.reports_dir = ROOT_DIR / "reports" / "seo-telemetry"
        self.sample_snapshot = self.archive_dir / "run_20261114T193932Z_live_stage6r_remediated_98_routes.json"

    def test_01_calculate_reporting_window(self):
        """Verify trailing reporting window calculates valid ISO dates."""
        start, end = calculate_reporting_window(days=7)
        self.assertEqual(len(start), 10)
        self.assertEqual(len(end), 10)
        self.assertTrue(start < end)

    def test_02_find_latest_prior_snapshot(self):
        """Verify locating most recent historical snapshot."""
        if self.sample_snapshot.exists():
            latest = find_latest_prior_snapshot(self.archive_dir)
            self.assertIsNotNone(latest)
            self.assertTrue(latest.exists())

    def test_03_execute_pipeline_from_snapshot(self):
        """Verify offline pipeline execution against a sample snapshot."""
        if self.sample_snapshot.exists():
            res = execute_pipeline(snapshot_path=str(self.sample_snapshot))
            self.assertEqual(res.get("status"), "success")
            self.assertIn("weekly_report", res.get("stages", {}).get("reports", {}))
            self.assertIn("indexation_matrix", res.get("stages", {}).get("reports", {}))
            self.assertIn("alerts", res.get("stages", {}))
            self.assertEqual(res.get("status_message"), "System Healthy & Stable")

    def test_04_auth_failure_raises(self):
        """Verify that authentication failure stops pipeline execution."""
        with patch("scripts.telemetry.run_pipeline.verify_connectivity", return_value={"status": "failure"}):
            with self.assertRaises(RuntimeError):
                execute_pipeline(skip_inspection=True)


if __name__ == "__main__":
    unittest.main()

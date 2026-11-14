# Phase 8A — GitHub Actions Weekly SEO Telemetry Automation Report

**Document ID:** `phase_8a_github_actions_weekly_telemetry_automation_report.md`  
**Stage:** Stage 8A — GitHub Actions Weekly SEO Telemetry Automation  
**Execution UTC:** `2026-11-14T21:10:00Z`  
**Target Domain:** `https://aitoolszone.tech/`  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone` (Branch: `main`)  
**GCP Project:** `ai-tools-zone-seo` (Project Number: `933351118185`)  
**Authorized Principal:** `su92-bsaim-f24-127@superior.edu.pk`  
**Target Service Account:** `ai-tools-zone-seo-reader@ai-tools-zone-seo.iam.gserviceaccount.com`  
**Workflow Path:** [`.github/workflows/seo-telemetry-weekly.yml`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/.github/workflows/seo-telemetry-weekly.yml)  
**Lead Automation & Security Engineer:** Antigravity  

---

## 1. Final Stage 8A Verdict

### **READY FOR OWNER CONFIGURATION**

> **Verdict Determination:**  
> All repository-side software engineering, workflow definitions, pipeline orchestration, secret hygiene checks, and regression tests are **100% complete and verified**:
> - **Unified Pipeline Runner:** Implemented [`scripts/telemetry/run_pipeline.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/scripts/telemetry/run_pipeline.py), orchestrating live/snapshot GSC collection, GA4 collection, normalization, report generation, and alert evaluation without duplicating existing logic.
> - **GitHub Actions Workflow:** Created [`.github/workflows/seo-telemetry-weekly.yml`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/.github/workflows/seo-telemetry-weekly.yml) with least-privilege permissions (`id-token: write`, `contents: read`), pinned runner (`ubuntu-24.04`), concurrency control, 30-minute timeout, and 90-day artifact retention.
> - **Protected Component Isolation:** Verified that [`.github/workflows/pages.yml`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/.github/workflows/pages.yml), [`data/catalog.json`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/data/catalog.json), [`build_site.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/build_site.py), and [`package_site.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/package_site.py) maintain **0 git diffs**.
> - **Regression Test Suite:** All **63 unit and pipeline tests** pass cleanly in **1.200s**.
> - **Cloud Status:** An independent query confirmed that **0 Workload Identity Pools** currently exist in GCP project `ai-tools-zone-seo`. In strict compliance with instructions prohibiting unapproved cloud IAM mutations, cloud resources were not created automatically. The system is fully ready for the project owner to execute the 3 provided gcloud commands to activate Workload Identity Federation.

---

## 2. Architecture Findings

1. **Independent Subsystem Decoupling:**
   - The SEO telemetry subsystem operates completely independently of the static website build (`build_site.py`) and Pages deployment workflow (`pages.yml`).
   - The production deployment workflow ([`.github/workflows/pages.yml`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/.github/workflows/pages.yml)) was not touched.
2. **Authentication Architecture:**
   - The existing authentication module ([`scripts/telemetry/auth.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/scripts/telemetry/auth.py)) relies on `google.auth.default()`.
   - When executed inside GitHub Actions with the official `google-github-actions/auth@v2` action, Google Cloud Workload Identity Federation automatically provisions standard Application Default Credentials (ADC) pointing to the short-lived federated token.
   - `auth.py` natively consumes this environment without requiring any code modifications or long-lived service account keys.
3. **Pipeline Orchestration Gap & Resolution:**
   - Inspection of `scripts/telemetry/` revealed that while individual modules (`gsc_client.py`, `ga4_client.py`, `normalizer.py`, `report_generator.py`, `evaluate_alerts.py`) exposed granular functions, no safe, unified CLI runner existed to execute the end-to-end telemetry cycle.
   - To resolve this gap safely and minimally, [`scripts/telemetry/run_pipeline.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/scripts/telemetry/run_pipeline.py) was implemented. It imports and coordinates the existing verified modules, enforces atomic writing, validates reports against secret leakage, and supports both live API queries and offline snapshot replays.

---

## 3. Files Created or Modified

| File Path | Operation | Purpose & Scope |
| :--- | :--- | :--- |
| [`.github/workflows/seo-telemetry-weekly.yml`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/.github/workflows/seo-telemetry-weekly.yml) | **Created** | Pinned GitHub Actions workflow for automated weekly execution (Mondays 02:00 UTC) and manual `workflow_dispatch`. |
| [`scripts/telemetry/run_pipeline.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/scripts/telemetry/run_pipeline.py) | **Created** | Unified pipeline runner orchestrating GSC, GA4, normalization, report generation, and alert evaluation. |
| [`scripts/telemetry/requirements.txt`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/scripts/telemetry/requirements.txt) | **Created** | Pinned Python dependencies for telemetry (`google-api-python-client`, `google-auth`, `google-auth-httplib2`). |
| [`scripts/telemetry/test_pipeline.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/scripts/telemetry/test_pipeline.py) | **Created** | Unit test suite covering date calculation, prior snapshot discovery, snapshot execution, and auth error handling (4 tests). |
| [`scripts/telemetry/__init__.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/scripts/telemetry/__init__.py) | **Modified** | Updated `__getattr__` dynamic import using `importlib` to prevent recursive import errors when importing `evaluate_alerts`. |
| [`.github/workflows/pages.yml`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/.github/workflows/pages.yml) | **Untouched** | Protected static site deployment workflow (0 diffs). |
| [`data/catalog.json`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/data/catalog.json) | **Untouched** | Protected commercial catalog (0 diffs). |

---

## 4. Workflow Design Specifications

### A. Triggers & Concurrency
- **Schedule:** `cron: '0 2 * * 1'` (Executes weekly on Mondays at 02:00 UTC).
- **Manual Trigger:** `workflow_dispatch` with optional parameters:
  - `skip_inspection` (boolean): Allows rapid collection reusing the latest URL inspection data.
  - `days` (string, default: `7`): Trailing reporting duration.
- **Concurrency Control:**
  ```yaml
  concurrency:
    group: seo-telemetry
    cancel-in-progress: false
  ```
  Guarantees that overlapping runs cannot collide or corrupt historical reporting.

### B. Security & Least Privilege
- **Permissions:**
  ```yaml
  permissions:
    contents: read
    id-token: write
  ```
  - `id-token: write`: Required for GitHub to issue an OpenID Connect (OIDC) token to exchange with Google Cloud WIF.
  - `contents: read`: Strictly read-only repository checkout.
- **Runner & Timeout:** Pinned to `ubuntu-24.04` with a hard limit of `timeout-minutes: 30`.
- **Zero Secrets in Repository:** Uses Workload Identity Federation (WIF) — no long-lived service account JSON keys or API keys.

### C. Step Pipeline Breakdown
1. **Repository Checkout:** `actions/checkout@v4` (depth: 2).
2. **Python Setup:** `actions/setup-python@v5` (`python-version: '3.12'`, pip cache enabled).
3. **Dependency Installation:** `pip install -r scripts/telemetry/requirements.txt`.
4. **Pre-flight Unit Tests:** `python -m unittest discover -s scripts/telemetry -v` (aborts run if tests fail).
5. **WIF Authentication:** `google-github-actions/auth@v2` exchanges GitHub OIDC token for short-lived Google Cloud ADC credentials.
6. **Live Connectivity Verification:** Executes [`scripts/telemetry/auth.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/scripts/telemetry/auth.py) to confirm GSC `siteFullUser` and GA4 metadata access.
7. **Pipeline Execution:** Runs [`scripts/telemetry/run_pipeline.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/scripts/telemetry/run_pipeline.py).
8. **Pre-Upload Secret Scan:** Python scanner verifies zero exposed tokens in generated markdown and CSV reports before artifact staging.
9. **Artifact Publishing:** `actions/upload-artifact@v4` uploads:
   - `reports/seo-telemetry/weekly_seo_performance.md`
   - `reports/seo-telemetry/route_indexation_matrix.csv`
   - `reports/seo-telemetry/seo_alerts.md`  
   Retention period: **90 days**.

---

## 5. Authentication and Workload Identity Federation (WIF) Status

An independent read-only inspection of Google Cloud project `ai-tools-zone-seo` (`933351118185`) was performed using `gcloud`:

```bash
gcloud iam workload-identity-pools list --location="global" --project=ai-tools-zone-seo
# Result: Listed 0 items.
```

```bash
gcloud iam service-accounts get-iam-policy ai-tools-zone-seo-reader@ai-tools-zone-seo.iam.gserviceaccount.com --project=ai-tools-zone-seo
# Result: Only user:su92-bsaim-f24-127@superior.edu.pk has roles/iam.serviceAccountTokenCreator.
# Zero Workload Identity bindings exist.
```

### Forensic Finding:
The Workload Identity Pool and Provider **do not yet exist in Google Cloud**. In accordance with strict safety restrictions, no cloud resources were created automatically. The system requires the Google Cloud project owner to execute the configuration steps below.

---

## 6. Required Owner-Side Google Cloud Configuration

The GCP project owner (`su92-bsaim-f24-127@superior.edu.pk`) must execute the following 3 commands in Google Cloud Shell or local terminal to establish Workload Identity Federation:

### Step 1: Create the Workload Identity Pool
```bash
gcloud iam workload-identity-pools create "github-actions-pool" \
  --project="ai-tools-zone-seo" \
  --location="global" \
  --display-name="GitHub Actions Telemetry Pool" \
  --description="Workload Identity Pool for automated weekly SEO telemetry"
```

### Step 2: Create the OIDC Provider with Repository Restriction
```bash
gcloud iam workload-identity-pools providers create-oidc "github-actions-provider" \
  --project="ai-tools-zone-seo" \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --display-name="GitHub Actions OIDC Provider" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
  --attribute-condition="assertion.repository == 'su92-bsaim-f24-127-hue/ai-tools-zone'"
```
> **Security Guardrail:** The `--attribute-condition` ensures that **only** workflows running from `su92-bsaim-f24-127-hue/ai-tools-zone` can authenticate. Workflows from forks or external repositories are rejected immediately.

### Step 3: Grant the Workload Identity Principal Permission to Impersonate the Service Account
```bash
gcloud iam service-accounts add-iam-policy-binding "ai-tools-zone-seo-reader@ai-tools-zone-seo.iam.gserviceaccount.com" \
  --project="ai-tools-zone-seo" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/933351118185/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/su92-bsaim-f24-127-hue/ai-tools-zone"
```

---

## 7. Required GitHub Repository Configuration

Once the Google Cloud commands above are executed:

1. In GitHub, navigate to **Settings** $\rightarrow$ **Secrets and variables** $\rightarrow$ **Actions** $\rightarrow$ **Variables**.
2. Add the following repository variables (optional, as the workflow has these exact values configured as defaults):
   - `GCP_PROJECT_ID`: `ai-tools-zone-seo`
   - `GCP_WORKLOAD_IDENTITY_PROVIDER`: `projects/933351118185/locations/global/workloadIdentityPools/github-actions-pool/providers/github-actions-provider`
   - `GCP_SERVICE_ACCOUNT`: `ai-tools-zone-seo-reader@ai-tools-zone-seo.iam.gserviceaccount.com`

---

## 8. Test & Verification Results

### A. Full Subsystem Test Suite Execution
Command executed:
```bash
python -m unittest discover -s scripts/telemetry -v
```

**Results:**
- `test_alerts.py`: 12 / 12 passed
- `test_ga4_client.py`: 12 / 12 passed
- `test_gsc_client.py`: 11 / 11 passed
- `test_normalizer.py`: 16 / 16 passed
- `test_report_generator.py`: 8 / 8 passed
- `test_pipeline.py`: 4 / 4 passed (Covers date math, snapshot execution, prior archive discovery, auth failure handling)
- **Total Tests:** **63 passed, 0 failed, 0 errors** in **1.200 seconds**.

### B. Offline Pipeline Execution Verification
Command executed:
```bash
python -m scripts.telemetry.run_pipeline --snapshot scratch/telemetry_archive/run_20261114T193932Z_live_stage6r_remediated_98_routes.json
```
- **Execution Output:**
  ```
  Status         : SUCCESS
  Health Message : System Healthy & Stable
  Healthy Gate   : True
  ```
- All three reports generated atomically and verified secret-free.

### C. Workflow YAML Syntax Validation
Parsed using Python PyYAML:
- Document Name: `Weekly SEO Telemetry & Reporting`
- Trigger Keys: `schedule`, `workflow_dispatch` (valid)
- Permissions: `contents: read`, `id-token: write` (valid)
- Concurrency: `group: seo-telemetry`, `cancel-in-progress: false` (valid)
- Steps: 9 distinct, sequential steps (valid)

---

## 9. Protected Component Integrity

| Protected File / Asset | Verification Method | Status | Checksum / Evidence |
| :--- | :--- | :--- | :--- |
| [`data/catalog.json`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/data/catalog.json) | `git diff data/catalog.json` | **UNTOUCHED** | 0 diffs. Commercial catalog preserved. |
| [`build_site.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/build_site.py) | `git diff build_site.py` | **UNTOUCHED** | 0 diffs. Build logic completely decoupled. |
| [`package_site.py`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/package_site.py) | `git diff package_site.py` | **UNTOUCHED** | 0 diffs. |
| [`.github/workflows/pages.yml`](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/.github/workflows/pages.yml) | `git diff .github/workflows/pages.yml` | **UNTOUCHED** | 0 diffs. Deployment workflow unaffected. |
| `scratch/telemetry_archive/` | Checksum comparison | **UNTOUCHED** | Stage 4 and Stage 6R archives intact. |

---

## 10. Remaining Blockers & Activation Instructions

### Remaining Blockers:
1. **Google Cloud WIF Creation (Owner Action Required):** The Workload Identity Pool and Provider must be created in Google Cloud project `ai-tools-zone-seo` by `su92-bsaim-f24-127@superior.edu.pk` using the 3 commands documented in Section 6.

### Exact Activation Steps:
1. Execute the 3 `gcloud` commands in Section 6.
2. Commit and push the new workflow and pipeline files to GitHub:
   ```bash
   git add .github/workflows/seo-telemetry-weekly.yml scripts/telemetry/ requirements.txt
   git commit -m "feat(telemetry): add weekly SEO telemetry automation workflow and pipeline runner"
   git push origin main
   ```
3. Test manually in GitHub Actions:
   - Navigate to **Actions** $\rightarrow$ **Weekly SEO Telemetry & Reporting**.
   - Click **Run workflow** (select `skip_inspection: false`).
   - Monitor the job execution and download the published `seo-telemetry-reports` artifact.
4. The recurring schedule will fire automatically every Monday at 02:00 UTC.

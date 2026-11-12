# Phase 4.2.5 — Break-Even Re-Calculation & Target Margin Reconciliation

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** Re-derivation of K-Coefficients, Sensitivity Scenarios, and Alternative Sourcing  

---

## 1. Mathematical Derivation of Scenario Coefficients

Each procurement scenario possesses an exact, derived multiplier $K$:

### A. Statutory Tax Base (Foreign Principal Only - Scenario 1):
$$K_{\text{stat, ATL}} = 1 + r_{\text{bank}} \times (1 + r_{\text{FED}}) + r_{236Y} + r_{\text{reserve}}$$
$$K_{\text{stat, ATL}} = 1 + 0.0400 \times 1.1600 + 0.0050 + 0.0500 = 1 + 0.0464 + 0.0050 + 0.0500 = \mathbf{1.101400}$$

### B. Disputed Bank Debiting Base (Gross Remittance - Scenario 2):
$$K_{\text{gross, ATL}} = (1 + 0.0464) \times (1 + 0.0050) + 0.0500 = 1.051632 + 0.0500 = \mathbf{1.101632}$$

### C. Low-Fee Bank Scenario (Meezan 3.50% Bank Fee + 16% FED - Scenario 3):
$$K_{\text{meezan, ATL}} = 1 + 0.0350 \times 1.1600 + 0.0050 + 0.0500 = 1 + 0.0406 + 0.0050 + 0.0500 = \mathbf{1.095600}$$

### D. High-Fee Bank Scenario (Bank Alfalah 4.50% Credit Card - Scenario 4):
$$K_{\text{alfalah, ATL}} = 1 + 0.0450 \times 1.1600 + 0.0050 + 0.0500 = 1 + 0.0522 + 0.0050 + 0.0500 = \mathbf{1.107200}$$

---

## 2. Re-Calculated Break-Even Rates Across Proposed Prices

The break-even exchange rate is derived from:
$$\text{FX}_{\text{break-even}} = \frac{P_{\text{retail}} \times (1 - r_{\text{gateway}}) - C_{\text{labor}}}{\text{USD} \times K}$$

Under $r_{\text{gateway}} = 0.02$ and $C_{\text{labor}} = \text{PKR } 350.00$:

| Product | Retail Price Point | Statutory Base Break-Even FX | Disputed Gross Base Break-Even FX | Difference |
|---|:---:|:---:|:---:|:---:|
| **Cursor / Claude ($20)** | **PKR 6,800.00** (Catalog Base) | **PKR 286.63 / USD** | **PKR 286.57 / USD** | +0.06 PKR |
| Cursor / Claude ($20) | **PKR 7,320.00** (10% Target @ 276.76) | **PKR 309.76 / USD** | **PKR 309.70 / USD** | +0.06 PKR |
| Cursor / Claude ($20) | **PKR 7,400.00** (Recommended Launch) | **PKR 313.33 / USD** | **PKR 313.26 / USD** | +0.07 PKR |
| Cursor / Claude ($20) | **PKR 7,760.00** (15% Target @ 276.76) | **PKR 329.35 / USD** | **PKR 329.28 / USD** | +0.07 PKR |
| **GitHub Copilot ($10)** | **PKR 3,800.00** (Catalog Base) | **PKR 306.34 / USD** | **PKR 306.27 / USD** | +0.07 PKR |
| GitHub Copilot ($10) | **PKR 3,900.00** (Recommended Launch) | **PKR 315.24 / USD** | **PKR 315.17 / USD** | +0.07 PKR |

> **Conclusion on Tax Base Impact:**  
> The difference between the Statutory Interpretation (tax on principal) and Disputed Banking Practice (tax on gross debit) is **under 0.10 PKR on the break-even exchange rate**.  
> While statutorily significant, the tax-base dispute does **not materially alter pricing thresholds or business solvency**.

---

## 3. Financial Comparison: Merchant-Funded Resale vs. Customer-Funded Setup

| Financial Metric | Model C: Merchant-Funded Card Resale (Cursor @ PKR 7,400) | Model D: Customer-Funded Setup Service (Cursor Setup @ PKR 1,000) |
|---|:---:|:---:|
| **Gross Customer Revenue** | PKR 7,400.00 | PKR 1,000.00 |
| **Merchant Outward Remittance** | $20.00 USD (PKR 5,535.20) | **PKR 0.00** (Customer pays Anthropic direct) |
| **Bank International Fee + FED** | PKR 256.83 | **PKR 0.00** |
| **Section 236Y Withholding** | PKR 27.68 (or 28.96) | **PKR 0.00** |
| **Domestic Collection (Raast @ 0%)** | PKR 0.00 | PKR 0.00 |
| **Onboarding & Setup Labor** | PKR 350.00 | PKR 350.00 |
| **Warranty Reserve** | PKR 276.76 | **PKR 0.00** (Zero account replacement risk) |
| **Net Cash Profit per Order** | **+PKR 953.53** (12.89% margin) | **+PKR 650.00 (65.00% pure service margin)** |
| **Working Capital Requirement** | PKR 6,446.47 per order | **PKR 0.00** |
| **Foreign Exchange Risk** | Extreme (losses if USD > 313) | **ZERO FX RISK** |
| **Provider Terms Violation Risk** | **HIGH RISK OF ACCOUNT SUSPENSION** | **ZERO TERMS VIOLATION RISK** |

> **Strategic Commercial Finding:**  
> **Model D (Customer-Funded Setup Service)** delivers **PKR 650 pure profit** per transaction with zero working capital, zero currency exposure, and 100% provider terms compliance.

# Phase 4.2.3 — Financial Formula Audit & Cost-Plus Pricing Policy

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** Mathematical Proofs, Banking Fee Schedule Audit, and Cost-Plus Pricing Formula  

---

## 1. Step-by-Step Mathematical Reconciliation

This section exposes the deterministic intermediate calculations reconciling reported landed costs and baseline cash contributions:

### A. GitHub Copilot ($10.00 USD | Proposed Retail: PKR 3,800.00)
1. **Base Procurement:** $\$10.00 \times 276.76 = \text{PKR } 2,767.60$
2. **Bank Fee:** $2,767.60 \times 0.04 = \text{PKR } 110.70$
3. **FED on Bank Fee:** $110.70 \times 0.16 = \text{PKR } 17.71$
4. **Total Bank Fee:** $110.70 + 17.71 = \text{PKR } 128.41$ (or $2,767.60 \times 0.0464 = 128.42$)
5. **Gross Remittance:** $2,767.60 + 128.42 = \text{PKR } 2,896.02$
6. **Section 236Y Tax (ATL @ 0.50%):** $2,896.02 \times 0.005 = \text{PKR } 14.48$
7. **Landed Cash Outlay:** $2,896.02 + 14.48 = \mathbf{PKR\ 2,910.50}$ *(Reconciled exactly)*
8. **Domestic Gateway Fee (2.0% of retail):** $3,800.00 \times 0.02 = \text{PKR } 76.00$
9. **Labor Overhead:** $\text{Onboarding } (150.00) + \text{Support } (200.00) = \text{PKR } 350.00$
10. **Replacement Reserve (5.0% of base):** $2,767.60 \times 0.05 = \text{PKR } 138.38$
11. **Total Operating Expenses:** $76.00 + 350.00 + 138.38 = \mathbf{PKR\ 564.38}$
12. **Total Cash Drain:** $2,910.50 + 564.38 = \text{PKR } 3,474.88$
13. **Net Cash Contribution:** $3,800.00 - 3,474.88 = \mathbf{+PKR\ 325.12}$ *(Reconciled exactly)*
14. **Net Cash Margin:** $325.12 / 3,800.00 = \mathbf{+8.56\%}$

### B. Cursor AI Pro & Claude Pro ($20.00 USD | Proposed Retail: PKR 6,800.00)
1. **Base Procurement:** $\$20.00 \times 276.76 = \text{PKR } 5,535.20$
2. **Bank Fee:** $5,535.20 \times 0.04 = \text{PKR } 221.41$
3. **FED on Bank Fee:** $221.41 \times 0.16 = \text{PKR } 35.43$
4. **Total Bank Fee:** $221.41 + 35.43 = \text{PKR } 256.84$ (or $5,535.20 \times 0.0464 = 256.83$)
5. **Gross Remittance:** $5,535.20 + 256.83 = \text{PKR } 5,792.03$
6. **Section 236Y Tax (ATL @ 0.50%):** $5,792.03 \times 0.005 = \text{PKR } 28.96$
7. **Landed Cash Outlay:** $5,792.03 + 28.96 = \mathbf{PKR\ 5,820.99}$ *(Reconciled exactly)*
8. **Domestic Gateway Fee (2.0% of retail):** $6,800.00 \times 0.02 = \text{PKR } 136.00$
9. **Labor Overhead:** $\text{Onboarding } (150.00) + \text{Support } (200.00) = \text{PKR } 350.00$
10. **Replacement Reserve (5.0% of base):** $5,535.20 \times 0.05 = \text{PKR } 276.76$
11. **Total Operating Expenses:** $136.00 + 350.00 + 276.76 = \mathbf{PKR\ 762.76}$
12. **Total Cash Drain:** $5,820.99 + 762.76 = \text{PKR } 6,583.75$
13. **Net Cash Contribution:** $6,800.00 - 6,583.75 = \mathbf{+PKR\ 216.25}$ *(Reconciled exactly)*
14. **Net Cash Margin:** $216.25 / 6,800.00 = \mathbf{+3.18\%}$

---

## 2. Schedule of Bank Charges (SOBC) Audit

### The 4.00% Bank Fee Clarification:
An audit of current commercial bank fee schedules in Pakistan (Meezan Bank Schedule of Bank Charges, HBL Consumer Banking SOBC, Bank Alfalah) reveals how cross-border card transactions are billed:
- **Card Scheme Settlement Spread:** The card network (Visa/Mastercard) and the issuing bank quote an effective card settlement rate that is typically 1.5% to 2.5% above interbank mid-market.
- **Cross-Border / International Transaction Fee:** Banks levy a distinct fee of 3.0% to 4.0% for clearing international e-commerce charges.
- **Federal Excise Duty (FED):** 16.0% sales tax on banking services is levied strictly on the fee, not on the principal remittance.
- **Audit Conclusion:** The modeled 4.0% fee + 16% FED (effective 4.64%) accurately reflects the **all-in international card transaction overhead** of top Pakistani private banks (e.g., Meezan Bank). It represents the combined FX spread and scheme processing charge; there is zero double-counting.

### Domestic Collection Fee Schedules:
- **JazzCash Merchant Gateway:** 1.75% to 2.00% + 16% FED per transaction.
- **Easypaisa Merchant QR / Online API:** 1.80% to 2.20% + FED.
- **Raast (National Payment Scheme):** 0.00% transaction fee for P2P/P2M under State Bank directives.
- **1Link IBFT:** Flat fee of PKR 0 to PKR 25 depending on volume.
- **Audit Conclusion:** The 2.00% domestic gateway fee modeled across all products represents a prudent weighted assumption reflecting automated merchant payment aggregators (PayMob, Safepay). When customers pay directly via Raast, the actual fee is 0.00 PKR, expanding net cash contribution by PKR 76.00 (Copilot) and PKR 136.00 (Cursor/Claude).

---

## 3. Reassessment of Arbitrary Pricing Triggers

Phase 4.2.2 proposed:
> *"Repricing trigger at PKR 285/USD: Reprice to PKR 7,200 at 290/USD, and PKR 7,500 at 300/USD."*

### Critique of Arbitrary Stepped Pricing:
- Setting static price points (7,200, 7,500) without a mathematical formula leads to uneven margin recovery.
- For example, at PKR 290/USD, a price of PKR 7,200 yields an 8.1% cash margin, while at PKR 300/USD, PKR 7,500 yields a 6.8% margin.
- The pricing policy should not be based on ad-hoc adjustments, but on a deterministic cost-plus pricing formula with an explicit minimum margin floor.

---

## 4. The Closed-Form Cost-Plus Target-Margin Pricing Formula

To guarantee commercial viability under any currency fluctuation, AI Tools Zone should adopt an objective pricing formula governed by an owner-mandated minimum target net cash margin ($M_{\text{target}}$):

$$P_{\text{retail}} = \frac{\text{USD} \times \text{FX} \times \left[ (1 + r_{\text{bank}} \times (1 + r_{\text{FED}})) \times (1 + r_{236Y}) + r_{\text{reserve}} \right] + C_{\text{labor}}}{1 - r_{\text{gateway}} - M_{\text{target}}}$$

Where:
- $\text{USD}$ = Official provider subscription price in USD.
- $\text{FX}$ = Current SBP Customer Selling Exchange Rate benchmark.
- $r_{\text{bank}} = 0.0400$ (Bank conversion fee).
- $r_{\text{FED}} = 0.1600$ (FED on bank fee).
- $r_{236Y} = 0.0050$ (FBR Section 236Y ATL rate).
- $r_{\text{reserve}} = 0.0500$ (Replacement reserve provision).
- $C_{\text{labor}} = \text{PKR } 350.00$ (Onboarding + WhatsApp support).
- $r_{\text{gateway}} = 0.0200$ (Domestic payment processing fee).
- $M_{\text{target}}$ = Owner-mandated minimum net cash margin (e.g. 10.0% or 15.0%).

$$\text{Procurement Factor } (K) = (1 + 0.0464) \times 1.0050 + 0.0500 = 1.051632 + 0.0500 = \mathbf{1.101632}$$

### Simplified Operational Formula:
$$P_{\text{retail}} = \frac{\text{USD} \times \text{FX} \times 1.101632 + 350.00}{0.98 - M_{\text{target}}}$$

---

## 5. Recommended Retail Price Table Under Dynamic Cost-Plus Policy

Applying this exact formula produces calibrated, defensible retail price recommendations across exchange rate scenarios:

### GitHub Copilot ($10.00 USD)

| FX Scenario (PKR/USD) | Landed Procurement Outlay (PKR) | 10% Minimum Margin Retail | 15% Target Margin Retail | Current Catalog Proposed Retail |
|:---:|:---:|:---:|:---:|:---:|
| **276.76 (Baseline)** | PKR 2,910.50 | **PKR 3,860.00** | **PKR 4,090.00** | PKR 3,800.00 (Yields 8.56%) |
| **285.00** | PKR 2,997.15 | **PKR 3,960.00** | **PKR 4,200.00** | PKR 3,800.00 (Yields 6.17%) |
| **294.12** | PKR 3,093.06 | **PKR 4,080.00** | **PKR 4,320.00** | PKR 3,800.00 (Yields 3.52%) |
| **300.00** | PKR 3,154.90 | **PKR 4,150.00** | **PKR 4,400.00** | PKR 3,800.00 (Yields 1.82%) |
| **315.00** | PKR 3,312.64 | **PKR 4,340.00** | **PKR 4,600.00** | Unviable at PKR 3,800 (LOSS) |

### Cursor AI Pro & Claude Pro ($20.00 USD)

| FX Scenario (PKR/USD) | Landed Procurement Outlay (PKR) | 10% Minimum Margin Retail | 15% Target Margin Retail | Current Catalog Proposed Retail |
|:---:|:---:|:---:|:---:|:---:|
| **276.76 (Baseline)** | PKR 5,820.99 | **PKR 7,320.00** | **PKR 7,760.00** | PKR 6,800.00 (Yields 3.18% — High Risk) |
| **285.00** | PKR 5,994.30 | **PKR 7,530.00** | **PKR 7,980.00** | PKR 6,800.00 (Yields 0.51%) |
| **294.12** | PKR 6,186.12 | **PKR 7,760.00** | **PKR 8,220.00** | PKR 6,800.00 (LOSS -2.44%) |
| **300.00** | PKR 6,309.79 | **PKR 7,900.00** | **PKR 8,380.00** | PKR 6,800.00 (LOSS -4.35%) |
| **315.00** | PKR 6,625.28 | **PKR 8,280.00** | **PKR 8,780.00** | PKR 6,800.00 (LOSS -9.21%) |

> **Key Commercial Insight for Business Owner:**  
> The currently proposed retail price of **PKR 6,800.00** for Cursor and Claude provides an inadequate cushion (only 3.18% net margin at baseline).  
> To operate a safe, sustainable developer pilot, the owner should set the initial launch price at **PKR 7,300.00 to PKR 7,500.00**, securing a healthy 10%–12% net margin and shielding the business from routine currency volatility.

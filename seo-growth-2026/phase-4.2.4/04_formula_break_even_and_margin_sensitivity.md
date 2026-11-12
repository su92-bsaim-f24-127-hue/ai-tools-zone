# Phase 4.2.4 — Master Cost Formula, Break-Even Reconciliation & Margin Sensitivity

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** Re-derivation of K-Coefficient, Break-Even Threshold Re-calculation, and Payment Channel Sensitivity  

---

## 1. Re-Derivation of the Procurement Multiplier ($K = 1.101632$)

The procurement multiplier $K$ must not be accepted as a black-box constant. It is derived from verified individual contractual and statutory parameters:

```
Let:
  r_bank    = 0.0400  (Commercial bank international card fee: 4.00%)
  r_FED     = 0.1600  (Sales tax on financial services: 16.00% applied strictly to bank fee)
  r_236Y    = 0.0050  (FBR statutory withholding tax for Active Taxpayers: 0.50%)
  r_reserve = 0.0500  (Replacement and warranty reserve provision: 5.00% on base)

Step 1: Effective Bank Fee Rate
  Bank_Factor = 1 + [r_bank * (1 + r_FED)]
              = 1 + [0.0400 * 1.1600]
              = 1 + 0.0464 = 1.046400

Step 2: Landed Cross-Border Outlay Factor (including Section 236Y)
  Landed_Factor = Bank_Factor * (1 + r_236Y)
                = 1.046400 * 1.005000
                = 1.051632

Step 3: Master Procurement Cash Factor (K_cash, ATL)
  K_cash, ATL = Landed_Factor + r_reserve
              = 1.051632 + 0.050000
              = 1.101632  (Q.E.D.)
```

For Non-ATL transactions ($r_{236Y} = 0.0100$):
$$K_{	ext{cash, Non-ATL}} = 1.046400 	imes 1.010000 + 0.050000 = 1.056864 + 0.050000 = \mathbf{1.106864}$$

For Economic Cost Basis (where Section 236Y is credited against annual income tax):
$$K_{	ext{econ, ATL}} = 1.046400 + 0.050000 = \mathbf{1.096400}$$

---

## 2. Re-Derivation of the Closed-Form Pricing Equation

Equating gross cash inflow to total cash outflow plus target cash margin ($M_{	ext{target}}$):

$$P_{	ext{retail}} - [(	ext{USD} 	imes 	ext{FX} 	imes K) + (P_{	ext{retail}} 	imes r_{	ext{gateway}}) + C_{	ext{labor}}] = P_{	ext{retail}} 	imes M_{	ext{target}}$$
$$P_{	ext{retail}} 	imes (1 - r_{	ext{gateway}} - M_{	ext{target}}) = 	ext{USD} 	imes 	ext{FX} 	imes K + C_{	ext{labor}}$$
$$P_{	ext{retail}}(M_{	ext{target}}) = rac{	ext{USD} 	imes 	ext{FX} 	imes K + C_{	ext{labor}}}{1 - r_{	ext{gateway}} - M_{	ext{target}}}$$

Where $r_{	ext{gateway}} = 0.0200$ and $C_{	ext{labor}} = 	ext{PKR } 350.00$.

---

## 3. Resolution of the Break-Even Inconsistency in Phase 4.2.3

### The Error in Phase 4.2.3:
In Phase 4.2.3, the audit recommended increasing Cursor AI Pro and Claude Pro prices to **PKR 7,400**, yet the text narrative inadvertently asserted that:
> *"The products break even at PKR 286.57 / USD."*

### Mathematical Correction:
The break-even threshold is a mathematical function of the retail price. Setting a higher retail price expands the break-even exchange rate:

$$	ext{FX}_{	ext{break-even}} = rac{P_{	ext{retail}} 	imes (1 - r_{	ext{gateway}}) - C_{	ext{labor}}}{	ext{USD} 	imes K}$$

### Re-Calculated Break-Even Rates Across Retail Price Points:

| Product | Retail Price Point | Available Procurement Fund (PKR) | Landed Multiplier ($K$) | Re-Calculated Break-Even FX Rate |
|---|:---:|:---:|:---:|:---:|
| **Cursor / Claude ($20)** | **PKR 6,800.00** (Catalog Base) | $6800 	imes 0.98 - 350 = 	ext{PKR } 6,314.00$ | $20 	imes 1.101632$ | **PKR 286.57 / USD** *(Thin Margin)* |
| Cursor / Claude ($20) | **PKR 7,320.00** (10% Target @ 276.76) | $7320 	imes 0.98 - 350 = 	ext{PKR } 6,823.60$ | $20 	imes 1.101632$ | **PKR 309.70 / USD** *(Strong Buffer)* |
| Cursor / Claude ($20) | **PKR 7,400.00** (Recommended Launch) | $7400 	imes 0.98 - 350 = 	ext{PKR } 6,902.00$ | $20 	imes 1.101632$ | **PKR 313.26 / USD** *(Robust Defense)* |
| Cursor / Claude ($20) | **PKR 7,760.00** (15% Target @ 276.76) | $7760 	imes 0.98 - 350 = 	ext{PKR } 7,254.80$ | $20 	imes 1.101632$ | **PKR 329.28 / USD** *(Premium Defense)* |
| **GitHub Copilot ($10)** | **PKR 3,800.00** (Catalog Base) | $3800 	imes 0.98 - 350 = 	ext{PKR } 3,374.00$ | $10 	imes 1.101632$ | **PKR 306.27 / USD** *(Healthy Buffer)* |
| GitHub Copilot ($10) | **PKR 3,900.00** (Recommended Launch) | $3900 	imes 0.98 - 350 = 	ext{PKR } 3,472.00$ | $10 	imes 1.101632$ | **PKR 315.17 / USD** *(Resilient)* |

> **Audit Finding:**  
> Pricing Cursor and Claude at **PKR 7,400** elevates the break-even threshold from PKR 286.57 to **PKR 313.26 / USD**, completely neutralizing currency risk up to PKR 313 / USD.

---

## 4. Sensitivity to Alternative Domestic Payment Channels

Domestic customer payment fees vary based on the collection channel used by AI Tools Zone:

| Payment Channel | Channel Fee Rate | Copilot Cash Margin @ PKR 3,800 | Cursor/Claude Cash Margin @ PKR 6,800 | Impact on Net Contribution |
|---|:---:|:---:|:---:|---|
| **Aggregator Gateway (PayMob/Safepay)** | **2.00%** | **8.56% (+PKR 325.12)** | **3.18% (+PKR 216.25)** | Baseline model assumption. |
| **Easypaisa Merchant QR / API** | **1.80%** | **8.77% (+PKR 332.72)** | **3.38% (+PKR 229.85)** | +PKR 7.60 (Copilot) / +PKR 13.60 (Cursor). |
| **JazzCash Merchant Gateway** | **1.75%** | **8.82% (+PKR 334.62)** | **3.43% (+PKR 233.25)** | +PKR 9.50 (Copilot) / +PKR 17.00 (Cursor). |
| **Direct Raast P2M / 1Link IBFT** | **0.00%** | **10.56% (+PKR 401.12)** | **5.18% (+PKR 352.25)** | **+PKR 76.00 (Copilot) / +PKR 136.00 (Cursor) pure margin expansion.** |

> **Operational Strategy:**  
> Prioritizing direct Raast bank transfers on the WhatsApp checkout channel completely eliminates the 2% gateway expense, boosting Cursor/Claude baseline cash margin from 3.18% to **5.18%** without changing consumer prices.

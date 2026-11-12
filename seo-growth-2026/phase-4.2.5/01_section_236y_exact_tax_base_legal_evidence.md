# Phase 4.2.5 — Section 236Y Exact Tax-Base Determination & Statutory Analysis

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** Statutory Construction of "Sum Remitted Outside Pakistan", Tax Base Dissection, and Legal Risk  

---

## 1. Statutory Context & Primary Legal Texts

This audit investigates the precise legal tax base for advance withholding tax on cross-border card transactions under Pakistan tax law:

### Governing Statutory Provisions:
1. **Income Tax Ordinance, 2001 — Section 236Y(1):**
   > *"Every banking company shall collect advance tax, at the time of transfer of any sum remitted outside Pakistan through credit or debit or prepaid cards, from the person whose card is used for such remittance, at the rate specified in Division XXVII of Part IV of the First Schedule."*
2. **First Schedule, Part IV, Division XXVII:**
   - **Active Taxpayers List (ATL / Filers):** **0.50%** of gross remitted amount (Finance Act 2026 / TY2027 Rate Card).
3. **Tenth Schedule, Rule 1:**
   - **Non-ATL (Inactive Taxpayers):** 100% statutory increase = **1.00%** of gross remitted amount.
4. **Section 168(1) & (3):**
   - Establishes that advance tax collected under Section 236Y is an **adjustable tax credit** against annual income tax liability.

---

## 2. Four-Way Transaction Cost Component Dissection

When an international card purchase occurs, the customer's account experiences distinct debits:

```
[Total Cardholder PKR Cash Debit]
   │
   ├─► Component A: Foreign Purchase Principal (USD Converted to PKR)
   │               --> Remitted outside Pakistan to foreign merchant.
   │
   ├─► Component B: Bank Processing Fee / Cross-Border Markup (3.50% - 4.50%)
   │               --> RETAINED IN PAKISTAN by the issuing bank as service income.
   │
   ├─► Component C: Federal Excise Duty (FED @ 16.00% on Bank Fee)
   │               --> PAID LOCALLY IN PAKISTAN to FBR / Provincial Revenue Authority.
   │
   └─► Component D: Section 236Y Advance Withholding Tax
                   --> Deducted by bank and deposited into Federal Treasury.
```

---

## 3. The Core Statutory Question: What Constitutes "Sum Remitted Outside Pakistan"?

The central legal ambiguity is whether the tax base of Section 236Y is:
- **Interpretation 1 (Strict Statutory Construction):** The foreign purchase principal alone ($P_{\text{base}}$); or
- **Interpretation 2 (Aggressive Core Banking Practice):** The entire gross debit including locally retained bank processing fees ($P_{\text{base}} + \text{Bank Fee} + \text{FED}$).

### Interpretation 1: Strict Statutory Construction (Principal Only)
- **Legal Argument:**  
  Section 236Y(1) explicitly restricts withholding to *"any sum remitted outside Pakistan"*.  
  - The bank processing fee (e.g. PKR 110.70) is retained within Pakistan by the Pakistani commercial bank as local fee income.  
  - The FED (e.g. PKR 17.71) is a domestic tax paid to provincial revenue boards (SRB, PRA, BRA) or FBR.  
  - Neither Component B nor Component C is transferred across international borders to the overseas vendor.  
  - Taxing domestic banking fees under an "advance tax on remittances outside Pakistan" is legally contradictory.
- **Tax Base:** Foreign purchase principal converted to PKR ($P_{\text{base}} = \text{USD} \times \text{FX}$).
- **Tax Withheld (Copilot @ $10.00 / 276.76):** $\text{PKR } 2,767.60 \times 0.0050 = \mathbf{PKR\ 13.84}$.

### Interpretation 2: Disputed Core Banking Practice (Gross Debit Base)
- **Banking Reality:**  
  Several Pakistani commercial banks (e.g. automated 1Link card-clearing switches) debit Section 236Y on the aggregate gross transaction block before itemizing domestic charges, calculating tax as:
  $$\text{Tax Base} = P_{\text{base}} + \text{Bank Fee} + \text{FED}$$
- **Bank Compliance Rationale:** Bank legal departments adopt an aggressive withholding stance to protect the financial institution from FBR audit penalties for under-withholding under Section 161/205.
- **Tax Base:** Gross remittance outflow ($P_{\text{base}} \times 1.0464$).
- **Tax Withheld (Copilot @ $10.00 / 276.76):** $\text{PKR } 2,896.02 \times 0.0050 = \mathbf{PKR\ 14.48}$.
- **Quantitative Delta:** **PKR 0.64 per $10 order** (or **PKR 1.28 per $20 order**).

---

## 4. Formal Legal Status & Audit Flag

> [!IMPORTANT]
> **Audit Classification: REQUIRES WRITTEN PAKISTANI TAX ADVICE**  
> While the quantitative difference between Interpretation 1 and Interpretation 2 is minimal (PKR 0.64 to PKR 1.28 per transaction), the statutory discrepancy remains unresolved by official FBR circulars.  
> Prior to scaling operations beyond the initial pilot, the business owner must obtain written confirmation from an ICAP-licensed Chartered Accountant confirming whether the merchant's corporate return should treat Section 236Y as calculated on net foreign remittance or gross card debit.

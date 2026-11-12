# Phase 4.2.2 — Authoritative FBR Section 236Y Tax Reconciliation & Cross-Border Fee Audit

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** Statutory Withholding Tax, Banking Surcharges, and Economic Cost Analysis  

---

## 1. Executive Summary & Statutory Authority

This audit establishes the definitive legal and financial basis for calculating cross-border payment costs under Pakistan tax law, resolving material errors in prior project phases.

### Primary Regulatory & Statutory Sources:
1. **Income Tax Ordinance, 2001 (Ordinance No. XLIX of 2001):**
   - **Section 236Y:** *"Advance tax on persons remitting amounts abroad through credit or debit or prepaid cards."*
   - **First Schedule, Part IV, Division XXVII:** Prescribed rates of collection for Section 236Y.
   - **Tenth Schedule, Rule 1:** Statutory mechanism for 100% tax surcharge on persons not appearing on the Active Taxpayers List (Non-ATL).
   - **Section 168 & Section 169:** Tax credit and adjustable nature of advance withholding taxes.
2. **Federal Board of Revenue (FBR) Official Withholding Tax Rate Card:**
   - **Applicable Edition:** Tax Year 2027 Withholding Tax Rates (updated through 30 June 2026), published by the FBR Directorate of Withholding Taxes (`https://www.fbr.gov.pk/`).
3. **State Bank of Pakistan (SBP) Foreign Exchange Manual (8th Edition, updated through 2026):**
   - FE Circular No. 04 / 2023 and Banking Policy & Regulations Department (BPRD) cross-border card settlement directives.

---

## 2. Official Section 236Y Statutory Tax Rates

Under **Division XXVII of Part IV of the First Schedule** of the Income Tax Ordinance, 2001:

| Taxpayer Status | Statutory Classification | Applicable Rate (TY2027 Rate Card) | Previous Historical Rate (TY2024–TY2026) |
|---|---|:---:|:---:|
| **Active Taxpayer List (ATL / Filer)** | Person whose name appears on the ATL on the date of transaction | **0.50%** | **5.00%** |
| **Non-ATL (Non-Filer)** | Person whose name does not appear on the ATL (Tenth Schedule 100% surcharge) | **1.00%** | **10.00%** |

### Legislative Chronology:
- **Finance Act, 2022:** Section 236Y introduced at 1.0% for ATL and 2.0% for Non-ATL.
- **Finance Act, 2023 (Effective 1 July 2023):** Rates increased to 5.0% for ATL and 10.0% for Non-ATL.
- **Finance Act, 2026 / Tax Year 2027 (Effective 1 July 2026):** Rationalized downward to **0.50% for ATL** and **1.00% for Non-ATL** to reduce friction on digital software imports and IT infrastructure.

---

## 3. Dissection & Rejection of the Phase 4.2.1 Assumption

In Phase 4.2.1, the financial model operated under an assumption of:
> *"5% filer tax and an additional 2.5% non-filer tax (7.5% total)"*

### Independent Statutory Verdict: **UNSUPPORTED / FABRICATED CALCULATION**
1. **Zero Statutory Precedent:** There has never been an FBR rate of 7.5% or a 2.5% surcharge under Section 236Y in the legislative history of Pakistan.
2. **Tenth Schedule Mechanics:** Under Rule 1 of the Tenth Schedule, the tax collection rate for non-filers is strictly **100% higher than the rate specified in First Schedule** (i.e. exactly 2.0× the base rate). It is never 1.5× (+2.5%).
3. **Double Error in Phase 4.2.1:**
   - It conflated the older historical 5.0% filer rate with the current TY2027 rate card (0.50%).
   - It invented a 2.5% non-filer increment that has no basis in Pakistan tax statute.

---

## 4. Disentangling Cross-Border Banking & Tax Surcharges

When a Pakistani entity remits foreign exchange abroad via an authorized commercial bank card (e.g., Meezan Bank, HBL, Bank Alfalah, Standard Chartered), the transaction incurs distinct fees that must not be lumped together:

```
Gross Customer Card Settlement = 
    Base Foreign Exchange (SBP Customer Selling Benchmark)
  + Bank Foreign Exchange Spread (3.00% – 4.00%)
  + Bank International Transaction Processing Fee
  + Provincial Sales Tax / Federal Excise Duty (FED @ 16.00% on Bank Fee)
  + Section 236Y Advance Withholding Tax (0.50% ATL or 1.00% Non-ATL)
```

### Comprehensive Component Breakdown:

| Surcharge Component | Levying Authority | Calculation Basis | Typical Commercial Rate | Accounting Classification |
|---|---|---|:---:|---|
| **1. SBP Base Benchmark** | State Bank of Pakistan | Published daily customer selling rate | SBP Spot Rate (e.g. 276.76) | Base procurement cost |
| **2. Bank FX Spread** | Commercial Bank | Spread over interbank revaluation | 3.00% to 4.00% | Direct procurement expense |
| **3. Bank Cross-Border Fee** | Card Scheme / Bank | International scheme clearance fee | Included in bank FX fee | Direct procurement expense |
| **4. FED on Bank Fee** | Provincial Revenue Authority / FBR | Sales tax on financial services | 16.00% of Bank Fee (0.64% of Base) | Irrecoverable indirect tax |
| **5. Section 236Y Tax** | FBR (Federal Govt) | Gross remitted PKR outflow | **0.50% (ATL) / 1.00% (Non-ATL)** | **Adjustable Advance Income Tax** |
| **6. Domestic Gateway Fee** | Local Payment Gateway | Collected on PKR customer receipt | 1.50% to 2.50% of Retail | Domestic operating expense |
| **7. Replacement Reserve** | Internal Policy | Modeled provision on base cost | 5.00% of Base Procurement | Internal accounting reserve |

---

## 5. Critical Distinction: Cash-Flow Impact vs. Economic Cost

A central failure of Phase 4.2.1 was treating Section 236Y advance tax as an irrecoverable margin-eroding economic cost.

### Statutory Reality:
Under **Section 168 of the Income Tax Ordinance, 2001**:
> *"Any sum deducted or collected, or purporting to be deducted or collected under this Chapter shall be treated as payment of tax on behalf of the person... and credit shall be given to him for the amount so deducted or collected in computing the tax payable by him for the tax year."*

Section 236Y is strictly an **adjustable advance tax**. It is **not** a final tax (FTR/PTR) or minimum turnover tax under Section 113.

### Financial Treatment Comparison:

| Dimension | Active Taxpayer (ATL Filer) | Non-Active Taxpayer (Non-ATL) |
|---|---|---|
| **Immediate Cash-Flow Outlay** | Bank deducts 0.50% cash at checkout. Reduces immediate working capital liquidity. | Bank deducts 1.00% cash at checkout. Greater working capital drain. |
| **Annual Tax Return Filing** | Merchant submits FBR IRIS annual return. The withheld amount directly offsets income tax payable on business net profit. | Non-filer does not submit return or maintain audited books. Cannot claim credit. |
| **Net Economic Expense** | **0.00 PKR** (Direct 1:1 tax credit against business tax liability, minus time-value of money). | **100% Deadweight Loss** (Irrecoverable forfeiture). |
| **Model Treatment** | Deducted from **Cash Margin**, credited back in **Economic Net Margin**. | Deducted from **both Cash Margin and Economic Net Margin**. |

---

## 6. Scope Clarification: Domestic PKR Transactions

Section 236Y applies **solely and exclusively** to cross-border foreign-currency remittances executed via debit, credit, or prepaid payment cards.

> **Crucial Commercial Finding:**  
> Customer purchases conducted domestically in Pakistan via **JazzCash, EasyPaisa, Raast, or 1Link IBFT** incur **0.00% Section 236Y advance tax**.  
> The tax applies only on the merchant's outward procurement leg when funding subscriptions with overseas providers in USD.

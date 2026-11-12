# DELIVERABLE 53: OFFICIAL TAX AND PAYMENT EVIDENCE REGISTER

**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Date:** 2026-11-12  
**Audit Stage:** Phase 2.2.1 — Tax & Payment Channel Reconciliation  

---

## 1. Statutory Foundation: Section 236Y of the Income Tax Ordinance, 2001

### 1.1 Legal Text & Governing Section
Section 236Y of the Income Tax Ordinance, 2001 governs the collection of advance income tax on outward foreign currency remittances executed through banking cards:
> *"Every banking company shall at the time of transfer of any sum remitted outside Pakistan through credit, debit or prepaid card collect advance tax from such person..."*

- **Statutory Authority:** Federal Board of Revenue (FBR), Government of Pakistan.
- **Governing Law:** Income Tax Ordinance, 2001, Section 236Y.
- **Enforcing Entities:** State Bank of Pakistan (SBP) licensed commercial banks and Electronic Money Institutions (EMIs).

### 1.2 Official Rate Card Evidence Register
The official tax rates published by the FBR are documented below:

| Field | Primary Evidence Record |
|---|---|
| **Governing Section** | Section 236Y, Income Tax Ordinance, 2001 |
| **Official Title** | Advance tax on persons remitting amounts abroad through credit, debit or prepaid cards |
| **Official Source URL** | `https://www.fbr.gov.pk/withholding-taxes-rate-card/174298/174301` |
| **Secondary Legal Source** | `https://www.fbr.gov.pk/` (Income Tax Ordinance, 2001 amended up to 30th June 2024 / Tax Year 2027) |
| **Verification Date** | 2026-11-12 |
| **Applicable Tax Year** | Tax Year 2027 / Current Fiscal Directives |
| **Active Taxpayer List (ATL) Rate** | **0.5%** of the gross transaction amount |
| **Non-ATL (Non-Filer) Rate** | **1.0%** (100% increased rate under the Tenth Schedule to the Ordinance) |
| **Tax Nature** | **Advance Adjustable Income Tax** (Creditable against annual income tax liability) |
| **Evidence Confidence** | **High** (Official FBR Statutory Documentation) |

---

## 2. Payment Method Applicability Matrix

Section 236Y does NOT apply to every transaction. It is strictly triggered by cross-border card payments:

| Payment Rail / Method | Applicable Section 236Y Rate | Legal Trigger / SBP Regulatory Mechanism | Commercial Assessment for AI Tools Zone |
|---|---|---|---|
| **Pakistani Bank Credit Card** | **0.5%** (ATL) / **1.0%** (Non-ATL) | Direct foreign CNP (Card-Not-Present) e-commerce transaction | SBP circular mandates automated withholding by issuing bank. |
| **Pakistani Bank Debit Card** | **0.5%** (ATL) / **1.0%** (Non-ATL) | Direct foreign CNP transaction | Deducted from linked current/savings account at transaction settlement. |
| **Prepaid EMI Card (SadaPay / NayaPay)** | **0.5%** (ATL) / **1.0%** (Non-ATL) | Direct foreign CNP transaction | Deducted from EMI wallet balance at authorization. |
| **Domestic Bank Transfer (Raast / IBFT)** | **0.0% (Exempt)** | Domestic PKR interbank clearing | Settled via SBP PRISM / Raast network; zero cross-border remittance. |
| **Mobile Wallets (JazzCash / Easypaisa)** | **0.0% (Exempt)** | Domestic PKR branchless banking | Domestic retail payment; Section 236Y does not apply. |
| **Cash on Delivery / Physical Over-the-Counter** | **0.0% (Exempt)** | Domestic currency physical transfer | Domestic transaction; Section 236Y does not apply. |
| **International Wire Transfer (SWIFT / TT)** | Governed by Section 152 | SBP Form 'M' / Foreign exchange regulations | Governed by general withholding on foreign payments, not 236Y. |
| **Foreign Subsidiary Card (Non-Pakistani)** | **0.0% (Not Subject to FBR)** | Foreign financial institution jurisdiction | Subject to foreign card issuer rules; exempt from Pakistani FBR taxes. |

---

## 3. Tax Accounting: Advance Adjustable Tax vs Operating Expense

1. **Cash Outlay vs Profit & Loss Impact:**
   - When AI Tools Zone uses a Pakistani bank card to pay $20.00 (PKR 5,535.20), the bank deducts PKR 27.68 as Section 236Y advance tax.
   - For working capital planning, cash outlay must cover PKR 5,535.20 + bank fees + PKR 27.68.
   - For accounting and tax filing, this PKR 27.68 is recorded on the balance sheet under **Advance Income Tax (Current Assets)**, NOT in the Cost of Goods Sold (COGS).
   - When filing annual tax returns with the FBR, this advance tax is fully credited against final tax liability.
2. **Non-Filer Exposure:**
   - If payments are made using a card registered to a Non-ATL entity, the tax doubles to 1.0% (PKR 55.35). Non-filers cannot claim this adjustment without filing.
   - AI Tools Zone operations must strictly utilize Active Taxpayers List (ATL) registered corporate or proprietor payment instruments.

---

## 4. Requirement for Professional Tax Review

> [!IMPORTANT]
> While the statutory rate of 0.5% under Section 236Y is verified from official FBR publications, the business owner must obtain formal advice from a licensed Pakistani tax advisor (ICAP / Institute of Taxation) regarding:
> 1. Classification of digital software concierge transactions for provincial sales tax on services (e.g., Punjab Revenue Authority PRA / Sindh Revenue Board SRB 15-16% sales tax on IT services).
> 2. Tax implications of facilitating card payments on behalf of third-party clients.
> 3. Maintenance of computerized withholding tax deduction certificates issued by the acquiring banks for annual return reconciliation.

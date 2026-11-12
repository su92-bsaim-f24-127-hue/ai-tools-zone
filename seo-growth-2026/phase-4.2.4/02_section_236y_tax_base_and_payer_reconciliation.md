# Phase 4.2.4 — Section 236Y Tax Base, Payer Identity & Statutory Reconciliation

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** Statutory Tax Base, Withholding Mechanics, and Legal vs. Commercial Policy Separation  

---

## 1. Statutory Foundations: Section 236Y & First Schedule

Under the **Income Tax Ordinance, 2001** (amended through Tax Year 2027, updated 30 June 2026):

### Primary Statutory Text:
- **Section 236Y(1):**  
  > *"Every banking company shall collect advance tax, at the time of transfer of any sum remitted outside Pakistan through credit or debit or prepaid cards, from the person whose card is used for such remittance, at the rate specified in Division XXVII of Part IV of the First Schedule."*
- **First Schedule, Part IV, Division XXVII:**  
  - **Active Taxpayers List (ATL / Filers):** **0.50%** of gross remitted amount.
- **Tenth Schedule, Rule 1:**  
  - **Non-ATL (Inactive Taxpayers):** Rate increased by 100% to **1.00%** of gross remitted amount.

---

## 2. Tax Base & Withholding Mechanics: Scenarios A, B, and C

### Scenario A — Merchant-Funded Card Procurement (Reseller Model)
- **Fulfillment Mechanism:** Customer orders on WhatsApp and pays AI Tools Zone in PKR domestically (JazzCash/Easypaisa/Raast). AI Tools Zone uses its own business debit/credit card to pay the overseas software vendor in USD.
- **Legal Cardholder & Taxpayer:** AI Tools Zone (the merchant entity or business owner).
- **Withholding Agent:** The merchant's Pakistani commercial bank.
- **Applicable Tax Base:** The gross PKR amount debited from the merchant's account for the foreign remittance (Principal + Bank Fee).
- **Statutory Rate Applied:** Determined **exclusively** by the merchant's standing on the Active Taxpayers List (0.50% for ATL; 1.00% for Non-ATL).
- **Customer Role:** Zero statutory tax involvement. SBP and FBR regulations hold the cardholder liable for Section 236Y, not the downstream recipient of a domestic digital service.

### Scenario B — Customer-Funded Card Procurement (Pure Concierge Setup)
- **Fulfillment Mechanism:** Customer sits at their own browser; AI Tools Zone guides them to enter the customer's own Pakistani card directly into the provider's checkout. AI Tools Zone collects only a domestic setup/consulting fee in PKR.
- **Legal Cardholder & Taxpayer:** The customer.
- **Withholding Agent:** The customer's issuing bank.
- **Applicable Tax Base:** The exact subscription amount billed by the provider to the customer's card.
- **Statutory Rate Applied:** Determined by the customer's CNIC standing on the ATL (0.50% or 1.00%).
- **AI Tools Zone Role:** AI Tools Zone executes zero foreign exchange transfer. Its Section 236Y tax liability is **PKR 0.00**.

### Scenario C — Domestic PKR Payment Collection
- **Fulfillment Mechanism:** Customer transfers retail price to AI Tools Zone via Raast, 1Link IBFT, JazzCash, or Easypaisa.
- **Statutory Reality:** Section 236Y applies **strictly to cross-border remittances remitted abroad**. Domestic PKR banking and wallet transfers attract **0.00% Section 236Y tax**.
- **Operating Expense:** Domestic gateway fees (1.50%–2.00% aggregator fee or PKR 0.00 on direct Raast) are local operational overhead, completely distinct from statutory cross-border taxes.

---

## 3. Statutory Adjustability vs. Commercial Sunk Cost

A critical distinction must be maintained between tax law and internal pricing policy:

### Statutory Adjustability (Section 168):
- Under Section 168 of the Income Tax Ordinance, 2001, advance tax collected under Section 236Y is an **adjustable tax credit**.
- When an active taxpayer files their annual corporate or individual income tax return (Form 114), the entire withheld amount directly offsets income tax payable on business profits. Rupee-for-rupee, the net economic expense is **PKR 0.00** (discounting the time-value of money).
- If an inactive taxpayer (Non-ATL) has tax deducted at 1.00%, the tax is **not legally lost forever**. When they file their return (and pay the Tenth Schedule Rule 2 late-filing restoration surcharge: PKR 1,000 for individuals), the FBR IRIS e-filing portal automatically credits the entire withheld amount against assessed tax liability.

### Internal Business Pricing Prudence:
- Although Section 236Y is legally adjustable, it represents an **immediate cash deduction** at the bank terminal that drains working capital at checkout.
- Therefore, in business pricing, the merchant must cover this cash outflow within its gross cash collection, while recognizing the tax credit in its annual audited financial statements.

---

## 4. Formal Legal Disclaimer & Audit Flags

> [!IMPORTANT]
> **Tax Professional Confirmation Flag:**  
> The tax interpretations set forth herein are based on primary statutory texts of the Income Tax Ordinance, 2001, and the official FBR Tax Year 2027 Withholding Tax Rate Card.  
> Prior to scaling operations beyond the initial pilot, the business owner should obtain formal written confirmation from a licensed Pakistani Chartered Accountant (ICAP) verifying the corporate entity's ability to adjust Section 236Y credits against commercial software trading turnover.

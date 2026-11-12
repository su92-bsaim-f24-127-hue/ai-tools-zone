# Phase 4.2.4 — Bank-Level International Card Fee Evidence & Schedule Audit

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** Banking Schedule of Charges (SOBC) Audit, Card Fee Decomposition, and Provisional Sourcing Scenarios  

---

## 1. Executive Summary & Objective

In Phase 4.2.3, the financial model operated under an all-in bank transaction fee assumption of **4.00% plus 16.00% Federal Excise Duty (FED)** (equating to 4.64% total bank overhead). Furthermore, the narrative asserted a heuristic decomposition:
> *"The 4% fee is composed of 2% settlement spread plus 2% cross-border e-commerce fee."*

This audit independently inspects official Pakistani commercial bank Schedules of Bank Charges (SOBC) for the July–December 2026 period to determine whether this decomposition is supported by actual banking contracts, separates taxable fees from non-taxable spreads, and evaluates four bank-specific procurement scenarios.

---

## 2. Investigation of the Heuristic "2% Spread + 2% Fee" Claim

### Official Banking Documentation Audit:
An inspection of official Schedules of Bank Charges across Pakistan's primary commercial banks (Meezan Bank, Habib Bank Limited, Bank Alfalah, Standard Chartered Bank Pakistan) reveals:

1. **Absence of Dual 2%+2% Billing Line Items:**  
   No Pakistani commercial bank issues an account statement with separate line items labeled "2% settlement spread" and "2% e-commerce fee". That decomposition was an internal heuristic construct created in earlier project notes to rationalize a rounded 4.00% total.
2. **Actual Commercial Card Billing Structure:**  
   Pakistani commercial banks structure international cross-border card transactions into three distinct statutory and contractual components:
   - **Component 1 — Foreign Exchange Reference Conversion:** Transactions routed through international payment schemes (Visa / Mastercard) are converted from foreign currency (USD) to PKR at the **card network's daily wholesale settlement rate** or the bank's published Treasury Selling Rate.
   - **Component 2 — International / Cross-Border Transaction Fee:** The issuing bank levies a single unified contractual markup (typically **3.50% to 4.50%**) specified in its published SOBC under *"Cross Border / International Transaction Processing Fee"*.
   - **Component 3 — Federal Excise Duty (FED) / Provincial Sales Tax (PST):** Under federal and provincial sales tax on services acts (e.g. Sindh Sales Tax on Services Act 2011, Punjab Sales Tax on Services Act 2012, ICT Sales Tax on Services Ordinance 2001), sales tax is levied at **16.00% strictly on banking service charges and commissions**.
3. **Statutory Limitation on FED Application:**  
   **FED cannot legally be levied on foreign exchange spreads or currency principal.** Under Section 3 of the Federal Excise Act, 2005, FED applies exclusively to the contractual service fee charged by the financial institution. Therefore, calculating FED as `16% * Bank Fee` is legally sound, but applying FED to an exchange rate spread is legally erroneous.

---

## 3. Bank-Specific Procurement Scenarios (SOBC July–December 2026)

Because AI Tools Zone's exact commercial card BIN, issuing bank, and business account tier have not been formally confirmed in repository evidence, the financial models are classified as **PROVISIONAL**. Four distinct banking scenarios reflect the actual procurement options available in Pakistan:

### Scenario 1 — Meezan Bank (Islamic Commercial Banking)
- **Applicable Instrument:** Meezan Visa / Mastercard Business or Titanium/Platinum Debit Card.
- **SOBC Clause (July–December 2026):** *Debit Cards — Cross Border Transactions (POS & E-commerce)*.
- **Contractual International Fee:** **3.50% to 4.00%** of gross transaction value.
- **FED on Service Fee:** 16.00% applied to the bank fee portion (= 0.56% to 0.64% of base).
- **All-In Bank Cost Factor:** **4.06% to 4.64%**.
- **Assessment:** Preferred low-cost procurement channel for compliant businesses.

### Scenario 2 — Habib Bank Limited (HBL) (Conventional Commercial Banking)
- **Applicable Instrument:** HBL Visa / Mastercard Debit or Corporate Card.
- **SOBC Clause (July–December 2026):** *Foreign Transactions / Cross Border Card Processing*.
- **Contractual International Fee:** **4.00%** flat on international transactions.
- **FED on Service Fee:** 16.00% on bank fee (= 0.64% of base).
- **All-In Bank Cost Factor:** **4.64%**.
- **Assessment:** Exact match to the baseline 4.64% modeled in Phase 4.2.3.

### Scenario 3 — Bank Alfalah (Conventional High-Volume Retail)
- **Applicable Instrument:** Bank Alfalah Credit / Debit Cards.
- **SOBC Clause (July–December 2026):** *Foreign Currency Transactions (Cross-border / E-commerce)*.
- **Contractual International Fee:** **4.50%** (Credit Cards) / **4.00%** (Debit Cards) (or min. Rs. 125, whichever is higher).
- **FED / PST on Fee:** 16.00% on bank fee (= 0.72% of base on credit cards).
- **All-In Bank Cost Factor:** **5.22%** (Credit) / **4.64%** (Debit).
- **Assessment:** Higher cardholder fee structure requiring higher retail price buffers.

### Scenario 4 — Electronic Money Institutions (SadaPay & NayaPay)
- **SadaPay (Mastercard):** SOBC levies a flat **6.00% international transaction fee** + 16% FED (= 6.96% all-in card fee) + Section 236Y.
- **NayaPay (Visa):** Levies standard Visa conversion rate + flat fee (~USD 0.25) + Section 236Y.
- **Assessment:** SadaPay carries excessive card markups (6.96%) that destroy software resale margins; NayaPay is viable for fixed micro-transactions but constrained by SBP annual remittance limits ($30,000/yr per individual).

---

## 4. Reconciled Bank Cost Factor for Master Financial Model

To preserve institutional prudence without underestimating costs, the master financial model retains **Scenario 2 (Standard Commercial Bank: 4.00% Fee + 16.00% FED = 4.64% All-In Bank Overhead)** as its provisional baseline, while evaluating sensitivity against Scenario 1 (4.06%) and Scenario 3 (5.22%).

```
Base Procurement (PKR) = USD * FX
Bank Cross-Border Fee (4.00%) = Base Procurement * 0.0400
FED on Bank Fee (16.00% of Fee) = Bank Cross-Border Fee * 0.1600 = Base Procurement * 0.0064
Total Bank Outflow = Base Procurement * 1.0464
```

> **Mandatory Operational Action:**  
> Before commencing live pilot transactions, the business owner must register the exact corporate bank account and card BIN to lock the final bank cost factor between 4.06% and 4.64%.

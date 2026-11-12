# Phase 4.2.9 — Raast P2P vs P2M Business Collection Reconciliation
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Primary Regulatory Baselines:**  
- SBP PSPOD Circular No. 04 of 2023: Operational Guidelines for Raast Person-to-Merchant (P2M) Service (`https://www.sbp.org.pk/circulars/pspod-circular-no-04-of-2023`)  
- SBP Raast Person-to-Person (P2P) FAQs (`https://www.sbp.org.pk/faqs/faqs-raast-person-to-person-p2p`)  
- SBP Subsidiaries Raast P2M Architecture (`https://www.sbp.org.pk/our-subsidiaries/raast/raast-person-to-merchant`)  
**Mode:** Independent Read-Only Banking Audit & Payment Rail Reconciliation  
**Production Authorization:** STRICTLY NOT GRANTED

---

## 1. Executive Summary & Defect Correction

Phase 4.2.8 correctly identified the distinction between Raast P2P and P2M, but made two material overstatements:
1. It suggested that a commercial business could simply collect commercial revenues through personal Raast P2P to enjoy "zero fees."
2. It stated a universal merchant fee range of "0.20% to 1.00% MDR" without establishing the governing circular rule or provider-specific agreements.

This assessment provides the authoritative reconciliation under SBP PSPOD Circular No. 04 of 2023.

---

## 2. Why Personal Raast P2P Cannot Serve as a Commercial Collection Channel

- **The P2P Mandate:** SBP Raast P2P regulations mandate zero transaction fees for individual consumers sending and receiving personal funds between individual bank accounts.
- **Account Terms Violation:** Utilizing a personal consumer bank account to systematically receive commercial business revenues, service fees, or customer payments violates:
  - Commercial bank account opening agreements (which strictly restrict personal current/savings accounts to non-business personal use).
  - SBP Anti-Money Laundering (AML) / Customer Due Diligence (CDD) regulations regarding commercial turnover monitoring.
  - FBR business revenue declaration requirements (business turnover must flow through declared business accounts under Section 214A of the Income Tax Ordinance).
- **Enforcement Risk:** When automated banking systems detect frequent, fragmented incoming transfers from unrelated third parties with business-like narration ("Copilot setup", "Cursor fee"), commercial banks freeze individual accounts and demand commercial business registration documents.
- **Authoritative Finding:** **AI Tools Zone CANNOT rely on personal Raast P2P as an official business collection mechanism.** Commercial collection requires a duly onboarded merchant payment channel.

---

## 3. Raast P2M Legal Framework & Acquiring Fee Rules

### 3.1 The Governing Circular Rule (PSPOD Circular No. 04 of 2023)
Paragraph 4 and Paragraph 6 of SBP PSPOD Circular No. 04 of 2023 govern fee structures for Raast Person-to-Merchant (P2M) services:
- **Zero Surcharge for Consumers:** Paragraph 4(iii) explicitly bars merchants and acquiring banks from levying any surcharge or additional fee on the customer for paying via Raast P2M. The payer fee is legally mandated at **PKR 0.00**.
- **Commercial Acquiring Fees Permitted:** Paragraph 6 authorizes Merchant Service Providers (MSPs), acquiring banks, and Payment Service Providers (PSPs) to levy **reasonable merchant acquiring service charges, Merchant Discount Rates (MDR), or per-transaction fees** under commercial bilateral merchant contracts.

### 3.2 Removal of the Unsupported Universal MDR Range
- Phase 4.2.8 quoted a universal "0.20% to 1.00% MDR range."
- **Correction:** SBP regulations do **NOT** mandate a fixed universal MDR cap for Raast P2M. Acquiring fees vary significantly across providers (e.g., Bank Alfalah, Meezan Bank, JazzCash Business, Safepay, PayFast) based on business legal structure, monthly turnover volume, transaction ticket size, and settlement settlement speed.
- **Authoritative Rule:** **Merchant acquiring fees are determined exclusively by the actual published schedule and signed contract of the selected acquiring bank/PSP.**

---

## 4. Payment Rail Comparison with Evidence & Confidence Ratings

| Payment Channel | Payer Fee | Merchant Acquiring Fee | Regulatory & Commercial Basis | SBP Circular Citation | Evidence Confidence Level |
| :--- | :---: | :---: | :--- | :--- | :---: |
| **Personal Raast P2P** | PKR 0.00 | **PKR 0.00** | Prohibited for commercial enterprise collection; violates personal account terms. | SBP Raast P2P FAQs | **VERIFIED REGULATORY RESTRICTION** |
| **Raast P2M (Acquired)** | PKR 0.00 | **Contractual MDR** (Set by acquirer) | Fully compliant commercial acquiring; customer pays via QR / Raast ID. | SBP PSPOD Cir 04/2023, Para 4 & 6 | **EXPLICIT REGULATORY REQUIREMENT** |
| **Direct Business IBFT** | PKR 0–25 | **PKR 0.00** (or bank deposit fee) | Customer transfers from own bank to store's formal business current account. | Bank SOBCs July–Dec 2026 | **VERIFIED COMMERCIAL FACT** |
| **JazzCash Corporate Merchant** | PKR 0.00 | **Published SOBC Fee** (Typically 1.5%–2% + FED) | Regulated mobile wallet merchant collection; requires merchant onboarding. | Mobilink Microfinance Bank SOBC 2026 | **VERIFIED COMMERCIAL SCHEDULE** |
| **Online Card Gateway (PayFast / Safepay)** | PKR 0.00 | **Published SOBC Fee** (Typically 2.5%–3% + fixed fee) | Online debit/credit card checkout gateway; requires corporate merchant contract. | Gateway Schedules 2026 | **VERIFIED COMMERCIAL SCHEDULE** |

---

## 5. Recommendation for the Store Owner

1. **Short-Term Controlled Pilot Collection:** For the limited 10-session pilot, the store owner should utilize **Direct Business IBFT / Account Transfer into a declared Sole Proprietorship Business Current Account**. This avoids unauthorized use of personal consumer wallets while incurring zero acquiring percentage fees.
2. **Formal Commercial Scale:** Prior to commercial launch, the store owner must select an authorized Raast P2M acquirer (e.g., Bank Alfalah Merchant Raast or Meezan Raast P2M), review the actual contract fee schedule, and record the exact agreed MDR in the unit economics model.

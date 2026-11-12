# Phase 4.2.8 — Raast P2P vs P2M Fee Architecture & Payment Rail Reconciliation
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Primary Regulatory Baselines:**  
- SBP Raast Person-to-Person (P2P) FAQs (`https://www.sbp.org.pk/faqs/faqs-raast-person-to-person-p2p`)  
- SBP PSPOD Circular No. 04 of 2023 (`https://www.sbp.org.pk/circulars/pspod-circular-no-04-of-2023`)  
- SBP Raast Person-to-Merchant (P2M) Architecture (`https://www.sbp.org.pk/our-subsidiaries/raast/raast-person-to-merchant`)  
**Mode:** Independent Read-Only Financial & Banking Reconciliation  
**Production Authorization:** STRICTLY NOT GRANTED

---

## 1. Executive Summary & Root Cause of Phase 4.2.7 Flaw

Phase 4.2.7 assumed a "universal 0.00% fee" for domestic payments by citing SBP's Raast initiative. This was an overstatement resulting from conflating **Raast Person-to-Person (P2P)** with **Raast Person-to-Merchant (P2M)**:
- **Raast P2P** is free for individual senders and recipients under SBP mandate.
- **Raast P2M** operates under a separate acquiring framework (PSPOD Circular No. 04 of 2023) where acquiring banks, Payment Service Operators (PSOs), and Payment Service Providers (PSPs) may charge merchant discount rates (MDR), integration fees, or transaction fees.

---

## 2. Separation of Raast P2P vs Raast P2M

### 2.1 Raast Person-to-Person (P2P)
- **Governing Mandate:** SBP Raast P2P Directives.
- **Customer / Sender Fee:** **PKR 0.00 (Free)**. Banks are legally barred from levying transaction fees on P2P Raast transfers.
- **Recipient Fee:** **PKR 0.00 (Free)** for individual account holders receiving funds via Raast ID (mobile number) or IBAN.
- **Operational Reality for AI Tools Zone:** If the store owner receives consulting fees into an individual business account via Raast P2P (customer inputs owner's Raast ID / mobile number), the transaction is **100% free of processing fees**.
- **Limitation:** High transaction volumes on an individual account can trigger bank AML queries if not registered as a commercial business account.

### 2.2 Raast Person-to-Merchant (P2M)
- **Governing Mandate:** SBP PSPOD Circular No. 04 of 2023 (Operational Guidelines for Raast P2M).
- **Architecture:** Enables formal merchants to accept payments via dynamic/static QR codes, Request-to-Pay (RTP), and Raast Merchant IDs integrated with billing systems.
- **Customer / Payer Fee:** **PKR 0.00 (Free)**. SBP mandates that customers pay zero surcharge for utilizing Raast P2M.
- **Merchant Acquiring Fees:** SBP regulations permit acquiring banks and licensed PSPs/PSOs to levy a **Merchant Discount Rate (MDR)**. While SBP has encouraged low-cost acquiring during rollout, commercial acquiring contracts typically specify an MDR ranging from **0.20% to 1.00% + Provincial Sales Tax / FED**, or a fixed per-transaction fee.
- **Subsidy Status:** Any zero-fee P2M merchant acquiring promotion offered by specific commercial banks or fintechs is a **time-limited promotional subsidy**, not an eternal statutory guarantee.

---

## 3. Domestic Payment Channel Comparison Matrix

The table below provides a reconciled comparison of domestic collection channels for AI Tools Zone's consulting fee:

| Domestic Payment Channel | Payer Fee | Merchant Acquiring Fee | Settlement Time | Source Authority & Document | Evidence Confidence Level | Pilot Recommendation |
| :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| **Raast P2P Transfer** | PKR 0.00 | **PKR 0.00** | Instant | SBP Raast P2P FAQs | **VERIFIED FACT** | **PRIMARY PILOT RAIL** (Manual verification via WhatsApp screenshot). |
| **Direct 1LINK IBFT** | PKR 0–25 | **PKR 0.00** | Instant | Commercial Bank SOBCs 2026 | **VERIFIED FACT** | **BACKUP PILOT RAIL** (Bank-to-bank transfer). |
| **Raast P2M (Acquired)** | PKR 0.00 | **0.20% to 1.00% MDR** | Instant / T+1 | SBP PSPOD Cir 04/2023 | **CONDITIONAL REGULATORY** | **POST-PILOT SCALE** (Requires merchant acquiring contract). |
| **JazzCash Merchant** | PKR 0.00 | **1.50% to 2.00% + FED** | T+1 Day | JazzCash Merchant SOBC 2026 | **VERIFIED COMMERCIAL** | **OPTIONAL CONVENIENCE** (Higher fee buffer required). |
| **Easypaisa Merchant** | PKR 0.00 | **1.50% to 2.00% + FED** | T+1 Day | Easypaisa Merchant SOBC 2026 | **VERIFIED COMMERCIAL** | **OPTIONAL CONVENIENCE** (Higher fee buffer required). |
| **Online Card Gateway (PayFast / Safepay)** | PKR 0.00 | **2.50%–3.00% + PKR 15** | T+2 to T+3 | Gateway Fee Schedules 2026 | **VERIFIED COMMERCIAL** | **NOT RECOMMENDED** (Excessive cost and settlement lag). |

---

## 4. Unit Economics Fee Policy for Phase 4.2.8

To ensure financial prudence, the unit economics model must NOT assume a zero-cost collection channel:
- **Baseline Planning Assumption:** Maintain a **2.00% payment collection buffer (PKR 10.00 on Tier 1; PKR 20.00 on Tier 2)** in baseline financial models to absorb potential merchant wallet or acquiring fees.
- **Upside Sensitivity:** Model the **0.00% Raast P2P scenario** as an explicit positive variance sensitivity, adding PKR 10.00 to Tier 1 and PKR 20.00 to Tier 2 operating contributions.

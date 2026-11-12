# Phase 4.2.7 — Evidence Register & Unresolved Evidence Log
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Classification:** Evidence Audit & Uncertainty Register  
**Production Authorization:** STRICTLY NOT GRANTED  
**Commercial Pilot Authorization:** STRICTLY NOT GRANTED

---

## 1. Categorized Evidence Register

### Category A: Verified Facts (Supported by Authoritative Primary Documents)
- **FBR ITO 2001 Section 236Y Rates:** Division XXVII, Part IV of First Schedule & Tenth Schedule confirm 0.50% ATL rate and 1.00% Non-ATL rate.
- **Anthropic Supported Country Status:** Pakistan is officially supported by Anthropic for direct user registration and payment.
- **Anysphere Anti-Resale Clauses:** Section 3 of Anysphere Terms of Service explicitly bars renting, leasing, lending, or selling the service.
- **Anthropic Consumer Restrictions:** Section 2 of Anthropic Consumer Terms prohibits reselling or sharing account credentials.
- **SBP Personal Card Restrictions:** Consumer credit/debit cards and personal EMI wallets are legally restricted to personal/household consumption.
- **Domestic Raast Fee:** SBP national mandate confirms 0.00% transaction fee on Raast P2P and merchant transfers.
- **Production Baseline Alignment:** Git commit `a09b8c42dfc17c4810bdac2813f9615b737bdd8a` is verified byte-identical against production catalog.

### Category B: Legal & Contractual Interpretations (Reasoned Analysis)
- **Section 236Y Statutory Tax Base:** Text refers to "sum remitted outside Pakistan". Domestic bank fees and FED are not remitted abroad. However, automated core banking withholds on gross debits (`REQUIRES WRITTEN PAKISTANI TAX ADVICE`).
- **Consulting vs Resale Boundary:** Providing IDE configuration and prompt engineering without handling credentials or subscriptions is legally independent consulting, not software resale.
- **Customer Email Fallacy:** Sponsoring a customer's personal email via a merchant-owned card remains an unauthorized proxy purchase; it does not grant resale rights.

### Category C: Planning Assumptions (Internal Operational Estimates)
- **Technician Labor Timing:** Estimated at 20 minutes for Tier 1 and 45 minutes for Tier 2 based on preliminary SOP analysis.
- **Technician Base Rate:** Modeled at PKR 600/hr (PKR 10/min) direct labor cost.
- **CAC Allocation:** Estimated at PKR 50.00 (Tier 1) and PKR 100.00 (Tier 2) for inbound WhatsApp acquisition.
- **Support Chat Overhead:** Estimated at PKR 50.00 (Tier 1) and PKR 75.00 (Tier 2).
- **Rework / Refund Provision:** Estimated at 5.0% of gross consulting fee.

### Category D: Unresolved Questions (Require External Resolution)
- **UNR-01: Customer Card International Failure Rate:** Empirical testing needed to determine exact percentage of Pakistani cards rejected by Stripe/vendor checkouts.
- **UNR-02: Commercial Card Documentation for Sole Proprietor:** Bank-by-bank verification required for Sole Proprietorship corporate debit card requirements.
- **UNR-03: Microsoft Partner Network Onboarding:** Verification of CSP indirect reseller status if volume licensing is pursued in the future.
- **UNR-04: Written Tax Opinion on Section 236Y Base:** Formal inquiry required to confirm whether gross withholding can be legally contested or adjusted.

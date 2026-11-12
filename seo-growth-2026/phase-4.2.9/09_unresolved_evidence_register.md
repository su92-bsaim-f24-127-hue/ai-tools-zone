# Phase 4.2.9 — Master Unresolved Evidence Register
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Mode:** Master Evidence Log & Risk Audit  
**Production Authorization:** STRICTLY NOT GRANTED

---

## 1. Categorized Evidence Register

### Category A: Verified Primary Regulatory & Statutory Evidence
- **SBP FE Circular No. 07 of 2022 (Para 2):** Annual USD 30,000 card limit is calculated on a year running strictly from **November 01 to October 31 of the next year**, NOT a calendar year.
- **SBP FE Circular No. 07 of 2022 (Para 3):** Banks must perform ongoing due diligence to ensure payments are for legitimate personal needs and have no commercial purpose.
- **SBP PSPOD Circular No. 04 of 2023:** Raast P2M framework mandates 0.00% surcharge on consumers, but permits Merchant Service Providers to contractually charge merchants an MDR.
- **FBR ITO 2001 Section 236Y:** First Schedule Div XXVII & Tenth Schedule confirm 0.50% ATL rate and 1.00% Non-ATL rate for card-based foreign remittances.
- **Anysphere Terms of Service Sec 3:** Explicitly prohibits renting, leasing, lending, or selling the service.
- **Anthropic Consumer Terms Sec 2:** Explicitly prohibits reselling services or sharing account credentials.
- **Anthropic Supported Country Schedule:** Confirms Pakistan is officially supported for consumer accounts.
- **Production Baseline Alignment:** Git commit `a09b8c42dfc17c4810bdac2813f9615b737bdd8a` verified byte-identical against production catalog.

### Category B: Regulatory & Contractual Interpretations
- **Freelancer Card Use Ambiguity:** Professional freelance software development sits in a regulatory grey area between personal digital consumption and commercial business expenditure.
- **Independent Consulting Boundary:** Providing environment setup, `.cursorrules`, and prompt training without handling credentials or subscriptions is independent technical consulting (`NOT IDENTIFIED AS PROHIBITED IN REVIEWED TERMS`).
- **Customer Email Isolation:** Sponsoring a customer's personal email via a merchant card remains an unauthorized proxy purchase; customer ownership does not authorize third-party card funding.

### Category C: Planning Assumptions
- **Technician Base Labor Rate:** Modeled at PKR 600.00/hour (PKR 10.00/minute).
- **Customer Acquisition Cost (CAC):** Modeled at PKR 50.00 (Tier 1) and PKR 100.00 (Tier 2) via inbound WhatsApp.
- **Domestic Payment Collection Buffer:** Modeled conservatively at 2.00% of gross revenue (PKR 10.00 Tier 1; PKR 20.00 Tier 2).
- **Post-Delivery Support Chat:** Modeled at PKR 50.00 (Tier 1) and PKR 75.00 (Tier 2).
- **Refund & Rework Provision:** Modeled at 5.00% of gross consulting fee.

### Category D: Unresolved Questions Requiring External / Owner Action
- **UNR-01: Pilot Card Decline Frequency:** Empirical failure rate of Pakistani consumer cards at provider Stripe checkouts must be recorded during the 10-session pilot.
- **UNR-02: Sole Proprietor Corporate Card Underwriting:** Specific commercial card underwriting terms must be confirmed with store bank if merchant-funded corporate procurement is ever pursued.
- **UNR-03: Formal Raast P2M Commercial Contract:** Exact acquiring MDR schedule must be negotiated with a licensed bank/PSP prior to formal public scale.
- **UNR-04: Section 236Y Gross Withholding Advice:** Written tax opinion required if merchant ever resumes cross-border corporate procurement.

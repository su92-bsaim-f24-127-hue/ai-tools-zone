# Phase 4.2.4 — Unresolved Evidence Register & Operational Boundaries

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** Inventory of Material Uncertainties, Evidence Gaps, and Owner Action Items  

---

## 1. Unresolved Sourcing & Banking Evidence

| Item ID | Category | Material Uncertainty | Current Impact | Evidence Needed to Resolve | Owner Action Required |
|---|---|---|---|---|---|
| **E-01** | **Procurement Bank & Card BIN** | The exact commercial card BIN and issuing bank (Meezan, HBL, Bank Alfalah) have not been confirmed in repository records. | Financial models are classified as **PROVISIONAL** (bank fee ranges from 4.06% to 5.22%). | Redacted bank card statement or schedule confirming exact card type and international fee. | Confirm primary procurement card and issuing bank to lock baseline model factor. |
| **E-02** | **Tax Adjustability Written Legal Opinion** | Section 236Y adjustability is clear statutorily, but corporate tax filing readiness of the merchant entity is unverified. | Working capital drain must be absorbed; tax refund credit depends on return filing. | Written confirmation from licensed Pakistani Chartered Accountant (ICAP). | Engage tax counsel to confirm corporate return filing procedures under Section 114. |
| **E-03** | **Anysphere (Cursor) Corporate Sponsoring Policy** | Sponsoring developer seats via concierge card is not covered by formal reseller agreement. | Risk of automated fraud block if multiple developer seats are paid by one card. | Direct response from Anysphere support regarding third-party payment concierge. | Submit written inquiry to `support@anysphere.co` regarding corporate card proxy billing. |
| **E-04** | **Anthropic (Claude) Proxy Billing Policy** | Consumer terms prohibit reselling; third-party concierge billing is technically functional but contractually unformalized. | Account suspension risk if flagged as commercial resale. | Formal written clarification from Anthropic on educational/concierge billing. | Submit inquiry to Anthropic sales regarding authorized workspace agency billing. |
| **E-05** | **n8n Sustainable Use License Commercial Agreement** | Selling hosted Docker instances on managed VPS breaches n8n SUL without Enterprise/Embed license. | `n8n-starter` must remain on commercial hold. | Commercial quote and license terms from `license@n8n.io`. | Either contact n8n for commercial license or pivot to Customer-Owned Cloud Setup. |
| **E-06** | **Netflix Concierge Customer Willingness** | Transitioning from PKR 400 shared profiles to PKR 500 concierge setup (where customer pays Netflix Rs 450/800 direct) changes customer value proposition. | Commercial conversion rate on pure setup assistance is unmeasured. | Controlled WhatsApp inquiry test offering setup assistance. | Authorize testing of concierge messaging on customer support channel. |

---

## 2. Risk Boundaries Prior to Live Execution

1. **Catalog Immutability:** No catalog items or prices may be changed in `data/catalog.json` until Items E-01 through E-05 are addressed.
2. **Staging Protection:** All Group A staged pages must remain sealed with `<meta name="robots" content="noindex, nofollow"/>`.
3. **No Commercial Releases:** Production deployment remains strictly prohibited.

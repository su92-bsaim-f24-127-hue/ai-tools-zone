# Phase 4.2.5 — GitHub Copilot Commercial Workflow & Terms Audit

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** GitHub Customer Agreement, Copilot Product Terms, and Agency Sponsoring Evaluation  

---

## 1. Provider Product Structure & Terms Analysis

### Primary Legal Sources:
1. **GitHub Customer Agreement:** (`https://docs.github.com/en/site-policy/github-terms/github-customer-agreement`)
2. **GitHub Terms for Additional Products — GitHub Copilot:** (`https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#github-copilot`)

### Product Tiers:
- **Copilot Individual ($10.00 / month):** Personal subscription bound to a personal GitHub account (`github.com/username`). Intended strictly for personal developer use.
- **Copilot Business ($19.00 / user / month):** Managed seats centrally billed to a GitHub Organization or Enterprise account.
- **Copilot Enterprise ($39.00 / user / month):** Enterprise-grade security, custom models, and audit logs.

---

## 2. Evaluation of the Five Operational Models for GitHub Copilot

| Operational Model | Operational Description | Account & Credential Control | Data & Repository Visibility | Provider Terms Compliance | Pilot Eligibility Classification |
|---|---|---|---|---|:---:|
| **Model A: Standalone Retail Resale** | Merchant buys Copilot Individual and resells login to third party. | Merchant owns credentials; customer uses merchant login. | Severe privacy leak. | Direct breach of GitHub account sharing prohibition. | **NOT PERMITTED UNDER CURRENT EVIDENCE** |
| **Model B: Organization Seat Sponsoring** | Merchant creates GitHub Organization, subscribes to Copilot Business, and assigns seats to customer GitHub handles. | Customer retains 100% control of personal GitHub account; Merchant is Org Admin. | Org admin controls seat allocation, but cannot inspect customer's private repositories or local IDE code. | Standard for agency contractor management; however, publicly reselling seats to unvetted retail consumers requires Microsoft CSP partner status. | **REQUIRES COMMERCIAL LICENSE OR RESELLER AGREEMENT** |
| **Model C: Proxy Card Payment on Individual Account** | Customer creates personal GitHub account; merchant inputs card details into customer billing. | Customer controls GitHub account; merchant funds card. | Private code execution. | High risk of automated Stripe/Microsoft risk flagging for repeated proxy card billing. | **UNRESOLVED / HIGH RISK** |
| **Model D: Customer-Funded Direct Setup Service** | Customer enters own card at GitHub checkout; AI Tools Zone charges PKR 500 setup labor to configure VS Code extension and environment. | Customer owns account, card, and billing. | 100% isolated. | **100% COMPLIANT**. Legitimate technical support and onboarding service. | **PERMITTED CUSTOMER-FUNDED SETUP SERVICE** |
| **Model E: Pure Technical Advisory** | AI Tools Zone provides educational prompt engineering and Copilot documentation. | Customer self-manages. | 100% isolated. | **100% COMPLIANT**. | **PERMITTED CUSTOMER-FUNDED SETUP SERVICE** |

---

## 3. Governance Conclusion for GitHub Copilot

- For merchant-funded resale (Model B / Model C), the service is classified as **`REQUIRES COMMERCIAL LICENSE OR RESELLER AGREEMENT`**.
- For customer-funded setup assistance (Model D), the service is classified as **`PERMITTED CUSTOMER-FUNDED SETUP SERVICE`**.

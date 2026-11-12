# DELIVERABLE 57: CUSTOMER OWNERSHIP, PRIVACY AND REFUND RISK UPDATE

**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Date:** 2026-11-12  
**Audit Stage:** Phase 2.2.1 — Operational Governance & Risk Audit  

---

## 1. The 11 Core Operational and Privacy Governance Questions

Before any candidate can be considered for commercial operations, it must satisfy the 11 foundational questions below:

### 1. Who owns the account?
- **Standard:** The customer must be the sole legal owner of the account whenever personal data, proprietary code, or confidential text is processed.
- **Rule:** For Claude Pro, Cursor, and Grammarly, accounts must be created directly by the customer using their own personal/business email. AI Tools Zone must NOT maintain primary ownership of customer accounts.

### 2. Who controls recovery email and MFA?
- **Standard:** The customer must retain 100% control over the primary recovery email and Multi-Factor Authentication (MFA) credentials.
- **Rule:** Sellers must never attach their own phone numbers or recovery emails to customer accounts.

### 3. Who can access customer data?
- **Standard:** Strict zero-data-access architecture.
- **Rule:** AI Tools Zone personnel must have zero access to customer chats, proprietary prompts, uploaded documents, codebases, or generated assets.

### 4. Does the seller need customer credentials?
- **Standard:** Zero password sharing.
- **Rule:** AI Tools Zone must operate via single-use virtual cards or remote payment sessions. Customers should never disclose their passwords to WhatsApp agents.

### 5. Can the customer revoke access?
- **Standard:** Customer maintains full autonomy.
- **Rule:** The customer can change their password or disconnect payment methods at any time without contacting AI Tools Zone.

### 6. What happens when the subscription expires?
- **Standard:** Transparent renewal or graceful fallback.
- **Rule:** On day 30 or day 365, the account simply reverts to the provider's free tier (e.g. Claude Free, Office 365 free web apps). The customer does not lose historical data.

### 7. What happens if a provider suspends the account?
- **Standard:** Clear liability demarcation.
- **Rule:** If suspension is due to vendor payment decline on a seller-provided card, AI Tools Zone provides a replacement payment or full prorated refund within 24 hours. If suspension is due to customer violation of provider Acceptable Use Policies (e.g. generating prohibited content), the seller bears zero replacement liability.

### 8. What happens if a payment fails?
- **Standard:** 24-hour resolution SLA.
- **Rule:** If a virtual card declines during renewal, the seller issues an alternative card within 24 hours.

### 9. What refund or replacement promise can actually be fulfilled?
- **Standard:** Financially backed, sustainable warranties.
- **Rule:** AI Tools Zone explicitly rejects unviable "lifetime replacement" claims. Warranties are capped at the active subscription duration (e.g., 30 days) and funded by a mandatory 5.0% warranty reserve fund.

### 10. What customer information must be retained?
- **Standard:** Minimum necessary data retention under privacy principles.
- **Rule:** Retain only customer WhatsApp number, order reference, transaction timestamp, payment method reference, and subscription expiry date. Never store passwords, MFA seeds, or prompt content.

### 11. What security and privacy risks exist?
- **Risks:** Unauthorized session drops, provider IP banwaves, and Stripe Radar chargeback disputes.
- **Mitigation:** Transparent customer disclosures, strict avoidance of shared credentials, and verified payment rails.

---

## 2. Customer Policy Requirements by Product Category

### 2.1 Class A Coding & Enterprise Tools (Claude, Cursor, Copilot)
- **Privacy Assessment:** **High Risk / Critical Privacy Need**.
- **Customer Requirement:** Software developers and agencies handle proprietary intellectual property. Shared accounts are strictly unacceptable.
- **Mandatory Policy:** 100% customer-owned account on customer's own domain or email. Zero seller password possession.

### 2.2 Class A Generation Tools with Quotas (Runway ML Gen-3)
- **Credit Quota Disclosure:** Runway Pro grants 2,250 credits/month. Once depleted, rendering stops.
- **Mandatory Policy:** The customer terms must state explicitly that credits are strictly finite, non-refundable upon consumption, and cannot be replenished until the next billing cycle.

### 2.3 Excluded Products (Midjourney, SEMrush, Spotify, Turnitin, All-in-One)
- **Failure Mode:** Inherent terms breach and security compromise.
- **Customer Harm:** Customers experience frequent mid-cycle session logouts, loss of work history, and potential security flagging of their local IP addresses.
- **Policy:** Permanent exclusion from commercial catalog.

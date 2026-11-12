# Phase 4.2.3 — Section 236Y Payer Attribution, Cardholder Identity & Commercial Workflows

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** Legal Tax Payer Attribution, Cardholder Responsibility, and Workflow Separation  

---

## 1. Executive Summary: The Taxpayer Attribution Disconnect

Prior project phases introduced an erroneous compliance requirement by mandating that:
> *"All customers purchasing via AI Tools Zone must be verified on the FBR Active Taxpayers List (ATL)."*

This audit resolves the legal and practical disconnect between Pakistan withholding tax law and the actual commercial fulfillment workflows:

### Core Legal Finding:
Under **Section 236Y of the Income Tax Ordinance, 2001**, advance withholding tax is collected by banking companies from the **person remitting amounts abroad through a credit, debit, or prepaid card** (the cardholder).
- When a customer purchases through AI Tools Zone and pays domestically in PKR (via JazzCash, Easypaisa, or Raast), the customer **makes zero international remittance**.
- The qualifying foreign remittance is executed exclusively by **AI Tools Zone (the merchant)** when procuring the overseas software subscription using the merchant's business card.
- Therefore, the **merchant is the legal taxpayer and cardholder**. The bank withholds tax based exclusively on the **merchant's ATL status**, not the customer's.
- Mandating customer ATL status for domestic PKR purchases was legally and operationally unfounded and is hereby formally rescinded.

---

## 2. Comprehensive Reconciliation of Three Operational Scenarios

### Scenario A — Merchant-Funded International Procurement (Current Active Reseller / Concierge Model)
- **Workflow:**  
  1. Pakistani customer orders on AI Tools Zone WhatsApp channel and transfers PKR (e.g. PKR 3,800 for Copilot or PKR 6,800 for Cursor/Claude) via JazzCash, Easypaisa, or Raast.  
  2. AI Tools Zone receives PKR into its domestic commercial account.  
  3. AI Tools Zone uses its own international commercial bank card (e.g. Meezan Bank, HBL, Bank Alfalah Visa/Mastercard) to pay the overseas provider ($10.00 to GitHub or $20.00 to Cursor/Anthropic).
- **Actual Cardholder & Taxpayer:** AI Tools Zone (the merchant entity or sole proprietor).
- **Issuing Bank:** Merchant's Pakistani commercial bank.
- **Cardholder ATL Status:** Governed exclusively by the merchant's NTN/CNIC standing on the FBR Active Taxpayers List.
- **Section 236Y Tax Withholding:**  
  - If Merchant is on ATL: Bank deducts **0.50%** on the gross remitted PKR amount.  
  - If Merchant is Non-ATL: Bank deducts **1.00%** (via Tenth Schedule Rule 1).
- **Customer Tax Role:** None. Customer is an end-buyer paying domestic PKR; customer ATL status is completely irrelevant.

### Scenario B — Customer-Funded Direct International Payment (Pure White-Glove Setup Assistance)
- **Workflow:**  
  1. Customer creates their own personal account on the provider's website (e.g. Netflix, Gamma, Replit).  
  2. Customer inputs their own Pakistani international debit/credit card directly into the provider's checkout.  
  3. AI Tools Zone provides step-by-step guidance on WhatsApp to resolve 2FA, billing address, or regional configuration.  
  4. AI Tools Zone charges a standalone domestic service fee (e.g. PKR 500 to PKR 1,500) for setup labor, collected via JazzCash/Raast.
- **Actual Cardholder & Taxpayer:** The customer.
- **Issuing Bank:** Customer's personal bank.
- **Cardholder ATL Status:** Customer's CNIC standing on the ATL determines the tax rate.
- **Section 236Y Tax Withholding:** Customer's bank deducts 0.50% (ATL) or 1.00% (Non-ATL) directly from customer's account.
- **AI Tools Zone Tax Role:** AI Tools Zone touches zero foreign exchange. Section 236Y liability for AI Tools Zone is **PKR 0.00**.

### Scenario C — Domestic PKR Payment Collection
- **Workflow:** Customer transfers retail price to AI Tools Zone via JazzCash, Easypaisa, Raast, or 1Link IBFT.
- **Statutory Application:** Section 236Y applies strictly to *foreign remittances remitted abroad*. Domestic interbank transfers and mobile wallet transactions attract **0.00% Section 236Y advance tax**.
- **Commercial Expense:** Domestic collection costs (1.50%–2.00% merchant gateway fee or nominal Raast fee) are local operational overhead, not cross-border withholding tax.

---

## 3. Statutory Adjustability vs. Practical Recovery of Non-ATL Tax

In Phase 4.2.2, non-ATL withholding was characterized as *"permanently irrecoverable deadweight loss"*. This must be refined from a strict statutory perspective:

### Legal Reality (Section 168, Income Tax Ordinance, 2001):
1. **Statutory Character:** Section 236Y is an **adjustable advance income tax**. It is **not** a minimum tax (Section 113) and **not** a final tax (Section 169).
2. **Late-Filing Adjustability:** If an inactive taxpayer (non-ATL) has tax withheld at the higher 1.00% rate, the tax is **not legally forfeited**.  
   - When the taxpayer files their annual income tax return under Section 114 (and pays the ATL restoration surcharge under Rule 2 of the Tenth Schedule: PKR 1,000 for individuals), their name is restored to the ATL.
   - The FBR IRIS e-filing system automatically pulls all Section 236Y withholding entries tied to the taxpayer's CNIC from 1Link/banking databases.
   - The entire withheld amount (including the penalty portion) is credited rupee-for-rupee against the taxpayer's assessed annual income tax liability, or carried forward as a tax refund credit under Section 170.

### Practical Commercial Reality:
- For an unregistered, non-filing informal merchant who never files tax returns or maintains audited books, the tax deducted by the bank cannot be claimed back in cash at the counter.
- In financial modeling, treating non-ATL withholding as a cash drain is essential for working capital, but legally it remains an adjustable advance tax upon return submission.

---

## 4. Policy Revisions for AI Tools Zone Operations

1. **Rescission of Customer ATL Check:** Customer checkout on WhatsApp must **never** demand customer FBR Active Taxpayer verification for Group A orders funded by the merchant.
2. **Merchant Card Governance:** AI Tools Zone must ensure that its primary and secondary international procurement cards are linked to NTN/CNICs actively maintained on the Active Taxpayers List, guaranteeing the baseline **0.50% withholding rate** and allowable Section 168 corporate tax credit.

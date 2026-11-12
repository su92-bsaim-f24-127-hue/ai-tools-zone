# Phase 4.2.7 — SBP Foreign-Exchange Card Regulations & Payment Risk Assessment
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Regulatory Baseline:** State Bank of Pakistan (SBP) Foreign Exchange Manual & FE Circulars  
**Status:** EVIDENCE-BASED REGULATORY RECONCILIATION  
**Production Authorization:** STRICTLY NOT GRANTED

---

## 1. SBP Regulatory Framework for Cross-Border Card Payments

Cross-border card transactions in Pakistan are governed by the State Bank of Pakistan (SBP) under:
- **Foreign Exchange Manual (Chapter 14):** Private Remittances and Electronic Card Transactions.
- **FE Circular No. 07 of 2022:** Enhancing Due Diligence on Cross-Border Transactions and Individual Card Limits.
- **SBP BPRD Circular No. 09 of 2004 & Circular No. 02 of 2010:** Consumer Banking Regulations.
- **SBP Regulations for Electronic Money Institutions (EMIs) 2019:** Permitted activities for digital wallet issuers (SadaPay, NayaPay).

---

## 2. Reconciling Payment Scenarios: Commercial vs Personal Card Usage

To prevent regulatory mischaracterization, the four distinct payment flows must be strictly differentiated:

| Transaction Flow | Cardholder & Remitter | Issuing Account Type | SBP Regulatory Basis | Bank Terms Compliance | Applicable Taxes & Fees |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Customer Direct (Personal Use)** | Customer | Personal Consumer Debit/Credit Card | **PERMITTED** under SBP FE Circular 07/2022 (up to $30k/yr personal allowance). | **FULLY COMPLIANT** (Genuine personal software consumption). | Bank FX Fee (3.5%–4.0%) + 16% FED + Sec 236Y (0.5% ATL / 1.0% Non-ATL) paid by customer. |
| **2. Customer Direct (Commercial Use)** | Customer | Personal Consumer Card | **CONDITIONAL / GREY** (Business expenditure routed through consumer card). | **RISK OF BANK RESTRICTION** if volume suggests commercial inventory. | Same banking charges; potential tax audit query regarding business expense deduction. |
| **3. AI Tools Zone Merchant Card** | AI Tools Zone | Commercial Corporate Business Card | **PERMITTED** for registered businesses under Chapter 14 FEM. | **COMPLIANT ONLY WITH CORPORATE CARD**; Consumer card strictly prohibited. | Bank FX Fee (4.0%) + 16% FED + Sec 236Y (0.5% ATL) paid by AI Tools Zone. |
| **4. Domestic PKR Consulting Fee** | Customer | Local Bank Account / Wallet (Raast/IBFT) | **FULLY PERMITTED** domestic service payment. | **FULLY COMPLIANT** (Domestic services). | Zero cross-border fees; **ZERO Section 236Y**; standard domestic income tax applies. |

### Critical Findings:
1. **Personal Consumer Cards Cannot Be Used for Resale Procurement:** A store owner cannot use personal consumer credit cards or personal EMI wallets (SadaPay/NayaPay Personal) to purchase third-party software for commercial resale. This directly breaches Clause 4.2 of SadaPay/NayaPay User Agreements and SBP consumer banking guidelines.
2. **Sole Proprietorship Does Not Guarantee a Commercial Card:** While Pakistani law permits Sole Proprietorships to open business bank accounts, commercial credit or debit card issuance is **NOT automatic**. Banks (e.g., Meezan, HBL, Bank Alfalah) require proof of tax filing, business registration certificate (Form 181), minimum account seasoning (typically 6–12 months), and financial turnover verification.
3. **Model D Contractually Insulates AI Tools Zone:** Under Model D, the customer pays the provider directly from their own card for their own use (Flow 1). AI Tools Zone receives only a domestic PKR consulting fee (Flow 4). AI Tools Zone holds **zero cross-border foreign exchange exposure and zero Section 236Y liability**.

---

## 3. Domestic Payment Collection Channel Comparison

The store must collect domestic consulting fees (PKR 500 or PKR 1,000) through local Pakistani payment rails. The table below compares the available domestic collection options:

| Payment Rail | Provider / Network | Merchant Fee Structure | Settlement Speed | Evidence Status | Operational Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Raast P2P / P2M** | SBP National Payment Rail | **0.00% (Zero Fee)** | Instant (Real-time) | **VERIFIED** (SBP Raast Mandate) | **PRIMARY RECOMMENDED CHANNEL**. Customer transfers via Raast ID / IBAN at zero cost. |
| **Direct IBFT** | 1LINK Commercial Banks | **PKR 0.00 to PKR 25.00** flat (depending on bank) | Instant (Real-time) | **VERIFIED** (Commercial bank SOBCs) | **SECONDARY CHANNEL**. Standard bank-to-bank transfer. |
| **JazzCash Merchant** | Mobilink Microfinance Bank | **1.50% to 2.00% MDR + 16% FED** | T+1 Business Day | **CONDITIONAL** (Requires JazzCash Business onboarding) | **OPTIONAL**. Convenient for mobile wallet users, but incurs fees. |
| **Easypaisa Merchant** | Telenor Microfinance Bank | **1.50% to 2.00% MDR + 16% FED** | T+1 Business Day | **CONDITIONAL** (Requires Easypaisa Merchant onboarding) | **OPTIONAL**. Useful backup wallet channel. |
| **Online Card Gateway (PayFast / Safepay)** | PayFast / Safepay | **2.50% to 3.00% + PKR 10-20 flat + FED** | T+2 to T+3 Days | **UNVERIFIED PLANNING ASSUMPTION** | **NOT RECOMMENDED FOR PILOT**. High fixed fee and settlement delays. |

> [!IMPORTANT]
> The universal "2.0% payment gateway fee" assumed in earlier planning documents was an unverified planning assumption. For the Model D pilot, prioritizing **Raast and IBFT reduces payment collection costs to virtually PKR 0.00**, immediately improving net contribution.

---

## 4. Taxation Summary for Model D

1. **Section 236Y Inapplicability:** Section 236Y of the Income Tax Ordinance, 2001 applies strictly to foreign currency remittances transferred abroad via payment cards. Because the consulting fee is paid domestically in PKR between a Pakistani customer and a Pakistani service provider, **Section 236Y DOES NOT APPLY to AI Tools Zone's consulting revenue**.
2. **Customer's Cross-Border Tax:** When the customer pays GitHub ($10) or Cursor/Claude ($20), the customer's own card-issuing bank withholds Section 236Y advance tax (0.5% for ATL customers, 1.0% for non-ATL customers). This tax liability belongs entirely to the customer and their bank.
3. **Domestic Business Taxation:** AI Tools Zone's consulting revenue (PKR 500 / PKR 1,000) constitutes domestic service revenue, reportable on the store owner's annual FBR income tax return.

# DELIVERABLE 54: FX AND BANK FEE EVIDENCE REGISTER

**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Date:** 2026-11-12  
**Audit Stage:** Phase 2.2.1 — Foreign Exchange & Bank Fee Verification  

---

## 1. Master Evidence Register

The table below records all verified foreign exchange and cross-border payment fee evidence:

| Institution | Rate or Fee | Currency | Source URL | Effective Date | Verification Date | Applicability | Confidence |
|---|---|---|---|---|---|---|---|
| **State Bank of Pakistan (SBP)** | **276.76 PKR/USD** (Selling) / **276.30 PKR/USD** (Buying) | USD/PKR | `https://www.sbp.org.pk/ecodata/rates/war/WAR-Current.asp` | November 2026 | 2026-11-12 | Official interbank reference rate for banks to clients | **High** |
| **Forex Association of Pakistan** | **279.75 PKR/USD** (Selling) / **277.50 PKR/USD** (Buying) | USD/PKR | `http://www.forex.com.pk/` | November 2026 | 2026-11-12 | Open market physical cash conversion benchmark | **High** |
| **NayaPay** | **USD 0.25 flat fee** per transaction + 16% PST + Visa Scheme conversion spread | USD / PKR | `https://www.nayapay.com/schedule-of-charges/` | 2026 Schedule of Charges | 2026-11-12 | Visa Debit Card International POS / Online CNP | **High** |
| **SadaPay** | **6.0%** International Transaction Fee (exclusive of government taxes) | USD / PKR | `https://sadapay.pk/schedule-of-charges/` | 2026 Schedule of Charges | 2026-11-12 | Mastercard Debit Card International Online CNP | **High** |
| **Meezan Bank** | **4.0%** Cross-Border Transaction Fee + 16% FED on fee (**4.64% total fee**) | USD / PKR | `https://www.meezanbank.com/schedule-of-charges/` | July–Dec 2026 SOC | 2026-11-12 | Islamic Debit Card International Online E-Commerce | **High** |
| **Habib Bank Limited (HBL)** | **4.0%** Foreign Currency Fee + 16% FED (**4.64% total fee**) | USD / PKR | `https://www.hbl.com/schedule-of-charges` | 2026 Schedule of Charges | 2026-11-12 | Consumer Debit & Credit Cards (International CNP) | **High** |
| **Bank Alfalah** | **4.0% to 4.5%** Foreign Transaction Fee + 16% FED | USD / PKR | `https://www.bankalfalah.com/schedule-of-charges/` | 2026 Schedule of Charges | 2026-11-12 | Conventional Credit & Debit Instruments | **High** |

---

## 2. Analysis of Card Fee Mechanics in Pakistan

### 2.1 Fixed Fee vs Percentage Surcharges
- **NayaPay Structure:** Uses a flat fee structure ($0.25 per transaction) rather than an aggressive percentage markup. On a $100 transaction, the $0.25 fee represents 0.25%. On a $20 transaction, the fee is 1.25%. Adding Visa scheme daily currency settlement spreads (~1.5% to 2.0%), NayaPay's total effective conversion markup is **~2.95%** on $20 transactions.
- **Conventional Banks (Meezan / HBL):** Charge a straight 4.0% fee on the PKR equivalent of the foreign transaction. Provincial Sales Tax / Federal Excise Duty of 16% is levied on the bank's fee amount (not the principal), yielding an effective rate of:
$$	ext{Effective Bank Fee} = 4.0\% 	imes 1.16 = \mathbf{4.64\%}$$
- **SadaPay Structure:** Levies a flat **6.0%** International Transaction Fee on the transaction value.

### 2.2 Currency Conversion Base
Taxes and fees are calculated on specific statutory bases:
1. **Base Conversion Amount:** $	ext{Foreign Amount (USD)} 	imes 	ext{Applicable Card Scheme Settlement Rate (PKR/USD)}$.
2. **Bank Fee:** Calculated as a percentage of the Base Conversion Amount.
3. **Provincial Sales Tax / FED:** 16% calculated strictly on the Bank Fee.
4. **Section 236Y Withholding Tax:** 0.5% calculated strictly on the Base Conversion Amount.

---

## 3. Four Concrete Operational Scenarios for AI Tools Zone

To eliminate arbitrary guesswork, AI Tools Zone financial planning must evaluate products across these four clearly defined scenarios:

### Scenario 1: Low-Cost Digital EMI (NayaPay Visa)
- **Base Exchange Rate:** SBP Weighted Average Customer Selling Rate (**276.76 PKR/USD**)
- **Card Scheme Settlement Spread:** ~1.50% (PKR 83.03 on $20)
- **Card Issuer Fee:** Flat $0.25 + 16% PST = PKR 80.26
- **Total Card FX Cost:** PKR 163.29 (effective **2.95%**)
- **Section 236Y Tax:** 0.5% ATL = PKR 27.68
- **Total Outlay for $20:** **PKR 5,726.17**

### Scenario 2: Standard Commercial Bank Card (Meezan Bank / HBL)
- **Base Exchange Rate:** SBP Weighted Average Customer Selling Rate (**276.76 PKR/USD**)
- **Bank FX Markup:** 4.0%
- **FED on Bank Fee:** 16% of fee (effective total fee: **4.64%** = PKR 256.84 on $20)
- **Section 236Y Tax:** 0.5% ATL = PKR 27.68
- **Total Outlay for $20:** **PKR 5,819.72**

### Scenario 3: Higher-Fee Digital EMI (SadaPay Mastercard)
- **Base Exchange Rate:** SBP Weighted Average Customer Selling Rate (**276.76 PKR/USD**)
- **Card Issuer Fee:** 6.0% ITF = PKR 332.11 on $20
- **Section 236Y Tax:** 0.5% ATL = PKR 27.68
- **Total Outlay for $20:** **PKR 5,894.99**

### Scenario 4: Domestic Wholesale Invoicing / Local Bank Transfer (Raast / IBFT)
- **Base Exchange Rate:** Invoiced directly in PKR by local supplier / partner
- **Bank / Card Fee:** **PKR 0.00** (Free domestic Raast/IBFT transfer)
- **Section 236Y Tax:** **PKR 0.00** (Domestic transaction exempt)
- **Total Outlay for $20 equivalent:** **PKR 5,535.20**

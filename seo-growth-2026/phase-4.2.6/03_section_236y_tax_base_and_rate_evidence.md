# Phase 4.2.6 — Section 236Y Tax Base & Rate Evidence Dossier
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Governing Statute:** Income Tax Ordinance, 2001 (as amended through Finance Act 2024 / TY2027)  
**Status:** REQUIRES WRITTEN PAKISTANI TAX ADVICE  
**Production Authorization:** STRICTLY NOT GRANTED

---

## 1. Statutory Framework & Applicable Tax Rates

Section 236Y of the Income Tax Ordinance, 2001 governs advance tax collection on payment through debit, credit, or prepaid cards for foreign transactions.

### 1.1 Correct Tax Rate Schedule (TY2027 / FBR Consolidated Card)
- **Active Taxpayer List (ATL) Persons:** **0.50%** (specified under Division XXVII, Part IV of the First Schedule).
- **Non-Active Taxpayer List (Non-ATL) Persons:** **1.00%** (governed by the Tenth Schedule rules applicable to Section 236Y).
  > [!IMPORTANT]
  > Earlier planning notes assumed a 2.50% or 5.00% non-ATL rate. Under the current consolidated rate card, the standard non-ATL rate for Section 236Y is confirmed at **1.00%**. All financial models in Phase 4.2.6 have been recalculated using this rate.

---

## 2. Statutory Construction vs Bank Withholding Behavior

### 2.1 Interpretation 1: Strict Statutory Construction (Foreign Principal Only)
- **Statutory Text:** Section 236Y(1) mandates advance tax collection on the *"sum remitted outside Pakistan"*.
- **Legal Reality:** The foreign transaction principal ($10.00 or $20.00 converted to PKR) is the exact sum remitted through international card scheme rails (Visa/Mastercard) to the foreign merchant abroad.
- **Domestic Fee Isolation:** The commercial bank's foreign exchange processing fee (e.g., 4.00%) and Federal Excise Duty (16.00%) are retained domestically by the Pakistani issuing bank and disbursed to provincial/federal revenue authorities within Pakistan. Zero percent of the bank fee or FED is remitted abroad.
- **Tax Base:** Strictly the Foreign Currency Principal converted to PKR at the interbank/TT rate.

### 2.2 Interpretation 2: Observed Core Banking Behavior (Gross Debit Withholding)
- **Observed Behavior:** Automated core banking platforms across major Pakistani commercial banks (Meezan Bank, HBL, Bank Alfalah) frequently apply the withholding formula to the gross settlement debit:
  $$\text{Withholding Base} = \text{Foreign Principal (PKR)} + \text{Bank Processing Fee (PKR)} + \text{FED (PKR)}$$
- **Technical Mechanism:** Automated middleware triggers Section 236Y calculation on the aggregate authorization hold before splitting line-item fees.

### 2.3 Mathematical Materiality of the Variance (at FX 276.76)

| Product | USD Price | Gross Base | Principal Base | ATL Delta (0.5%) | Non-ATL Delta (1.0%) | Break-Even FX Shift |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **GitHub Copilot** | $10.00 | PKR 2,896.02 | PKR 2,767.60 | **+PKR 0.64** | **+PKR 1.28** | **< 0.06 PKR/USD** |
| **Cursor AI Pro** | $20.00 | PKR 5,792.03 | PKR 5,535.20 | **+PKR 1.28** | **+PKR 2.57** | **< 0.06 PKR/USD** |
| **Claude Pro** | $20.00 | PKR 5,792.03 | PKR 5,535.20 | **+PKR 1.28** | **+PKR 2.57** | **< 0.06 PKR/USD** |

---

## 3. The Required Written Question for Pakistani Tax Counsel

Because statutory authority rests with the Federal Board of Revenue and judicial tax tribunals rather than commercial bank software logic, neither interpretation is presented as a final legal finding. The store owner must submit the following formal question to a licensed Pakistani Advocate High Court or Chartered Accountant:

> **Formal Legal/Tax Query:**  
> *"Under Section 236Y(1) of the Income Tax Ordinance, 2001 (as amended through Finance Act, 2024), does the statutory phrase 'sum remitted outside Pakistan' legally restrict the withholding tax base strictly to the foreign exchange principal remitted to the non-resident vendor, or does it legally encompass locally retained banking processing fees and domestic Federal Excise Duty (FED) charged by the domestic card-issuing bank? Furthermore, in the event an issuing bank withholds tax on the gross debit, does the excess deduction constitute an adjustable advance tax credit under Section 168 claimable against the taxpayer's final annual income tax liability?"*

---

## 4. Cardholder & Remitter Identity by Payment Scenario

| Model | Remitting Party (Cardholder) | Applicable Section 236Y Rate | Tax Withheld From | Section 168 Credit Entitlement | AI Tools Zone Exposure |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Model A: Retail Resale** | AI Tools Zone Merchant Card | Merchant's Status (0.5% ATL) | Merchant's Bank Account | AI Tools Zone (against business NTN) | Merchant carries full tax cash outlay |
| **Model C: Proxy Card** | AI Tools Zone Merchant Card | Merchant's Status (0.5% ATL) | Merchant's Bank Account | AI Tools Zone (against business NTN) | Merchant carries full tax cash outlay |
| **Model D: Customer-Funded** | **Customer's Direct Card** | **Customer's Status (0.5% or 1.0%)** | **Customer's Bank Account** | **Customer (against customer's CNIC/NTN)** | **ZERO TAX EXPOSURE (No foreign remittance)** |

### 4.1 Resolution of Customer ATL Requirements
- Under **Model D (Customer-Funded Setup Service)**, AI Tools Zone **DOES NOT IMPOSE A UNIVERSAL ATL REQUIREMENT ON CUSTOMERS**.
- The customer settles directly with the foreign provider. The customer's card-issuing bank automatically determines withholding (0.5% if the customer is on the ATL, or 1.0% if non-ATL).
- AI Tools Zone remits zero foreign exchange and holds zero tax liability, completely eliminating commercial tax risk.

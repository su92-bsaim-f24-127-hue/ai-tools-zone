# Phase 3.1.5 — Grammarly Financial Copy Correction & Margin Reconciliation Report

**Project:** AI Tools Zone  
**Website:** https://aitoolszone.tech/  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Audit Scope:** Grammarly Premium Financial Model and Narrative Consistency  
**Authoritative Source:** `competitor-research/phase-3.1.4/97_independently_recalculated_financial_model.csv`  
**Audit Date:** 12 November 2026  
**Commercial Status:** `NOT AUTHORIZED — UNVIABLE AT RETAIL`  

---

## 1. Executive Summary

During Phase 3.1.4, an independent recalculation of the 12 candidate products in Group A established that Grammarly Premium possesses an official monthly retail subscription cost of **$30.00 / month**, yielding an economic landed cost of **PKR 8,688.05** and total cash outlay of **PKR 8,731.49**. 

At AI Tools Zone's proposed retail price of **PKR 7,500.00**, direct procurement produces an exact net contribution deficit of **`-PKR 1,953.19`** per transaction (-26.04% net margin).

However, in several narrative sections of the Phase 3.1.4 reports (Deliverables 98, 100, and 105), the text colloquially claimed that *"the commercial deficit exceeds PKR 5,000 per sale"*. This report documents the exact root cause of this narrative phrasing, resolves the ambiguity, updates all affected documents, and aligns all copy with the authoritative Decimal financial model without altering underlying financial inputs.

---

## 2. Authoritative Financial Model Inputs & Exact Mathematical Derivation

Source: [97_independently_recalculated_financial_model.csv](file:///C:/Users/ELITEBOOK/projects/ai-tools-zone/competitor-research/phase-3.1.4/97_independently_recalculated_financial_model.csv) (Row 5).

### Step-by-Step Mathematical Derivation (Decimal Arithmetic)
1. **Official Provider Retail Price:** $30.00 / month.
2. **SBP Customer Selling Benchmark:** PKR 276.76 / USD (Nov 2026).
3. **Base SBP Amount:** $30.00 \times 276.76 = \mathbf{\text{PKR } 8,302.80}$.
4. **Bank FX Spread (4.00%):** $8,302.80 \times 0.0400 = \mathbf{\text{PKR } 332.11}$.
5. **FED on Bank Fee (16.00%):** $332.11 \times 0.1600 = \text{PKR } 53.1376 \rightarrow \mathbf{\text{PKR } 53.14}$.
6. **Total Bank Transaction Fee (4.64%):** $332.11 + 53.14 = \mathbf{\text{PKR } 385.25}$.
7. **Gross Remittance Outflow / Economic Landed Cost:** $8,302.80 + 385.25 = \mathbf{\text{PKR } 8,688.05}$.
8. **Section 236Y Advance Withholding Tax (0.50% ATL):** $8,688.05 \times 0.0050 = \text{PKR } 43.44025 \rightarrow \mathbf{\text{PKR } 43.44}$.
9. **Total Upfront Cash Outlay:** $8,688.05 + 43.44 = \mathbf{\text{PKR } 8,731.49}$.
10. **Adjustable Tax Asset (Section 168/169 Credit):** $\mathbf{\text{PKR } 43.44}$.
11. **Proposed Customer Selling Price:** $\mathbf{\text{PKR } 7,500.00}$.
12. **Gross Contribution (Economic Basis):** $7,500.00 - 8,688.05 = \mathbf{\text{-PKR } 1,188.05}$ (-15.84% margin).
13. **Modeled Operating Expenses (OPEX):**
    - Onboarding Delivery Labor: PKR 150.00
    - WhatsApp Customer Support Labor: PKR 200.00
    - Replacement / Chargeback Reserve (5% of Base SBP): $8,302.80 \times 0.05 = \text{PKR } 415.14$
    - **Total Documented OPEX:** $150.00 + 200.00 + 415.14 = \mathbf{\text{PKR } 765.14}$.
14. **Net Contribution:** $-1,188.05 - 765.14 = \mathbf{\text{-PKR } 1,953.19}$ (-26.04% net margin).

---

## 3. Discrepancy Root Cause Analysis: The "PKR 5,000+" Context

### Where did the "PKR 5,000+" number originate?
In Phase 2 and Phase 2.1 competitor intelligence surveys, competing Pakistani platforms (`aitoolgems.tech` and `aitoolspak.tech`) were observed advertising Grammarly Premium at predatory grey-market price points between **PKR 2,500 and PKR 3,500**.

When comparing those competitor prices against the direct retail sourcing cost:
- **At PKR 2,500 Competitor Price:**
  $$\text{Cash Shortfall} = \text{PKR } 2,500.00 - \text{PKR } 8,731.49 = \mathbf{\text{-PKR } 6,231.49}$$
  $$\text{Economic Gross Shortfall} = \text{PKR } 2,500.00 - \text{PKR } 8,688.05 = \mathbf{\text{-PKR } 6,188.05}$$
- **At PKR 3,500 Competitor Price:**
  $$\text{Cash Shortfall} = \text{PKR } 3,500.00 - \text{PKR } 8,731.49 = \mathbf{\text{-PKR } 5,231.49}$$
  $$\text{Economic Gross Shortfall} = \text{PKR } 3,500.00 - \text{PKR } 8,688.05 = \mathbf{\text{-PKR } 5,188.05}$$

In preliminary research notes, the author noted that *"matching competitor prices produces an immediate deficit of over PKR 5,000 per sale"*. However, in subsequent drafts, this phrasing was carelessly applied to general summaries without distinguishing between the *competitor price point* (PKR 2,500–3,500) and AI Tools Zone's *modeled proposed retail price* (PKR 7,500).

---

## 4. Reconciliation & Editorial Corrections Applied

All narrative occurrences have been updated across the repository:

| Document Path | Section / Line | Pre-Correction Text | Corrected Text | Status |
| :--- | :--- | :--- | :--- | :--- |
| `competitor-research/phase-3.1.4/98_financial_discrepancy_resolution_report.md` | Line 88 | "...results in an immediate commercial deficit exceeding PKR 5,000 per transaction." | "...direct retail procurement results in an immediate net contribution deficit of **-PKR 1,953.19** (-26.04% net margin). If sold at competitor market rates (PKR 2,500–3,500), the unhedged cash shortfall would worsen to between -PKR 5,231.49 and -PKR 6,231.49." | **CORRECTED** |
| `competitor-research/phase-3.1.4/100_commercial_authorization_lock_matrix.csv` | Row 5 (Grammarly) | "Selling at competitor market prices (PKR 2,500-3,500) results in an immediate deficit of -PKR 5,000+ per transaction" | "At proposed retail price of PKR 7,500.00, net contribution deficit is -PKR 1,953.19 per transaction (-26.04% net margin). Selling at competitor market prices (PKR 2,500-3,500) yields an unviable cash deficit of -PKR 5,231.49 to -PKR 6,231.49" | **CORRECTED** |
| `competitor-research/phase-3.1.4/105_phase_3_1_4_final_owner_decision_dossier.md` | Line 63 | "Selling at Pakistani market rates (PKR 2,500–3,500) results in an immediate commercial deficit exceeding PKR 5,000 per transaction." | "At the proposed retail price of PKR 7,500.00, direct procurement produces an immediate net contribution deficit of **-PKR 1,953.19** per transaction (-26.04% net margin). Sourcing at competitor prices (PKR 2,500–3,500) creates an unviable cash deficit of -PKR 5,231.49 to -PKR 6,231.49." | **CORRECTED** |

---

## 5. Commercial Policy Affirmation

The commercial restriction on Grammarly Premium remains hard-locked:

> **COMMERCIAL STATUS: `NOT AUTHORIZED — UNVIABLE AT RETAIL`**  
> Grammarly Premium cannot be commercially sold or advertised as an active product until AI Tools Zone secures an authorized wholesale corporate team seat rate card that brings landed procurement costs safely below proposed retail pricing. Staged landing page remains strictly informational under ENQUIRE status (`Price on Enquiry`).

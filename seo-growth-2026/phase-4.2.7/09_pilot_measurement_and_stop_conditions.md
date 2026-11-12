# Phase 4.2.7 — Pilot Measurement Framework & Stop Conditions
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Scope:** Funnel Measurement, KPI Targets, and Pilot Stop Thresholds  
**Production Authorization:** STRICTLY NOT GRANTED  
**Commercial Pilot Authorization:** STRICTLY NOT GRANTED

---

## 1. Funnel Architecture: Dissecting Conversion Stages

To prevent inflated performance claims, the commercial funnel strictly separates automated web engagement from real paying customers:

```
[Stage 1: Web WhatsApp Click] ──> Analytics event (NOT a confirmed lead)
      ▼
[Stage 2: Actual Enquiry] ─────> Message received on WhatsApp Business
      ▼
[Stage 3: Qualified Lead] ─────> Verified developer with compatible device & payment card
      ▼
[Stage 4: Paid Booking] ───────> Domestic PKR fee paid; session scheduled
      ▼
[Stage 5: Completed Service] ──> Session delivered and verified
      ▼
[Stage 6: Satisfied Customer] ─> Positive post-service review; zero dispute
      ▼
[Stage 7: Repeat / Referral] ──> Books follow-up Tier 2 or refers colleague
```

> [!CRITICAL]
> Web clicks on WhatsApp buttons (`whatsapp_click`) represent top-of-funnel traffic intent only. They **MUST NEVER** be reported as sales or revenue.

---

## 2. Key Performance Indicators (KPIs) & Planning Targets

| Metric | Calculation Method | Planning Target (Tier 1) | Planning Target (Tier 2) |
| :--- | :--- | :---: | :---: |
| **Enquiry-to-Qualified Rate** | Qualified Leads / Actual Enquiries | 40.0% – 50.0% | 30.0% – 40.0% |
| **Qualified-to-Booking Rate** | Paid Bookings / Qualified Leads | 25.0% – 35.0% | 20.0% – 30.0% |
| **Booking-to-Completion Rate**| Completed Sessions / Paid Bookings | > 90.0% | > 90.0% |
| **Average Session Duration** | Direct Technician Time per Session | < 25 Minutes | < 50 Minutes |
| **Post-Delivery Support Time**| Cumulative chat support per client | < 10 Minutes | < 15 Minutes |
| **Rework Rate** | Sessions requiring follow-up fix / Total | < 10.0% | < 15.0% |
| **Refund Rate** | Total Refunds Issued / Total Paid Bookings | < 5.0% | < 5.0% |
| **Operating Contribution** | Gross Fee - Direct Labor - Allocated G&A | > PKR 130 / session | > PKR 300 / session |
| **Customer Satisfaction (CSAT)**| % Rating 4 or 5 out of 5 stars | > 85.0% | > 90.0% |

---

## 3. Pilot Scope & Recommended Sample Size

- **Recommended Pilot Cohort:** **10 to 15 completed sessions** (labeled strictly as a planning recommendation, not a statistically proven threshold).
- **Tool Allocation:** 
  - 5 sessions: Cursor AI Pro
  - 5 sessions: GitHub Copilot
  - 2 to 5 sessions: Claude Pro / Claude Code
- **Service Tier Allocation:** Approximately 60% Tier 1 (Guided Setup) and 40% Tier 2 (Advanced Setup).

---

## 4. Hard Pilot Stop Conditions

The pilot must be **IMMEDIATELY HALTED** if any of the following mandatory stop triggers are breached:

1. **Security / Privacy Incident:** Any accidental exposure or retention of customer passwords, MFA codes, or credit card numbers. *Action: Immediate halt, security audit, report to owner.*
2. **Provider Terms Action / Account Suspension:** Any customer account flagged, restricted, or suspended by GitHub, Anysphere, or Anthropic during or immediately following setup. *Action: Immediate halt, root-cause investigation.*
3. **Elevated Refund / Dispute Rate:** If the cumulative refund rate exceeds **15.0%** across the first 10 sessions. *Action: Pause pilot, re-evaluate intake qualification and technical instructions.*
4. **Severe Labor Time Overrun:** If average technician session duration exceeds **150% of budget** (e.g., > 35 mins on Tier 1; > 70 mins on Tier 2) across 3 consecutive sessions. *Action: Pause pilot, revise SOP and tool blueprints.*
5. **Customer Payment Failure Spike:** If more than **30%** of qualified customers experience provider card declines at checkout. *Action: Pause pilot, audit local bank card acceptance and update pre-check script.*
6. **Negative Operating Contribution:** If realized operating contribution falls below PKR 0 across 3 consecutive sessions. *Action: Immediate halt, economic restructuring.*

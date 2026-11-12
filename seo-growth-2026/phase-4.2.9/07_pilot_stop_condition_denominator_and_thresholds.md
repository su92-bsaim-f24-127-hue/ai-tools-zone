# Phase 4.2.9 — Pilot Stop Condition Thresholds & Measurement Metrics
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Governance Scope:** Hard Operational Stop Conditions for Controlled Pilot  
**Production Authorization:** STRICTLY NOT GRANTED  
**Commercial Pilot Authorization:** STRICTLY NOT GRANTED

---

## 1. Pilot Cohort Ceiling & Denominator Definition

To eliminate previous governance ambiguity:
- **Maximum Pilot Cohort Ceiling:** **Strictly capped at no more than 10 completed consulting sessions**.
- **Sample Allocation:** Up to 5 Cursor AI Pro sessions, up to 5 GitHub Copilot sessions, and up to 2 Claude Pro sessions (total completed sessions $\le 10$).
- **Measurement Window:** The pilot evaluation window opens upon the first customer booking and closes upon the completion or cancellation of the 10th session.

---

## 2. Hard Stop Conditions with Exact Numerators & Denominators

The commercial pilot must be **IMMEDIATELY HALTED** if any of the following explicit mathematical thresholds are triggered:

| Trigger # | Risk Category | Exact Stop Condition & Threshold | Mathematical Formula | Action Mandate |
| :---: | :--- | :--- | :---: | :--- |
| **ST-01** | **Security / Credential Leak** | **$\ge 1$ security incident** (technician captures, requests, or stores customer password, card CVV, or OTP). | $\frac{\text{Security Incidents}}{\text{Total Sessions}} \ge \frac{1}{10}$ | **IMMEDIATE HALT**. Terminate technician; notify customer; audit local machines. |
| **ST-02** | **Provider Account Suspension** | **$\ge 1$ customer account flagged or suspended** by provider during or immediately following setup. | $\frac{\text{Suspended Accounts}}{\text{Completed Sessions}} \ge \frac{1}{10}$ | **IMMEDIATE HALT**. Investigate root cause; verify terms alignment. |
| **ST-03** | **Refund / Dispute Rate** | **$\ge 2$ refunded sessions out of the 10-session cohort (20.0%)**, OR **2 refund requests within any 5 consecutive bookings**. | $\frac{\text{Refunds}}{\text{Total Bookings}} \ge \frac{2}{10}\ (20\%)$ | **IMMEDIATE HALT**. Re-evaluate customer pre-qualification and technical delivery. |
| **ST-04** | **Technician Session Overrun** | **$\ge 3$ consecutive sessions exceeding 150% of planned duration** (Tier 1 > 30 mins; Tier 2 Alt A > 67.5 mins / Alt B > 60 mins). | $\text{Consecutive Overruns} \ge 3$ | **PAUSE & REVIEW**. Review technical SOP; simplify configuration scripts. |
| **ST-05** | **Provider Card Decline Rate** | **$\ge 3$ customer card declines out of 10 attempted checkouts (30.0%)** at provider checkout. | $\frac{\text{Card Declines}}{\text{Checkout Attempts}} \ge \frac{3}{10}\ (30\%)$ | **PAUSE & REVIEW**. Update pre-flight intake checklist; audit local bank compatibility. |
| **ST-06** | **Negative Operating Contribution** | **3 consecutive sessions yielding negative operating contribution** after direct labor and allocated overhead. | $\text{Consecutive Negative Margin} \ge 3$ | **IMMEDIATE HALT**. Economic model restructuring; cease pilot. |

---

## 3. Reporting Protocol
Upon the occurrence of any stop trigger, the pilot lead must immediately issue a formal **Incident & Stop Notification** to the store owner within 2 hours, suspending all further scheduling until written owner review.

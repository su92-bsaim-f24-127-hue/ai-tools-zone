# Phase 4.2.7 — Customer Journey & Operational Acceptance Checklists
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Scope:** 11-Step Customer Workflow & 5 Operational Checklists  
**Production Authorization:** STRICTLY NOT GRANTED  
**Commercial Pilot Authorization:** STRICTLY NOT GRANTED

---

## 1. The 11-Step Customer Journey Workflow

```
[1. WhatsApp Inquiry] ──> [2. Clarify Need] ───> [3. Eligibility Check] ──> [4. Scope & Quote]
                                                                                   │
[8. Guided Session] <─── [7. Book Session] <── [6. Self-Checkout] <────── [5. Accept Terms]
         │
         ▼
[9. Verify Delivery] ──> [10. Client Acceptance] ──> [11. Close & Retain Record]
```

1. **WhatsApp Inquiry:** Customer clicks WhatsApp link on website or messages support requesting assistance with GitHub Copilot, Cursor, or Claude.
2. **Clarification of Need:** Support clarifies whether customer needs basic setup (Tier 1) or advanced context architecture (Tier 2).
3. **Eligibility & Provider Pre-Check:** Support confirms customer has compatible hardware and an active international payment card for the provider's subscription.
4. **Scope, Pricing & Exclusions Delivery:** Support sends standardized scope card: domestic service fee (PKR 500 or PKR 1,000), exact deliverables, estimated duration, and provider USD subscription cost.
5. **Customer Terms Acceptance:** Customer reviews and replies "ACCEPT" to the terms, privacy notice, and refund policy.
6. **Customer Payment & Booking:** Customer transfers domestic fee via Raast/IBFT and selects a consulting time slot.
7. **Session Setup:** Technician sends Google Meet / Zoom link and pre-flight instructions.
8. **Live Supervised Consulting:** Technician guides customer through registration, payment (paused screen share), and configuration.
9. **Deliverable Verification:** Customer executes a test completion or codebase query to verify active functionality.
10. **Customer Acceptance / Rework:** Customer confirms satisfactory delivery or requests adjustments within agreed scope.
11. **Closure & Record Retention:** Service record is logged in CRM; meeting chat notes cleared; receipt issued.

---

## 2. Operational Acceptance Checklists

### Checklist 1: Pre-Service Verification (Before Session)
- [ ] Customer hardware verified (Windows 10/11, macOS 12+, or modern Linux).
- [ ] Base IDE installed (VS Code, Cursor, or JetBrains).
- [ ] Customer confirms possession of active international debit/credit card with ecommerce 3DS activated.
- [ ] Written Scope of Work (SOW) and pricing card sent via WhatsApp.
- [ ] Customer explicit written acceptance ("ACCEPT") recorded.
- [ ] Domestic PKR service fee received via Raast/IBFT.
- [ ] Meeting link generated and pre-flight briefing delivered.

### Checklist 2: Execution & Security Controls (During Session)
- [ ] Supervised screen sharing active via Google Meet/Zoom (display only; no remote control).
- [ ] Customer verbally acknowledges closing of personal tabs and private documents.
- [ ] **MANDATORY:** Screen share PAUSED while customer inputs card details into provider checkout.
- [ ] Payment confirmed directly by provider; screen share resumed.
- [ ] Extensions / tools authenticated directly to customer's personal account.
- [ ] `.cursorrules` / configuration blueprints deployed to customer environment.
- [ ] Codebase indexing initiated with `.cursorignore` protecting sensitive local files.
- [ ] Zero passwords, MFA codes, or API secrets viewed or recorded by technician.

### Checklist 3: Completion & Handover (Post-Session)
- [ ] Inline completion and chat generation verified live on customer machine.
- [ ] Curated Quick-Start Guide / Prompt Pack delivered via chat/email.
- [ ] Handover summary provided detailing support duration (48h for Tier 1; 7d for Tier 2).
- [ ] Customer confirms completion in WhatsApp: *"Setup verified and accepted."*
- [ ] Domestic service receipt issued with disclaimer.
- [ ] Technician verifies zero customer files or credentials remain in local session cache.

### Checklist 4: Refund & Dispute Handling
- [ ] Determine cause of dispute (card decline, hardware issue, service dissatisfaction).
- [ ] Check eligibility against Refund Matrix (Deliverable 07).
- [ ] If eligible: log refund request and obtain store owner sign-off.
- [ ] Initiate domestic transfer via Raast/bank within 48 hours.
- [ ] Send payment confirmation screenshot to customer; close ticket.

### Checklist 5: Security Incident Response
- [ ] **Step 1 (Immediate Freeze):** Instruct customer to stop screen sharing immediately.
- [ ] **Step 2 (Containment):** Verify meeting recording was NOT active; clear meeting chat.
- [ ] **Step 3 (Remediation):** Guide customer to rotate exposed credentials / keys immediately.
- [ ] **Step 4 (Logging):** File internal incident report with date, time, and exposed data type.
- [ ] **Step 5 (Audit):** Security lead reviews technician machine to verify zero lingering data.

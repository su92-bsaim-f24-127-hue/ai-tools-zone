# Phase 4.2.7 — Technical Consulting Service Catalogue & Scope Specification
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Service Philosophy:** Genuine Developer Tool Configuration, Not Subscription Resale  
**Production Authorization:** STRICTLY NOT GRANTED  
**Commercial Pilot Authorization:** STRICTLY NOT GRANTED

---

## 1. Service Philosophy & Core Differentiation

The proposed services deliver **human technical expertise, local IDE setup, and customized workflow architecture**. They do not provide, resell, or broker software licenses. The customer pays the third-party provider directly for software access and separately hires AI Tools Zone for configuration engineering.

---

## 2. Service Tier Specifications

### Tier 1: Guided Setup Assistance (Provisional Planning Price: PKR 500)
- **Target Audience:** Individual developers, students, and freelancers adopting an AI coding tool for the first time who encounter environment configuration hurdles or need step-by-step guidance.
- **Estimated Working Time:** 20 minutes (Hard cap: 30 minutes).
- **Exact Scope of Work:**
  1. *Pre-Flight Verification:* Review operating system compatibility (Windows/macOS/Linux), Git installation, and IDE version (VS Code / JetBrains).
  2. *Supervised Vendor Registration:* Guide customer to official provider signup page and supervise checkout flow (with screen share paused during payment entry).
  3. *Basic IDE Configuration:* Assist in installing and authenticating the official extension (GitHub Copilot or Cursor IDE).
  4. *Initial Generation Verification:* Confirm that code autocompletion and basic chat prompt generation are firing successfully.
  5. *Handover Guide:* Deliver standard PDF shortcut cheat sheet and quick-start reference.
- **Deliverables:**
  - Fully functioning local AI coding extension authenticated to customer's personal account.
  - Verification test completed on customer workstation.
  - Standard AI Tools Zone Quick-Start Reference PDF.
- **Support Window:** 48 hours via WhatsApp chat for basic connection troubleshooting.
- **Rework Limits:** Maximum 1 follow-up session (up to 15 minutes) within 48 hours if initial extension stops connecting.
- **Acceptance Criteria:** Customer triggers an inline completion or chat response in their IDE and confirms completion via WhatsApp.

---

### Tier 2: Advanced Technical Setup & Prompt Architecture (Provisional Planning Price: PKR 1,000)
- **Target Audience:** Professional full-stack engineers, software agencies, and serious technical creators requiring customized workspace rules, prompt optimization, and context-window management.
- **Estimated Working Time:** 45 minutes (Hard cap: 60 minutes).
- **Exact Scope of Work:**
  1. *Complete Tier 1 Setup:* Full environment verification, supervised checkout, and extension authentication.
  2. *Custom Context Architecture (`.cursorrules`):* Author and deploy a tailored `.cursorrules` or system prompt file customized for the customer's specific tech stack (e.g., Next.js 15, FastAPI, Django, Flutter).
  3. *Repository Indexing Optimization:* Configure codebase indexing, `.cursorignore` files to exclude build artifacts and sensitive `.env` files, and optimize vector embedding cache.
  4. *Multi-Model Workflow Training:* Train customer on context tagging (`@Files`, `@Codebase`, `@Git`), test-driven generation patterns, and prompt chain design.
  5. *Curated Prompt Engineering Pack:* Deliver customized prompt templates for automated test creation, code refactoring, and API documentation.
  6. *Written Handover Blueprint:* Deliver a tailored 1-page markdown configuration summary for the customer's project repository.
- **Deliverables:**
  - Authenticated IDE environment with verified vector codebase indexing.
  - Custom `.cursorrules` / system context file committed to customer project root.
  - `.cursorignore` configured to protect local secrets and credentials.
  - AI Tools Zone Pro Prompt Engineering Pack (Markdown/PDF).
  - Written Handover Blueprint.
- **Support Window:** 7 calendar days via WhatsApp for prompt syntax tweaks and rule adjustments.
- **Rework Limits:** Up to 2 prompt or rule modifications within 7 days.
- **Acceptance Criteria:** Customer successfully runs an indexed codebase search, generates a component using the custom `.cursorrules`, and signs off on the delivered prompt pack.

---

## 3. Strict Operational Exclusions (Both Tiers)

The following items are **EXTRICTLY EXCLUDED** from both service tiers:
- ❌ **Subscription Fees:** Third-party subscription costs are not included. Customer pays the provider directly in USD.
- ❌ **Payment Handling:** Technicians will never enter their own cards or touch customer financial data.
- ❌ **Credential Storage:** Technicians will never store customer passwords, tokens, or MFA secrets.
- ❌ **Proprietary Code Debugging:** Technicians do not write or debug customer application business logic.
- ❌ **Third-Party Availability Guarantees:** AI Tools Zone does not guarantee provider server uptime, API rate limits, or AI model accuracy.
- ❌ **Account Ban Liability:** AI Tools Zone is not liable if a provider suspends a customer account for customer-initiated breaches of provider acceptable use policies.

---

## 4. Refund & Cancellation Terms

| Cancellation / Failure Scenario | Refund Entitlement | Rework Alternative |
| :--- | :---: | :--- |
| **Customer cancels before scheduled session begins** | **100% Refund** | Option to reschedule session at no extra charge. |
| **Customer card declined by provider during checkout** | **100% Refund** | Option to pause booking while customer contacts bank to activate 3DS. |
| **Customer cancels mid-session (after work begins)** | **50% Refund** | Covers technician allocated time; handover notes delivered. |
| **Technical incompatibility (hardware/OS incompatible)** | **100% Refund** | Free recommendation of compatible cloud alternatives. |
| **Session completed and deliverables accepted** | **0% Refund** | Free eligible rework within support window (48h Tier 1 / 7d Tier 2). |
| **Provider-side outage during scheduled session** | **0% Refund** | Session rescheduled for free once provider outage resolves. |

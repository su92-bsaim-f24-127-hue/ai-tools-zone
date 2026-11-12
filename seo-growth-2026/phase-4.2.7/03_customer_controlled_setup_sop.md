# Phase 4.2.7 — Customer-Controlled Setup Standard Operating Procedure (SOP)
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Classification:** Internal Technical Staff SOP & Security Standard  
**Production Authorization:** STRICTLY NOT GRANTED  
**Commercial Pilot Authorization:** STRICTLY NOT GRANTED

---

## 1. Foundational Security Principles

The Customer-Funded Technical Consulting workflow is built on an absolute separation of responsibilities:
- **The Customer is the Sole Account Principal:** The customer controls registration, credentials, payment information, Multi-Factor Authentication (MFA), renewal, cancellation, and generated intellectual property.
- **The Technician is an External Technical Guide:** The technician provides verbal and chat guidance, configuration blueprints, and prompt templates via live, customer-supervised screen sharing.
- **Zero Credential Retention Standard:** Technicians are strictly prohibited from receiving, viewing, or storing passwords, payment card details, OTP codes, session tokens, or API secrets.

---

## 2. Technician Behavioral Boundaries & Absolute Prohibitions

Technicians must strictly adhere to the following code of conduct during all consulting sessions:

| Prohibited Action | Severity Level | Consequence of Violation |
| :--- | :---: | :--- |
| **Requesting or recording customer passwords** | **CRITICAL** | Immediate termination of employment and session cancellation. |
| **Requesting MFA / 2FA SMS or authenticator codes** | **CRITICAL** | Immediate termination of employment and session cancellation. |
| **Viewing or recording credit/debit card numbers or CVVs** | **CRITICAL** | Immediate reporting to security lead and card rotation protocol. |
| **Storing API keys, access tokens, or session cookies** | **CRITICAL** | Immediate audit of local technician machines and credential revocation. |
| **Creating hidden or persistent remote access tools** | **CRITICAL** | Immediate legal review and security escalation. |
| **Operating shared master accounts or pooled logins** | **CRITICAL** | Immediate cessation of consulting activity. |
| **Making unprovable privacy or security guarantees** | **HIGH** | Mandatory retraining and formal warning. |

---

## 3. Supervised Screen-Sharing SOP: Step-by-Step Execution

```
[Step 1: Session Initiation] ──> Customer joins Google Meet / Zoom; technician confirms audio/video.
[Step 2: Pre-Check & Consent] ─> Customer reviews SOW and agrees to live supervised screen sharing.
[Step 3: Supervised Checkout] ─> Customer opens vendor site; PAUSES screen share to enter card details.
[Step 4: IDE & Tool Setup] ───> Customer resumes screen share; technician guides config and extensions.
[Step 5: Handover & Verification] ─> Customer verifies tool generation; session ends; zero data retained.
```

### 3.1 Step 1: Session Initiation & Tool Selection
- Consulting sessions are conducted exclusively over **Google Meet** or **Zoom**.
- **Remote Control Tools (AnyDesk, TeamViewer) Are Barred By Default:** Standard screen sharing (display only) is mandatory. If keyboard assistance is explicitly requested for terminal setup, it must be performed live with the customer sitting at the workstation, capable of disconnecting with one click.

### 3.2 Step 2: Customer Consent & Pre-Flight Briefing
1. Technician greets customer and verifies identity against the paid WhatsApp booking receipt.
2. Technician reads the mandatory verbal disclaimer:
   > *"Before we begin, please note that AI Tools Zone provides independent configuration assistance. You will be registering and paying the software provider directly. Please ensure that all personal files and private browser tabs are closed. You may pause or terminate this screen-sharing session at any moment."*
3. Customer verbally acknowledges consent.

### 3.3 Step 3: Supervised Registration & Payment Checkout
1. Technician instructs customer to navigate to the official provider URL (`github.com/settings/copilot`, `cursor.com/pricing`, or `claude.ai/upgrade`).
2. Customer completes personal account registration using their own personal email.
3. **MANDATORY PAYMENT PRIVACY PROTOCOL:**
   - When the customer reaches the Stripe/vendor checkout page, the technician **MUST EXPLICITLY INSTRUCT THE CUSTOMER TO PAUSE SCREEN SHARING**:
     > *"Please pause your screen share now while you enter your card details and complete checkout. Let me know when you see the confirmation screen."*
   - Technician confirms screen share is paused (blank screen / call window only).
   - Customer enters card details and completes 3DS verification.
   - Once payment is confirmed, customer resumes screen sharing.

### 3.4 Step 4: Technical Configuration & Environment Setup
1. **For Cursor:**
   - Technician guides customer to download and install Cursor.
   - Customer opens project repository.
   - Technician provides curated `.cursorrules` configuration via meeting chat.
   - Customer pastes configuration into `.cursor/rules` or project root.
   - Technician guides configuration of codebase indexing and privacy mode toggles.
2. **For GitHub Copilot:**
   - Technician guides installation of GitHub Copilot and Copilot Chat extensions in VS Code or JetBrains IDE.
   - Customer signs in via GitHub browser OAuth flow.
   - Technician guides configuration of keybindings, autocomplete trigger delays, and inline suggestions.
3. **For Claude / Claude Code:**
   - Customer verifies login at `claude.ai`.
   - Technician guides creation of Projects workspaces and custom style prompts.
   - If using Claude Code CLI: customer opens terminal, technician provides install command (`npm install -g @anthropic-ai/claude-code`), customer authorizes CLI in browser directly.

### 3.5 Step 5: Verification, Handover & Session Closure
1. Customer runs a sample prompt to verify completions are functioning correctly.
2. Technician delivers written handover notes (prompt pack, shortcut cheat sheet).
3. Technician verifies that no customer files or secrets remain on technician machine (clearing meeting chat).
4. Session is formally concluded.

---

## 4. Security Incident Response Procedure: Accidental Credential Exposure

If a customer accidentally displays a password, credit card number, API secret, or personal document on screen:

```
[Phase 1: Immediate Freeze] ──> Technician instructs customer to STOP sharing instantly.
[Phase 2: Active Containment] ─> Technician confirms no screenshots or recordings were taken.
[Phase 3: Remediation Advice] ─> Technician provides immediate rotation steps to customer.
[Phase 4: Internal Incident Log] ─> Incident documented in internal security log within 2 hours.
```

1. **Immediate Freeze (T + 0 Minutes):**
   - Technician immediately states: *"Please pause your screen share right now—sensitive information is visible."*
   - Technician averts gaze and minimizes call window.
2. **Remediation & Rotation Advice (T + 5 Minutes):**
   - **Exposed Password:** Instruct customer to immediately change their account password and activate MFA.
   - **Exposed Credit Card:** Instruct customer to monitor banking app and consider freezing/replacing card if CVV was visible.
   - **Exposed API Key:** Instruct customer to immediately revoke the exposed key in the provider console and generate a replacement.
3. **Internal Logging (T + 2 Hours):**
   - Technician files an internal incident report documenting date, time, nature of exposed data, and remediation steps advised.
   - Store owner reviews log to ensure zero customer secrets were captured in system buffers.

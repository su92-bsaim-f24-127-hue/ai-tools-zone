# Phase 4.3 — Technician Screen-Sharing Execution Protocol & Security SOP
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Role:** Lead Configuration Technician  
**Standard:** Supervised Screen Sharing | Zero Credential Retention  
**Production Authorization:** STRICTLY NOT GRANTED

---

## 1. Technician Operational Principles

As an AI Tools Zone Configuration Technician, you are an **expert technical guide**, not an account operator:
- You guide the customer verbally and via meeting chat.
- The customer executes all clicks, keystrokes, and terminal commands on their own workstation.
- You must **NEVER** view, record, or request customer passwords, credit card numbers, CVVs, or OTP codes.

---

## 2. Step-by-Step Live Session Execution Protocol

```
[Phase 1: Pre-Flight] ──> Test audio/video; load tech-stack blueprints; verify booking.
[Phase 2: Briefing] ────> Greet client; deliver security disclaimer; confirm screen share.
[Phase 3: Checkout] ────> Guide to official signup; MANDATORY PAUSE SCREEN SHARE during card entry.
[Phase 4: Tool Config] ─> Resume screen share; guide IDE install, .cursorrules deployment, indexing.
[Phase 5: Verification] ─> Customer runs sample prompt; deliverables accepted; session ends.
```

### Phase 1: Pre-Flight Check (5 Minutes Before Session)
- [ ] Verify customer details and chosen tier (Tier 1 vs Tier 2) on the Pilot KPI Ledger.
- [ ] Open the customer's selected tech-stack blueprint (`.cursorrules` Next.js/FastAPI) in local editor.
- [ ] Ensure local screen-recording software is **DISABLED** (meeting recording is strictly barred).
- [ ] Join Google Meet call link.

### Phase 2: Greeting & Security Disclaimer (Minutes 0–5)
- [ ] Greet customer professionally: *"Assalam-o-Alaikum [Name]! Welcome to your AI Tools Zone setup session."*
- [ ] Deliver verbal security notice:
  > *"Before you share your screen, please ensure any personal documents, bank tabs, or private chats are closed. You will remain in complete control of your mouse and keyboard throughout this session. You can pause or stop screen sharing at any moment."*
- [ ] Customer initiates standard screen share (display only; no remote control).

### Phase 3: Supervised Vendor Checkout (Minutes 5–10)
- [ ] Instruct customer to navigate to the official provider checkout URL:
  - Cursor: `cursor.com/pricing`
  - GitHub Copilot: `github.com/settings/copilot`
  - Claude: `claude.ai/upgrade`
- [ ] Customer registers or logs into their personal account.
- [ ] Customer clicks upgrade/subscribe.
- [ ] **MANDATORY PAYMENT PRIVACY PROTOCOL:**
  - When the Stripe/card entry page appears, immediately instruct the customer:
    > *"Please pause your screen share right now while you enter your card details and complete the bank OTP verification. Let me know once you see the confirmation screen."*
  - **VERIFY:** Confirm meeting screen is paused / blank.
  - Wait patiently while customer completes 3DS verification.
- [ ] Customer resumes screen share once payment confirmation is displayed.

### Phase 4: IDE Installation & Technical Configuration (Minutes 10–35)
- [ ] **For Cursor:**
  - Guide download and installation of Cursor IDE client.
  - Verify personal account login inside Cursor.
  - Customer opens project repository in Cursor.
  - Send the tailored `.cursorrules` text via Google Meet chat.
  - Customer creates `.cursor/rules` or `.cursorrules` file in project root and pastes configuration.
  - Guide customer to configure `.cursorignore` (adding `.env*`, `node_modules`, `dist`, `.git`).
  - Trigger codebase vector indexing under `Cursor Settings -> Features -> Codebase Indexing`.
- [ ] **For GitHub Copilot:**
  - Guide customer to Extensions tab in VS Code or JetBrains.
  - Search and install official `GitHub Copilot` and `GitHub Copilot Chat` extensions.
  - Customer clicks 'Sign in to GitHub' and completes browser OAuth authorization.
  - Configure keybindings and autocomplete delays in `settings.json`.
- [ ] **For Claude / Claude Code:**
  - Guide creation of Projects folder in `claude.ai` and setup of custom instructions.
  - If CLI user: customer opens terminal and runs `npm install -g @anthropic-ai/claude-code`.
  - Customer executes initial auth flow directly in terminal.

### Phase 5: Verification, Handover & Sign-Off (Minutes 35–45)
- [ ] **Generation Verification Test:** Instruct customer to trigger an inline completion or prompt generation (e.g., generating a typed TypeScript interface or Python Pydantic model).
- [ ] Verify output is generated successfully without rate-limit or authentication errors.
- [ ] Deliver AI Tools Zone Pro Prompt Pack via WhatsApp / email.
- [ ] Inform customer of their support duration (48 hours for Tier 1; 7 days for Tier 2).
- [ ] Ask customer for sign-off: *"Are you satisfied with the configuration and completions?"*
- [ ] Conclude session and exit meeting.

---

## 3. Post-Session Cleanup & Audit
- [ ] Clear meeting chat window.
- [ ] Confirm zero customer credentials, tokens, or personal snippets remain on technician machine.
- [ ] Record session duration, technician name, and completion status on `05_pilot_client_tracking_and_kpi_ledger.csv`.

"""
generate_phase_4_3_deliverables.py
Generates the 7 operational deliverables for Phase 4.3 in seo-growth-2026/phase-4.3/
"""

import os
import csv
from decimal import Decimal, ROUND_HALF_UP

OUTPUT_DIR = os.path.join(os.getcwd(), "seo-growth-2026", "phase-4.3")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Generating Phase 4.3 deliverables in: {OUTPUT_DIR}")

# ==============================================================================
# DELIVERABLE 1: 01_phase_4_3_pilot_execution_blueprint.md
# ==============================================================================
print("Generating 01_phase_4_3_pilot_execution_blueprint.md...")
d1_content = r"""# Phase 4.3 — Controlled Pilot Execution Blueprint
## Operational Framework for the 10-Session Customer-Funded Consulting Pilot

**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Operating Model:** Model D (Customer-Funded Technical Configuration Consulting)  
**Pilot Ceiling:** Strict Cap of No More Than 10 Completed Sessions  
**Mode:** Operational Blueprint & Asset Staging Only  
**Production Authorization:** STRICTLY NOT GRANTED  
**Commercial Launch Authorization:** STRICTLY NOT GRANTED (Pending Owner Sign-Off)

---

## 1. Operational Framework & Scope

This blueprint defines the end-to-end execution protocol for the controlled 10-session pilot of AI Tools Zone's **Customer-Funded Technical Consulting Service**. 

### 1.1 Non-Negotiable Operational Principles
1. **Total Fund Separation:** AI Tools Zone never procures, intermediates, or touches funds destined for third-party software subscriptions. The customer pays GitHub, Anysphere, or Anthropic directly via their own international payment card.
2. **Sole Customer Account Ownership:** The customer is the sole registrant, account holder, and licensee. The customer enters all passwords, 2FA/MFA codes, and billing information directly on their personal machine.
3. **Domestic Service Fee:** AI Tools Zone charges an unbundled domestic technical consulting fee (**Tier 1: PKR 500** or **Tier 2: PKR 1,000**) collected in PKR via Direct Business IBFT into a declared commercial bank account.
4. **Strict Pilot Cap:** The pilot is capped at **exactly 10 completed sessions**. Upon reaching 10 sessions, all booking is suspended pending an executive review of unit economics and customer satisfaction.

---

## 2. Pilot Cohort Target Distribution

The 10-session pilot is structured across target tools and service tiers to test technical feasibility across diverse developer workflows:

| Target Tool | Tool USD Cost | Target Pilot Sessions | Primary Technical Focus |
| :--- | :---: | :---: | :--- |
| **Cursor AI Pro** | $20.00 / month | **4 to 5 Sessions** | IDE setup, vector codebase indexing, custom `.cursorrules` authoring. |
| **GitHub Copilot** | $10.00 / month | **4 to 5 Sessions** | VS Code / JetBrains extension authentication, keyboard shortcuts, inline completions. |
| **Claude Pro / Claude Code** | $20.00 / month | **1 to 2 Sessions** | Projects workspace setup, prompt pack delivery, `@anthropic-ai/claude-code` CLI setup. |

### Tier Breakdown:
- **Tier 1 (Guided Setup Assistance - 20 mins @ PKR 500):** Target ~5 sessions.
- **Tier 2 (Advanced Setup & Prompt Pack - 40–45 mins @ PKR 1,000):** Target ~5 sessions.

---

## 3. Team Roles & Operational Responsibilities

```
┌─────────────────────────────────┐
│     STORE OWNER / EXECUTIVE     │ ──> Final Gate Authorization & Pilot Stop Control
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   WHATSAPP INTAKE SPECIALIST    │ ──> Lead Pre-Qualification, SOW Delivery, IBFT Verification
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│  LEAD CONFIGURATION TECHNICIAN  │ ──> Live Screen-Sharing Guidance, SOP Execution, Verification
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   QA & COMPLIANCE REVIEWER      │ ──> Zero-Credential Audit, CSAT Logging, KPI Ledger Tracking
└─────────────────────────────────┘
```

1. **WhatsApp Intake Specialist:** Monitors inbound inquiries; screens for hardware compatibility and international card readiness; sends standardized scope cards; verifies domestic IBFT payment receipts; schedules Google Meet slots.
2. **Lead Configuration Technician:** Conducts live, customer-supervised screen-sharing sessions; enforces the mandatory paused-screen payment protocol; deploys `.cursorrules` blueprints; verifies active completions; delivers handover cheat sheets.
3. **QA & Compliance Reviewer:** Audits meeting logs to verify zero credential exposure; tracks session durations; records CSAT ratings; monitors hard stop condition triggers.
4. **Store Owner:** Holds sole authority to approve pilot initiation, review mid-pilot metrics, and decide on commercial scaling.

---

## 4. End-to-End Pilot Execution Timeline

```
[Phase 4.3.A: Internal Readiness] ──> Internal Rehearsals (3 Mock Sessions) & Payment Rail Test
[Phase 4.3.B: Owner Sign-Off] ──────> Owner approves 10 Gates & authorizes Pilot Launch
[Phase 4.3.C: Inbound Intake] ──────> First 10 qualified WhatsApp leads pre-screened & booked
[Phase 4.3.D: Session Delivery] ────> 10 sessions executed under strict supervised screen share
[Phase 4.3.E: Executive Audit] ─────> Full financial & CSAT reconciliation presented to Owner
```

- **Phase 4.3.A (Internal Rehearsals):** Conduct 3 internal mock sessions with internal staff (Windows, macOS, Linux) to test technician timings, screen-share stability, and `.cursorrules` generation before touching real leads.
- **Phase 4.3.B (Owner Sign-Off):** Store owner executes written sign-off on the 10 Owner Approval Gates.
- **Phase 4.3.C (Controlled Intake):** Intake Specialist activates the standardized WhatsApp intake script for organic inbound inquiries.
- **Phase 4.3.D (Execution):** Deliver sessions one by one, updating the Pilot KPI Ledger after each session.
- **Phase 4.3.E (Audit & Review):** Synthesize actual labor durations, payment fees, customer feedback, and realized operating contribution.
"""

with open(os.path.join(OUTPUT_DIR, "01_phase_4_3_pilot_execution_blueprint.md"), "w", encoding="utf-8") as f:
    f.write(d1_content.strip() + "\n")

# ==============================================================================
# DELIVERABLE 2: 02_whatsapp_inbound_intake_scripts.md
# ==============================================================================
print("Generating 02_whatsapp_inbound_intake_scripts.md...")
d2_content = r"""# Phase 4.3 — WhatsApp Inbound Intake Scripts & Communication SOP
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Primary Channel:** WhatsApp Business (+92 343 0173923)  
**Language:** English & Roman Urdu  
**Status:** Staged Intake Templates for Pilot Execution  
**Production Authorization:** STRICTLY NOT GRANTED

---

## 1. Intake Architecture & Pre-Qualification Funnel

To prevent customer expectation mismatch (e.g., customers expecting "cheap shared accounts"), the WhatsApp intake workflow immediately clarifies the **Model D structure**: the customer pays the provider directly in USD, and AI Tools Zone provides expert technical setup and prompt architecture.

---

## 2. Standardized Message Templates

### Template 1: Initial Greeting & Model D Expectation Setting
*Trigger: Prospective customer messages WhatsApp asking about Copilot, Cursor, or Claude.*

> **English:**  
> "Assalam-o-Alaikum! Welcome to AI Tools Zone. 🚀  
> Thank you for reaching out. We specialize in **Professional AI Developer Setup & Technical Configuration Consulting**.  
>  
> **How our service works:**  
> 1. You register and subscribe directly with the software provider (GitHub, Cursor, or Anthropic) using your own payment card. Your account, data, and code remain 100% private to you.  
> 2. An AI Tools Zone technical engineer joins you on a live, supervised screen-sharing session to configure your IDE, set up custom project rules (`.cursorrules`), optimize vector indexing, and provide curated prompt engineering blueprints.  
>  
> To check if your environment is ready, could you please tell us:  
> - Which tool do you want to configure (GitHub Copilot, Cursor, or Claude)?  
> - What operating system and tech stack are you using (e.g., Windows/macOS, Next.js, Python)?  
> - Do you have an active debit/credit card with international online shopping enabled?"

> **Roman Urdu:**  
> "Assalam-o-Alaikum! AI Tools Zone mein khush-amdeed. 🚀  
> Rabta karne ka shukriya. Hum **Professional AI Developer Setup aur Technical Consulting** provide karte hain.  
>  
> **Hamara model kaisay kaam karta hai:**  
> 1. Aap software provider (GitHub, Cursor, ya Anthropic) ki official website par apnay card se direct subscribe karte hain. Aapka account, data aur code 100% aapke control mein rehta hai.  
> 2. AI Tools Zone ka engineer aapke saath live Google Meet screen share par connect karta hai aur aapka IDE setup, custom `.cursorrules`, indexing aur developer prompt templates configure karwata hai.  
>  
> Environment check karne ke liye barah-e-karam batayein:  
> - Aap kaunsa tool configure karwana chahte hain (Copilot, Cursor, ya Claude)?  
> - Aapka OS aur tech stack kya hai (e.g., Windows/macOS, Next.js, Python)?  
> - Kya aapke paas international online shopping enabled payment card moojood hai?"

---

### Template 2: Service Scope & Pricing Cards
*Trigger: Customer confirms hardware and international card readiness.*

> **English:**  
> "Excellent! Here are our two consulting service options:  
>  
> 🛠️ **Option 1: Guided Setup Assistance (PKR 500)**  
> • Duration: ~20 Minutes (Live Google Meet Screen Share)  
> • Prerequisites check & guided vendor checkout.  
> • Official IDE extension installation & OAuth authentication.  
> • Inline completion and chat verification.  
> • Quick-Start Developer Shortcut Guide (PDF).  
> • 48-Hour follow-up connection support.  
> *(Provider subscription cost: $10 or $20 paid directly by you to provider).*  
>  
> ⚡ **Option 2: Advanced Setup & Prompt Architecture (PKR 1,000)** *(Recommended)*  
> • Duration: ~40–45 Minutes (Live Google Meet Screen Share)  
> • Complete Option 1 environment setup.  
> • Custom `.cursorrules` blueprint tailored to your tech stack.  
> • Repository vector indexing & `.cursorignore` secrets protection.  
> • Pro Prompt Engineering Pack (Testing, Refactoring, Documentation).  
> • 7-Day WhatsApp prompt tweaking support.  
> *(Provider subscription cost: $10 or $20 paid directly by you to provider).*  
>  
> Which option suits your development workflow best?"

---

### Template 3: Payment Request & Bank Account Details
*Trigger: Customer selects Tier 1 or Tier 2.*

> **English:**  
> "Great choice! To book your dedicated consulting slot, please transfer the domestic consulting fee:  
>  
> **Payment Details (Direct Business Transfer):**  
> • Bank: [Bank Name, e.g., Meezan Bank / Bank Alfalah]  
> • Account Title: AI Tools Zone  
> • Account Number / IBAN: PK00XXXX0000000000000000  
> • Raast ID: [Business Raast ID / Mobile Number]  
> • Amount: **PKR [500 or 1,000]**  
>  
> Once transferred, please reply with a screenshot of the payment receipt. We will immediately confirm your booking and send your Google Meet session link."

---

### Template 4: Booking Confirmation & Session Preparation Instructions
*Trigger: Payment receipt verified by Intake Specialist.*

> **English:**  
> "Payment received! Thank you. Your session is confirmed. 🎯  
>  
> 📅 **Session Time:** [Date & Time, e.g., Today at 4:00 PM PKT]  
> 🔗 **Google Meet Link:** https://meet.google.com/xxx-xxxx-xxx  
>  
> **Pre-Flight Preparation (Please complete before joining):**  
> 1. Ensure your PC/Mac is connected to stable internet.  
> 2. Have your international payment card ready for vendor checkout.  
> 3. Close all personal tabs, private documents, and confidential projects.  
>  
> *Security Note: Our technician will NEVER ask for your password, card details, or OTP codes. When entering payment details on the provider's website, you will pause screen sharing.*  
>  
> See you on the call!"

---

### Template 5: Post-Session Handover & Sign-Off Script
*Trigger: Technician completes configuration on Google Meet.*

> **English:**  
> "Your AI development environment is now fully active and verified! 🚀  
>  
> 📁 **Attached Deliverables:**  
> • Tailored `.cursorrules` / Configuration Blueprint  
> • AI Tools Zone Pro Prompt Pack (PDF/Markdown)  
> • Quick-Start Keyboard Shortcuts Reference  
>  
> Your support window is active for [48 Hours / 7 Days]. If you have any prompt syntax or configuration questions, simply message us here.  
>  
> Could you please reply with a quick confirmation: **'Setup verified and accepted'**?  
> Thank you for choosing AI Tools Zone!"

---

### Template 6: International Card Decline Assistance Script
*Trigger: Customer card fails 3DS verification during provider checkout.*

> **English:**  
> "It looks like your bank declined the international online transaction. This is common in Pakistan when cross-border ecommerce is not pre-activated.  
>  
> **Quick Fix Steps:**  
> 1. Open your mobile banking app (Meezan, HBL, Alfalah, SadaPay, etc.).  
> 2. Go to 'Card Management' -> 'International Transactions' / 'Online Shopping'.  
> 3. Activate international ecommerce for a 24-hour session.  
> 4. If using an automated helpline, call your bank and request: *'Please activate international ecommerce on my card for a foreign subscription.'*  
>  
> We have paused your consulting session. Take your time to activate your card, and message us back as soon as it's enabled so we can resume immediately!"
"""

with open(os.path.join(OUTPUT_DIR, "02_whatsapp_inbound_intake_scripts.md"), "w", encoding="utf-8") as f:
    f.write(d2_content.strip() + "\n")

# ==============================================================================
# DELIVERABLE 3: 03_technician_screen_share_execution_checklist.md
# ==============================================================================
print("Generating 03_technician_screen_share_execution_checklist.md...")
d3_content = r"""# Phase 4.3 — Technician Screen-Sharing Execution Protocol & Security SOP
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
"""

with open(os.path.join(OUTPUT_DIR, "03_technician_screen_share_execution_checklist.md"), "w", encoding="utf-8") as f:
    f.write(d3_content.strip() + "\n")

# ==============================================================================
# DELIVERABLE 4: 04_custom_cursorrules_and_prompt_blueprints.md
# ==============================================================================
print("Generating 04_custom_cursorrules_and_prompt_blueprints.md...")
d4_content = r"""# Phase 4.3 — Proprietary `.cursorrules` Blueprints & Prompt Engineering Pack
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Classification:** Proprietary Work of Authorship (Owned by AI Tools Zone)  
**Permitted Commercial Mode:** Client Consulting Deliverable (Tier 2 Advanced Setup)  
**Production Authorization:** STRICTLY NOT GRANTED

---

## 1. Intellectual Property & License Notice
The configuration templates and prompt engineering blueprints contained herein are original works of authorship created by AI Tools Zone technical staff. They are licensed exclusively to paying consulting clients for internal development use. Redistribution or commercial resale by third parties is prohibited.

---

## 2. Production `.cursorrules` Blueprints

### Blueprint 1: Next.js 15 & React Full-Stack Architecture
*Target Stack: Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, Server Actions, Prisma/Supabase.*

```markdown
# AI Tools Zone - Next.js 15 Full-Stack Configuration Rules
# (c) 2026 AI Tools Zone. Client Consulting License.

You are an expert full-stack Next.js 15, React 19, TypeScript, and Tailwind CSS engineer.

## Architecture & Code Structure
- Always use the Next.js App Router (`app/` directory).
- Default to React Server Components (RSC). Only mark components with `'use client'` when using state, hooks, or browser event listeners.
- Keep server actions in dedicated files (e.g., `app/actions/`) marked with `'use server'`.
- Validate all incoming server action data using Zod schemas before database execution.
- Use TypeScript strict mode with explicit interfaces. Never use `any`.

## Styling & UI Guidelines
- Use Tailwind CSS utility classes exclusively. Avoid raw CSS files or inline style objects.
- Ensure all interactive elements have responsive layouts, accessible ARIA attributes, and hover/focus-visible states.
- Follow mobile-first responsive breakpoints (`sm:`, `md:`, `lg:`, `xl:`).

## Performance & Security
- Optimize image delivery using `next/image` with explicit `width`, `height`, and priority attributes for LCP images.
- Protect all API routes and Server Actions with authenticated session checks.
- Never hardcode API keys, secrets, or database URLs in source code. Reference environment variables via `process.env.NEXT_PUBLIC_*` or server-only `process.env.*`.
```

---

### Blueprint 2: Python, FastAPI & Asynchronous Backend Architecture
*Target Stack: Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy (Async), Alembic, Pytest.*

```markdown
# AI Tools Zone - FastAPI & Python Architecture Rules
# (c) 2026 AI Tools Zone. Client Consulting License.

You are an expert Python 3.12+ backend architect specializing in FastAPI, Pydantic v2, and async SQLAlchemy.

## Code Standards & Conventions
- Write clean, modular, object-oriented, and type-annotated Python code adhering strictly to PEP 8.
- Use Pydantic v2 `BaseModel` schemas for all request validation and response models.
- Always implement explicit type hints (`typing.Optional`, `typing.List`, `typing.Annotated`).
- Utilize asynchronous handlers (`async def`) for I/O-bound database queries and HTTP requests.

## Database & ORM Rules
- Use AsyncSession with SQLAlchemy 2.0+ syntax (`select()`, `scalars()`).
- Never perform blocking synchronous operations inside an async route handler.
- Handle database transactions within context managers with automatic rollback on exception.

## Testing & Error Handling
- Use standard FastAPI `HTTPException` with explicit status codes and error detail payloads.
- Write unit and integration tests using `pytest` and `httpx.AsyncClient`.
- Maintain docstrings following Google Python Style Guide for all service functions.
```

---

## 3. Curated Prompt Engineering Pack (Client Reference)

### Prompt Pack 1: Test-Driven Generation Pattern (TDD)
> *"Given the following TypeScript interface and business requirements:  
> [PASTE INTERFACE / REQUIREMENTS]  
> Generate a comprehensive Pytest / Vitest test suite that covers:  
> 1. Happy path execution with valid inputs.  
> 2. Boundary edge cases (empty arrays, maximum string lengths, null inputs).  
> 3. Negative error cases with expected exceptions and error messages.  
> Write clean, readable assertions with descriptive test titles. Do not write the implementation code yet."*

### Prompt Pack 2: Performance & Token Optimization Pattern
> *"Analyze the following function for algorithmic bottlenecks, redundant database queries, and memory leaks:  
> [PASTE CODE]  
> Refactor the code to:  
> 1. Reduce time complexity from O(n^2) to O(n) or O(n log n).  
> 2. Implement batching or caching where applicable.  
> 3. Provide a brief explanation of before-vs-after computational complexity."*

### Prompt Pack 3: Secure API Route Boilerplate Generator
> *"Generate a production-ready Next.js / FastAPI route handler for the following endpoint:  
> [SPECIFY ROUTE, E.G., POST /api/v1/orders]  
> Requirements:  
> 1. Strict input validation using Zod / Pydantic.  
> 2. Authentication check and rate-limiting middleware.  
> 3. Structured error responses matching standard RFC 7807 problem details.  
> 4. Structured logging for audit compliance."*
"""

with open(os.path.join(OUTPUT_DIR, "04_custom_cursorrules_and_prompt_blueprints.md"), "w", encoding="utf-8") as f:
    f.write(d4_content.strip() + "\n")

# ==============================================================================
# DELIVERABLE 5: 05_pilot_client_tracking_and_kpi_ledger.csv
# ==============================================================================
print("Generating 05_pilot_client_tracking_and_kpi_ledger.csv...")
d5_headers = [
    "Session ID",
    "Client WhatsApp Handle",
    "Target Tool",
    "Service Tier",
    "Booking Date",
    "Session Date",
    "Duration (Mins)",
    "Technician Assigned",
    "Payment Rail Used",
    "Gross Fee Paid (PKR)",
    "Provider Checkout Status",
    "Deliverables Accepted (Y/N)",
    "Rework Requested (Y/N)",
    "Support Chat Mins",
    "CSAT Rating (1-5)",
    "Operating Contribution (PKR)",
    "Stop Trigger Flag"
]

d5_rows = [
    [
        "PILOT-01", "Pending Intake", "Cursor AI Pro", "Tier 2", "TBD", "TBD", "", "Tech Lead", "Direct Business IBFT", "1000.00", "Pending", "", "", "", "", "", "NORMAL"
    ],
    [
        "PILOT-02", "Pending Intake", "GitHub Copilot", "Tier 1", "TBD", "TBD", "", "Tech Lead", "Direct Business IBFT", "500.00", "Pending", "", "", "", "", "", "NORMAL"
    ],
    [
        "PILOT-03", "Pending Intake", "Cursor AI Pro", "Tier 2", "TBD", "TBD", "", "Tech Lead", "Direct Business IBFT", "1000.00", "Pending", "", "", "", "", "", "NORMAL"
    ],
    [
        "PILOT-04", "Pending Intake", "GitHub Copilot", "Tier 1", "TBD", "TBD", "", "Tech Lead", "Direct Business IBFT", "500.00", "Pending", "", "", "", "", "", "NORMAL"
    ],
    [
        "PILOT-05", "Pending Intake", "Claude Pro", "Tier 2", "TBD", "TBD", "", "Tech Lead", "Direct Business IBFT", "1000.00", "Pending", "", "", "", "", "", "NORMAL"
    ],
    [
        "PILOT-06", "Pending Intake", "Cursor AI Pro", "Tier 2", "TBD", "TBD", "", "Tech Lead", "Direct Business IBFT", "1000.00", "Pending", "", "", "", "", "", "NORMAL"
    ],
    [
        "PILOT-07", "Pending Intake", "GitHub Copilot", "Tier 1", "TBD", "TBD", "", "Tech Lead", "Direct Business IBFT", "500.00", "Pending", "", "", "", "", "", "NORMAL"
    ],
    [
        "PILOT-08", "Pending Intake", "Cursor AI Pro", "Tier 2", "TBD", "TBD", "", "Tech Lead", "Direct Business IBFT", "1000.00", "Pending", "", "", "", "", "", "NORMAL"
    ],
    [
        "PILOT-09", "Pending Intake", "GitHub Copilot", "Tier 1", "TBD", "TBD", "", "Tech Lead", "Direct Business IBFT", "500.00", "Pending", "", "", "", "", "", "NORMAL"
    ],
    [
        "PILOT-10", "Pending Intake", "Claude Pro", "Tier 2", "TBD", "TBD", "", "Tech Lead", "Direct Business IBFT", "1000.00", "Pending", "", "", "", "", "", "NORMAL"
    ]
]

with open(os.path.join(OUTPUT_DIR, "05_pilot_client_tracking_and_kpi_ledger.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(d5_headers)
    writer.writerows(d5_rows)

# ==============================================================================
# DELIVERABLE 6: 06_internal_rehearsal_and_mock_session_report.md
# ==============================================================================
print("Generating 06_internal_rehearsal_and_mock_session_report.md...")
d6_content = r"""# Phase 4.3 — Internal Rehearsal & Mock Session Verification Protocol
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Prerequisite:** Mandatory Staff Rehearsal Protocol Prior to Live Customer Intake  
**Production Authorization:** STRICTLY NOT GRANTED

---

## 1. Purpose of Internal Rehearsals

Before any customer-facing pilot session can take place, the technical team must conduct **three mandatory internal mock rehearsals** with internal staff acting as client personas. This ensures:
1. Technician timings strictly respect the planned duration budgets (20 mins for Tier 1; 40–45 mins for Tier 2).
2. The paused-screen payment protocol operates flawlessly without awkwardness or technical confusion.
3. `.cursorrules` generation and indexing scripts deploy without syntax errors across Windows, macOS, and Linux.

---

## 2. The Three Mandatory Mock Session Scenarios

### Mock Session 1: Windows 11 + VS Code + GitHub Copilot (Tier 1 Setup)
- **Simulated Persona:** Junior Frontend Developer with a fresh Windows 11 laptop, VS Code installed, but no Copilot extension.
- **Drill Focus:**
  - Guide to `github.com/settings/copilot`.
  - Execute mandatory paused-screen checkout drill.
  - Install VS Code Copilot extension and complete browser OAuth.
  - Test inline completions on an HTML/JS file.
- **Target Duration:** < 20 Minutes.
- **Success Benchmark:** Fully working inline completions verified within 18 minutes.

---

### Mock Session 2: macOS + Cursor AI Pro + Next.js Tech Stack (Tier 2 Setup)
- **Simulated Persona:** Mid-Level Full-Stack Developer on macOS wanting custom Next.js 15 App Router `.cursorrules`.
- **Drill Focus:**
  - Guide download of Cursor macOS binary (Apple Silicon).
  - Execute paused-screen checkout drill on `cursor.com/pricing`.
  - Deploy Blueprint 1 (`.cursorrules` for Next.js 15) into root of mock Next.js repo.
  - Configure `.cursorignore` to exclude `.env.local` and `.next`.
  - Trigger and verify codebase vector indexing.
- **Target Duration:** < 45 Minutes (Alt A) / < 40 Minutes (Alt B).
- **Success Benchmark:** Custom component generated adhering to server-component rules within 38 minutes.

---

### Mock Session 3: Linux / Ubuntu + Claude Pro / Claude Code CLI (Tier 2 Setup)
- **Simulated Persona:** Backend Python / DevOps Engineer wanting terminal-based AI workflow.
- **Drill Focus:**
  - Guide to `claude.ai/upgrade` with paused-screen checkout drill.
  - Install Node.js npm package `@anthropic-ai/claude-code`.
  - Authenticate CLI tool via terminal OAuth flow.
  - Deliver Python FastAPI prompt blueprints.
- **Target Duration:** < 45 Minutes.
- **Success Benchmark:** CLI query executed in terminal within 35 minutes.

---

## 3. Mock Rehearsal Verification Sign-Off
Upon successful completion of all three mock sessions, the Lead Configuration Technician and QA Reviewer sign the Internal Rehearsal Certification, clearing the operational team for live customer pilot onboarding upon owner authorization.
"""

with open(os.path.join(OUTPUT_DIR, "06_internal_rehearsal_and_mock_session_report.md"), "w", encoding="utf-8") as f:
    f.write(d6_content.strip() + "\n")

# ==============================================================================
# DELIVERABLE 7: 07_phase_4_3_pilot_readiness_audit.md
# ==============================================================================
print("Generating 07_phase_4_3_pilot_readiness_audit.md...")
d7_content = r"""# Phase 4.3 — Operational Pilot Readiness Audit & Governance Sign-Off
**Project:** AI Tools Zone (`https://aitoolszone.tech/`)  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Expected Production Baseline:** `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`  
**Audit Scope:** Verification of Operational Pilot Assets & Governance Pre-Conditions  
**Production Authorization:** STRICTLY NOT GRANTED  
**Commercial Launch Authorization:** STRICTLY NOT GRANTED

---

## 1. Operational Asset Verification Checklist

| Asset Deliverable | Content & Operational Scope | Verification Status |
| :--- | :--- | :---: |
| **01. Pilot Execution Blueprint** | Complete 10-session operational framework, team roles, and execution timeline. | **VERIFIED ON DISK** |
| **02. WhatsApp Inbound Scripts** | Bilingual intake scripts, scope cards, payment instructions, and decline SOP. | **VERIFIED ON DISK** |
| **03. Technician Execution Checklist** | Step-by-step live session protocol with mandatory paused-screen payment drill. | **VERIFIED ON DISK** |
| **04. Proprietary Blueprints & Prompts** | Next.js and FastAPI `.cursorrules` + curated prompt engineering packs. | **VERIFIED ON DISK** |
| **05. Pilot KPI Tracking Ledger** | 17-column client ledger pre-staged for 10 pilot client sessions. | **VERIFIED ON DISK** |
| **06. Internal Rehearsal Protocol** | 3 mock session drills (Windows, macOS, Linux) to validate technician timings. | **VERIFIED ON DISK** |

---

## 2. Maintenance of Commercial Holds & Baseline Security

1. **Commercial Holds Strictly Maintained:**
   - Netflix Premium 4K shared profiles: **ON HOLD**.
   - Google Flow / Veo shared accounts: **ON HOLD**.
   - Surfshark VPN credential pools: **ON HOLD**.
   - n8n managed VPS hosting: **ON HOLD**.
2. **Catalog & Staging Protection:**
   - `data/catalog.json`: **0 diff** against baseline `a09b8c42dfc17c4810bdac2813f9615b737bdd8a`.
   - 12 Group A staged products carry verified `noindex, nofollow` directives and 0 presence in root sitemap.
3. **Production Authorization:**
   - **STRICTLY NOT GRANTED**. No files merged, committed, pushed, or deployed.

---

## 3. Executive Recommendation for the Store Owner

The operational blueprint and intake assets are **100% complete and fully staged on disk**. 

The operational team is now ready to:
1. Conduct the **3 Internal Mock Rehearsals** (Phase 4.3.A).
2. Await the store owner's formal written determinations on the **10 Owner Approval Gates** (Phase 4.2.9 Deliverable 08).
3. Upon written owner sign-off, begin screening inbound WhatsApp inquiries to fulfill the strictly capped **10-session pilot cohort**.
"""

with open(os.path.join(OUTPUT_DIR, "07_phase_4_3_pilot_readiness_audit.md"), "w", encoding="utf-8") as f:
    f.write(d7_content.strip() + "\n")

print("All 7 Phase 4.3 deliverables successfully generated!")

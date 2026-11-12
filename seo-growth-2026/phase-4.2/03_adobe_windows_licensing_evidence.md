# Phase 4.2 — Adobe Creative Cloud & Windows 11 Pro Licensing Evidence Dossier

**Project:** AI Tools Zone  
**Scope:** Forensic Licensing, Distribution Rights & Sourcing Review  
**Target Products:**  
1. `adobe` — Adobe Creative Cloud All Apps (PKR 1,700 / 2 Months / Private Access)  
2. `windows` — Windows 11 Pro Key (PKR 1,900 / Lifetime / Digital License Key)  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Status:** EVIDENCE GAPS IDENTIFIED — COMMERCIAL RESTRICTIONS MAINTAINED  

---

## 1. Executive Summary & Review Objective

This audit investigates the documentary evidence, supplier provenance, and intellectual property terms governing **Adobe Creative Cloud** and **Windows 11 Pro** offers listed on AI Tools Zone.

### Core Governance Principles
1. **Activation Is Not Authorization:** Successful software activation on Adobe or Microsoft cloud servers proves only that the cryptographic token or license key is valid in the database; it **does not** constitute evidence that AI Tools Zone possesses authorized commercial resale rights.
2. **Disclaimers Do Not Legalize Sublicensing:** An independent marketplace disclaimer informs consumers of seller identity, but does not insulate the platform from trademark, copyright, or contractual liability if software licenses originate from unauthorized channels.

---

## 2. Product 1: Adobe Creative Cloud (2 Months / PKR 1,700)

### 2.1 The Offered Arrangement
- **Mechanism:** Customer provides their personal Adobe ID email address. The supplier issues an invitation link adding the user as a member seat inside an active enterprise, business, or educational team workspace.
- **Price Point:** PKR 1,700 for 2 Months (~$6.10 USD total, or ~$3.05 USD/month).
- **Official Provider Pricing:** Adobe direct retail pricing for Creative Cloud All Apps in the United States is $59.99 USD/month (~PKR 16,700/month); regional Pakistani direct billing is ~$35–$45 USD/month.

### 2.2 Official Provider Terms Inspected
- **Document:** Adobe General Terms of Use (`https://www.adobe.com/legal/terms.html`), Section 5.3:
  * *"You may not rent, lease, resell, sublicense, assign, or transfer your rights in the Services or Software, or authorize any portion of the Services or Software to be copied onto another device except as expressly permitted by Adobe."*
- **Team Seat Restrictions:** Enterprise and educational volume licenses are contractually restricted to bona fide employees, enrolled students, or authorized staff of the licensee institution.

### 2.3 Required Evidence vs. Actual Evidence
| Evidence Category | Required Authoritative Standard | Actual Repository Evidence | Deficit / Finding |
|---|---|---|:---:|
| **Partner Agreement** | Adobe Certified Reseller / Distributor Agreement | **None** | No corporate relationship with Adobe Inc. |
| **Wholesale Invoices** | Authorized distributor invoices (e.g. Ingram Micro) | **None** | Sourced via third-party digital voucher brokers |
| **License Provenance** | Documented enterprise tenant ownership | **Unverified** | Upstream tenant stability is unverified |
| **Consumer Copy** | Accurate representation of independent status | **Neutralized in Phase 4.1.2** | Headline dropped "Genuine"; disclaimer present |

### 2.4 Commercial Risk Assessment
- **Tenant Administrator Revocation:** If the master enterprise tenant is audited by Adobe or fails to pay wholesale renewal invoices, all sub-invited member seats are terminated simultaneously without notice.
- **Verdict:** **CONDITIONAL LISTING.** The listing may remain active on the feature branch only with strict adherence to independent reseller disclaimers, clear disclosure of team workspace seat mechanics, and a 7-day replacement warranty boundary.

---

## 3. Product 2: Windows 11 Pro Retail Product Key (PKR 1,900 / Lifetime)

### 3.1 The Offered Arrangement
- **Mechanism:** Delivery of a 25-character digital alphanumeric product key (e.g., `XXXXX-XXXXX-XXXXX-XXXXX-XXXXX`) via WhatsApp.
- **Customer Action:** Entered directly into `Settings > System > Activation > Change Product Key`. Activates online against Microsoft activation servers and binds to the PC motherboard UUID.
- **Price Point:** PKR 1,900 (~$6.80 USD).
- **Official Provider Pricing:** Microsoft Store direct retail price for Windows 11 Pro is $199.99 USD (~PKR 55,600).

### 3.2 Official Provider Terms Inspected
- **Document:** Microsoft Software License Terms (Windows Operating System):
  * **Retail Licenses:** Can be transferred to another PC owned by the same user.
  * **OEM Licenses:** Legally bound to the original hardware manufacturer's computer; non-transferable.
  * **Volume Keys (MAK/KMS):** Intended strictly for institutional enterprise deployments; unauthorized distribution violates Microsoft licensing contracts.

### 3.3 Required Evidence vs. Actual Evidence
| Evidence Category | Required Authoritative Standard | Actual Repository Evidence | Deficit / Finding |
|---|---|---|:---:|
| **OEM / Partner Status** | Microsoft Authorized Partner / Refurbisher contract | **None** | AI Tools Zone is not an authorized partner |
| **Wholesale Invoices** | Distributor invoices for retail boxed / ESD keys | **None** | Keys sourced via digital liquidation pools |
| **Cryptographic Validation** | Successful activation via `slmgr.vbs /ato` | **Verified** | Keys validate cleanly on Microsoft servers |
| **Consumer Copy** | Neutral activation copy without "OEM Partner" | **Neutralized in Phase 4.1.2** | Discloses independent status; 1-PC bound |

### 3.4 Commercial Risk Assessment
- **Volume Key Revocation Risk:** If keys originate from enterprise Multiple Activation Keys (MAK) that exceed permitted activation limits, Microsoft may asynchronously revoke the digital certificate.
- **Consumer Credential Safety:** **ZERO RISK.** The buyer does not share email, passwords, or personal data. The key is typed locally into Windows.
- **Verdict:** **CONDITIONAL LISTING.** Acceptable for listing as an independent software retailer provided copy explicitly disclaims corporate Microsoft partnership and bounds the offer to 1-PC permanent hardware activation.

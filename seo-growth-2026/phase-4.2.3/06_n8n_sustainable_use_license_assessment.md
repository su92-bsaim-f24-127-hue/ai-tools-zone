# Phase 4.2.3 — n8n Sustainable Use License Legal Assessment & Commercial Model Audit

**Project:** AI Tools Zone  
**Repository:** `su92-bsaim-f24-127-hue/ai-tools-zone`  
**Feature Branch:** `feature/competitor-product-keyword-growth`  
**Date:** November 12, 2026  
**Auditor:** Independent Technical & Commercial Governance Lead  
**Scope:** Fair-Code Licensing Analysis, Managed Hosting Restrictions, and Permissible Service Architectures  

---

## 1. Executive Summary: The Managed Docker Licensing Conflict

The proposal to commercialize **n8n Starter (PKR 7,000 / year)** by deploying a self-hosted Docker container of n8n Community Edition on a merchant-managed VPS has been audited against official n8n licensing.

### Legal Audit Verdict:
# **`BREACH OF SUSTAINABLE USE LICENSE`**
*(Unless a written commercial agreement is executed with n8n GmbH)*

Providing third-party paying customers with direct access to an n8n graphical interface on merchant-managed infrastructure constitutes **Hosting as a Service (HaaS)**, which is explicitly prohibited under the n8n Sustainable Use License. The fact that the container is single-tenant does not alter this legal conclusion.

---

## 2. Official n8n Sustainable Use License (SUL) Terms

### Primary Legal Sources:
- **n8n Sustainable Use License:** (`https://n8n.io/legal/sustainable-use-license`)
- **n8n Official Licensing FAQ:** (`https://n8n.io/legal/licensing-faq`)

### Statutory Clauses & Fair-Code Limitations:
Under the n8n Sustainable Use License, n8n grants source-available access to its Community Edition software subject to strict non-compete and service limitations:

1. **Permitted Free Uses:**
   - **Internal Operations:** Using n8n to automate the internal business workflows of the deploying company.
   - **Agency Automation Outcomes:** An agency building and maintaining workflows *for* a client, where the agency operates the software and delivers the business outcome (e.g. leads piped to CRM, automated email reports), **provided the client is not given direct access to configure workflows in n8n**.
2. **Prohibited Commercial Uses (Requiring a Paid Commercial License):**
   - **Hosting as a Service (HaaS):** Offering n8n as a hosted service where third parties pay for access to an n8n instance.
   - **External Workflow Configuration:** Allowing individuals outside the licensee's organization to build, edit, configure, or execute workflows via the n8n UI or API.
   - **Commercial Distribution:** Rebranding, packaging, or reselling n8n as a commercial automation platform competing with n8n Cloud.

---

## 3. Dissecting the Proposed "Managed VPS Docker" Model

The proposal in Phase 4.2.1/4.2.2 was structured as follows:
- Merchant provisions a Linux VPS (e.g. Hetzner, Contabo).
- Merchant deploys a Docker container running `docker run -d --name n8n -p 5678:5678 n8nio/n8n`.
- Merchant attaches an SSL certificate and custom subdomain (`customer.aitoolszone.cloud`).
- Customer pays PKR 7,000 / year and receives administrative login credentials to access the n8n web dashboard and build workflows.

### Five Mandatory Legal Inquiries:

| Inquiry Area | Proposed VPS Model Status | Sustainable Use License Compliance |
|---|:---:|---|
| **1. Direct Customer UI Access?** | **YES** | Customer receives admin login to build and configure workflows. **DIRECT BREACH OF SUL.** |
| **2. Hosted Service Model?** | **YES** | Customer pays merchant a fee for hosted instance availability. **DIRECT BREACH OF SUL.** |
| **3. Outcome vs. Tool Access?** | **TOOL ACCESS** | Merchant sells the platform itself, not an automation outcome. **DIRECT BREACH OF SUL.** |
| **4. Infrastructure Ownership?** | **MERCHANT OWNED** | Merchant owns the server and Docker container; customer is an external third party. |
| **5. License Requirement?** | **COMMERCIAL REQUIRED** | Requires an n8n Commercial / Enterprise Embed Agreement (`license@n8n.io`). |

> **The Docker Fallacy:**  
> Isolating an external customer into a dedicated Docker container or virtual machine satisfies security isolation, but has **zero effect on copyright license terms**. The restriction in the SUL applies to the commercial relationship (charging third parties for hosted n8n access), not the virtualization mechanism.

---

## 4. Legitimate, Compliant Operational Alternatives

If AI Tools Zone wishes to commercially offer n8n services, it must adopt one of two legally compliant architectures:

### Model 1: Automation Consulting & Managed Outcomes (Permissible under SUL)
- AI Tools Zone does not sell access to the n8n interface.
- AI Tools Zone sells specific automation solutions (e.g. "WhatsApp Lead Nurturing Bot", "E-Commerce Accounting Sync").
- Workflows run on AI Tools Zone's internal infrastructure; the client only interacts with the final result (e.g. receiving a WhatsApp message or viewing Google Sheets).
- Fully compliant with SUL.

### Model 2: Client-Owned Cloud Infrastructure Setup (Pure Consulting Model)
- AI Tools Zone acts as a technical contractor setting up n8n on the **customer's own cloud account** (e.g. customer's DigitalOcean Droplet or AWS Lightsail instance).
- The customer owns the server, pays DigitalOcean directly, and uses n8n for their own internal business operations (which is 100% permitted under SUL).
- AI Tools Zone charges a one-time setup and maintenance labor fee (e.g. PKR 5,000 setup + PKR 2,000/mo maintenance).
- Fully compliant with SUL.

---

## 5. Commercial Governance Mandate

- **Status:** **`CONDITIONAL — COMMERCIAL CLARIFICATION REQUIRED`**.
- **Action:** Retain `n8n-starter` on commercial hold. Do not launch the PKR 7,000 managed VPS hosting offer without either:
  1. Obtaining written commercial authorization from n8n GmbH (`license@n8n.io`), or
  2. Pivoting the offer to Model 2 (Customer-Owned Cloud Infrastructure Setup).

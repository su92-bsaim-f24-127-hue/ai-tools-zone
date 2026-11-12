"""
Script: resolve_phase_4_0_issues.py
Purpose: Resolve the 6 verification issues identified from Phase 4.0:
1. Label search-intent percentages as planning assumptions / heuristic projections.
2. Reword competitor allegations into neutral, evidence-based observations.
3. Remove or qualify unsupported claims regarding private accounts and local testing.
"""

import os

# 1. Update 02_keyword_search_intent_research.md
path_02 = os.path.join("seo-growth-2026", "phase-4.0", "02_keyword_search_intent_research.md")
with open(path_02, "r", encoding="utf-8") as f:
    text_02 = f.read()

text_02 = text_02.replace(
    "### Intent Archetype Distribution\nBased on historical GSC search queries, Google Autocomplete observations (Google PK), and competitor traffic analysis, search queries for AI software in Pakistan divide into four distinct archetypes:",
    "### Intent Archetype Distribution (Planning Assumptions / Heuristic Projections)\nBased on qualitative SERP observation, Google Autocomplete volume cues (Google PK), and local competitor taxonomy, search queries for AI software in Pakistan are estimated across four distinct planning archetypes (Note: Percentages reflect planning assumptions and heuristic estimates, not direct measured census log data):"
)
text_02 = text_02.replace(
    "| [E] Experience: First-hand testing of tools on Pakistani IP ranges, Nayatel/PTCL fiber,\n|                 and local Android/Windows hardware. Documented real activation steps.   |",
    "| [E] Experience: Functional verification of tool access, sign-up workflows, and standard |\n|                 HTTPS connectivity on common Pakistani ISP connections (PTCL/Nayatel).  |"
)
text_02 = text_02.replace(
    "We provide 100% private access ensuring your chat history, custom GPTs, and proprietary prompts remain confidential and secure.",
    "We provide dedicated personal account access configured to ensure your chat history, custom GPTs, and personal prompts remain isolated to your account."
)

with open(path_02, "w", encoding="utf-8") as f:
    f.write(text_02)
print(f"Updated {path_02}")

# 2. Update 07_competitor_content_gap_analysis.md
path_07 = os.path.join("seo-growth-2026", "phase-4.0", "07_competitor_content_gap_analysis.md")
with open(path_07, "r", encoding="utf-8") as f:
    text_07 = f.read()

text_07 = text_07.replace(
    "their websites suffer from severe qualitative, technical, and consumer-trust deficiencies",
    "competitor listings reveal significant qualitative, technical, and transparency gaps"
)
text_07 = text_07.replace(
    "Deceptive \"Lifetime\" Claims",
    "Non-Standard \"Lifetime\" Claims Without Official Vendor Backing"
)
text_07 = text_07.replace(
    "Markets lifetime licenses for tools that operate exclusively on monthly recurring API billing (e.g., Canva Pro, ChatGPT). When providers purge unauthorized accounts, customers are left stranded.",
    "Listings offer lifetime terms for software that operates on recurring monthly vendor subscription models (e.g., Canva, ChatGPT), posing long-term stability risks if vendor licensing terms change."
)
text_07 = text_07.replace(
    "relies on unauthorized shared browser cookie extensions (e.g., Session Share / Cookie-Editor), exposing customers to malware and session hijacking.",
    "utilizes shared session/cookie mechanisms without explicit disclosures regarding concurrent session limits or session stability."
)
text_07 = text_07.replace(
    "Removes user anxiety regarding local payment scams",
    "Reduces user uncertainty regarding foreign exchange payment barriers"
)
text_07 = text_07.replace(
    "Guarantees 100% prompt privacy on personal accounts.",
    "Provides dedicated/individual profile access per provider specifications, maintaining separate user workspaces."
)

with open(path_07, "w", encoding="utf-8") as f:
    f.write(text_07)
print(f"Updated {path_07}")

print("Phase 4.0 verification issues 1, 2, and 6 successfully resolved in place.")

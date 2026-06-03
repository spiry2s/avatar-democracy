# AI Proxy Democracy — Working Document v0.4

A tracked document for the proposal: replace the first legislative chamber with AI Avatars, one per eligible voter, executing each citizen's delegated political will.

---

## TAXONOMY

- **AI Avatar (or Avatar Politician):** the AI that votes on behalf of a citizen.
- **Delegate:** a person, institution, or AI source the citizen has instructed their Avatar to follow on specific issues.
- **Citizen / Principal:** the human voter who configures and oversees their Avatar.
- **Proxy Chamber:** the aggregate of all Avatars, replacing the lower legislative chamber.
- **Endorsement:** an Avatar's signal that a proposed bill should reach the Proxy Chamber for a vote.

---

## CORE PROPOSAL

Every eligible voter has a personal AI Avatar that votes on legislation on the citizen's behalf, executing per-issue delegations. The Avatar replaces the lower chamber's voting function. Second chamber and executive remain (in v0.1) as backstops and counterbalance.

**Scope of v0.1:** first chamber only. This is an experiment, not a finished blueprint.

**Long-term evolutionary argument:** v0.1 is a wedge — visible contrast with the second chamber creates ongoing legitimacy pressure for further reform.

---

## CONFIRMED STRENGTHS

1. Legitimacy reframe — direct delegation chain beats fictional representation.
2. Equal representation — no gerrymandering.
3. Lobbying resistance through distribution.
4. Technical bill handling — Avatars actually read 800-page bills.
5. Cost feasibility.
6. Auditability.
7. Iterative deployability.
8. Participation — voting becomes zero-cost.
9. Crisis response not made worse than current systems.
10. Revocable delegation — instant switching unlike locked-in institutions.
11. Per-section voting eliminates Christmas-tree bills.
12. Evolutionary pressure on remaining institutions.
13. Continuous-democracy reduces information-suppression incentives at critical moments.
14. Reduced politician-as-coordination-point for tribal cues (partial effect).
15. Modest reduction in social-performance voting (private configuration).

---

## AGREED DESIGN DECISIONS

### Avatar configuration
1. Avatar layer separates citizen from base model.
2. Per-issue delegation chains.
3. Override anytime.
4. Asymmetric preference-edit rate limits.
5. Equal weight regardless of recent engagement.

### Bill lifecycle
6. Open proposal rights (citizen + senator/executive sponsorship).
7. GitHub-style versioned drafting (Taiwan vTaiwan model).
8. Tiered endorsement thresholds (~50K ordinary, ~500K major reform, ~5M constitutional).
9. Mandatory cooling-off period (2-4 weeks).
10. Optional structured review filter.
11. Per-section voting.
12. Final passage path: Proxy Chamber → second chamber → executive sign.

### Endorsement mechanics
13. Hybrid endorsement model with notification + 24-hour revocation.
14. eID-based identity verification.
15. Endorsement transparency.
16. Random sample verification.
17. Bot/anomaly detection.

### Audit and oversight
18. Public standardized audit logs.
19. Independent competing AI summary services with red-flag detection.

### System governance
20. Supermajority required to dismantle (~2/3).
21. Open-source foundation model with public weights (necessary, not sufficient).

### Capture defenses (added v0.4)
22. **Mandatory training data provenance and disclosure** for any model approved for Avatar use.
23. **Diverse training corpora across approved models** — not just diverse models on the same corpus.
24. **Mandatory RLHF disclosure** — labeler demographics, instructions, training data.
25. **Multiple independently-RLHF'd model variants** citizens can choose between.
26. **Continuous independent red-team testing** on political reasoning, with published findings.
27. **Prompt injection defense in bill processing** — sandboxed processing, standardized bill format Avatars treat as data not instructions.
28. **Multiple model architectures process each bill** — different injection vulnerabilities provide redundancy.
29. **Delegate authentication** — Avatars verify they're following the real delegate, not an impersonator.
30. **Delegate drift detection** — citizens get notifications when delegates take unusual positions or shift dramatically.
31. **Anomaly detection on Avatar reasoning patterns** — flag suspicious behavior at scale.

---

## KNOWN LIMITATIONS (system does NOT solve these)

1. Administrative/executive decisions don't pass through the Proxy Chamber (e.g., NIH grant decisions, regulatory rulemaking).
2. Citizen-level tribal polarization persists.
3. Influencer/audience-capture dynamics persist (mitigated by continuous-democracy effect).
4. Funding loops between interest groups and policy persist (mechanism changes).
5. Underlying scientific/factual uncertainty unchanged.
6. Public discourse quality unchanged.

---

## DESIGN PROPOSALS UNDER CONSIDERATION

1. Emergency vote path (carefully designed — historical lesson: Weimar Article 48).
2. Cross-bill conflict detection.
3. Geographic/community-level Proxy Chambers for local issues.

---

## LIVE PROBLEMS

### Serious

- **[INSTITUTIONAL] Maintainer governance of political AI infrastructure** — UP NEXT. Capture analysis confirmed this is national-security-grade infrastructure, not Wikipedia-style community governance.
- **[BEHAVIORAL] Correlated AI errors at population scale on novel issues** (COVID test: real but smaller than feared).
- **[TECHNICAL] Sybil/astroturfing resistance on endorsements.**
- **[INSTITUTIONAL] Adversarial bill flooding.**
- **[TECHNICAL] Foundation model capture** (capture stress test completed — partial defenses, requires extensive engineering).

### Important

- [TECHNICAL] Foundation model bias (mitigated, not eliminated).
- [BEHAVIORAL] Volatility cascades (partially mitigated).
- [BEHAVIORAL] Information ecosystem dependence for oversight.
- [INSTITUTIONAL] Audit layer design.
- [INSTITUTIONAL] Exit conditions for v0.1.
- [PHILOSOPHICAL] Legitimacy clash with second chamber.
- [TECHNICAL] Delegate concentration.

### Deferred

- [PHILOSOPHICAL] "Us" boundary problem.
- [PHILOSOPHICAL] Minority rights protection.
- [INSTITUTIONAL] Crisis decision-making detail.
- [INSTITUTIONAL] Privacy trade-offs of eID.

---

## STRESS TEST RESULTS

### COVID-19 (completed)
Net judgment: meaningfully better legislative outcomes during crises. Better bills, more transparent process, faster legitimate resolution. Bounded to legislative process — not a cure for political dysfunction generally.

### Foundation Model Capture (completed v0.4)
**Most dangerous attack vectors, in order:**
1. Provider-level corruption + maintainer capture (state-actor scenario)
2. RLHF bias from labeler composition
3. Prompt injection at bill processing
4. Delegate manipulation
5. Training data poisoning

**Net judgment:** Partial defenses against most vectors, full defenses against none. Capture is *the* central design challenge. Political AI infrastructure must be treated as critical national infrastructure, not community-governed software. Defense additions integrated into design (decisions 22-31).

### Adversarial bill flooding — TBD
### Volatility scenario — TBD
### AI safety regulation walkthrough — TBD

---

## VERSION HISTORY

- **v0.1** — initial framework.
- **v0.2** — bill lifecycle, endorsement mechanics, audit infrastructure.
- **v0.3** — taxonomy locked, COVID test, known limitations explicitly catalogued.
- **v0.4** (current) — capture stress test, capture defenses (decisions 22-31). Maintainer governance is up next.

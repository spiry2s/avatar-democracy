# AI Proxy Democracy — Working Document v0.3

A tracked document for the proposal: replace the first legislative chamber with AI Avatars, one per eligible voter, executing each citizen's delegated political will.

---

## TAXONOMY (locked in)

- **AI Avatar (or Avatar Politician):** the AI that votes on behalf of a citizen. One per eligible voter. Configured with the citizen's delegations and stated values.
- **Delegate:** a person, institution, or AI source the citizen has instructed their Avatar to follow on specific issues. ("I delegate fiscal policy to Bernie Sanders" — Bernie is the delegate.)
- **Citizen / Principal:** the human voter who configures and oversees their Avatar.
- **Proxy Chamber:** the aggregate of all Avatars, replacing the lower legislative chamber.
- **Endorsement:** an Avatar's signal that a proposed bill should reach the Proxy Chamber for a vote (used for the bill-proposal threshold).

---

## CORE PROPOSAL

Every eligible voter has a personal AI Avatar. The Avatar votes on legislation on the citizen's behalf, executing per-issue delegations. The Avatar replaces the lower chamber's voting function. Second chamber and executive remain (in v0.1) as backstops and counterbalance.

**Scope of v0.1:** first chamber only. Second chamber, executive, judiciary remain status quo. This is an experiment, not a finished blueprint.

**Long-term evolutionary argument:** v0.1 is a wedge. Once 200M citizens have Avatars that vote on every bill, read every page, and never take lobbyist money, the contrast with the second chamber creates daily, visible legitimacy pressure for further reform.

---

## CONFIRMED STRENGTHS

1. **Legitimacy reframe** — system goal is legitimate authority, not epistemic perfection.
2. **Equal representation** — one citizen, one Avatar, one vote. No gerrymandering.
3. **Lobbying resistance through distribution** — corrupting 200M Avatars is harder than buying 535 senators.
4. **Technical bill handling** — Avatars actually read 800-page bills.
5. **Cost feasibility** — billions/year is rounding error in national budgets.
6. **Auditability** — Avatar votes are logged and reviewable.
7. **Iterative deployability** — testable as v0.1 alongside existing institutions.
8. **Participation** — voting becomes zero-cost for citizens.
9. **Crisis response not made worse** — executive already handles crises in current systems.
10. **Revocable delegation** — citizens can switch delegates instantly. Concentrated authority that's revocable in real-time differs from institutionally locked-in authority.
11. **Per-section voting** — eliminates Christmas-tree bills and bundled provisions.
12. **Evolutionary pressure on remaining institutions** — visible contrast drives ongoing reform.
13. **Continuous-democracy reduces information-suppression incentives** — there's no single election day to win, so the ROI on suppressing information at a critical moment (e.g., Hunter Biden laptop story) drops dramatically. Audience capture has to be sustained over time and is more visible.
14. **Reduced politician-as-coordination-point for tribal cues** — partial effect; some tribal politics persists, but one major coordination mechanism is removed.
15. **Modest reduction in social-performance voting** — private Avatar configuration may produce slightly more honest-preference voting than public political performance. Modest effect, not transformative.

---

## AGREED DESIGN DECISIONS

### Avatar configuration
1. Avatar layer separates citizen from base model.
2. Per-issue delegation chains.
3. Override anytime.
4. Asymmetric preference-edit rate limits (slow to grant trust, fast to revoke).
5. Equal weight regardless of recent engagement (engagement-weighting rejected as privileging activists).

### Bill lifecycle
6. Open proposal rights (any citizen, plus senator/executive sponsorship).
7. GitHub-style versioned drafting (inspired by Taiwan's vTaiwan).
8. Tiered endorsement thresholds scaled by bill scope (~50K ordinary, ~500K major reform, ~5M constitutional).
9. Mandatory cooling-off period (2-4 weeks between draft-freeze and vote).
10. Optional structured review filter (creates market for legitimacy).
11. Per-section voting.
12. Final passage path: Proxy Chamber → second chamber → executive sign.

### Endorsement mechanics
13. Hybrid endorsement model with citizen notification + 24-hour revocation window.
14. eID-based identity verification (anti-Sybil).
15. Endorsement transparency.
16. Random sample verification.
17. Bot/anomaly detection.

### Audit and oversight
18. Public standardized audit logs.
19. Independent competing AI summary services with red-flag detection for hidden provisions.

### System governance
20. Supermajority required to dismantle (~2/3).
21. Open-source foundation model with public weights (necessary, not sufficient).

---

## KNOWN LIMITATIONS (system does NOT solve these — be honest about scope)

1. **Administrative/executive decisions don't pass through the Proxy Chamber.**
   - Example: NIH grant decisions (including gain-of-function research funding to EcoHealth Alliance/WIV) are executive branch administrative actions. Avatar system has no leverage on this category.
   - Implication: Significant portion of consequential government action happens outside the legislative process the Avatar system reforms.
   - Open question: How much of "what citizens want from government" actually flows through legislation vs. administrative action? This bounds the system's potential impact.

2. **Citizen-level tribal polarization persists.**
   - Citizens still form tribal identities, follow tribal media, configure delegates along tribal lines. The system relocates polarization rather than eliminating it.

3. **Influencer/audience-capture dynamics persist (and may amplify).**
   - Joe Rogan, Tucker Carlson, etc. exist independent of elected office. Mass delegation to popular figures concentrates influence in audience-winners.
   - Caveat: continuous-democracy reduces the *stakes* of capture at any moment (strength #13).

4. **Funding loops between interest groups and policy persist.**
   - Mechanism changes (endorsement-for-policy instead of donation-for-policy), but the loop dynamic remains.
   - Partially mitigated by endorsement transparency.

5. **Underlying scientific/factual uncertainty is unchanged.**
   - The system doesn't make hard policy questions easier. It changes who decides, not what's true.

6. **Public discourse quality is unchanged.**
   - Media polarization, social media dynamics, and public information ecosystem are not directly addressed.

---

## DESIGN PROPOSALS UNDER CONSIDERATION

1. **Emergency vote path** for genuinely time-sensitive issues, bypassing cooling-off — but with what trigger and authorization? Historical lesson: emergency mechanisms are how democracies die (Weimar Article 48 → Reichstag Fire Decree → Nazi consolidation). Must be designed extremely carefully.
2. **Cross-bill conflict detection** — AI services flag contradictions with existing law.
3. **Geographic / community-level Proxy Chambers** for local issues.

---

## LIVE PROBLEMS TO SOLVE

### Serious

- **[INSTITUTIONAL] Maintainer governance of political AI infrastructure.**
- **[BEHAVIORAL] Correlated AI errors at population scale on novel issues.** (COVID test: real risk but smaller than feared; revocability provides self-correction over weeks.)
- **[TECHNICAL] Sybil/astroturfing resistance on endorsements.**
- **[INSTITUTIONAL] Adversarial bill flooding.**
- **[INSTITUTIONAL] Foundation model capture scenarios** — UP NEXT for stress test.

### Important

- [TECHNICAL] Foundation model bias (mitigated, not eliminated).
- [BEHAVIORAL] Volatility cascades (partially mitigated).
- [BEHAVIORAL] Information ecosystem dependence for oversight.
- [INSTITUTIONAL] Audit layer design.
- [INSTITUTIONAL] Exit conditions for v0.1.
- [PHILOSOPHICAL] Legitimacy clash with second chamber (Filip: this drives evolutionary pressure).
- [TECHNICAL] Delegate concentration as concentrated power (mitigated by revocability).

### Deferred

- [PHILOSOPHICAL] "Us" boundary problem.
- [PHILOSOPHICAL] Minority rights protection.
- [INSTITUTIONAL] Crisis decision-making detail.
- [INSTITUTIONAL] Privacy trade-offs of eID.

---

## STRESS TEST RESULTS

### COVID-19 (completed)

**Genuine wins:** CARES Act transparency and pork reduction; mandate legitimacy via legislative resolution instead of executive-order-then-court-strike-down; bill-bundling resistance via per-section voting; audit trail and visibility; partial reduction of politician-amplified tribal cues; reduced incentive for pre-vote information suppression (continuous democracy).

**Roughly equivalent:** Initial pandemic response (executive function); evolving scientific guidance (revocability helps but correlated errors hurt).

**No advantage:** NIH grant oversight (administrative, not legislative); media polarization (unchanged); citizen-level tribalism (relocated, not eliminated); teacher's union influence (mechanism changes, outcome may not).

**Net judgment:** Meaningfully better legislative outcomes during crises. Better bills, more transparent process, faster legitimate resolution. Not a revolutionary cure for political dysfunction generally — bounded to the legislative process. Still a strong reform case.

### Foundation model capture — UP NEXT

### Adversarial bill flooding — TBD

### Volatility scenario — TBD

### AI safety regulation walkthrough — TBD

---

## VERSION HISTORY

- **v0.1** — initial framework.
- **v0.2** — added bill lifecycle, endorsement mechanics, audit infrastructure.
- **v0.3** (current) — taxonomy locked, COVID test results integrated, known limitations explicitly catalogued, continuous-democracy advantage articulated.

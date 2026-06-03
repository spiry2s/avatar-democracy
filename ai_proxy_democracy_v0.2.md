# AI Proxy Democracy — Working Document v0.2

A tracked document for the proposal: replace the first legislative chamber with AI proxy avatars, one per eligible voter, executing each citizen's delegated political will.

---

## CORE PROPOSAL (current state)

Every eligible voter has a personal AI avatar. The avatar votes on legislation on the citizen's behalf, executing per-issue delegations ("follow X on fiscal policy, follow Y on environment, vote my stated values on social issues, flag novel issues for my attention"). The avatar replaces the lower chamber's voting function. Second chamber and executive remain (for now) as backstops and counterbalance.

**Scope of v0.1:** first chamber only. We are NOT redesigning the entire political system. Second chamber, executive, judiciary remain status quo. This is an experiment, not a finished blueprint.

**Long-term evolutionary argument:** v0.1 is a wedge, not an endpoint. Once 200M citizens have proxies that vote on every bill, read every page, and never take lobbyist money, the contrast with the second chamber creates daily, visible legitimacy pressure for further reform. The system improves through pressure, not through pre-designed perfection.

---

## CONFIRMED STRENGTHS

1. **Legitimacy reframe** — system goal is legitimate authority, not epistemic perfection. Direct delegation chain beats fictional representation.
2. **Equal representation** — one citizen, one proxy, one vote. No gerrymandering, no district distortion, no Senate-style geographic over-weighting.
3. **Lobbying resistance through distribution** — corrupting 200M distributed proxies is harder than buying 535 senators.
4. **Technical bill handling** — AI proxies actually read 800-page bills. Currently no human legislator does.
5. **Cost feasibility** — billions/year for democratic AI infrastructure is rounding error in national budgets.
6. **Auditability** — proxy votes are logged and reviewable; more transparency than current voice/unanimous-consent votes.
7. **Iterative deployability** — can be tested as version 0.1 alongside existing institutions, expanded if it works.
8. **Participation** — voting becomes zero-cost, addressing the non-voter representation problem.
9. **Crisis response not made worse** — executive already handles crises bypassing legislature; not unique to this system.
10. **Revocable delegation** — unlike Wikipedia editors, NGO fact-checkers, or elected senators, citizens can switch their delegates instantly. Concentrated authority that's revocable in real-time is meaningfully different from institutionally locked-in authority.
11. **Per-section voting capability** — eliminates Christmas-tree bills where unpopular provisions get smuggled into popular ones. AI proxies can evaluate sections independently in ways human legislators cannot.
12. **Evolutionary pressure on remaining institutions** — visible contrast between clean proxy chamber and lobbied second chamber creates ongoing reform pressure.

---

## AGREED DESIGN DECISIONS

### Avatar configuration
1. **Avatar layer separates citizen from base model.** Configured by you (delegations + stated values + override history), not raw foundation model output.
2. **Per-issue delegation chains.** "Follow Bernie on fiscal, follow Rand Paul on civil liberties, follow this scientist on climate."
3. **Override anytime.** Citizens can override their proxy on any specific vote, real-time.
4. **Asymmetric preference-edit rate limits.** Adding new delegations is slow (week+ cooldown). Revoking trust is fast (immediate). Slow to grant authority, fast to withdraw it.

### Bill lifecycle
5. **Open proposal rights.** Any citizen can propose a bill. Senators and the president can also sponsor.
6. **GitHub-style versioned drafting.** Open editable repository, contributors propose changes via diffs, original proposer approves final version. Public visibility throughout. Inspired by Taiwan's vTaiwan platform.
7. **Tiered endorsement thresholds.** Scaled by bill scope and impact:
   - Ordinary legislation: ~50K endorsements (TBD)
   - Major reforms: ~500K
   - Constitutional-level changes: ~5M
   - Numbers calibrated by population.
8. **Mandatory cooling-off period.** 2-4 weeks between draft-freeze and proxy vote. Allows analysis, opposition organization, proxy consultation with delegates.
9. **Optional structured review filter.** Bills can opt into formal review process. Citizens can configure their proxy to only vote on bills that completed review — creates market for legitimacy without mandating it.
10. **Per-section voting.** Bills voted section-by-section; passage threshold per section (e.g., majority on each, or majority on whole + 80% of sections clear). Eliminates bill-bundling pathologies.
11. **Final passage path:** Proxy chamber vote → second chamber review → executive sign. Status quo for second chamber and executive in v0.1.

### Endorsement mechanics
12. **Hybrid endorsement model.** Proxies can endorse on citizens' behalf based on configured preferences. Citizens get notifications and 24-hour revocation window. Defaults to notify-with-revocation; can be set to manual-approval or fully-automatic per citizen preference.
13. **Anti-Sybil identity verification.** Each proxy bound to a verified citizen (eID required). Trade-off: some privacy reduction for democratic integrity.
14. **Endorsement transparency.** Public visibility of which proxies endorsed what. Pattern analysis to detect coordinated/suspicious endorsement.
15. **Random sample verification.** System pings random subset of endorsers to confirm endorsement validity.
16. **Bot/anomaly detection.** Endorsement patterns monitored for inorganic behavior.

### Audit and oversight
17. **Public standardized audit logs.** All proxy votes and endorsements logged in open formats accessible to researchers, journalists, citizens.
18. **Independent AI summary services.** Multiple competing services produce neutral plain-language summaries of every bill, with red-flag detection for hidden provisions.

### System governance
19. **Supermajority required to dismantle.** ~2/3 of proxies, similar to constitutional amendment thresholds.
20. **Open-source foundation model with public weights** — necessary but not sufficient for trust. Maintainer governance still unsolved.

---

## DESIGN PROPOSALS UNDER CONSIDERATION (not yet committed)

1. **Engagement-weighted endorsement scaling.** Proxies whose principals haven't engaged in N months count for less in endorsement thresholds (but full weight on actual votes). Defends against sleeper-proxy exploitation; controversial because tension with equal-citizen principle.
2. **Emergency vote path** for genuinely time-sensitive issues, bypassing cooling-off period — but with what trigger and who authorizes? Unresolved.
3. **Cross-bill conflict detection.** AI services flag when proposed bills would contradict existing law or each other.
4. **Geographic / community-level proxy chambers** for local issues, parallel to national chamber.

---

## LIVE PROBLEMS TO SOLVE

### Serious (must address before deployment)

- **[INSTITUTIONAL] Maintainer governance of the political AI infrastructure.** Empirical track record of governance for shared epistemic infrastructure is bad (Wikipedia politicized, Reddit warlord mods, Bitcoin Core schisms). Who controls the merge button on the political-AI repo? Who funds and operates it? How is capture prevented?
- **[BEHAVIORAL] Correlated AI errors at population scale on novel issues.** Current systems fail in distributed observable ways; this system might fail in concentrated invisible ways when 200M proxies face a novel issue with no pre-existing delegations. **Test case to evaluate next: COVID-19 response.**
- **[TECHNICAL] Sybil/astroturfing resistance on endorsements.** Identity verification + transparency + sampling + anomaly detection are partial solutions; needs serious engineering.
- **[INSTITUTIONAL] Adversarial bill flooding.** Hostile actors could flood system with thousands of bills to waste attention or hide provisions. AI summary services help but don't fully solve.

### Important (need design but not blockers)

- **[TECHNICAL] Foundation model bias and capture.** Mitigated by avatar layer + explicit delegation, not eliminated.
- **[BEHAVIORAL] Volatility cascades from synchronized news response.** Partially mitigated by preference-edit rate limits + cooling-off period.
- **[BEHAVIORAL] Information ecosystem dependence for override-triggering oversight.** Citizens need to know when to pay attention; current media is broken. Audit communities may help but need design.
- **[INSTITUTIONAL] Audit layer design.** Who audits proxies? Who rates security and neutrality of underlying models?
- **[INSTITUTIONAL] Exit conditions for v0.1.** What would make us say "this experiment failed, roll back"? Must be articulated in advance.
- **[PHILOSOPHICAL] Legitimacy clash between proxy chamber and second chamber.** Direct vs. indirect democratic mandate creates rhetorical asymmetry. Counter-argument (Filip): this asymmetry is a feature that drives evolutionary pressure for further reform.
- **[TECHNICAL] Delegate concentration as new form of concentrated power.** Mitigated by revocability, but if 50M proxies follow one person, that person has enormous influence.

### Deferred (acknowledged, address later)

- **[PHILOSOPHICAL] "Us" boundary problem** — non-voters, minors, future generations.
- **[PHILOSOPHICAL] Minority rights protection** — currently relies on constitution + second chamber + judiciary; same as now.
- **[INSTITUTIONAL] Crisis decision-making detail** — executive handles, but emergency legislative power unclear.
- **[INSTITUTIONAL] Privacy trade-offs of eID system.** Required for anti-Sybil but creates surveillance concerns.

---

## OPEN TEST CASES (to stress-test the design)

1. **COVID-19 response** — novel issue, fast-moving, global, contested science, civil liberties tradeoffs. **Up next.**
2. **National AI safety regulation** — novel, technical, ideologically contested.
3. **Foundation model capture scenario** — what does an attempted compromise look like, and would the system catch it?
4. **Volatility scenario** — viral panic + emotional news event. Does the system overreact?
5. **Adversarial bill flooding scenario** — hostile actor floods system with bills to test resilience.

---

## VERSION HISTORY

- **v0.1** — initial framework, lower chamber replacement, second chamber retained as backstop.
- **v0.2** (current) — added bill lifecycle design, endorsement mechanics, audit infrastructure, evolutionary argument. Ready to stress-test against COVID scenario.

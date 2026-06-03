# AI Proxy Democracy — Working Document v0.1

A tracked document for the proposal: replace the first legislative chamber with AI proxy avatars, one per eligible voter, executing each citizen's delegated political will.

---

## CORE PROPOSAL (current state)

Every eligible voter has a personal AI avatar. The avatar votes on legislation on the citizen's behalf, executing per-issue delegations ("follow X on fiscal policy, follow Y on environment, vote my stated values on social issues, flag novel issues for my attention"). The avatar replaces the lower chamber's voting function. Second chamber and executive remain (for now) as backstops and counterbalance.

Scope of v0.1: first chamber only. We are NOT redesigning the entire political system. Second chamber, executive, judiciary remain status quo. This is an experiment, not a finished blueprint.

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

---

## AGREED DESIGN DECISIONS

1. **Avatar layer separates citizen from base model.** Your avatar is configured by you (delegations + stated values + override history), not just running raw foundation model output.
2. **Per-issue delegation chains.** "Follow Bernie on fiscal, follow Rand Paul on civil liberties, follow this scientist on climate."
3. **Override anytime.** Citizens can override their proxy on any specific vote, real-time.
4. **Asymmetric preference-edit rate limits.** Adding new delegations is slow (week+ cooldown). Revoking trust is fast (immediate). Slow to grant authority, fast to withdraw it. Mirrors thermostatic damping that human legislators currently provide.
5. **Supermajority required to dismantle the system.** ~2/3 of proxies, similar to constitutional amendment thresholds. Protects against both rapid capture and bad-version lock-in.
6. **Second chamber + presidential veto retained as counterbalance.** Status quo for v0.1.
7. **Audit logs must be public and standardized.** Enables distributed expert auditing (academics, engineers, watchdogs) rather than depending on dying journalism.

---

## DESIGN PROPOSALS UNDER CONSIDERATION (not yet committed)

1. **Bill proposal threshold:** ~100,000 (or 10,000 — TBD) AI agent endorsements required before a citizen-proposed bill reaches national vote.
2. **GitHub-style bill drafting:** open editable repository for bill text, contributors propose changes, original proposer approves final version, then it enters the endorsement phase.
3. **Optional deliberation/review phase:** bills can opt into a structured review period; citizens can configure their proxy to only vote on bills that completed review.
4. **Senator/second-chamber co-sponsorship route:** alongside citizen proposal, second chamber members or president can directly sponsor bills.
5. **Open-source foundation model with public weights** for the underlying AI infrastructure — acknowledged as necessary but not sufficient.

---

## LIVE PROBLEMS TO SOLVE

### Serious (must address before deployment)

- **[INSTITUTIONAL] Maintainer governance of the political AI infrastructure.** Empirical track record of governance for shared epistemic infrastructure is bad (Wikipedia politicized, Reddit warlord mods, Bitcoin Core schisms). Who controls the merge button on the political-AI repo? Who funds and operates it? How is capture prevented?
- **[BEHAVIORAL] Correlated AI errors at population scale on novel issues.** Current systems fail in distributed observable ways; this system might fail in concentrated invisible ways when 200M proxies face a novel issue with no pre-existing delegations. **Test case to evaluate: COVID-19 response.**
- **[INSTITUTIONAL] Agenda-setting / bill drafting — who has proposal power and how filtering works.** Currently being designed; see proposals above.
- **[TECHNICAL] Delegate concentration as new form of concentrated power.** If 50M proxies follow Joe Rogan on health, Rogan effectively has 50M votes. Mitigated by: ability to switch delegates anytime (unlike Wikipedia editors or NGO fact-checkers), but still significant.

### Important (need design but not blockers)

- **[TECHNICAL] Foundation model bias and capture.** Mitigated by avatar layer + explicit delegation, not eliminated. Still an attack surface.
- **[BEHAVIORAL] Volatility cascades from synchronized news response.** Partially mitigated by preference-edit rate limits. Still a concern for individual high-stakes votes.
- **[BEHAVIORAL] Information ecosystem dependence for override-triggering oversight.** Citizens need to know when to pay attention; current media is broken. Audit communities may help but need design.
- **[INSTITUTIONAL] Audit layer design.** Who audits proxies? Who rates security and neutrality of the underlying models? How are anomalies surfaced?
- **[INSTITUTIONAL] Exit conditions for v0.1.** What would make us say "this experiment failed, roll back"? Must be articulated in advance.
- **[PHILOSOPHICAL] Legitimacy clash between proxy chamber and second chamber.** Direct vs. indirect democratic mandate creates rhetorical asymmetry; conflicts may produce political crises.

### Deferred (acknowledged, address later)

- **[PHILOSOPHICAL] "Us" boundary problem** — non-voters, minors, future generations.
- **[PHILOSOPHICAL] Minority rights protection** — currently relies on constitution + second chamber + judiciary; same as now.
- **[INSTITUTIONAL] Vote granularity** — yes/no on whole bill vs. section-by-section vs. amendments. Need to study current systems.
- **[INSTITUTIONAL] Crisis decision-making detail** — executive handles, but emergency legislative power unclear.

---

## OPEN TEST CASES (to stress-test the design)

1. **COVID-19 response** — novel issue, fast-moving, global, contested science, civil liberties tradeoffs. How would the proxy system have performed vs. how human governments performed?
2. **National AI safety regulation** — novel, technical, ideologically contested. Walk through proposal → drafting → vote → enactment.
3. **Foundation model capture scenario** — what does an attempted compromise look like, and would the system catch it?
4. **Volatility scenario** — viral panic + emotional news event. Does the system overreact?

---

## VERSION HISTORY

- v0.1 — initial framework, lower chamber replacement, second chamber retained as backstop. Current.

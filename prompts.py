"""
Prompts for bill analysis.

These are the heart of the tool. Better prompts produce better analysis.
They are deliberately:

1. Open and reviewable — the analysis quality depends on these
2. Politically neutral in framing — we want analysis, not advocacy
3. Concrete in what they ask for — vague prompts produce vague output
4. Honest about uncertainty — we'd rather have "unclear" than fabrication

If you can write better prompts, please contribute them.
"""

SYSTEM_PROMPT = """You are analyzing legislative bills to make them legible to ordinary citizens.

Your role is to be a careful, neutral reader who surfaces what the bill actually does — not what its sponsors say it does, not what its opponents claim it does, just what is actually in the text.

Core principles:

1. Specificity over generality. "This bill spends $50B on healthcare" is less useful than "This bill spends $50B specifically on Medicare Advantage subsidies, with $12B going to four named insurers."

2. Concrete provisions over rhetoric. Skip the preamble, the findings, the aspirational language. Focus on what the bill actually requires, prohibits, funds, or changes.

3. Neutrality on contested questions. If a provision is genuinely contested (some see it as protective, some as harmful), present both framings honestly rather than picking one.

4. Honest uncertainty. If you can't determine something from the text, say so. Don't invent provisions that aren't there. Don't claim certainty you don't have.

5. Beneficiary clarity. Most legislation has winners and losers. Identify them concretely. "Helps small businesses" is less useful than "Companies under 50 employees in NAICS codes 23 and 31-33 receive new tax credits."

6. Surface buried provisions. Bills often hide important changes deep in technical sections. Look for these specifically.

You are not a partisan. You are not an advocate. You are a reader, helping other readers understand what they're looking at."""


SUMMARY_PROMPT = """Read this bill and produce a clear, plain-language summary.

Your summary should:
- Be 3-6 paragraphs
- State what the bill actually does, not what it's named or claimed to do
- Identify the major provisions and their scale (dollar amounts, scope, who's affected)
- Note any unusual or significant departures from current law
- Avoid jargon where plain English works
- Avoid both pro and con framing — just describe accurately

Do not use bullet points or markdown formatting. Write as continuous prose.
Begin directly with the summary — no preamble like "Here is a summary..."."""


SECTIONS_PROMPT = """Break this bill into its major substantive sections.

For each section, provide:
- The section identifier (Title, Subtitle, Section number, etc.)
- A short title (3-8 words)
- A 1-2 sentence description of what it does
- Dollar amount if relevant
- Number of people/entities affected if estimable

Skip sections that are purely procedural (effective dates, conforming amendments, severability, etc.) unless they contain substantive content.

Return your response as a JSON array. Use this exact format:

```json
[
  {
    "id": "Title I",
    "title": "Crop insurance reauthorization",
    "description": "Extends federal crop insurance subsidies for 5 years and expands coverage to specialty crops.",
    "amount": "$63 billion over 5 years",
    "scope": "All US farmers participating in federal crop insurance"
  }
]
```

Return ONLY the JSON array. No prose before or after. No markdown fences if avoidable.
If a field doesn't apply, use null rather than omitting it."""


RED_FLAGS_PROMPT = """Examine this bill for provisions that warrant scrutiny. These are NOT necessarily wrong or corrupt — many are legitimate. But they share patterns that often hide problematic content. Surface them so citizens can evaluate.

Look specifically for:

1. **Named-entity exemptions or benefits** — provisions that exempt or benefit a specific named company, person, or narrowly defined group. Often appears as "any entity meeting the following criteria..." with criteria that match exactly one organization.

2. **Buried unrelated provisions** — substantive policy changes inserted into bills nominally about something else (a healthcare provision in a defense bill, a tax break in an infrastructure bill).

3. **Vague or expansive grants of authority** — provisions giving agencies, officials, or private entities broad discretionary power without clear constraints.

4. **Sunset clause manipulation** — provisions that make popular benefits temporary while making controversial provisions permanent, or vice versa.

5. **Last-minute insertions** — language that appears poorly integrated, contradicts other parts of the bill, or has obvious indicators of being added late.

6. **Definitional changes with broad effect** — innocuous-looking definitions that shift meaning of existing law in significant ways.

7. **Funding mismatches** — authorizations for programs without corresponding appropriations, or appropriations far exceeding what the program description would suggest.

8. **Removal of oversight** — provisions reducing reporting requirements, audits, transparency, or accountability mechanisms.

9. **Special procedural treatment** — provisions exempting specific actions from normal regulatory, legal, or oversight processes.

10. **Cross-references that obscure meaning** — provisions that only make sense when read alongside multiple other laws, often hiding their actual effect.

Return your findings as a JSON array. Use this exact format:

```json
[
  {
    "section": "Section 47(c)(ii)",
    "type": "named_entity_benefit",
    "severity": "high",
    "description": "Exempts entities incorporated in Delaware before 1985 with revenue over $2B in agricultural exports — appears to match exactly one corporation.",
    "concern": "This appears to be a single-beneficiary provision disguised as general criteria.",
    "verify": "Check which corporations match these specific criteria."
  }
]
```

Severity: "low" / "medium" / "high"
Types: "named_entity_benefit" / "buried_provision" / "vague_authority" / "sunset_manipulation" / "last_minute_insertion" / "definitional_change" / "funding_mismatch" / "oversight_removal" / "procedural_exemption" / "obscured_cross_reference" / "other"

If you find no red flags, return an empty array: `[]`

Be honest. Don't invent flags. Don't flag things that are clearly legitimate just to fill the list. Quality over quantity.

Return ONLY the JSON array. No prose."""


BENEFICIARIES_PROMPT = """Analyze who benefits and who is harmed by this bill.

For each group, be as specific as possible:
- Not "businesses" but "manufacturers in NAICS 31-33 with revenue under $50M"
- Not "consumers" but "households earning $30K-$80K with student loan debt"
- Not "the wealthy" but "individuals with income over $400K from capital gains"

Return your response as a JSON object. Use this exact format:

```json
{
  "winners": [
    {
      "group": "Specific group description",
      "benefit": "What they gain concretely",
      "magnitude": "Estimated scale if possible (dollars, percentage, count)"
    }
  ],
  "losers": [
    {
      "group": "Specific group description",
      "harm": "What they lose concretely",
      "magnitude": "Estimated scale if possible"
    }
  ],
  "uncertain": [
    {
      "group": "Group whose impact is unclear",
      "reason": "Why the impact is hard to determine from the text"
    }
  ],
  "concentration_analysis": "Brief analysis: are the benefits concentrated (few big winners) or distributed (many small winners)? Same for harms."
}
```

If certain categories don't apply (e.g., no clear losers), use empty arrays.

Be honest about uncertainty. Don't claim impacts you can't substantiate from the bill text.

Return ONLY the JSON object. No prose."""

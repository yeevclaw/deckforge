# Phase 2.5 — Content Research Prompt (optional)

Use this **only when** the topic needs factual grounding (industry data, competitor info, latest standards, named entities, statistics). Skip it when the user has supplied all source material themselves.

---

## When to research

✅ Run research when:
- The deck makes claims that can be true or false (market sizes, dates, share prices, names, product specs)
- The audience is external (investors, customers, public) — facts must hold up
- The topic is fast-moving (AI, crypto, regulation)

❌ Skip research when:
- The user gave you a source doc — use that instead
- The topic is purely internal (Q4 team retro)
- The deck is hypothetical or instructional (no facts to verify)

## How to research

Feed each *part title* from the outline (not the deck topic) to your search tool, one at a time. The author of the source article recommends Grok for this; in this skill, use whatever web search tool is available (`WebSearch`, `WebFetch`, or an MCP search tool). Save findings per part.

For each part, gather:
- 3–5 verified facts (with source URL)
- 1–2 quotable expert opinions (with attribution)
- 1 contrarian / counter-view to keep things honest
- Any recent (last 6 months) developments

## Output format

Save to `research.md` in the working directory:

```markdown
# Research notes

## Part 1: <part_title>
- Fact: … (source: URL)
- Fact: … (source: URL)
- Quote: "…" — Person, Role, Date (source: URL)
- Counter-view: … (source: URL)
- Latest: … (date, source: URL)

## Part 2: ...
```

## Pass to Phase 2 / 3

When running the Outline Architect (Phase 2) or Planning Draft (Phase 3) prompts, paste the relevant section of `research.md` as the **背景調研信息 (Context)** block. The Architect prompt is already designed to use it.

## Quality bar

- Never use unsourced "facts". If you can't find a source, mark it `[unverified]`.
- Prefer primary sources (company filings, official docs) over third-party blog summaries.
- If two sources disagree, note both.

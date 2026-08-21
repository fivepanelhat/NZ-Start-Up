---
name: aether-decision-council
description: Use when the user needs rigorous multi-perspective pressure-testing of a high-stakes decision, strategy, trade-off, pivot, pricing, grant positioning, partnership term, architecture choice, or founder dilemma. Runs a structured 5-advisor council with anonymous peer review and chairman synthesis. Always apply for genuine uncertainty with meaningful stakes. Triggers include council this, run the council, pressure-test this, stress-test this, war room this, debate this, should I X or Y, which option, get multiple perspectives, I can't decide. Do not trigger on factual lookups, simple yes/no, or low-stakes creative tasks. Enforces HITL presentation for any verdict touching production, funding, cultural, or sovereignty matters. Owner Coastal Alpine Tech.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-21"
  maturity: Gold
  related: [aether-core, cat-architectural-standards, aether-hitl-protocol, te-mana-raraunga-controls]
  source_inspiration: Karpathy LLM Council + fivepanelhat/claude-skills-llm-council adaptation
---

# Aether Decision Council

Coastal Alpine Tech production skill. Transforms a single high-stakes question into five independent expert analyses, anonymous peer review, and a chairman synthesis. Designed for founder-mode decisions under uncertainty.

This skill is the official CAT-badged evolution of the LLM Council pattern. It is optimised for Aether / Super Grok sessions and carries mandatory HITL and Te Mana Raraunga overlays.

## When to Activate

Activate only when all of the following are true:
- Genuine uncertainty exists (more than one plausible path).
- Stakes are material (business, technical, cultural, capital, or relational consequences).
- The user benefits from structured multi-perspective challenge rather than a single recommendation.

Do **not** activate for:
- Pure factual questions.
- Simple preference or low-stakes creative requests.
- Validation-seeking without openness to critique.

## Core Process (Mandatory Sequence)

### 1. Frame & Enrich
- Restate the decision neutrally.
- Pull relevant context from the current conversation, memory, open files, recent transcripts, and CAT principles (sovereignty, HITL, unit economics, Te Tiriti alignment).
- If the question is underspecified, ask **one** clarifying question before proceeding.
- Explicitly note the primary standard if relevant (Gold / Platinum / Diamond) using `cat-architectural-standards`.

### 2. Convene the Five Advisors (Parallel, Independent)
Spawn five sub-agents. Each must fully inhabit its lens and produce 150–300 words. No cross-talk at this stage.

**Advisor Lenses (fixed):**

1. **The Contrarian**  
   Assumes fatal flaws exist. Actively hunts downside, second-order risks, failure modes, and reasons the idea should not proceed.

2. **The First-Principles Thinker**  
   Strips away assumptions, language, and inherited framing. Rebuilds the problem from fundamentals and questions whether the right problem is being solved.

3. **The Expansionist**  
   Focuses on upside, hidden optionality, scale potential, network effects, and pathways that could multiply impact or value.

4. **The Outsider**  
   Approaches with zero prior context or loyalty to CAT / Aether / Mana Kai narratives. Catches insider blind spots and jargon-induced groupthink.

5. **The Executor**  
   Demands feasibility. Answers “What exactly happens on Monday morning?” Focuses on sequencing, resource constraints, reversible steps, and immediate next actions.

### 3. Anonymous Peer Review
- Label the five responses A–E (no persona names visible to reviewers).
- Spawn five independent reviewer passes. Each reviewer must identify:
  - The strongest response and why.
  - The biggest blind spot across the set.
  - What every response missed.

### 4. Chairman Synthesis
One synthesis agent (the Chairman) receives all original analyses + peer reviews and produces the final structured verdict. The Chairman may override majority if the reasoning is stronger. The Chairman must surface any Te Mana Raraunga, cultural-safety, or HITL implications explicitly.

### 5. Present the Verdict (Structured Output)
Always use this exact markdown structure:

```markdown
## Council Verdict: {short topic}

### Where the Council Agrees
- ...

### Where the Council Clashes
- ...

### Blind Spots the Council Caught
- ...

### The Recommendation
{Clear, actionable recommendation. State confidence level.}

### The One Thing to Do First
{Single, concrete next action.}

### HITL & Sovereignty Notes
{Any required human approval gates, cultural review flags, or data-sovereignty considerations. If none, state “None material.”}
```

### 6. HITL Gate (Non-Negotiable)
If the recommendation touches any of the following, the skill **must** pause and present the full verdict for explicit user approval before treating it as final guidance:
- Production code, architecture, or deployment decisions.
- Funding, grants, capital allocation, or valuation positioning.
- Cultural content, Te Mana Raraunga claims, iwi/mana whenua engagement, or Mana Kai pathways.
- Any irreversible or high-cost action.

Present the verdict and ask:  
“Council complete. Do you want to accept this recommendation, adjust the framing and re-run, or take a different path?”

## Progressive Disclosure & Efficiency
- Keep the main body focused. Detailed persona prompts and example transcripts live in `references/`.
- Prefer parallel sub-agent calls where the runtime supports them.
- Do not generate long transcripts unless the user requests a saved record.

## Guardrails
- Never claim the council is infallible. It reduces single-model bias; it does not eliminate it.
- Never present the verdict as medical, legal, or cultural advice without clear disclaimers and HITL.
- Respect data sovereignty: do not invent or assume consent for any real farm, whānau, or iwi data.
- Align with `aether-core` and `aether-hitl-protocol` at all times.

## Versioning & Ownership
- Owned by Coastal Alpine Tech.
- Material changes require version bump and update to `metadata.last_updated`.
- Compatible with Aether Gold / Platinum / Diamond execution modes.

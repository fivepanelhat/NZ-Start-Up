---
name: aether-tool-selection
version: "1.0.0"
requires_hitl: true
description: Use when choosing which concrete tools to call for a task step — bash, file tools, GitHub MCP, browser, web search, X tools, connected services, image tools, or none. Produces an ordered tool ladder with load posture and HITL gates. Triggers include tool selection, which tool, choose tools, tool ladder, tool router, right tool for this, what should I call.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-23"
  maturity: Gold
  family: skill-meta
  related:
    - aether-skill-composition
    - aether-skill-companions
    - agent-hardening
    - aether-hitl-protocol
    - aether-core
    - cat-architectural-standards
    - cat-egress-sentinel
    - aether-git-workflow
  side_effect_class: read-only
  min_hitl_level: L1
  network_posture: none
  sovereignty_notes: Prefer local and owner-controlled tools before any network egress.
---

# Aether Tool Selection (v1.0.0)

Choose the right *tools* for the current step — not skills, not models, not agents.

Complements:
- `aether-skill-composition` → which skills to load
- `aether-skill-companions` → companion skills
- `aether-agent-routing` / performance → which model
- This skill → which concrete tool calls

## Core principles

1. **Local-first.** Prefer filesystem, local bash, and already-loaded context before network.
2. **Read before write.** Prefer read-only probes before any mutating tool.
3. **Least privilege.** Prefer the narrowest tool that can finish the step.
4. **No invented tools.** Never invent `send_`, `file_`, `pay_`, or results from tools not actually called (`agent-hardening`).
5. **Sovereignty.** Flag unexpected egress; align with `cat-egress-sentinel` for anything leaving the site.
6. **HITL on side effects.** External, production, funding, cultural, or money-adjacent actions need explicit human approval.

## Default tool ladder (prefer top → bottom)

| Rank | Class | Examples | Use when |
|------|--------|----------|----------|
| 1 | Context already in session | Prior messages, open files, memory | Answer is already known |
| 2 | Local read | `read_file`, local `bash` (ls/cat/rg) | Need repo or disk facts |
| 3 | Local write (sandboxed) | `write_file`, `edit_file`, local artefacts | Drafting skills, docs, code in workspace |
| 4 | Connected read (explicit) | GitHub get/list, Drive read | Need remote source of truth user connected |
| 5 | Network read | `web_search`, `browse_page`, X search | Public facts not in repo |
| 6 | Connected write | GitHub push/PR, Vercel deploy | Only after HITL for production paths |
| 7 | Browser interactive | `browser_tab` | Needs JS/session/UI state search cannot give |
| 8 | Heavy / generative | Image gen/edit, long media (ffmpeg) | Explicit visual or media goal |

Skip ranks that cannot help. Do not climb the ladder “just in case.”

## Decision process

1. **Restate the step** — one sentence: what must become true after this step.
2. **Classify side effects** — `none` | `local-write` | `external-read` | `external-write` | `production`.
3. **Pick the lowest rank** that can achieve the step with acceptable confidence.
4. **Name the tools** — exact tool names, not vague categories.
5. **State refusals** — tools that must *not* be used for this step and why.
6. **HITL gate** — if side effect ≥ external-write or production, stop for approval before calling.

## Output contract

```yaml
step: "one-sentence goal of this step"
side_effect_class: none | local-write | external-read | external-write | production
tool_ladder:
  - rank: 1
    tool: exact_tool_name
    purpose: why this call
    load: required | optional
refusals:
  - tool: ...
    reason: ...
hitl_required: true | false
hitl_reason: "if true"
sovereignty_notes: "egress / data residency if relevant"
```

## Common mappings (CAT)

| Task type | Prefer | Avoid first |
|-----------|--------|-------------|
| Read local skill / repo fact | `read_file`, local `bash` | web_search |
| Author skill / doc in workspace | `write_file` / `edit_file` | GitHub push until approved |
| GitHub state / PR / branch | GitHub connected tools | Scraping github.com in browser |
| NZ regulatory public page | `browse_page` / `web_search` | Inventing thresholds |
| Live X / social signal | X tools | Generic web search only |
| Edge node health | local probes / `cat-doctor` patterns | Cloud monitoring APIs |
| Customer send / file / pay | **none — human only** | Any autonomous send tool |

## Anti-patterns

- Calling web search when the answer is in an open local file
- Opening browser when a single `browse_page` or API read suffices
- Pushing to `main` or production without HITL
- Parallel tool spam without a ranked ladder
- Treating model memory as a substitute for a tool read

## Companions

Always consider with: `agent-hardening`, `aether-skill-composition`, `aether-skill-companions`.
For git/production: `aether-git-workflow`, `aether-hitl-protocol`, `release-preflight`.
For data leaving site: `cat-egress-sentinel`, `aether-data-sovereignty`.

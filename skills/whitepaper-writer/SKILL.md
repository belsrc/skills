---
name: whitepaper-writer
description: Use when creating or updating a comprehensive technical whitepaper documenting a repo's (or monorepo package's) architecture, design philosophy, and implementation for an engineer who has never seen the codebase. Dispatches subagents in parallel — a fixed baseline (docs/living-docs/specs, core architecture, types/data models, tests-as-behavior) plus one per subsystem found during recon — so coverage scales with repo size. Reads docs/, documentation/, living docs (ARCHITECTURE.md, CONSTRAINTS.md, JARGON.md, EPISTEMIC-MAP.md, README.md), and openspec/specs/ (INDEX.md when present, spec.md files directly when not), but code is always the final authority when any of these disagree. Use whenever the user asks for a "technical whitepaper," "architecture whitepaper," or comprehensive "system documentation," wants to document "how X system works" in depth, asks to update an existing whitepaper ("bump the revision," "add X to WHITEPAPER.md"), or wants documentation in the shape of a prior rev-N whitepaper.
metadata:
  version: "1.0.0"
---

# Whitepaper Writer

This skill produces the kind of document that takes many long conversations to get right by hand: a comprehensive, engineer-to-engineer technical whitepaper covering a system's architecture, design philosophy, mathematical or algorithmic model (when one genuinely exists), extension points, and implementation details — grounded entirely in what the code actually does.

"Whitepaper" here does not mean marketing collateral. It means the register of `references/whitepaper-template.md`'s reference examples: dense, precise, written for someone who is about to work in this codebase and needs the real model of it, not a sales pitch — and not a code review of the repo either. It documents a system. It does not narrate the process that produced the document.

## Requirement Language

This skill uses MUST / MUST NOT / SHOULD / SHOULD NOT / MAY as in RFC 2119. MUST and MUST NOT are non-negotiable — skipping one is a defect in the output, not a judgment call. SHOULD and SHOULD NOT are strong defaults; deviate only when there's a concrete reason specific to the repo at hand, and be able to name that reason. MAY is genuinely optional, left to judgment.

## When to Use This Skill

- Generating a first whitepaper for an undocumented or under-documented system
- Updating an existing whitepaper after the system has changed (new features, architectural changes, removed subsystems)
- A user references a specific package/directory as the scope ("write a whitepaper for packages/rule-engine")
- A user wants documentation "at the level of" or "in the style of" an existing whitepaper they show you

## When NOT to Use This Skill

- A simple README for installation/usage — a narrower task than this skill covers
- API reference generation (JSDoc/TSDoc extraction) — use language-appropriate doc tooling
- A changelog or release notes
- Documenting a single function or small utility — this skill is for systems, not snippets

## How to Use

### Step 1: Scope the Whitepaper

You MUST determine what you're documenting before exploring anything:

- **Scope boundary**: whole repo, or a single package/directory in a monorepo? If unclear, you MUST ask before proceeding — this determines where the reconnaissance pass starts and which `openspec/specs/` entries are in-scope.
- **Fresh or update?** You MUST check for an existing whitepaper first (common locations: repo root, `docs/`, wherever the user points you). If one exists, this is an update: you MUST read it fully before exploring code, so you know what it already claims and can check each claim against current code rather than re-deriving everything from zero. See `references/revision-history.md`.
- **Output location**: if updating, you MUST write back to the same path. If fresh, you SHOULD default to `WHITEPAPER.md` at the scope root unless the user specifies otherwise or an existing convention (e.g. a `docs/` directory holding other long-form docs) suggests a better fit.
- **The system's name**: you SHOULD identify what to call the system being documented (from its package name, repo name, or an established name in existing docs) before writing anything. This name becomes the subject of the document — see `references/whitepaper-template.md`'s Voice section.

### Step 2: Reconnaissance Pass — One Subagent, Not the Main Thread

You MUST dispatch a single subagent to build the inventory rather than doing it in the main thread yourself. Recon touches a lot of raw surface area — every living doc's existence, every OpenSpec capability, every top-level package's shape — and none of that needs to sit in your context once a plan has been drawn from it. This is not the fixed+dynamic swarm from Step 3; it MUST be exactly one subagent, dispatched alone, whose entire job is to hand back a compact dispatch plan instead of a pile of raw discovery output.

**Explore**: `docs/` and `documentation/` directories; which living docs exist at the scope root (`ARCHITECTURE.md`, `CONSTRAINTS.md`, `JARGON.md`, `EPISTEMIC-MAP.md`, `README.md` — existence only, not a deep read; that happens in Step 3); `openspec/specs/`, which MUST be checked whenever it exists regardless of whether an `INDEX.md` sits inside it (see `references/exploration.md` for the with/without-index procedure); top-level source directories/packages/modules and their entry points; test directory locations.

**Return**: a dispatch plan — which living docs exist and where, the OpenSpec capability picture (parsed from `INDEX.md` or reconstructed from `spec.md` files when there's no index), a proposed subsystem list for Step 3's dynamic subagents with cross-cutting capabilities assigned to each, and test directory locations. This MUST be a plan, not raw file dumps.

You MUST wait for this plan before moving to Step 3 — the dynamic subagent list depends on it. Full task template and the OpenSpec with/without-index procedure are in `references/exploration.md`.

### Step 3: Dispatch Subagents

Two kinds of subagents, dispatched together once recon's plan is in hand:

**Fixed baseline** — MUST always be spawned, regardless of repo size; this is the coverage guarantee:
1. Docs, living-docs, and specs synthesis
2. Core architecture and entry points
3. Types and data models
4. Tests-as-behavior

**Dynamic subsystem subagents** — you MUST spawn one per subsystem the reconnaissance pass found; this is what scales with repo size instead of flattening a 12-package repo into 4 buckets:
- One per top-level package/module/directory that has enough surface area to warrant its own exploration
- You MUST cross-check dynamic subagent scope against the OpenSpec capability list so that a capability with no obvious directory (a cross-cutting concern like filtering or suppression logic threaded through several files) still gets assigned to some subagent rather than being silently dropped

Every subagent, fixed or dynamic, MUST return the same contract: a verified purpose statement (checked against code, not copied from docs), file:line references for every claim, representative snippets worth quoting, any conflicts it found between docs/specs and code, and candidate mathematical structure if the subsystem actually has one. This return contract is **input to you, the orchestrator** — it is not a preview of the finished prose. File:line references exist so you can verify and reconcile; they MUST NOT be transcribed wholesale into the whitepaper (see Step 5 and `references/code-truth-and-conflicts.md`). Full task templates are in `references/exploration.md`.

### Step 4: Reconcile Sources Against Code

Code MUST win every disagreement. This is not a soft preference — it's the organizing principle of the whole skill. Documenting current behavior as the primary claim, everywhere, is not optional.

A conflict between what a doc claims and what the code does is still worth tracking as you find it — it's often the single most valuable thing exploration turns up (a stale doc, a migration in progress, deliberate drift) — but it MUST NOT become a dedicated section or subsection in the whitepaper. Headers like "Current doc drift," "Documentation gaps," or similar MUST NOT appear anywhere in the document. Where a specific conflict is genuinely load-bearing for understanding a subsystem, it MAY be folded into that subsystem's ordinary prose as a brief aside — sparingly, the rare exception, not a recurring feature every section gets. Full reconciliation rules, including source priority order and exactly where the line sits between "worth a brief aside" and "noise," are in `references/code-truth-and-conflicts.md`.

Every conflict found MUST still be tracked — its destination is the conversational report to the user in Step 8, not the file itself.

### Step 5: Structure and Write the Whitepaper

You MUST follow the structural template in `references/whitepaper-template.md`: Abstract, System Overview (problem domain, design philosophy, architecture diagram, core model), one deep-dive section per subsystem, extensibility/integration, technical stack, conclusion, appendices with full worked examples.

Decisions that reference file walks through in detail:

- **Voice.** The system MUST be named and used as the grammatical subject throughout ("The X System provides...," "The X System addresses..."), matching how the reference examples write. It MUST NOT be repeatedly called "the repo," "the codebase," or "this repository" as the default subject — that describes a git repository, not the system it implements, and reads as commentary about the code rather than documentation of the system.
- **No meta-narration.** The document MUST NOT describe its own writing process, sourcing, or verification methodology — no sentences like "the code is the source of truth" or "drift is called out where it matters." Those are true of how this skill works, not true of the system being documented, and have no place in the output.
- **Depth proportional to actual complexity.** A section's length MUST track what the subsystem actually has to say, not a target length. You MUST NOT pad a simple subsystem's section to match the apparent depth of a complex one, and you SHOULD cut any sentence that only restates the sentence before it in different words ("this means...," "therefore...," "this is best described as...") without adding new information.
- **Whether to formalize the core model as math.** You SHOULD formalize it as LaTeX only when the system has genuine algebraic or compositional structure worth writing that way (filter composition, state transitions, type-level computation). If the "model" is really a taxonomy or a decision tree, you MUST present it as a categorized breakdown with a diagram instead — manufacturing notation over what's actually a list of enum values reads as rigor theater, not rigor.
- **Code examples MUST use the repo's actual language(s)** — you MUST NOT translate a snippet into a different language for the reader's convenience. A bare filename MAY be mentioned sparingly when it helps the reader; systematic `(file:line)` citations after nearly every claim MUST NOT appear in the prose — see `references/code-truth-and-conflicts.md`.

### Step 6: Revision History

If this is an update to an existing whitepaper, you MUST append a new revision entry rather than rewriting history — see `references/revision-history.md` for the format and how to derive what changed (git log since the prior revision date where available, otherwise a structural diff against what the previous version documented).

### Step 7: Structural Validation

Before presenting the whitepaper, you MUST run the validator bundled with this skill (`scripts/validate_structure.py`, relative to this skill's own directory — its install location varies by agent/environment):

```bash
python3 scripts/validate_structure.py <path-to-whitepaper.md>
```

This checks required sections are present and that fenced code blocks are at least syntactically well-formed (JSON parses, brace/paren balance for C-family languages, Python compiles, Rust/TS get a best-effort brace-balance check since a full compile needs the surrounding project). It will not catch bad technical content, meta-narration, drift sections, or citation noise — a qualitative review MUST still happen — but it catches the mechanical failures (a truncated code block, invalid JSON in a config example) that are embarrassing to ship. A FAIL from this script MUST be fixed before presenting the whitepaper; a WARN SHOULD be reviewed but does not block presenting.

### Step 8: Report Drift Findings Separately

Any documentation drift tracked during Step 4 (stale docs, specs that no longer match code, gaps between what's documented and what's implemented) MUST stay out of the whitepaper file. Instead, after presenting the whitepaper, you SHOULD summarize what was found in your conversational reply to the user — a short list is enough. This keeps the whitepaper focused on documenting the system as it is, while still surfacing doc-quality issues the user will want to know about.

## Writing-Quality Pass

Dense technical writing is exactly where AI slop hides best — inflated significance, promotional tone ("leverages," "robust," "seamlessly"), claims about what a design "elegantly solves" that outrun what the document's own citations support. Before finalizing, you SHOULD run the whitepaper through a writing-quality skill, in order of preference: `human-english` if it is available, otherwise `humanizer` if that is available. If neither is available, you MAY use your own judgment to reread for the same patterns instead — this step is not a hard requirement, but it SHOULD NOT be skipped silently.

## Example Trigger Phrases

- "We haven't documented the layer-orchestration package yet, can you write a full technical whitepaper for it?"
- "Update WHITEPAPER.md — we added REST dataset support since the last revision, bump the revision history"
- "Write a whitepaper for this repo at the level of detail as [existing example], code is the source of truth if anything's out of date"
- "Document how the extension system actually works, comprehensively, citing the real code"

## Important Notes

- **Code MUST always be the source of truth.** Every other source (docs/, living docs, OpenSpec specs whether via `INDEX.md` or direct `spec.md` files, an existing whitepaper being updated) is context to verify against code, never to transcribe.
- **This skill MUST NOT backfill missing living docs by generating them.** It documents the system as it currently stands. If living docs exist, treat them as input; if they don't, proceed without them.
- **Monorepo scope MUST stay inside its boundary.** You MUST NOT document a sibling package's internals as though they belong to the one in scope, though referencing a sibling as a dependency is fine.
- **Numbered sections SHOULD stay comparatively tight; appendices SHOULD carry the exhaustive detail** — full, non-truncated, realistic worked examples belong there.
- **The whitepaper documents the system, not itself.** No meta-narration about methodology, no dedicated drift/gaps sections, no systematic file:line citation noise — see Steps 4, 5, and 8.

# whitepaper-writer

Create or update a technical whitepaper that explains how a system works, for an engineer who needs the real model of the codebase.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When not to use](#when-not-to-use)
- [How it works](#how-it-works)
- [What the whitepaper contains](#what-the-whitepaper-contains)
- [Validation](#validation)
- [File layout](#file-layout)
- [References](#references)
- [Related skills](#related-skills)

## Installation

```bash
npx skills add https://github.com/belsrc/skills --skill whitepaper-writer
```

## Quick Start

Ask for a whitepaper in plain language:

```text
write a whitepaper for packages/rule-engine
```

Update an existing document:

```text
Update WHITEPAPER.md — we added REST dataset support since the last revision, bump the revision history
```

Ask for comprehensive system documentation:

```text
Document how the extension system actually works, comprehensively, citing the real code
```

The skill writes a new `WHITEPAPER.md` at the scope root, or updates the existing whitepaper in place.

## What it does

This skill produces long-form technical documentation for a whole repo or a scoped package. The output is a whitepaper, not a README and not an API reference.

It focuses on four things:

- Scope the system before exploration starts
- Read code, docs, specs, and tests together
- Reconcile disagreements with code as the final authority
- Produce a structured whitepaper with revision handling and validation

It uses real code and config examples from the target repo. It does not invent examples.

The package includes a validator script and supporting references for exploration, structure, revision history, and conflict handling.

## When to use

Use this skill when you want to:

- Generate a first whitepaper for an undocumented system
- Update an existing `WHITEPAPER.md` after architecture or feature changes
- Document one package or directory inside a monorepo
- Produce deep system documentation for engineers, not marketing copy
- Capture design philosophy, subsystem structure, data models, and extension points in one document

## When not to use

Do not use this skill for:

- A simple README
- Generated API reference docs
- Release notes or changelogs
- Documentation for a single function or small utility

## How it works

### 1. Scope first

The skill identifies the documentation boundary before it explores anything. It checks whether the request targets a whole repo or one package. It also checks whether a whitepaper already exists.

If a whitepaper exists, the skill reads it first, then verifies its claims against current code.

### 2. Run one reconnaissance subagent

The first pass is a single recon subagent. It maps the surface area and returns a dispatch plan instead of raw file dumps.

Recon checks:

- `docs/` and `documentation/`
- Living docs such as `ARCHITECTURE.md`, `CONSTRAINTS.md`, `JARGON.md`, `EPISTEMIC-MAP.md`, and `README.md`
- `openspec/specs/`, with or without `INDEX.md`
- Top-level packages, modules, entry points, and test directories

### 3. Dispatch the main exploration in parallel

After recon returns the plan, the skill runs a fixed baseline plus one subagent per subsystem.

The fixed baseline always covers:

1. Docs, living docs, and OpenSpec synthesis
2. Core architecture and entry points
3. Types and data models
4. Tests as behavior

Dynamic subagents cover each subsystem that recon found. Cross-cutting OpenSpec capabilities get assigned to one of those subsystem passes so they do not fall through the cracks.

### 4. Reconcile sources

The skill compares code, specs, living docs, and any existing whitepaper.

Source priority is:

1. Code
2. OpenSpec `spec.md` files
3. Living docs
4. Existing whitepaper

The whitepaper documents current behavior. Drift findings stay out of the file and go in the follow-up report.

### 5. Write the whitepaper

The skill uses the bundled template to build the document. It names the system, writes a system overview, adds one deep-dive section per subsystem, and puts full worked examples in appendices.

If the existing document is an update, the skill appends a new revision entry instead of rewriting history.

## What the whitepaper contains

The default structure comes from `references/whitepaper-template.md`.

Typical sections include:

- Revision date and version, when available
- Abstract
- System overview
- Problem domain and design philosophy
- Architecture diagram in Mermaid
- Core model
- One deep-dive section per subsystem
- Extensibility and integration
- Technical stack and dependencies
- Conclusion
- Appendices with full worked examples
- Revision history on updates

## Validation

Before delivery, the skill runs the bundled validator:

```bash
python3 scripts/validate_structure.py path/to/WHITEPAPER.md
```

The validator checks:

- Required top-level sections
- Prohibited drift or gaps sections
- Inline citation density
- Fenced code block syntax for supported languages
- Mermaid block presence and shape

The script uses Python 3. It can also use `bash`, `node`, and `PyYAML` when they are available.

## File layout

```text
whitepaper-writer/
├── README.md
├── SKILL.md
├── references/
│   ├── code-truth-and-conflicts.md
│   ├── exploration.md
│   ├── revision-history.md
│   └── whitepaper-template.md
└── scripts/
    └── validate_structure.py
```

## References

- `SKILL.md`: core workflow, trigger phrases, and operating rules
- `references/whitepaper-template.md`: default section structure and writing guidance
- `references/exploration.md`: recon flow and subagent dispatch model
- `references/revision-history.md`: update handling and revision entry format
- `references/code-truth-and-conflicts.md`: source priority, drift handling, and citation rules
- `scripts/validate_structure.py`: structural and code-block validation

## Related skills

- `human-english`: preferred final writing pass for clearer prose

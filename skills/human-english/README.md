# human-english

Write or rewrite text so it reads as clear and human, not AI slop.

This skill merges two approaches to detecting and fixing machine-generated text. The first is **Simplified Technical English (ASD-STE100)**, structural rules for clarity. The second is a **content-pattern catalog** for spotting AI writing tells. I liked the `humanizer` skill and the `simple-english` skill so I combined them. The `simple-english` rules take precedence.

## Table of Contents

- [Installation](#installation)
- [What It Does](#what-it-does)
- [When to Use](#when-to-use)
  - [Pragmatic Mode (default)](#pragmatic-mode-default)
  - [Strict Mode](#strict-mode)
  - [Voice Mode](#voice-mode)
- [Quick Start](#quick-start)
  - [Example Transformations](#example-transformations)
- [How It Works](#how-it-works)
  - [Structural Rules (Pragmatic/Strict)](#structural-rules-pragmaticstrict)
  - [Content Patterns (All Modes)](#content-patterns-all-modes)
- [Precedence Rules](#precedence-rules)
- [Untouchables](#untouchables)
- [Beyond Documentation](#beyond-documentation)
- [Self-Check Minimum](#self-check-minimum)
- [References](#references)
- [Limits](#limits)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Metadata](#metadata)

## Installation

```bash
npx skills add https://github.com/belsrc/skills --skill human-english
```

## What It Does

**Simplified Technical English (STE)** is the controlled language aerospace and defense manufacturers use for maintenance documentation. Its rules exist so a tired reader who is not a native English speaker cannot misread an instruction. The rules require short sentences, one meaning per word, active voice, approved modals, and condition before command.

**The content-pattern catalog** (originally from the `humanizer` skill) targets the specific tells of LLM-generated prose. These include inflated significance, promotional language, vague attributions, rule-of-three padding, em-dash overuse, and sycophantic tone. The patterns are cataloged from Wikipedia's "Signs of AI writing" project.

Both remove the same broad family of problems (long sentences, synonym rotation, hedges, filler, decorative clauses), so they combine cleanly. Where they genuinely disagree, **STE's structural rules win within STE's scope** (technical and procedural text).

## When to Use

### Pragmatic Mode (default)
Technical and procedural text where clarity is critical:
- Documentation, READMEs, runbooks
- Error messages, release notes
- Incident reports, API guides
- Agent instructions (AGENTS.md, prompts, skills)

### Strict Mode
When full STE compliance matters:
- User mentions "STE", "ASD-STE100", or compliance
- Aerospace, defense, or regulated industries
- Translation preparation (reduces ambiguity)

### Voice Mode
Non-technical content where personality matters:
- Blog posts, marketing copy
- Essays, narrative prose
- Brand voice writing

## Quick Start

The skill operates in one of three modes based on the text type and user request:

```
/human-english
```

By default, the skill analyzes the text and selects the appropriate mode. For technical text, it applies STE structural rules and content-pattern detection. For blog or marketing content, it applies only content-pattern detection with voice guidance.

### Example Transformations

**Before (AI slop):**
```
The migration has been completed successfully, and the table is currently
being rebuilt, ensuring that all data remains accessible to users throughout
this pivotal process.
```

**After (human-english):**
```
The migration is complete. The database rebuilds the table. All data stays
accessible during the rebuild.
```

**Before (promotional puffery):**
```
Our solution boasts a vibrant ecosystem of integrations, marking a pivotal
moment in the industry's journey toward seamless interoperability.
```

**After (human-english):**
```
The platform integrates with 12 third-party services.
```

## How It Works

1. **Select the mode**: Pragmatic (technical/procedural), Strict (compliance), or Voice (narrative)
2. **Classify text**: Procedural (instructions) vs. descriptive (explanations)
3. **Fix vocabulary**: One word per concept (check/verify/confirm, pick one)
4. **Apply structural rules**: 53 rules across 9 sections (Pragmatic/Strict only)
5. **Scan for content patterns**: 15 AI writing tells (all modes)
6. **Add personality**: Voice mode only
7. **Run self-check**: Verify against the checklist

### Structural Rules (Pragmatic/Strict)

- **Sentence limits**: 20 words (procedural), 25 words (descriptive)
- **Approved modals**: can, will, must (banned: should, would, may, might, could)
- **Verb forms**: Simple tenses only (no present perfect, no passive except when agent is unknown)
- **One meaning per word**: No synonym rotation for variety
- **Active voice**: "The script deletes the cache" not "The cache is deleted"
- **Condition before command**: "If the build fails, read the log" not "Read the log if the build fails"
- **No contractions**: Keep articles and complete grammar

### Content Patterns (All Modes)

15 patterns from Wikipedia's AI writing detection project:

| Pattern | Fix |
|---------|-----|
| Inflated significance ("pivotal", "testament to") | State the concrete fact |
| Promotional language ("boasts", "nestled in") | Replace with plain facts |
| Vague attribution ("experts argue") | Name the source or delete |
| Superficial -ing clauses | Delete or make its own sentence |
| Rule-of-three padding | Cut to actual count |
| Synonym cycling (one thing, many names) | Pick one term |
| Em-dash overuse | Use commas or split sentences |
| Sycophantic tone ("Great question!") | Delete the praise |
| Collaborative residue ("I hope this helps!") | Delete entirely |

Full catalog with before/after examples in `references/patterns.md`.

## Precedence Rules

Where STE and content-pattern guidance conflict:

- **Inside STE scope** (technical/procedural text): structural rules win (no contractions even if warmer, no banned modals for hedging, no digressions past word ceiling)
- **Outside STE scope** (blog/marketing/narrative): content-pattern catalog and voice guidance apply in full (STE never claimed this territory)

## Untouchables

Never modify these, even when they break rules:

- Code blocks, inline code, identifiers, CLI commands
- Quoted error messages and log lines
- Product names, API endpoints, config keys
- File paths, numbers with units

## Beyond Documentation

The same rules apply to different content types:

- **Error messages**: What happened (past tense), cause, fix (imperative), no "Oops" or apologies
- **Runbooks**: Imperative steps, conditions first, warnings before the step
- **Incident reports**: Simple past only with timestamps ("Between 14:02 and 14:31 UTC, 12% of requests failed")
- **Release notes**: Breaking changes follow warning pattern (command first, risk second)
- **Agent instructions**: One instruction per sentence, no "should", condition first

See `references/use-cases.md` for detailed adaptations.

## Self-Check Minimum

Before delivery (Pragmatic/Strict):

1. Count words in three longest sentences (over 20/25 limit? Split them)
2. Search for contractions (`'ll`, `'re`), `has been`, `should`, `-ing` verbs after comma, semicolons
3. Check all `if`/`when` (each starts its sentence, before the command)
4. Verify vocabulary consistency (did you use "check" everywhere or mix in "verify"?)
5. Scan against CP-1 through CP-15 pattern catalog

Voice mode: skip steps 1-4 (structural), run step 5, then verify against `references/voice-mode.md`.

Full checklist with searchable patterns in `references/checklist.md`.

## References

- **[vocabulary.md](references/vocabulary.md)**: Word substitution table, modal ladder, consistency rotations
- **[patterns.md](references/patterns.md)**: Before/after examples for all 15 content patterns
- **[voice-mode.md](references/voice-mode.md)**: Personality and voice guidance for narrative content
- **[checklist.md](references/checklist.md)**: Full verification pass with searchable patterns
- **[use-cases.md](references/use-cases.md)**: Long-form adaptations for error messages, runbooks, incidents, etc.

## Limits

STE structural rules apply to technical facts and instructions only. Do not apply them to marketing copy, blog voice, or brand writing because they delete persuasion by design. When a user asks for STE on marketing text, offer Voice mode instead.

The content-pattern catalog (CP-1 through CP-15) has no such restriction; it applies to any AI-sounding text in any mode.

## Disclaimer

This skill is an unofficial tool combining an ASD-STE100 implementation with a Wikipedia-sourced pattern catalog. It is not affiliated with or endorsed by ASD, STEMG, or the Wikipedia WikiProject AI Cleanup. No tool can guarantee ASD-STE100 compliance or that text will pass as human-written.

ASD-STE100 is a registered trademark of ASD. The official standard is a free download at [asd-ste100.org](https://asd-ste100.org).

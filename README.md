# Skills

There are hundreds of skills out there now. Most are variations on the same few ideas. This repo contains only the ones I thought were genuinely novel.

## What's Here

### `socratic-tutor`
Interactive tutoring that teaches from first principles. It checks prerequisites, builds understanding step by step, and makes you use what you learned.

### `engineering-council`
A council of engineering personas (Knuth, Carmack, Beck, etc.) that evaluates a hard technical decision from different viewpoints. Each persona runs in isolation, so you get real disagreement instead of one averaged answer.

### `human-english`
A rewrite skill for docs, prompts, runbooks, release notes, and other prose. It combines Simplified Technical English with a pass that removes common AI writing tells.

### `ticket-creator`
Turns a loose feature request, bug report, or task description into a structured project ticket with clear acceptance criteria.

### `whitepaper-writer`
Creates or updates a technical whitepaper for a repo or package. It reads code, docs, specs, and tests, then writes a long-form system document with code as the final authority.

## Installation

Use the `skills.sh` package to install the skills you want:

```bash
npx skills add https://github.com/belsrc/skills --skill socratic-tutor
npx skills add https://github.com/belsrc/skills --skill engineering-council
npx skills add https://github.com/belsrc/skills --skill human-english
npx skills add https://github.com/belsrc/skills --skill ticket-creator
npx skills add https://github.com/belsrc/skills --skill whitepaper-writer
```

Each skill also has its own README in `skills/<name>/README.md`.

## Usage

### Socratic Tutor

```text
Teach me about binary search
```

The tutor builds a syllabus, checks prerequisites, explains the concept in more than one way, and asks questions to verify that you understand it.

### Engineering Council

```text
Should I rewrite this entity update loop to be data-oriented,
or is the object-per-entity version fine until it shows up in a profile?
```

The skill classifies the question, picks the relevant personas, grounds the discussion in repo facts when needed, and names the tradeoff they disagree on.

### Human English

```text
/human-english
```

Use it to rewrite technical or narrative prose so it reads clearly and sounds human.

### Ticket Creator

```text
create a ticket: add --json flag to scan command for programmatic output
```

The skill researches the repo, detects project metadata, and writes a ticket with actionable acceptance criteria.

### Whitepaper Writer

```text
write a whitepaper for packages/rule-engine
```

The skill creates or updates a `WHITEPAPER.md` by reading code, docs, specs, and tests.

## Why These Skills

Each skill here solves a problem that generic prompting usually handles badly.

**Socratic Tutor** because most "teach me X" chats stop at explanation. I wanted something that checks prerequisites, builds a real mental model, and makes you apply it.

**Engineering Council** because hard design questions need competing views, not one polished answer. The value is in seeing the disagreement clearly.

**Human English** because a lot of generated prose is technically correct and still hard to read. This one fixes both the structure and the tone.

**Ticket Creator** because "turn this into a ticket" sounds simple until you need project context, numbering, and acceptance criteria that another engineer can act on.

**Whitepaper Writer** because a README is not enough when a new engineer needs the real model of a system.

These are the problems I kept running into, so these are the skills I built.

# Skills

There are hundreds of skills out there now. Most are variations on the same few ideas. This repo contains only the ones I thought were genuinely novel.

## What's Here

### `socratic-tutor`
Interactive tutoring that actually teaches. Uses Socratic questioning to build understanding from first principles. Checks comprehension at every step. Works for learning anything - algorithms, calculus, distributed systems, whatever.

### `engineering-council`
Convenes a council of engineering personas (Knuth, Carmack, Beck, etc.) to evaluate technical decisions from opposing viewpoints. Each persona runs in isolation, so you get real disagreement instead of averaged mush. The output names the axis they split on.

## Installation

Add to your Claude Code environment:

```bash
# Clone the repo
git clone https://github.com/belsrc/skills
cd skills

# Link to your Claude Code skills directory
ln -s $(pwd)/skills/* ~/.claude/skills/
```

Or install individually:

```bash
npx skills add https://github.com/belsrc/skills --skill socratic-tutor
npx skills add https://github.com/belsrc/skills --skill engineering-council
```

## Usage

### Socratic Tutor

```
Teach me about binary search
```

The tutor builds a syllabus, checks prerequisites, explains the concept formally and intuitively, then asks questions to verify you actually get it. Includes exercises.

### Engineering Council

```
Should I rewrite this entity update loop to be data-oriented,
or is the object-per-entity version fine until it shows up in a profile?
```

The skill classifies the question, selects relevant personas (e.g., Carmack vs Muratori for performance), runs each in isolation, and synthesizes where they agree and where they split.

## Why These Two

**Socratic Tutor** because most "explain X" interactions are shallow. This one builds mental models from scratch and tests whether you actually learned anything. The multi-session design with checkpoints means you can learn large topics across multiple conversations without losing the thread.

**Engineering Council** because single-model answers to hard design questions give you one confident take when what you need is the set of competing takes and why they disagree. Isolated subagents produce uncorrelated perspectives. Keyword-first routing keeps the selection deterministic. The synthesis names the split instead of pretending there's consensus.

Both solve problems I had.

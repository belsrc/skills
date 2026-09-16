# Whitepaper Structure

The section template below is distilled from two whitepapers that converged on this shape through a lot of iteration. It is the default skeleton, not a rigid form to fill in mechanically: you SHOULD adjust section count and depth to what the system actually has, and you MUST NOT manufacture a section out of nothing just to match the template.

---

## Required Skeleton

```
**Revision Date:** <date>
**Version:** <if the repo has one — omit if not>

## Abstract

## 1. System Overview
### 1.1 Problem Domain
### 1.2 Design Philosophy
### 1.3 Architecture Overview        (mermaid flowchart)
### 1.4 Core [Mathematical] Model    (see "Formalizing the Core Model" below)

## 2. <Subsystem Deep-Dive>
## 3. <Subsystem Deep-Dive>
...
## N. <Subsystem Deep-Dive>

## Extensibility and Integration
## Technical Stack and Dependencies   (omit if the system has no notable external deps)

## Conclusion
### Key <Architectural Strengths|Characteristics>

## Appendices
### Appendix A: <Full Worked Example>
### Appendix B: <Full Worked Example>
...

## Revision History     (only on updates — see references/revision-history.md)
```

No other headers belong at this level. In particular, sections or subsections named things like "Current doc drift," "Documentation gaps," or "Drift" MUST NOT appear anywhere in the document — see `references/code-truth-and-conflicts.md` for where conflict findings actually go.

### Per-Subsystem Section Pattern

Each numbered deep-dive section (2 through N) tends to follow a recurring micro-pattern, because it's the pattern that makes dense technical writing readable: state the problem before the solution.

1. **The challenge** — what problem this subsystem exists to solve, stated concretely (not "flexibility is important" — the actual failure mode that motivated the design)
2. **The solution** — the approach taken, at the level of a paragraph or two
3. **Structural details** — types, algorithms, data flow, whatever the subsystem's actual substance is
4. **Examples** — real code/config pulled from the repo, cited by path

Not every section needs all four beats explicitly labeled, but the shape underneath MUST be there. A section that's just a wall of type definitions with no framing of why they exist reads as a dump, not documentation.

**Depth MUST track what the subsystem actually has, not a target length.** A genuinely simple subsystem gets a short section; you MUST NOT pad it with restated framing to make it look as deep as a complex neighbor. The clearest symptom of padding is the summary-of-summary sentence — "this means...," "therefore...," "this is best described as..." — that recaps what the paragraph just said instead of adding something the reader didn't already have. Cut those on sight. Every sentence SHOULD earn its place by adding information; if it doesn't, it doesn't belong, regardless of whether the section "looks thin" without it.

---

## Voice

The system MUST be named and used as the grammatical subject throughout — "The Layer Orchestration System provides...," "The system follows..." — the way the reference examples write. Establish the name early (Step 1's scoping, or the Abstract) and then use it, or a consistent stand-in like "the system," for the rest of the document.

**"The repo" and "the codebase" MUST NOT be the default subject.** A sentence like "the repo is extensible in four practical ways" describes a git repository, not the system it implements, and reads as commentary about the code rather than documentation of what the system does. This is a small substitution with a large effect on register — it's the difference between a whitepaper and a long code review comment. Consistency matters more than variety here: don't swap between "the repo," "the codebase," "this repository," and the system's actual name to avoid repeating a word — pick the name (or "the system") and stay with it.

**The document MUST NOT narrate its own production.** No sentences describing this skill's own methodology — "the code is the source of truth," "drift is called out where it matters," or similar. Those describe how the whitepaper was written, not what the system does, and a reader of technical documentation has no use for either. If a sentence is more true of the writing process than of the system, it does not belong in the document.

---

## Formalizing the Core Model

This is the highest-leverage judgment call in the whole document, and it's easy to get wrong in both directions.

**You SHOULD formalize as LaTeX when the system has genuine compositional/algebraic structure** — a transformation pipeline where the *composition itself* is the thing worth explaining precisely (filter composition rules, state transition functions, type-level computation with real generic constraints). In that case, the model MUST be defined formally: what maps to what, under what conditions, with explicit cases. A worked example:

```latex
$$
\mathcal{L}_T = \mathcal{O}_T(D, C, I_T) \circ \mathcal{D} \circ \mathcal{F}_{\text{impl}} \circ \mathcal{E} \circ \mathcal{H} \circ S_T
$$
```

...followed by a definition of every symbol, and case-by-case breakdowns for any piecewise logic (filter composition truth tables, conditional dispatch), written as proper case notation rather than prose paragraphs describing branches.

**You MUST NOT formalize when the "model" is really a taxonomy or a decision tree.** If a system's core logic is "there are four categories of X, and detection falls into one of them based on a few boolean flags," that's a categorization, not an algebra — dressing it up in set-builder notation manufactures an appearance of rigor the system doesn't actually have. It MUST instead be presented as a labeled breakdown (bold category names, bullet characteristics, a code type showing the actual discriminant) plus a diagram. This is not a lesser treatment — done well, a clear taxonomy is exactly as rigorous as the domain calls for, and forcing math onto it makes the document less trustworthy, not more.

The test: could you write the LaTeX version and have every symbol correspond to something the code actually computes, with the equation predicting behavior you could otherwise only get by reading the implementation? If yes, it SHOULD be formalized. If the equation would just be restating "if A then B else C" with Greek letters, it MUST NOT be.

---

## Diagrams

Mermaid `flowchart` for pipelines and architecture overviews; `sequenceDiagram` for multi-actor interactions and request/response workflows. Style key nodes (input, output, decision points) with `style` directives for visual anchoring — light blue for entry, green for terminal output, orange/pink for branch points is a reasonable default palette, but match whatever visual language the rest of the document already uses if this is an update.

Every diagram MUST be traceable to what a subagent actually found, not an idealized version of the architecture. If the real control flow has an awkward special case, the diagram MUST show it.

---

## Code Examples

- **Code examples MUST use the repo's actual language(s).** You MUST NOT translate a Rust snippet to TypeScript for the reader's convenience — the whitepaper documents this codebase, not a generic version of it.
- **A bare filename MAY be mentioned sparingly** when it helps the reader ("from `src/orchestration/heatmap.ts`"). Systematic `(file:line)` citations after nearly every claim MUST NOT appear — they read as noise, they drift out of sync with the code almost immediately, and a reader can't verify one just by looking at it anyway. File:line tracking belongs in the subagent return contracts you verify against (Step 3/4), not in the finished prose.
- **CLI/config examples** get their natural format: `bash` for commands, `json`/`yaml` for config files.
- **Real signatures SHOULD be preferred over paraphrase.** `parse<T extends Config>(path: string, options?: ParseOptions): Promise<T>` teaches more than "a generic parse function."

---

## Tables

Use tables for anything with parallel structure across rows — trade-off comparisons (mode A vs. mode B across several dimensions), rule catalogs, configuration schemas. A table with `Aspect | Option A | Option B` columns communicates a comparison faster than the equivalent prose ever will.

---

## Conclusion and Key Strengths

The conclusion is not a restatement of the abstract. It's a compressed synthesis: 3-6 enumerated points, each naming a specific architectural decision and why it mattered, not generic praise ("well-designed," "robust"). If the system has genuine limitations or trade-offs the design accepted, a conclusion that's honest about them is stronger than one that isn't — this is engineering documentation, not marketing.

---

## Appendices

This is where exhaustiveness belongs. Numbered sections SHOULD stay comparatively tight (a deep-dive section explains the pattern; it doesn't need to enumerate every field). Appendices MUST hold full, non-truncated, realistic worked examples — a complete dataset configuration, a complete orchestration config, a full usage example wired end-to-end. Realistic-looking data (real-shaped IDs, plausible field names) SHOULD be used rather than `foo`/`bar` placeholders; it reads as documentation of a real system rather than a toy.

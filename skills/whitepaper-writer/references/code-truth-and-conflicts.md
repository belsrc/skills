# Code Truth and Conflict Reconciliation

## Source Priority

When sources disagree, they MUST be resolved in this order:

1. **Code** — what actually executes, always wins
2. **OpenSpec `spec.md` files** — design intent, but specs describe what a change was proposed to do, not necessarily what the code still does months later
3. **Living docs** (`ARCHITECTURE.md`, `CONSTRAINTS.md`, etc.) — useful context, same staleness risk
4. **Existing README** — often the most-maintained doc but also the most likely to describe an earlier, simpler version of the system

This is not about ignoring docs — it's about what happens when they disagree. Most of the time they won't disagree, and the docs are exactly right; treat that as the common case, not the exception you're hunting for.

## Writing Up a Conflict

When you find one, you MUST NOT silently overwrite the doc's claim and move on — a conflict is often the most valuable single finding of the whole exploration, because it surfaces exactly the kind of drift that's expensive to rediscover later (a migration that's half-finished, a doc nobody updated after a refactor, a spec describing a design that got simplified during implementation). "Valuable to know about" and "belongs in the whitepaper" are two different things, though, and this is where it's easy to overcorrect.

Current behavior MUST be documented as the primary claim in the relevant section, in the normal flow of the prose, as if the conflict did not exist. That's the default outcome for nearly every conflict found — most of them are exactly this simple: document what the code does, and stop.

A dedicated header or subsection for drift — "Current doc drift," "Gaps," "Known discrepancies," anything in that shape — MUST NOT appear in the whitepaper. Not once, and not as a running feature under each subsystem section. If exploration turns up five conflicts across five subsystems, the correct number of drift *sections* in the document is zero, every time — see Step 8 in `SKILL.md` for where those five findings actually go (the conversational report to the user, not the file).

The narrow exception: where a specific conflict is genuinely load-bearing for understanding the subsystem itself — the reader would be confused or misled without knowing about it — it MAY be folded into the ordinary prose as a single sentence or clause, woven into the paragraph that's already explaining that behavior. Not a blockquote, not a bullet under its own mini-header, not a paragraph that exists only to discuss the conflict. For example, inside a paragraph that's already describing how filter composition works, one clause is enough:

> Filter composition treats either the constant or conditional filter as optional, defaulting to the other when one is absent — a deliberate relaxation of the stricter rule `ARCHITECTURE.md` still describes.

That's the ceiling, not a template to fill in per section. Most subsystems, even ones with a conflict behind them, should read as if reconciliation happened silently — because from the reader's point of view, it did. If you notice yourself writing a callout in more than one or two sections across the whole document, that's a signal you're treating "found a conflict" as license to write about it rather than as something to fold in only where the reader actually needs it.

## Citation Discipline

Every subagent MUST track file:line references while it explores — this is what makes the fixed-baseline docs-synthesis findings verifiable against what the other subagents found in code, and it's what Step 4's reconciliation runs on. This tracking is for you, the orchestrator, not for the reader.

**The finished whitepaper's prose MUST NOT carry systematic `(file:line)` citations.** A citation after nearly every sentence is not rigor, it's noise: a reader can't verify `sh/utils.sh:211-279` by looking at it, the range drifts out of sync with the code on the next refactor regardless of how careful anyone is, and a document where every claim is footnoted this way reads like a legal filing, not the reference examples this skill is modeled on. A bare filename, mentioned occasionally and only where it actually helps the reader find something ("the logic lives in `sh/utils.sh`"), is fine. A parenthetical line range after every clause is not, even though it looks precise — precision that immediately goes stale isn't precision, it's a promise the document can't keep.

What you MUST still be able to do: produce the citation if asked, and flag as unverified (rather than stated as fact) any claim you can't trace back to a specific place in the code. Neither of those requires putting the citation in the document.

## Tracking Conflicts for the User Report

Since conflicts mostly don't appear in the whitepaper itself, they need a home somewhere, or the work of finding them is wasted. Keep a running list as subagents report conflicts back to you during Step 3/4 — subsystem, what the doc/spec claimed, what the code actually does. This list is not part of the whitepaper; it's what Step 8 turns into a short summary in your conversational reply to the user once the document is presented.

## What "Last Touched By" Actually Tells You

If cross-referencing an OpenSpec `INDEX.md`, remember its `Last Touched By` column names the change proposal that last edited the *spec file* — it says nothing about when the code last changed. A spec last touched eight months ago sitting next to code that's been refactored twice since is exactly the kind of drift this reconciliation process exists to catch, not evidence the spec is current. Spec freshness and code freshness MUST be treated as two separate questions, and the code one MUST be answered by actually reading the code.

If cross-referencing an OpenSpec `INDEX.md`, remember its `Last Touched By` column names the change proposal that last edited the *spec file* — it says nothing about when the code last changed. A spec last touched eight months ago sitting next to code that's been refactored twice since is exactly the kind of drift this reconciliation process exists to catch, not evidence the spec is current. Spec freshness and code freshness MUST be treated as two separate questions, and the code one MUST be answered by actually reading the code.

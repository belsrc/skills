# engineering-council

A skill that convenes a small council of engineering personas to evaluate a technical decision from opposing viewpoints, then synthesizes where they agree and where they conflict.

The point is not a single answer. It is a legible map of the decision space, with the tradeoffs made explicit by people who would weigh them differently.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [What it does](#what-it-does)
- [Why it exists](#why-it-exists)
- [Invocation and modes](#invocation-and-modes)
- [How routing works](#how-routing-works)
- [Contracts](#contracts)
- [Output format](#output-format)
- [File layout](#file-layout)
- [Examples](#examples)
- [Extending the council](#extending-the-council)
- [Design invariants](#design-invariants)
- [Provenance](#provenance)

## Installation

```bash
npx skills add https://github.com/belsrc/skills --skill engineering-council
```

## Quick Start

Ask for a council review in plain language. The skill picks the members and runs them.

```
Should I rewrite this entity update loop to be data-oriented,
or is the object-per-entity version fine until it shows up in a profile?
```

The skill classifies that as a `performance-investigation` question, selects the `carmack vs muratori` pair, runs each persona in its own isolated subagent, and returns their positions plus the contested axis between them. Before it spawns anything it prints the routing decision, so you can see and override how the council was chosen:

```
Council: performance-investigation · duo
Members: carmack, muratori
Routed by: keyword
Why: matched anchors "profile", "data-oriented"
```

## What it does

The skill runs a request past several engineering personas, each modeled on the documented public philosophy of a well-known engineer (Knuth, Beck, Carmack, Lamport, Fowler, Schneier, Hickey, and others). Each persona reasons in isolation and returns a structured verdict. The orchestrator then diffs those verdicts to find the real disagreements and writes a synthesis that surfaces them rather than averaging them away.

Two interaction structures are available. A `duo` is a polarity pair (two opposing lenses, dialectical). A `triad` is three members chosen to cover distinct relevant domains (multi-perspective).

## Why it exists

A single model answering a hard design question tends to give you one confident take. The value you actually want on a contested call is the set of competing takes and the axis they disagree on, so you can decide with the tradeoff in view.

Three properties make this skill different from asking one model to "list some perspectives":

- **Isolation produces uncorrelated takes.** Each persona runs in its own subagent with only its own definition and the request. It never sees the others, so the personas do not converge or self-consciously over-contrast the way they do when one context role-plays all of them in sequence.
- **Routing is mostly deterministic.** Which members get picked is a table lookup, not a vibe. The only non-deterministic step is the topic classification, and that is keyword-first with a model fallback only when nothing matches.
- **Output is structured dissent, not a vote.** Forcing consensus manufactures false precision on questions whose honest answer is "it depends, and here is on what." The synthesis names the split.

Use it for hard architecture, performance, security, ML, context, agent, API, testing, refactoring, and distributed-systems calls. For a settled question with one correct answer, skip it and just ask.

## Invocation and modes

The skill parses intent from your message. You can steer it three ways, listed here in the order the skill resolves them.

| You do this | Routing branch | Determinism |
|-------------|----------------|-------------|
| Name members ("ask Knuth and Beck", "Carmack vs Muratori") | `explicit` | fully deterministic, skips classification |
| Name a topic ("run the optimization-decision council") | `explicit` | fully deterministic, table lookup |
| Just describe the problem | `keyword`, then `llm` fallback | keyword path is stable; fallback only when no anchor matches |

Mode defaults to `duo`. Say "triad" or name three members to get the three-perspective structure. Mode also changes which members are chosen, beyond the count: a duo is the polarity pair whose axis straddles the core tension, and a triad is three members spanning the relevant domains.

## How routing works

Routing runs in two layers so the decision is auditable after the fact.

```
request ──► [Layer 1: classify] ──► topic ──► [Layer 2: lookup] ──► members
              keyword-first,                      pure table,
              llm fallback                        deterministic
```

**Layer 2** is a literal lookup in `references/routing.md`. A topic plus a mode always yields the same member set. There is no model in this layer.

**Layer 1** picks the topic key. It scans the request for the anchor terms listed per topic and selects the highest-scoring topic. On a tie, a fixed precedence list (narrow, concrete topics above broad catch-alls) breaks it. The model only reasons over the closed set of 18 topic keys when no anchor term matches anything, and even then it cannot invent a topic outside the enum.

Every routing decision is echoed before any subagent runs, including a `routedBy` field recording which branch fired, so a flaky route is visible rather than silent.

The 18 topics:

```
architecture-review      distributed-systems       microservices-vs-monolith
security-audit           cryptography              performance-investigation
optimization-decision    ml-system-design          code-review
api-design               language-type-design      incident-response
production-debugging     refactoring-strategy      testing-strategy
context-engineering      agent-engineering         system-design-new-project
```

## Contracts

Two data shapes hold the system together. Both live in `SKILL.md` and follow the repo's TypeScript conventions (`type` over `interface`, no classes).

Every persona subagent returns this, and nothing else, so synthesis is mechanical rather than prose-parsing:

```typescript
type CouncilVerdict = "for" | "against" | "depends";

type PersonaResponse = {
  readonly member: string;             // canonical id, e.g. "knuth"
  readonly stance: string;             // the member's lens applied to the request
  readonly verdict: CouncilVerdict;
  readonly keyConcerns: readonly string[];
  readonly tradeoffsRaised: readonly string[];
  readonly recommendation: string;
};
```

The orchestrator resolves the council into this. It is pure once `routedBy` is `explicit` or `keyword`:

```typescript
type Mode = "duo" | "triad";

type Selection = {
  readonly topic: string;              // closed enum member from routing.md
  readonly mode: Mode;
  readonly members: readonly string[]; // from the static topic table
  readonly routedBy: "explicit" | "keyword" | "llm";
  readonly note: string;               // why this topic, for the echo
};
```

The orchestrator finds the contested axes by diffing `verdict` and `tradeoffsRaised` across the returned `PersonaResponse` objects, so disagreement is detected from the data, not guessed.

## Output format

```
## <topic> council · <mode>

### Positions
- **<Member>** (<verdict>): condensed stance plus recommendation
- ... one per member

### Where they agree
the shared ground, omitted if there is none

### Where they split
each contested axis, naming the tradeoff and which member sits on which side

### Reading
a synthesized recommendation when the evidence points one way, or an explicit
handoff: "the call hinges on <axis>; if you weight X over Y, go with <member>'s read"
```

A verdict tally appears only when the question is genuinely binary, and even then the split is shown.

## File layout

```
engineering-council/
├── SKILL.md                       orchestration: mode, selection, spawn, synthesis
├── README.md                      this file
└── references/
    ├── council.md                 roster (32 members) + 16 polarity pairs; read to route
    ├── routing.md                 Layer 2 topic table + tie-break precedence
    └── personas/                  32 persona prompts, one per member
        knuth.md  beck.md  carmack.md  muratori.md  lamport.md  vogels.md
        fowler.md  dhh.md  schneier.md  kaminsky.md  marlinspike.md  green.md
        martin.md  hickey.md  lecun.md  pearl.md  ng.md  chollet.md
        allspaw.md  majors.md  pike.md  hejlsberg.md  kay.md  torvalds.md
        ousterhout.md  abramov.md  karpathy.md  khattab.md  chase.md
        willison.md  husain.md  yao.md
```

`council.md` is lightweight and the orchestrator reads it on every run to route and to resolve a flex duo. A persona file is heavy and loads only inside the subagent assigned that member, which ties the token cost to the council size rather than the full roster of 32.

## Examples

**Deterministic keyword route, duo.**

```
Is it worth optimizing this hot loop that runs once per frame,
or am I optimizing prematurely?
```

Anchors "optimizing" and "prematurely" route to `optimization-decision`, spawning Knuth vs Beck. Knuth wants the profile and the asymptotic picture before touching anything; Beck wants a test and the simplest thing that ships. The split is measure-the-critical-3-percent against solve-the-problem-you-actually-have.

**Triad, broader phrasing.**

```
We're rebuilding the ingestion path and I want the performance
characteristics right from the start. Convene a triad.
```

The anchors lean `performance-investigation`, so the precedence list keeps it out of the broad `system-design-new-project` bucket, and the triad is Knuth, Carmack, Muratori.

**Explicit member pin.**

```
Carmack vs Muratori on whether to hand-roll this allocator.
```

Named members skip classification entirely. Fully deterministic.

## Extending the council

The skill is data, so extension is mostly editing reference files. After any change, run the consistency check at the end of this section.

**Add a persona.** Create `references/personas/<id>.md` from the shape every other persona uses: a Lens section, a "What you push on" section, a Voice section, and an Output block that emits a `PersonaResponse` with `"member": "<id>"`. Add a roster row to `references/council.md`. If the member should be selectable by routing, add them to a topic's `defaultDuo` or `defaultTriad`, and add a polarity pair if they have a natural opposite. Keep the file opponent-agnostic (see invariants).

**Add a topic.** Add a `### <topic>` block to `references/routing.md` with `anchors`, `defaultDuo`, and `defaultTriad`. Insert the topic into the tie-break precedence list at the position that matches its specificity (concrete topics sit above broad ones). Confirm every member you referenced has a persona file.

**Change routing only.** Edit the anchors or the precedence order in `routing.md`. Layer 2 stays a pure table, so do not introduce model judgment there.

Consistency check (every member named in the roster or routing must have a persona file):

```bash
cd engineering-council
grep -oE '^\| [a-z]+ +\|' references/council.md | tr -d '| ' | sort > /tmp/roster
ls references/personas | sed 's/.md//' | sort > /tmp/files
comm -23 /tmp/roster /tmp/files   # prints any roster id missing a persona file
```

## Design invariants

Preserve these when updating the skill. They are the load-bearing decisions, and breaking one quietly degrades the whole thing.

1. **Personas are opponent-agnostic.** A persona file never references a specific rival, because a member appears in several pairings (Carmack is in `performance-investigation` against Muratori and in `production-debugging` against Majors). Contrast is reconstructed at synthesis, never hardcoded in the persona.
2. **Layer 2 is a pure lookup.** Topic plus mode maps to members with no model in the loop. Keep classification confined to Layer 1.
3. **Referential integrity.** Every member named in `routing.md` or `council.md` has a persona file. Run the check above.
4. **Personas channel documented public philosophy**, framed as that philosophy applied to the request, with no fabricated quotes. This is both a courtesy to real people and a quality lever, since anchoring on documented positions keeps the lenses sharp.
5. **The `PersonaResponse` schema is the synthesis contract.** Change it and you must update the synthesis step in `SKILL.md` and the Output block in all 32 persona files together.
6. **House style.** No em dashes or en dashes anywhere; restructure instead. TypeScript uses `type` over `interface` and functions over classes.

## Acknowledgements

The idea for this skill came from the Council of High Intelligence project by 0xNyk: https://github.com/0xNyk/council-of-high-intelligence. That project convenes a council of personas to reason together, and this skill borrows the shape and points it at engineering decisions.

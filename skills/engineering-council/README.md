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
- [Discovery and grounding](#discovery-and-grounding)
- [Debate round](#debate-round)
- [Contracts](#contracts)
- [Output format](#output-format)
- [File layout](#file-layout)
- [Examples](#examples)
- [Extending the council](#extending-the-council)
- [Design invariants](#design-invariants)
- [Future additions](#future-additions)
- [Acknowledgements](#acknowledgements)

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

The skill classifies that as a `performance-investigation` question, selects the `carmack vs muratori` pair, runs each persona in its own isolated subagent, and returns their positions plus the contested axis between them. If you are in a repo and the question points at real code, it first runs a discovery pass to ground the council in what the code actually does. Before it spawns the council it prints the routing decision and what it read, so you can see and override both:

```
Council: performance-investigation · duo
Members: carmack, muratori
Routed by: keyword
Why: matched anchors "profile", "data-oriented"
Grounded: yes
Files read: src/entity/update.ts, bench/update.bench.ts
Brief: update loop allocates a new array per entity per frame; an
       existing benchmark covers it; no SoA layout in the codebase yet
Debate: on
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
- **Verdicts are grounded in the code, not just the prompt.** When you run it in a repo, a discovery pass reads the relevant files and hands every persona the same brief, so a take is anchored in what the tool actually does rather than in the wording of your question.

Use it for hard architecture, performance, security, ML, context, agent, API, testing, refactoring, and distributed-systems calls. For a settled question with one correct answer, skip it and just ask.

## Invocation and modes

The skill parses intent from your message. You can steer it three ways, listed here in the order the skill resolves them.

| You do this | Routing branch | Determinism |
|-------------|----------------|-------------|
| Name members ("ask Knuth and Beck", "Carmack vs Muratori") | `explicit` | fully deterministic, skips classification |
| Name a topic ("run the optimization-decision council") | `explicit` | fully deterministic, table lookup |
| Just describe the problem | `keyword`, then `llm` fallback | keyword path is stable; fallback only when no anchor matches |

Mode defaults to `duo`. Say "triad" or name three members to get the three-perspective structure. Mode also changes which members are chosen, beyond the count: a duo is the polarity pair whose axis straddles the core tension, and a triad is three members spanning the relevant domains.

Debate is an orthogonal flag, on by default and independent of mode. The rebuttal round runs unless you opt out ("no debate", "single round", "just the takes"), and it skips itself when round one is unanimous. It works with either a duo or a triad. See [Debate round](#debate-round) for what it does and what it costs.

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

## Discovery and grounding

When the skill runs in a repo and the question points at real code, it grounds the council in that code before anyone reasons. Discovery sits after routing, never before, so the cheap deterministic routing is never blocked on reading files.

It runs as a fan-out that mirrors the council. The orchestrator derives one to a few scoped questions from the request and the topic, spawns a discovery subagent per question, and each subagent reads a bounded set of files in its own context. Crucially, raw file contents stay inside those subagents. Only a structured finding comes back, and the orchestrator merges the findings into one lean brief. So no matter how much the discovery agents read, the orchestrator's context (the one that has to survive all the way to synthesis) never fills with file dumps.

```
[discover]  map: 1..n discovery subagents, each reads files in isolation
            reduce: merge findings ──► one lean RepoBrief
                                          │
                                          ▼
            every persona subagent receives the same brief
```

The topic seeds what discovery looks for, the same way it seeds member selection. An `api-design` discovery looks at the public surface and existing flags; a `performance-investigation` discovery looks for hot paths and benchmarks. The per-topic hints live at the bottom of `references/routing.md`.

Discovery is on by default. It fires when you are in a repo and the request implicates concrete artifacts (a named file, a command, a module, or a possessive like "this CLI tool"). It skips for abstract questions that repo state cannot change ("optimize early or late, in general"), and it degrades to text-only when there is no repo. To turn it off for one run, say so ("skip the repo", "just the principle"); to force it on a borderline question, ask it to ground the answer.

Each grounded persona carries a `groundedIn` list naming the repo facts its verdict leans on, and the synthesis tags each position as grounded or from principle. So a `carmack vs muratori` call on a data-oriented rewrite stops being abstract: Carmack's "show me the profile first" arrives next to the fact that a benchmark already exists, and Muratori's "do not pessimize" arrives next to the fact that the loop allocates per entity per frame.

One assumption worth stating: discovery feeds file contents to subagents, which is a prompt-injection surface if the repo holds untrusted material. For your own codebases that is a non-issue, so the skill assumes a trusted repo rather than defending against it.

## Debate round

By default the council runs two rounds. Round one is the isolated pass: each persona reasons alone, never seeing the others. Round two is the rebuttal: the orchestrator re-spawns each member with the others' round-one positions attached and asks it to engage them, concede a point that lands, sharpen a disagreement the others underweighted, or hold firm with a better argument. The synthesis then runs over round two and adds a "How positions moved" section, which is often the most informative part, since a persona changing its verdict after a specific counterargument tells you where the real hinge is.

Without the rebuttal, the personas never actually respond to each other and the synthesis can only reconstruct the contrast from juxtaposed first reactions. The debate round is what turns the council from parallel monologues into an argument, which is why it is on by default.

```
[council]  round one: N isolated persona subagents ──► PersonaResponse[]
   │
   ▼
[debate]   round two: re-spawn each member with the others' round-one
           positions ──► PersonaRebuttal[]                 (opt-in, capped at two rounds)
```

Two properties are kept deliberately. Isolation holds within each round: a round-two subagent sees the others' round-one outputs but never their live round-two reasoning, because they all run in parallel from the same round-one context, so the second pass stays uncorrelated. And it is capped at two rounds, because subagents cannot talk to each other (the orchestrator shuttles context between rounds, making round two serially dependent on round one and roughly doubling the cost to 2N calls), and a third round does not earn its keep.

It is on by default because the rebuttal is core to the result, not a luxury. Two cases skip it: opting out ("no debate", "single round") when you want a fast single-round read, and a unanimous round one, where there is no contested axis for a rebuttal to engage and the second pass would only burn calls.

## Contracts

The data shapes hold the system together. All of them live in `SKILL.md` and follow the repo's TypeScript conventions (`type` over `interface`, no classes).

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
  readonly groundedIn?: readonly string[]; // repo facts the verdict leans on; absent when not rooted
};
```

When a debate runs, each member returns this on the second pass instead, carrying the movement delta plus the final recommendation. Synthesis reads the post-debate position from it and still draws on the round-one `tradeoffsRaised` for the fuller axis picture:

```typescript
type PersonaRebuttal = {
  readonly member: string;
  readonly respondsTo: readonly string[];  // members whose points this answers
  readonly revisedVerdict: CouncilVerdict;  // may match round one or move
  readonly stance: string;                  // refined position after seeing the others
  readonly recommendation: string;          // final recommendation, which can change when moved
  readonly moved: boolean;                   // whether this persona changed its position
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

Discovery uses two more. Each discovery subagent returns a finding; the orchestrator folds the findings into one brief that every persona receives:

```typescript
type DiscoveryFinding = {
  readonly question: string;           // the scoped question this agent investigated
  readonly filesRead: readonly string[];
  readonly facts: readonly string[];   // concrete observations, each tied to a file
  readonly relevant: boolean;          // false when nothing bearing on the question was found
};

type RepoBrief = {
  readonly rooted: boolean;                // false when no repo, or discovery was skipped
  readonly filesRead: readonly string[];   // union across findings, echoed for audit
  readonly conventions: readonly string[]; // language, build tooling, existing patterns
  readonly summary: string;                // synthesis of the findings, not raw file dumps
};
```

The orchestrator finds the contested axes by diffing `verdict` and `tradeoffsRaised` across the returned `PersonaResponse` objects, so disagreement is detected from the data, not guessed.

## Output format

```
## <topic> council · <mode>

### Positions
- **<Member>** (<verdict>): condensed stance plus recommendation [grounded | from principle]
- ... one per member

### Where they agree
the shared ground, omitted if there is none

### Where they split
each contested axis, naming the tradeoff and which member sits on which side;
a split that turns on a repo fact is flagged as such

### How positions moved
debate only: for each member who shifted, what changed and the argument that
moved them, plus who held firm; omitted entirely when debate was off

### Reading
a synthesized recommendation when the evidence points one way, or an explicit
handoff: "the call hinges on <axis>; if you weight X over Y, go with <member>'s read"
```

A verdict tally appears only when the question is genuinely binary, and even then the split is shown. The grounded-or-from-principle tag appears only when discovery ran; with no brief, it is dropped. The movement section appears only when a debate ran.

## File layout

```
engineering-council/
├── SKILL.md                       orchestration: mode, selection, spawn, synthesis
├── README.md                      this file
└── references/
    ├── council.md                 roster (33 members) + 18 polarity pairs; read to route
    ├── routing.md                 Layer 2 topic table + tie-break precedence + discovery hints
    └── personas/                  33 persona prompts, one per member
        knuth.md  beck.md  carmack.md  muratori.md  lamport.md  vogels.md
        fowler.md  dhh.md  schneier.md  kaminsky.md  marlinspike.md  green.md
        martin.md  hickey.md  lecun.md  pearl.md  ng.md  chollet.md
        allspaw.md  majors.md  pike.md  hejlsberg.md  kay.md  torvalds.md
        ousterhout.md  abramov.md  karpathy.md  khattab.md  chase.md
        willison.md  husain.md  yao.md  dijkstra.md
```

`council.md` is lightweight and the orchestrator reads it on every run to route and to resolve a flex duo. A persona file is heavy and loads only inside the subagent assigned that member, which ties the token cost to the council size rather than the full roster of 33.

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

**Grounded run in a repo.**

```
Should this CLI save scan output to a file, or should users just redirect with > result.json?
```

Routes to `api-design` (Ousterhout vs Pike). Because the question names a concrete tool, discovery fires: a subagent reads the CLI entry point and finds it already writes only to stdout and imports no filesystem module, and another checks sibling subcommands for an existing `--output` flag. Both personas still land on "use redirection," but now Ousterhout's verdict carries `groundedIn: ["scan writes only to stdout", "no fs import in the scan path"]`, so the synthesis tags it grounded rather than argued in the abstract. Had discovery found an existing `--output` flag on a sibling command, the same unanimous call would instead surface a consistency split the text alone could not see.

**Debate by default.**

```
Should this service own its data, or share the existing database with the monolith?
```

Routes to `microservices-vs-monolith` (Fowler vs DHH), and the rebuttal pass runs without being asked. Round one gives the two positions in isolation. Round two re-spawns each with the other's round-one stance attached, so DHH gets to answer Fowler's evolvability argument directly and Fowler gets to answer DHH's "you do not have that scale problem yet." The synthesis adds a "How positions moved" section: if Fowler concedes that a shared database is fine until a concrete seam appears, that concession is the most useful line in the output, because it tells you the call hinges on whether that seam exists yet. Add "single round" to the request if you want the faster one-pass read instead.

## Extending the council

The skill is data, so extension is mostly editing reference files. After any change, run the consistency check at the end of this section.

**Add a persona.** Create `references/personas/<id>.md` from the shape every other persona uses: a Lens section, a "What you push on" section, a Voice section, and an Output block that emits a `PersonaResponse` with `"member": "<id>"`, including the `RepoBrief` preamble and the optional `groundedIn` field exactly as the other persona files have them. Add a roster row to `references/council.md`. If the member should be selectable by routing, add them to a topic's `defaultDuo` or `defaultTriad`, and add a polarity pair if they have a natural opposite. Keep the file opponent-agnostic (see invariants).

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
5. **The `PersonaResponse` schema is the synthesis contract.** Change it and you must update the synthesis step in `SKILL.md` and the Output block in all 33 persona files together. The `groundedIn` field is part of that schema, so the same rule applies to it. `PersonaRebuttal` (the debate round-two shape) is part of the synthesis contract too, but it is supplied by the orchestrator at round two and is not in the persona files.
6. **Discovery grounds, it does not route.** Discovery runs after routing and only feeds the personas evidence. Do not let it pick the topic or the members, since that would reintroduce the chicken-and-egg problem (you need the topic to scope discovery) and sacrifice the deterministic routing.
7. **Raw file content stays inside discovery subagents.** Only distilled `DiscoveryFinding` and `RepoBrief` data reaches the orchestrator. The whole point of the fan-out is to keep file dumps out of the context that has to survive to synthesis, so never paste file contents into the brief.
8. **Discovery is default-on with opt-out, and degrades gracefully.** Keep the trigger conditions (in a repo, request implicates concrete artifacts) and the no-repo and skip paths intact. Assume a trusted repo; if that assumption ever changes, the prompt-injection surface has to be addressed before discovery can be trusted on untrusted code.
9. **The debate round is on by default with opt-out, capped at two rounds, and isolated within a round.** It skips only on explicit opt-out or a unanimous round one. Round two sees only round-one outputs, never live round-two reasoning, so the second pass stays uncorrelated. The rebuttal format and the cross-persona context are supplied by the orchestrator at round two, never baked into the persona files, which keeps personas round-one and reusable.
10. **House style.** No em dashes or en dashes anywhere; restructure instead. TypeScript uses `type` over `interface` and functions over classes.

## Future additions

One extension was designed but deferred to keep the cost bounded. It is not implemented yet, and it is additive: it expands an existing fan-out rather than changing the pipeline, so it would not disturb what is in place. (The debate round, previously listed here, is now implemented; see [Debate round](#debate-round).)

### Per-persona discovery

Today discovery produces one centralized `RepoBrief` and every persona receives the same evidence. That is the right default and it keeps cost near one extra fan-out. But different lenses want different evidence, and a shared brief cannot anticipate all of them. Kaminsky wants the attack surface, Carmack wants the hot path, Willison wants to know whether the lethal trifecta lines up, Schneier wants the trust boundaries. A single brief either omits some of this or bloats trying to cover everyone.

Per-persona discovery gives each persona its own scoped pass on top of the shared brief. The elegant part is that the seed already exists: a persona's "What you push on" section is exactly the list of things that lens should go looking for in the repo, so the per-persona discovery questions can be derived from the persona file itself rather than authored separately. The recommended shape is a hybrid, not a replacement: keep the centralized brief as the shared baseline, and let each persona request a small lens-specific supplement on top. That bounds the cost to a thin per-persona delta rather than a full N-times multiplication of discovery, and it keeps the shared facts shared.

Two contracts for the supplement, not yet implemented:

```typescript
// not yet implemented
type LensQuery = {
  readonly member: string;
  readonly questions: readonly string[];   // derived from the persona's "What you push on"
};

type LensBrief = {
  readonly member: string;
  readonly filesRead: readonly string[];
  readonly facts: readonly string[];       // lens-specific findings, on top of the shared RepoBrief
};
```

Scope this to the topics that actually benefit rather than running it always. Audit-type and diagnostic topics (`security-audit`, `production-debugging`, `performance-investigation`) are where lenses diverge most in what they need to see; for a clean api-design question the shared brief is usually enough. Cost and reproducibility are the tradeoffs, since each supplement is another model-driven read, so the per-persona pass should stay opt-in or topic-gated.

Why deferred: the centralized brief delivers grounding at roughly one extra pass and matches the token-economy goals of v1. Per-persona discovery is the depth lever for audits, worth adding once there is a real audit workload to justify the extra reads.

## Acknowledgements

The idea for this skill came from the Council of High Intelligence project by 0xNyk: https://github.com/0xNyk/council-of-high-intelligence. That project convenes a council of personas to reason together, and this skill borrows the shape and points it at engineering decisions.

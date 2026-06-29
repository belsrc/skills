---
name: engineering-council
description: Convene a council of engineering personas (Knuth, Beck, Carmack, Lamport, Fowler, Schneier, Hickey, and more) to evaluate a technical decision from opposing viewpoints, then synthesize where they agree and where they conflict. Use this whenever the user wants multiple expert perspectives on a hard call, a design or architecture review, a debate between schools of thought, a tradeoff analysis, or says "engineering council", "council", "duo", "triad", or "what would X think". Trigger even when the user does not name the skill but is weighing a difficult architecture, performance, security, ML, API, testing, refactoring, or distributed-systems decision and would benefit from contrasting expert takes rather than a single answer.
---

# Engineering Council

Convene a small council of engineering personas, get an independent take from each, then synthesize the agreements and the live disagreements. The value is the tension between opposing but valid viewpoints, so the goal is never a forced consensus. It is a legible map of the decision space.

## How it works

The skill runs in two layers so the routing is auditable:

```
request ──► [Layer 1: classify] ──► topic ──► [Layer 2: lookup] ──► members
              keyword-first,                      pure table,
              llm fallback                        deterministic
```

Layer 2 is a literal lookup in `references/routing.md`: a topic plus a mode always yields the same member set. Layer 1 picks the topic, and it is keyword-first so the common path is reproducible. The model only reasons over the closed topic enum when no anchor terms match.

Selection is then run through three independent isolated subagents (one per member), so each persona reasons from a clean context anchored only on its own definition and the request. That isolation is the whole point: it produces uncorrelated takes instead of personas that have read each other and converged.

## Step 1: Determine the mode

Default is `duo` (a polarity pair, dialectical, two opposing lenses). Use `triad` (three members, multi-perspective) when the user asks for it, names three members, or the request clearly spans more than one domain.

A duo is not just "two members". It is the polarity pair whose axis straddles the core tension of the request. A triad is three members chosen to cover distinct relevant domains. Mode therefore changes *which* members get picked, not only how many.

## Step 2: Select the members

Resolve selection in this precedence order. The first match wins. Record which branch fired as `routedBy`.

1. **explicit members** (`routedBy: "explicit"`). The user named specific members ("ask Knuth and Beck", "Carmack vs Muratori on this"). Use exactly those. Skip classification entirely. Fully deterministic.
2. **explicit topic** (`routedBy: "explicit"`). The user named a topic key ("run the optimization-decision council"). Look it up in `references/routing.md`. Fully deterministic.
3. **keyword route** (`routedBy: "keyword"`). Scan the request for the anchor terms listed per topic in `references/routing.md`. Score each topic by anchor hits. Pick the highest. On a tie, use the precedence order at the bottom of `routing.md` (more specific topic wins). This is the intended common path and is stable.
4. **llm fallback** (`routedBy: "llm"`). Only when no anchor term matched anything. Choose the single best-fit topic from the closed enum in `routing.md`. Do not invent a topic outside the enum.

Once you have the topic, read the member set from the table: `defaultDuo` for duo mode, `defaultTriad` for triad mode. For the few topics whose duo is marked *flex*, pick the polarity pair from `references/council.md` whose axis best matches the request, and say so in the note.

## Step 3: Echo the selection before spawning

This is the audit gate. Print the resolved selection so the user can see and override how the council was chosen, then proceed without waiting unless the user objected on a prior turn.

```
Council: <topic> · <mode>
Members: <member list>
Routed by: <explicit | keyword | llm>
Why: <one line>
```

The `routedBy` field is the thing that makes a routing decision inspectable after the fact, so never omit it.

## Step 4: Spawn the council

Launch one subagent per selected member, all in the same turn so they run in parallel and isolated. Give each subagent exactly three things and nothing else:

1. an instruction to read `references/personas/<member>.md` and adopt it,
2. the user's request verbatim,
3. the instruction to return only a `PersonaResponse` JSON object (schema below), no prose around it.

Do not let a subagent see another member's response. The isolation is what keeps the takes uncorrelated.

## Step 5: Synthesize with structured dissent

Collect the `PersonaResponse` objects and produce the output below. Surface disagreement, do not vote it away. Diff the `verdict` and `tradeoffsRaised` fields across members to find the contested axes mechanically, rather than guessing where they disagree.

Use this exact structure:

```
## <topic> council · <mode>

### Positions
- **<Member>** (<verdict>): <one to two line condensation of stance + recommendation>
- ... one bullet per member

### Where they agree
<the shared ground, if any. omit the section if there is none>

### Where they split
<the contested axes. for each, name the tradeoff and which member sits on which side. this is the heart of the output>

### Reading
<either a synthesized recommendation when the evidence points one way, or an explicit handoff: "the call hinges on <axis>; if you weight <X> over <Y>, go with <member>'s read.">
```

Only produce a single verdict tally when the question is genuinely binary, and even then show the split.

## The persona response contract

Every subagent returns this shape. Fixing the schema makes synthesis mechanical instead of prose-parsing.

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

The selection itself follows this shape, which is pure once `routedBy` is `explicit` or `keyword`:

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

## Reference files

- `references/council.md` is the roster and the polarity pairs. It is lightweight and you read it to route and to resolve a *flex* duo. Read it first.
- `references/routing.md` is the unified topic table: anchor terms, `defaultDuo`, `defaultTriad`, and the tie-break precedence list. This is Layer 2.
- `references/personas/<member>.md` is the heavy persona prompt. A persona file loads only inside the subagent assigned that member, which keeps the token budget tied to the council size rather than the full roster.

## Guardrails

Each persona channels the documented public engineering philosophy of a real person. Frame their takes as that philosophy applied to the request, not as claims about what the individual privately believes, and do not fabricate quotes. Staying anchored on documented positions also makes the personas sharper, so this is a quality lever as much as a courtesy.

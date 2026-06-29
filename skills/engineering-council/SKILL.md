---
name: engineering-council
description: Convene a council of engineering personas (Knuth, Beck, Carmack, Lamport, Fowler, Schneier, Hickey, and more) to evaluate a technical decision from opposing viewpoints, then synthesize where they agree and where they conflict. Use this whenever the user wants multiple expert perspectives on a hard call, a design or architecture review, a debate between schools of thought, a tradeoff analysis, or says "engineering council", "council", "duo", "triad", or "what would X think". Trigger even when the user does not name the skill but is weighing a difficult architecture, performance, security, ML, API, testing, refactoring, or distributed-systems decision and would benefit from contrasting expert takes rather than a single answer.
---

# Engineering Council

Convene a small council of engineering personas, get an independent take from each, then synthesize the agreements and the live disagreements. The value is the tension between opposing but valid viewpoints, so the goal is never a forced consensus. It is a legible map of the decision space.

## How it works

Routing is deterministic and text-only. Discovery and the council are two map-reduce stages over isolated subagents.

```
request
   │
   ▼
[route]  Layer 1 classify ──► topic ──► Layer 2 lookup ──► members      deterministic
   │
   ▼
[discover]  map: 1..n discovery subagents read files in their own context
            reduce: merge findings into one lean RepoBrief                grounds the council
   │
   ▼
[echo]  selection + brief + files read                                   audit gate
   │
   ▼
[council]  map: one persona subagent per member, given the RepoBrief
           reduce: synthesize positions, agreements, splits               uncorrelated takes
```

Routing runs in two layers so it stays auditable. Layer 2 is a literal lookup in `references/routing.md`: a topic plus a mode always yields the same member set. Layer 1 picks the topic, keyword-first so the common path is reproducible, with the model reasoning over the closed topic enum only when no anchor terms match.

Both fan-outs use isolated subagents on purpose. In discovery, raw file contents live and die inside the discovery subagents, so only distilled findings reach the orchestrator and the council never holds file dumps. In the council, each persona reasons from a clean context anchored on its own definition, the request, and the shared brief, which produces uncorrelated takes instead of personas that have read each other and converged.

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

## Step 3: Discover repo context (centralized brief)

Discovery grounds the council in the actual codebase instead of only the request text. It is on by default. It runs when both hold: the skill is running inside a repo, and the request implicates concrete artifacts (a named file, command, or module, or a possessive such as "this CLI tool" or "our auth module"). It skips automatically for abstract questions whose answer repo state cannot change ("optimize early or late, in general"), and it degrades to text-only when there is no repo.

Triggering and overrides:

- **Default on** under the conditions above. Set `rooted: true` on the brief.
- **Opt out.** If the user asks to skip grounding ("no discovery", "just the principle", "skip the repo"), set `rooted: false` and reason from the request alone.
- **Force on.** If the user asks to ground it, run discovery even for a borderline-abstract request.
- **No repo, or nothing relevant found.** Set `rooted: false` (no repo) or `rooted: true` with a summary that says nothing bearing on the question was found, so the personas know they are reasoning from text.

How discovery runs, as map-reduce:

1. **Derive 1 to n scoped questions** from the request and the topic. Default to one question for a focused request. Fan out only when the request has separable facets ("does the tool already persist output?" and "is there an existing output flag elsewhere?" are two). Cap at 4. Use the topic's discovery hints in `references/routing.md` to seed what to look for, the same way the topic seeds member selection.
2. **Spawn one discovery subagent per question**, in parallel and isolated. Each reads a bounded set of files in its own context (cap each at a few files), and returns a `DiscoveryFinding`. Raw file contents stay inside the subagent; only the finding returns.
3. **Merge the findings into one lean `RepoBrief`.** Union `filesRead`, collect `conventions`, and synthesize the `facts` into `summary`. Do not paste raw file contents into the brief. The brief is what the council acts on, not a mirror of the tree.

Keep discovery scoped. The failure mode is a brief that balloons the context, which the fan-out prevents only if each subagent returns findings rather than file dumps.

Assume the repo is trusted. Feeding file contents to subagents is a prompt-injection surface if the repo holds untrusted material; for v1 that assumption is stated, not defended.

## Step 4: Echo the selection before spawning

This is the audit gate. Print the resolved selection and the discovery brief so the user can see and override both how the council was chosen and what it was grounded in, then proceed without waiting unless the user objected on a prior turn.

```
Council: <topic> · <mode>
Members: <member list>
Routed by: <explicit | keyword | llm>
Why: <one line>
Grounded: <rooted ? "yes" : "no">
Files read: <files, or "none (reasoning from the request)">
Brief: <one to three line summary, or "n/a">
```

The `routedBy` field makes the routing inspectable; the files-read line makes the grounding inspectable, so a mis-scoped discovery is visible rather than silent. Never omit either.

## Step 5: Spawn the council

Launch one subagent per selected member, all in the same turn so they run in parallel and isolated. Give each subagent exactly these things and nothing else:

1. an instruction to read `references/personas/<member>.md` and adopt it,
2. the user's request verbatim,
3. the shared `RepoBrief`,
4. the instruction to return only a `PersonaResponse` JSON object (schema below), no prose around it.

When the brief is `rooted`, the persona applies its lens to that evidence and not only the request text, and lists the specific repo facts its verdict leans on in `groundedIn`. When it is not rooted, the persona reasons from the request and omits `groundedIn`.

Do not let a subagent see another member's response. The isolation is what keeps the takes uncorrelated. Every persona gets the same brief, so the only thing that differs between them is the lens.

## Step 6: Synthesize with structured dissent

Collect the `PersonaResponse` objects and produce the output below. Surface disagreement, do not vote it away. Diff the `verdict` and `tradeoffsRaised` fields across members to find the contested axes mechanically, rather than guessing where they disagree. When members carry `groundedIn`, note where a position leans on a repo fact, and when a split turns on a repo fact rather than pure principle, say so, because that is the disagreement most worth the reader's attention.

Use this exact structure:

```
## <topic> council · <mode>

### Positions
- **<Member>** (<verdict>): <one to two line condensation of stance + recommendation> [grounded | from principle]
- ... one bullet per member

### Where they agree
<the shared ground, if any. omit the section if there is none>

### Where they split
<the contested axes. for each, name the tradeoff and which member sits on which side. flag any split that turns on a repo fact. this is the heart of the output>

### Reading
<either a synthesized recommendation when the evidence points one way, or an explicit handoff: "the call hinges on <axis>; if you weight <X> over <Y>, go with <member>'s read.">
```

Only produce a single verdict tally when the question is genuinely binary, and even then show the split. Mark each position as grounded or from principle only when discovery ran; with no brief, drop the tag.

## The contracts

Every persona subagent returns this shape. Fixing the schema makes synthesis mechanical instead of prose-parsing.

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

The selection follows this shape, which is pure once `routedBy` is `explicit` or `keyword`:

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

Each discovery subagent returns a finding, so the merge into a brief is mechanical:

```typescript
type DiscoveryFinding = {
  readonly question: string;           // the scoped question this agent investigated
  readonly filesRead: readonly string[];
  readonly facts: readonly string[];   // concrete observations, each tied to a file
  readonly relevant: boolean;          // false when nothing bearing on the question was found
};
```

The orchestrator folds the findings into one lean brief that every persona subagent receives. The raw `DiscoveryFinding[]` stays with the orchestrator for the echo; the personas get only this:

```typescript
type RepoBrief = {
  readonly rooted: boolean;                // false when no repo, or discovery was skipped
  readonly filesRead: readonly string[];   // union across findings, echoed for audit
  readonly conventions: readonly string[]; // language, build tooling, existing patterns
  readonly summary: string;                // synthesis of the findings, not raw file dumps
};
```

## Reference files

- `references/council.md` is the roster and the polarity pairs. It is lightweight and you read it to route and to resolve a *flex* duo. Read it first.
- `references/routing.md` is the unified topic table: anchor terms, `defaultDuo`, `defaultTriad`, the tie-break precedence list, and the per-topic discovery hints that tell discovery what to look for. This is Layer 2.
- `references/personas/<member>.md` is the heavy persona prompt. A persona file loads only inside the subagent assigned that member, which keeps the token budget tied to the council size rather than the full roster.

## Guardrails

Each persona channels the documented public engineering philosophy of a real person. Frame their takes as that philosophy applied to the request, not as claims about what the individual privately believes, and do not fabricate quotes. Staying anchored on documented positions also makes the personas sharper, so this is a quality lever as much as a courtesy.

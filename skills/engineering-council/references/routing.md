# Routing table (Layer 2)

A topic plus a mode is a pure lookup into this table. Same inputs, same members, every time. Layer 1 only has to pick the topic key; everything below is fixed.

Each topic lists:
- **anchors**: terms that, if present in the request, score a hit for this topic. Keyword routing picks the topic with the most hits.
- **defaultDuo**: the polarity pair for `duo` mode.
- **defaultTriad**: the three members for `triad` mode.

## Topics

### architecture-review
- anchors: architecture, design decision, system design review, layering, boundaries, ADR, module boundaries, coupling, structure
- defaultDuo: fowler vs dhh
- defaultTriad: fowler, dhh, lamport

### distributed-systems
- anchors: distributed, consensus, replication, partition, consistency, CAP, quorum, eventual consistency, leader election, raft, paxos
- defaultDuo: lamport vs vogels
- defaultTriad: lamport, vogels, hickey

### microservices-vs-monolith
- anchors: microservices, monolith, service boundaries, split the service, decompose, extract a service, service mesh, bounded context
- defaultDuo: fowler vs dhh
- defaultTriad: dhh, vogels, fowler

### security-audit
- anchors: security, threat, vulnerability, attack surface, audit, exploit, authentication, authorization, injection, hardening, pentest
- defaultDuo: schneier vs kaminsky
- defaultTriad: schneier, kaminsky, marlinspike

### cryptography
- anchors: crypto, cryptography, encryption, cipher, key exchange, TLS, signature, protocol, AEAD, nonce, KDF, zero knowledge
- defaultDuo: marlinspike vs green
- defaultTriad: green, marlinspike, schneier

### performance-investigation
- anchors: performance, latency, throughput, slow, profiling, hot path, bottleneck, allocation, cache miss, p99, regression
- defaultDuo: carmack vs muratori
- defaultTriad: knuth, carmack, muratori

### optimization-decision
- anchors: optimize, premature optimization, micro-optimization, worth optimizing, should I optimize, tune, is it fast enough, speed this up
- defaultDuo: knuth vs beck
- defaultTriad: knuth, beck, carmack

### ml-system-design
- anchors: model, training, machine learning, neural network, dataset, inference, embedding, fine-tune, scale the model, ML pipeline, causal
- defaultDuo: ng vs chollet
- defaultTriad: ng, chollet, pearl

### context-engineering
- anchors: context window, prompt, prompting, system prompt, RAG, retrieval, few-shot, in-context, skill, memory, token budget, context compression, instructions
- defaultDuo: karpathy vs khattab
- defaultTriad: karpathy, khattab, husain

### agent-engineering
- anchors: agent, agentic, harness, tool use, tool calling, orchestration, multi-agent, subagent, agent loop, ReAct, autonomy, workflow, MCP, scaffolding
- defaultDuo: chase vs willison
- defaultTriad: chase, willison, yao

### code-review
- anchors: code review, pull request, PR, readability, clean code, code smell, review this function, naming, maintainability
- defaultDuo: martin vs hickey
- defaultTriad: martin, hickey, beck

### api-design
- anchors: API, interface, library design, public surface, SDK, contract, endpoint design, method signature, ergonomics
- defaultDuo: ousterhout vs abramov
- defaultTriad: ousterhout, abramov, pike

### language-type-design
- anchors: type system, language design, generics, type safety, DSL, syntax, type inference, expressiveness, sum types
- defaultDuo: pike vs hejlsberg
- defaultTriad: pike, hejlsberg, hickey

### incident-response
- anchors: incident, outage, postmortem, on-call, retrospective, root cause, blameless, pager, SLA breach
- defaultDuo: allspaw vs majors
- defaultTriad: allspaw, majors, vogels

### production-debugging
- anchors: debug, debugging, reproduce, heisenbug, trace, intermittent, why is this failing, flaky, cannot reproduce, instrument
- defaultDuo: majors vs carmack
- defaultTriad: majors, kaminsky, carmack

### refactoring-strategy
- anchors: refactor, restructure, technical debt, cleanup, untangle, legacy code, rewrite, extract, simplify this
- defaultDuo: martin vs hickey
- defaultTriad: fowler, beck, martin

### testing-strategy
- anchors: testing, tests, TDD, coverage, unit test, integration test, property-based, verify, mock, test strategy
- defaultDuo: beck vs lamport
- defaultTriad: beck, martin, lamport

### system-design-new-project
- anchors: new project, greenfield, from scratch, starting a, design a system, build a new, clean slate, initial architecture
- defaultDuo: kay vs torvalds (flex)
- defaultTriad: lamport, beck, vogels

## Tie-break precedence

When two topics score equally on keyword hits, the more specific topic wins. Resolve ties by the first match in this order:

1. cryptography
2. optimization-decision
3. performance-investigation
4. production-debugging
5. incident-response
6. microservices-vs-monolith
7. distributed-systems
8. security-audit
9. api-design
10. language-type-design
11. testing-strategy
12. code-review
13. refactoring-strategy
14. context-engineering
15. agent-engineering
16. ml-system-design
17. architecture-review
18. system-design-new-project

The rationale: narrow, concrete topics (a crypto question, an "is this worth optimizing" question, a context-window or agent-harness question) sit above broad catch-alls (architecture-review, system-design-new-project), so a specific request does not get swallowed by a general bucket. The two AI-application topics sit above ml-system-design so a question about prompts, context, or agent harnesses does not route into the classical-ML bucket.

## Discovery hints

When discovery runs (see Step 3 in `SKILL.md`), the topic seeds what to look for in the repo. These are starting points for the scoped questions, not a fixed checklist. Discovery stays bounded regardless.

| topic | look for |
|-------|----------|
| architecture-review | module boundaries, dependency directions, where layering is enforced or violated |
| distributed-systems | shared state, retry/timeout/idempotency handling, consistency assumptions |
| microservices-vs-monolith | current service or module boundaries, shared data stores, the deployment unit |
| security-audit | input handling, auth checks, trust boundaries, where untrusted data flows |
| cryptography | which primitives and libraries are used, key handling, custom vs standard constructions |
| performance-investigation | hot paths, loops over large data, allocations, existing benchmarks |
| optimization-decision | whether the code is on a hot path, any benchmark, current complexity |
| ml-system-design | the data pipeline, the eval or metric, the model and training setup |
| code-review | the function or module under review, its tests, surrounding conventions |
| api-design | the public surface, existing signatures and flags, call sites, consistency with siblings |
| language-type-design | existing type definitions, generic usage, how the surface is typed |
| incident-response | relevant logs or runbooks, recent changes, error handling around the failure |
| production-debugging | the failing path, instrumentation present, reproduction conditions |
| refactoring-strategy | the target code, its tests, coupling and call sites |
| testing-strategy | existing tests, coverage gaps, test tooling and patterns |
| context-engineering | how prompts and context are assembled, retrieval or memory, token budgeting |
| agent-engineering | the agent loop, tool definitions, orchestration and state, trust boundaries |
| system-design-new-project | existing scaffolding, the chosen stack and conventions, stated constraints |

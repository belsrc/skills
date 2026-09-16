---
name: human-english
description: |
  Write or rewrite text so it reads as clear and human, not AI slop. Merges
  ASD-STE100 Simplified Technical English (structural rules: sentence
  limits, one-word-one-meaning, active voice, approved modals,
  condition-before-command) with a catalog of AI-writing tells (inflated
  significance, promotional puffery, vague attribution, AI vocabulary,
  rule-of-three, em-dash/boldface overuse, sycophancy, filler, hedging).
  STE governs technical text: docs, READMEs, runbooks, error messages,
  release notes, incident reports, API guides, agent instructions
  (AGENTS.md, prompts, skills). For blog posts, marketing, essays, and
  other narrative prose, where STE does not apply, only the content-pattern
  catalog and voice guidance apply. Use for "de-slop", "humanize this",
  "make this sound human", "STE", "Simplified Technical English",
  "ASD-STE100", "write for non-native readers", "remove AI patterns/tells",
  or any request to check or rewrite AI-sounding text.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
compatibility: claude-code cursor codex gemini-cli opencode
metadata:
  version: 1.0.1
  standard: ASD-STE100 Issue 9 (2025-01-15)
  merged-from: simple-english v1.0.0 (structural precedence), humanizer v2.1.1 (content-pattern layer)
---

# STE + Humanizer: Write Like an Aerospace Manual, Not Like a Chatbot

This skill merges two approaches to the same problem — text that reads as machine-generated.

**Simplified Technical English (ASD-STE100)** is the controlled language aerospace and defense manufacturers use for maintenance documentation. Its rules exist so a tired reader who is not a native English speaker cannot misread an instruction: short sentences, one meaning per word, active voice, approved modals, condition before command.

**The content-pattern catalog** (originally the `humanizer` skill) targets the specific tells of LLM-generated prose: inflated significance, promotional language, vague attributions, rule-of-three padding, em-dash overuse, sycophantic tone, and more — cataloged from Wikipedia's "Signs of AI writing" project.

Both remove the same broad family of problems (long sentences, synonym rotation, hedges, filler, decorative clauses), so they combine cleanly almost everywhere. Where they genuinely disagree, **STE's structural rules win, and only within STE's own declared scope.** See Precedence below.

## Precedence

STE's own Limits section (near the end of this file) states it applies to technical facts and instructions, not to marketing copy, blog voice, or brand writing, because it deletes persuasion by design. That line is the exact boundary this merge uses:

- **Inside STE's scope** (technical/procedural/descriptive text — docs, runbooks, error messages, reports, agent instructions): if a content-pattern fix would violate a structural rule, the structural rule wins. Concretely: no contractions even if it reads warmer without STE (Rule 4.2), no first-person opinion injection, no deliberately varied "punchy then meandering" rhythm past the word ceiling, no banned modals for hedging (Section on modals below), no digressions or "let some mess in" (Rule 4.1, one topic per paragraph). The content-pattern catalog's diagnostic value — *this phrase is filler, this claim is vague, this is a formulaic frame* — still applies; only the "add first-person soul" remedy is out of scope here.
- **Outside STE's scope** (blog posts, marketing, essays, narrative, brand voice — anything STE itself disclaims): the content-pattern catalog applies in full, including the voice-injection guidance in `references/voice-mode.md`. Nothing here overrides that, because STE was never claiming that territory.

If you are unsure which side a passage falls on, classify it the way Step 1 below does: procedural or descriptive means STE governs; if it's neither (it's persuasive, personal, or literary), it's Voice mode.

## Your Task

1. **Select the mode**: Pragmatic, Strict, or Voice (below).
2. **Pragmatic/Strict only** — classify each passage as procedural or descriptive. Every structural rule below depends on this.
3. **Fix your vocabulary before drafting.** Pick one verb for the check/verify/confirm/validate concept and one noun for config/settings. Use no other word for these concepts in the whole document. See `references/vocabulary.md` for the full substitution table.
4. **Apply the structural rules** from the catalog below (Pragmatic/Strict) or skip straight to content patterns (Voice).
5. **Scan for content patterns** (CP-1 through CP-15, below) in every mode. See `references/patterns.md` for full before/after examples of each.
6. **Voice mode only** — apply `references/voice-mode.md` to add personality back in.
7. **Run the self-check** before you deliver. Not optional. Full checklist in `references/checklist.md`.
8. **Never touch code**, identifiers, commands, or quoted errors (Untouchables, below) in any mode.

When asked to CHECK text instead of writing it, report each violation as: rule or pattern ID, the offending text, a compliant rewrite. Cite only IDs that exist in this file or its references — do not invent rule numbers.

## Three Modes

| Mode | When | What governs |
|---|---|---|
| **Pragmatic** (default) | Docs, READMEs, error messages, release notes, incident reports, runbooks, agent instructions — the user wants clear technical text | Sections 1-9 structural rules + content-pattern catalog. Domain words stay ("idempotent", "webhook"). |
| **Strict** | User names STE, ASD-STE100, or compliance | Pragmatic + full vocabulary discipline, and tell the user full compliance needs the official dictionary (free at asd-ste100.org). |
| **Voice** | The text is blog, marketing, essay, narrative, or brand voice — content STE explicitly excludes — or the user asks to "humanize" non-technical prose | Content-pattern catalog only, no sentence-count ceiling, no banned-modal list, no contraction ban. Apply `references/voice-mode.md` for personality. |

## Step 1: Classify the Text (Pragmatic / Strict only)

| | Procedural (instructions) | Descriptive (explanations) |
|---|---|---|
| Purpose | Tell the reader what to do | Explain what a thing is or does |
| Verb form | Imperative: "Install the pump." | Simple present/past/future |
| Sentence limit | **20 words** (Rule 5.1) | **25 words** (Rule 6.3) |
| Unit rule | One instruction per sentence (5.2) | One topic per paragraph (6.5), max six sentences per paragraph (6.6) |

Do not mix the two in one passage. A "Getting started" section is procedural. An "Architecture" section is descriptive. A note inside a procedure is descriptive (25-word limit, no imperative). Neither is Voice mode.

## THE STRUCTURAL RULE CATALOG (Pragmatic / Strict)

53 rules in 9 sections, paraphrased from ASD-STE100 Issue 9 with software examples. The official wording is in the free standard at asd-ste100.org.

### Section 1 — Words (Rules 1.1-1.14)

| Rule | Instruction |
|---|---|
| 1.1 | Use only approved words, technical nouns, or technical verbs. |
| 1.2 | Use an approved word only as its listed part of speech. |
| 1.3 | Use an approved word only with its approved meaning. |
| 1.4 | Use only the approved forms of verbs and adjectives. |
| 1.5 | You can use domain words as technical nouns ("webhook", "commit", "endpoint"). |
| 1.6 | Use an unapproved word only when it is a technical noun or part of one. |
| 1.7 | Do not use technical nouns as verbs. |
| 1.8 | Use the technical nouns of your project or industry. |
| 1.9 | When you pick a technical noun, pick a short and clear one. |
| 1.10 | No regional, slang, or jargon words as technical nouns. |
| 1.11 | One item, one name. Do not call it "config" here and "settings" there. |
| 1.12 | You can use domain verbs as technical verbs ("deploy", "compile", "merge"). |
| 1.13 | Do not use technical verbs as nouns. |
| 1.14 | Use American English spelling. |

In pragmatic mode, rules 1.5, 1.8, and 1.12 do the heavy lifting: your domain vocabulary is legal. The ones agents break are 1.7, 1.11, and 1.13. Rule 1.11 also kills CP-10 below (synonym cycling) for free — one name per item leaves no room for elegant variation.

**Before:** You can webhook the event, then do a deploy.
**After:** Send the event to the webhook. Then deploy the service.

### Section 2 — Multi-word nouns (Rules 2.1-2.2)

| Rule | Instruction |
|---|---|
| 2.1 | Write multi-word nouns of three words or fewer. |
| 2.2 | When a technical noun needs more than three words, write it in full once, then give a short form or hyphenate the units. |

Break long noun chains with prepositions (of, on, in, for):

**Before:** the connection pool timeout configuration value
**After:** the timeout value for the connection pool

### Section 3 — Verbs (Rules 3.1-3.7)

| Rule | Instruction |
|---|---|
| 3.1 | Use only the verb forms that the dictionary gives. |
| 3.2 | Use only: infinitive, imperative, simple present, simple past, simple future, past participle as adjective. |
| 3.3 | Use the past participle only as an adjective ("the cached response"). |
| 3.4 | No auxiliary verbs for complex constructions. No present perfect, no "is to be installed". |
| 3.5 | Use an "-ing" form only as a technical noun or inside one ("logging", "the mounting bracket") — never as a verb, and never tacked onto a sentence as a fake-depth clause (CP-3). |
| 3.6 | Active voice. In descriptive text, passive is legal only when the agent is unknown. |
| 3.7 | Describe an action with a verb, not a noun ("compress the file", not "perform compression of the file"). |

**Approved modals: can, will, must. Banned: should, would, may, might, could.**
The standard rejects "could" even for possibility: write "an explosion can occur", never "could occur". For "should": a requirement becomes "must"; a suggestion is stated as fact or deleted. This subsumes the content catalog's hedging pattern (originally its own item, "excessive hedging") — "It could potentially possibly be argued that..." fails on banned modals before it fails on anything else. Fix both at once with the modal ladder below.

| You wrote | Write instead |
|---|---|
| should (requirement) | must |
| should (recommendation) | Delete it, or state it as fact: "X is better because Y." |
| may / might / could (possibility) | can |
| may (permission) | can |
| would (hypothetical) | Restructure: "If X occurs, Y occurs." |
| could potentially possibly / might arguably | Delete the stack of hedges. State the claim or drop it. |

**Before:** The migration has completed and the table is being rebuilt.
**After:** The migration is complete. The database rebuilds the table.

**Before:** The flag can be set in the config file, making restarts unnecessary.
**After:** You can set the flag in the config file. Then a restart is not necessary.

### Section 4 — Sentences (Rules 4.1-4.5)

| Rule | Instruction |
|---|---|
| 4.1 | Write short and clear sentences. |
| 4.2 | Do not omit words or use contractions to shorten sentences. Keep articles, keep "that". |
| 4.3 | Use a vertical list for complex text. |
| 4.4 | Use connecting words between sentences on related topics ("Then", "As a result"). |
| 4.5 | Put an article (the, a, an) or a demonstrative adjective (this, these) before nouns where applicable. |

Rule 4.2 is the anti-terseness rule. STE is short sentences with complete grammar, not telegraph style, and it is also why Voice mode's contraction-friendly, tangent-friendly guidance does not carry over into Pragmatic or Strict mode (see Precedence above).

**Wrong shortening:** Ensure file exists before running.
**STE:** Make sure that the file exists before you run the command.

### Section 5 — Procedural writing (Rules 5.1-5.5)

| Rule | Instruction |
|---|---|
| 5.1 | Maximum 20 words per sentence. Warnings and cautions included. |
| 5.2 | One instruction per sentence, unless two actions happen at the same time. |
| 5.3 | Write instructions in the imperative: "Run the migration." |
| 5.4 | Put a required condition before the command, divided by a comma: "If the build fails, read the log." |
| 5.5 | Notes give information, never instructions. Notes get the 25-word limit. |

**Before:** You'll want to grab the API key from the dashboard before configuring the client, which you can do under Settings.
**After:** Get the API key from the dashboard, under Settings. Then configure the client with this key.

### Section 6 — Descriptive writing (Rules 6.1-6.6)

| Rule | Instruction |
|---|---|
| 6.1 | Give information gradually: one new fact per sentence. |
| 6.2 | Use key words and phrases to give the text a logical structure. |
| 6.3 | Maximum 25 words per sentence. |
| 6.4 | Group related information in paragraphs. |
| 6.5 | One topic per paragraph. |
| 6.6 | Maximum six sentences per paragraph. |

No imperative in descriptive text. Descriptions explain; procedures instruct.

### Section 7 — Safety instructions (Rules 7.1-7.3)

| Rule | Instruction |
|---|---|
| 7.1 | Use a word that shows the risk level ("WARNING" = injury, "CAUTION" = damage). |
| 7.2 | Start with a clear command or condition. |
| 7.3 | Then give the risk or the possible result. |

Never bury the instruction after the explanation. The pattern transfers directly to destructive CLI flags, irreversible migrations, and dangerous API options.

**Before:** Note that data loss may occur in some circumstances if the destructive flag happens to be enabled when running against production.
**After:** CAUTION: Do not use the `--force` flag against production. The flag deletes rows that do not match the source.

### Section 8 — Punctuation and word count (Rules 8.1-8.7)

| Rule | Instruction |
|---|---|
| 8.1 | All standard punctuation is legal except the semicolon. Write two sentences instead. |
| 8.2 | Use hyphens to connect words that act as one unit. |
| 8.3 | Parentheses are legal for references, item numbers, abbreviations, plural forms, explanations, alternatives. |
| 8.4 | In a vertical list, the lead-in colon ends a sentence for word count. |
| 8.5 | Text inside parentheses counts as one word. |
| 8.6 | Count as one word each: numbers, numbers with units, abbreviations, alphanumeric identifiers, quoted text, titles, labels, proper nouns. |
| 8.7 | A hyphenated word counts as one word. |

Rule 8.6 matters for software text: `sqlpipe run --config sqlpipe.yaml` in backticks is quoted text and counts as one word. Long identifiers do not blow your sentence budget.

The em dash is legal punctuation under 8.1 — STE never banned it. The content catalog's em-dash guidance (CP-12) is a frequency cap, not a ban: use it sparingly, prefer the comma or two sentences, because overuse is a tell independent of STE.

### Section 9 — Writing practices (Rules 9.1-9.4, GR-1 to GR-8)

| Rule | Instruction |
|---|---|
| 9.1 | When a word-for-word replacement does not work, restructure the sentence. |
| 9.2 | Use each approved word correctly: approved meaning, approved part of speech. |
| 9.3 | Do not build phrasal verbs ("go down" → "decrease", "set up" → "install" or "configure"). |
| 9.4 | Keep one consistent style and terminology through the whole document. |

General recommendations GR-1 to GR-8: keep the conjunction "that", be careful with "with", give pronouns clear referents, prefer "this + noun" over bare "this", avoid false friends, avoid Latin abbreviations, use inclusive language, and use the possessive apostrophe form only when you are sure it is correct (GR-8: if unsure, do not use it — non-native readers find it hard).

GR-6 for software docs: "e.g." → "for example", "i.e." → "that is", and delete "etc." — name the items or write "and more".

## THE CONTENT-PATTERN CATALOG (all modes)

15 patterns cataloged from Wikipedia's "Signs of AI writing" project (WikiProject AI Cleanup), covering tells that STE's structural rules do not already catch. Full before/after examples for each are in `references/patterns.md`; the master word/phrase substitution list is in `references/vocabulary.md`. In Pragmatic/Strict mode, apply these alongside the structural rules above; in Voice mode, these plus `references/voice-mode.md` are the whole job.

| ID | Pattern | One-line fix |
|---|---|---|
| CP-1 | Inflated significance / legacy language ("marks a pivotal moment", "a testament to") | State the concrete fact; delete the significance claim. |
| CP-2 | Notability / media-coverage puffery ("cited in the NYT, BBC...", "active social media presence") | Cite one specific claim from one specific source, or delete. |
| CP-3 | Superficial "-ing" tacked-on analysis ("..., ensuring users can accomplish their goals") | Delete the clause, or make it its own sentence with a real subject. See also Rule 3.5. |
| CP-4 | Promotional / advertisement language ("nestled in the heart of", "boasts a vibrant...") | Replace with the plain fact. See `references/vocabulary.md`. |
| CP-5 | Vague attribution / weasel words ("experts argue", "industry reports suggest") | Name the source, or delete the claim. |
| CP-6 | Formulaic frames: "Challenges and Future Outlook" sections, generic upbeat conclusions | Replace with one dated, sourced fact, or cut the section. |
| CP-7 | Copula avoidance ("serves as", "stands as", "boasts") in place of is/are/has | Use is/are/has. |
| CP-8 | Negative parallelism ("It's not just X, it's Y") | State Y. Delete the "not just X" half. |
| CP-9 | Rule-of-three padding (forcing ideas into groups of three) | Cut to however many items are actually true. |
| CP-10 | Elegant variation / synonym cycling (protagonist/main character/central figure/hero for one entity) | Pick one term. Already required by Rule 1.11 in Pragmatic/Strict; apply the same discipline in Voice mode. |
| CP-11 | False ranges ("from the Big Bang to the cosmic web") where the endpoints are not on a real scale | Name what is actually covered. |
| CP-12 | Formatting tells: em-dash overuse, mechanical **boldface**, inline-header bullet lists ("**Security:** ..."), emoji decoration, curly quotes | Plain punctuation, sentence-case headings, no emoji, straight quotes. Curly quotes are also an Untouchables risk near code — see below. |
| CP-13 | Collaborative chat residue ("I hope this helps!", "Certainly!", "Let me know if...") pasted into delivered content | Delete. It was never part of the document. |
| CP-14 | Knowledge-cutoff disclaimers ("As of [date]...", "based on available information...") | State the fact with its actual date, or omit if unknown — do not hedge about the model's own limits. |
| CP-15 | Sycophantic / servile tone ("Great question! You're absolutely right that...") | Delete the praise. State the substance. |

## Untouchables

These are technical names (Rules 1.5, 8.6) and exact strings. Leave them exact, in every mode, even when they break vocabulary or formatting rules:

- Code blocks, inline code, identifiers, CLI commands, flags, file paths
- Quoted error messages and log lines
- Product names, API endpoint names, config keys
- Numbers with units — each counts as one word in the sentence limit
- Straight vs. curly quotes inside any of the above: never "smarten" a quote character next to code, since some parsers treat `'` and `'` differently.

## Beyond Documentation

Same structural rules, different targets. Full adaptations in `references/use-cases.md`:

- **Error messages**: state what happened (simple past), the cause if known, then the fix as an imperative. No "Oops", no "Please ensure", no apology filler (CP-13, CP-15).
- **Runbooks**: STE's home turf. Imperative steps, conditions first, warnings before the step.
- **Incident reports**: simple past only. "We have identified an issue that may have impacted" becomes "Between 14:02 and 14:31 UTC, 12% of requests failed." Watch for CP-6's generic-conclusion pattern at the end of the report.
- **Release notes**: breaking changes follow the warning pattern — command first, risk second. Watch for CP-9 (rule-of-three feature lists) and CP-1 (inflated "this represents a major milestone" framing).
- **Agent instructions (prompts, AGENTS.md)**: a system prompt is a procedure for a reader that cannot ask questions. One instruction per sentence, no "should", condition first.
- **Translation prep**: STE's original job. One meaning per word plus complete grammar removes most translation ambiguity.
- **Blog posts, marketing, essays, narrative**: out of Pragmatic/Strict scope entirely. Switch to Voice mode and `references/voice-mode.md`.

## Self-Check Before You Deliver

Not optional. Full version with searchable patterns in `references/checklist.md`. Minimum pass, Pragmatic/Strict:

1. Count words in your three longest sentences. Over the 20/25 limit → split them.
2. Search your draft for: `'ll`, `'re`, `'s` (contraction), `has been`, `have been`, `should`, `-ing` verbs after a comma, semicolons.
3. Search for every `if` and `when`. Each one stands at the START of its sentence, before the command.
4. Search for the verbs you did NOT pick in Your Task step 3 (the check/verify/confirm set). Replace every hit with your chosen verb.
5. Scan against the CP-1 through CP-15 table above and `references/vocabulary.md`. Fix or delete every hit.

Voice mode: skip checks 1-4 (they are structural, not applicable). Run check 5, then confirm against `references/voice-mode.md` that the piece has an actual point of view and varied rhythm, not just an absence of AI-tells.

## Limits

STE's structural rules are for technical facts and instructions. Do not apply Sections 1-9 to marketing copy, blog voice, or brand writing — they delete persuasion by design. When a user asks for STE on marketing text, say so and offer Voice mode instead, or STE for the docs the marketing page links to.

The content-pattern catalog (CP-1 through CP-15) has no such restriction; it applies to any AI-sounding text in any mode.

This skill is an unofficial aid combining an ASD-STE100 implementation with a Wikipedia-sourced pattern catalog. It is not affiliated with or endorsed by ASD, STEMG, or the Wikipedia WikiProject AI Cleanup. No tool can guarantee ASD-STE100 compliance or that text will pass as human-written. ASD-STE100 is a registered trademark of ASD. The official standard is a free download at asd-ste100.org.

## References

- `references/vocabulary.md` — master word/phrase substitution table (STE slop table + AI-vocabulary words + promotional language + significance-inflation phrases), the modal ladder, and the consistency-pass rotations
- `references/patterns.md` — full before/after examples for CP-1 through CP-15
- `references/voice-mode.md` — personality and voice guidance for Voice mode only (blog, marketing, narrative, essay); does not apply in Pragmatic or Strict mode
- `references/checklist.md` — full verification pass with searchable patterns, for check mode and final audits
- `references/use-cases.md` — long-form adaptations: error messages, runbooks, incident reports, commits, UI copy, i18n

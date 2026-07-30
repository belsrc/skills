# Verification checklist

Run this pass on every draft before you deliver it. The checks are ordered from mechanical to judgment. Section A applies to Pragmatic and Strict mode only. Section B applies to every mode, including Voice.

## Section A — Structural checks (Pragmatic / Strict only)

### Mechanical checks (searchable)

Search the draft for each pattern. Every hit outside code blocks and quoted text is a violation.

| Search for | Violation | Fix |
|---|---|---|
| `'ll`, `'re`, `'ve`, `n't`, `it's` | Contraction (Rule 4.2) | Expand it. |
| `has been`, `have been`, `had been` | Present/past perfect (Rule 3.4) | Simple past or simple present. |
| `has` / `have` + past participle | Present perfect (Rule 3.4) | Simple past. |
| `should`, `would`, `may`, `might`, `could` | Unapproved modal (Rule 3.2) | See the modal ladder in `vocabulary.md`. |
| `is being`, `are being`, `was being` | Progressive passive (Rules 3.4, 3.5) | Active, simple tense. |
| `, making`, `, allowing`, `, enabling`, `, ensuring` | "-ing" clause as verb (Rule 3.5, CP-3) | New sentence with a real subject. |
| `;` | Semicolon (Rule 8.1) | Two sentences. |
| `e.g.`, `i.e.`, `etc.` | Latin abbreviation (GR-6) | "for example", "that is", name the items. |
| `simply`, `easily`, `seamlessly`, `robust` | Filler (no fact) | Delete. |
| ` if `, ` when ` (mid-sentence) | Trailing condition (Rule 5.4) | Move the condition to the start of the sentence, add a comma. |

### Countable checks

1. **Sentence length.** Count words in each sentence. Procedural limit: 20. Descriptive limit: 25. Notes: 25. Backticked commands, numbers with units, and identifiers count as one word each (Rule 8.6).
2. **Paragraph size.** Maximum six sentences per paragraph (Rule 6.6).
3. **Multi-word nouns.** Any noun chain over three words → break it with prepositions (Rule 2.1).
4. **Instructions per sentence.** One, unless the actions are simultaneous (Rule 5.2).

### Judgment checks

5. **Classification.** Is each passage cleanly procedural or descriptive? Procedures in imperative, descriptions never in imperative.
6. **Voice.** Any passive sentence: is the agent truly unknown, and is the passage descriptive? Otherwise make it active (Rule 3.6).
7. **Condition placement.** Every "if/when" stands before its command, with a comma (Rule 5.4).
8. **Synonym rotation.** One term per concept across the whole document (Rules 1.11, 9.4; also CP-10). Scan for check/verify/confirm, config/settings, run/execute.
9. **Warnings.** Command or condition first, risk second (Rules 7.2, 7.3).
10. **Completeness.** Articles present, "that" present after "make sure", no telegraph style (Rule 4.2).
11. **Untouchables intact.** Code, identifiers, quoted errors, and proper nouns are unchanged, including quote-character style next to code.

## Section B — Content-pattern checks (all modes, including Voice)

### Mechanical checks (searchable)

| Search for | Pattern | Fix |
|---|---|---|
| serves as, stands as, boasts, features [a] | CP-7 copula avoidance | is / are / has |
| Additionally, delve, crucial, pivotal, showcase, tapestry, landscape, testament, underscore, vibrant | AI-vocabulary words | Delete or replace, see `vocabulary.md` |
| nestled, breathtaking, stunning, must-visit, groundbreaking, renowned | CP-4 promotional language | Replace with the plain fact |
| Industry reports, Experts argue, Observers have cited | CP-5 vague attribution | Name the source or delete |
| Despite these challenges, Future Outlook, exciting times lie ahead | CP-6 formulaic frames | Replace with a dated fact or cut |
| It's not just..., it's... / not only...but... | CP-8 negative parallelism | State the point directly |
| — (em dash) | CP-12, count per paragraph | More than one or two per paragraph is a tell; convert extras to commas or new sentences |
| **bolded phrase:** at the start of a bullet | CP-12 inline-header list | Rewrite as plain sentences |
| ## Title Case Headings | CP-12 | Sentence case |
| 🚀 💡 ✅ (or any emoji) | CP-12 | Delete |
| " " (curly quotes) | CP-12 | Straight quotes, especially near code |
| I hope this helps, Let me know, Certainly! | CP-13 chat residue | Delete |
| as of [date], based on available information | CP-14 cutoff disclaimer | State the fact with its real date, or say "not documented" |
| Great question!, You're absolutely right | CP-15 sycophancy | Delete |

### Judgment checks

12. **Rule of three (CP-9).** Any list of exactly three items — is it because there are really three things, or because three felt complete?
13. **Elegant variation (CP-10).** Track every entity mentioned more than twice. Same name each time?
14. **False ranges (CP-11).** Any "from X to Y" — do X and Y actually sit on one scale?
15. **Voice mode only: soullessness.** Every sentence the same length and shape? No opinion, no "I", no acknowledged uncertainty? See `voice-mode.md`.

## When reporting violations (check mode)

For each violation give: the rule or pattern ID, the offending text, and a compliant rewrite. Cite only IDs that appear in SKILL.md or this file — the numbering across both rule systems is unintuitive and models invent IDs that do not exist (tested: an agent without this file cited "Rule 3.1: short sentences"; the real Rule 3.1 is about verb forms).

End the report with this statement when the user asked for STE compliance: "No tool can guarantee ASD-STE100 compliance. Final approval rests with the writer. The official standard is a free download at asd-ste100.org."

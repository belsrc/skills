# Use cases beyond documentation

STE was built for aircraft maintenance manuals. The same properties — one meaning per word, short sentences, condition-first commands — transfer to any text where misreading has a cost. By the end of Issue 8, 64% of registered STE users were outside aerospace and defense. The content-pattern catalog transfers even more broadly, since AI-writing tells show up anywhere an LLM drafts text, technical or not.

Each case below names the mode and the adaptations. Cases through "UI copy" are Pragmatic or Strict (STE governs). The last two are Voice mode.

## Error messages and CLI output

Mode: procedural. This is the highest-value target: an error message is a 2 a.m. instruction to a stressed reader.

Pattern: state what happened (past simple), state the cause if known, give the command or condition to fix it. Watch for CP-13 (chat residue like "Please ensure") and CP-15 (apology filler) — error messages are where these leak in most often.

> **Before:** Oops! Something went wrong while attempting to establish a connection. Please ensure your credentials are properly configured and try again.
> **After:** Connection to the database failed. The password for user `app` was not correct. Set `DB_PASSWORD` and connect again.

## Runbooks and standard operating procedures

Mode: strict-leaning procedural. This is STE's home turf — an on-call runbook is a maintenance manual.

- Every step imperative, one instruction per step, conditions first.
- Warnings before the step, command first, risk second.
- 20-word limit enforced hard: an operator under pager stress reads each sentence once.

## Incident reports and postmortems

Mode: descriptive. Simple past only — a timeline in present perfect ("we have identified...") hides when things happened.

> **Before:** We have identified an issue that may have impacted some users' ability to access the service.
> **After:** Between 14:02 and 14:31 UTC, 12% of requests failed. A deploy at 14:00 removed the cache warmup step.

STE bans hedges ("may have impacted") — the report states what is known and says "unknown" for the rest. This reads more honest because it is. Watch for CP-6's generic-conclusion pattern creeping into the postmortem's closing paragraph.

## Commit messages and PR descriptions

Mode: descriptive body, imperative subject. Convention already matches STE: imperative subject line, plain past facts in the body. Apply the vocabulary substitution table and the 25-word limit to the body. Delete "this PR aims to" (CP-1-adjacent inflated framing).

## API changelogs and release notes

Mode: descriptive. One entry, one change, one sentence where possible. "Breaking:" entries follow the warning pattern — command first: "Update your calls to `v2/users`. The `name` field split into `first_name` and `last_name`." Watch for CP-9 (rule-of-three feature bullets) and CP-1 ("this represents a major milestone" framing) in release announcements.

## Instructions for AI agents (prompts, AGENTS.md, skills)

Mode: procedural. A system prompt is a procedure executed by a reader with no ability to ask questions — the exact reader STE was designed for.

- One instruction per sentence keeps rules independently quotable and hard to half-follow.
- One word, one meaning prevents the model from treating "check", "verify", and "validate" as three different operations.
- Condition-first ("If the build fails, stop") beats trailing conditions, which models drop.
- No "should" — a model reads "should" as optional. Write "must" or delete the rule.

## Support macros and status-page updates

Mode: descriptive, 25-word limit. Non-native readers are the majority of many user bases. No "we sincerely apologize for any inconvenience this may have caused" (CP-15) — "The API was down for 18 minutes. Uploads made during this time were saved and will process today."

## Translation and localization prep

Mode: strict. STE's original purpose was making English readable for non-native maintenance crews, and it doubles as pre-editing for machine translation. One meaning per word plus complete grammar (articles, "that") removes most translation ambiguity. If your docs get localized, STE cuts the error rate and the cost.

## UI copy and empty states

Mode: procedural, hard length limits. Buttons and labels are technical names (exempt). Body copy follows the rules: "No projects yet. Create a project to start." Nothing else survives at this length anyway.

## Blog posts, essays, and narrative writing

Mode: Voice. STE's structural rules do not apply here by design — see Limits in SKILL.md. Run the content-pattern catalog to remove AI tells, then apply `references/voice-mode.md` to put a point of view back in. A blog post about your project can be persuasive and personal; the README it links to should still be Pragmatic mode.

## Marketing and brand writing

Mode: Voice. Same reasoning as blog posts. If a user asks for STE compliance on marketing copy, say plainly that STE deletes persuasion by design and is the wrong tool for that page — offer Voice mode instead, or offer STE for the technical documentation the page links to.

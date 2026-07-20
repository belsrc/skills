# ticket-creator

Create well-structured project tickets from conversational intent, with automatic context detection and intelligent defaults.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Features](#features)
- [How it works](#how-it-works)
- [Ticket template structure](#ticket-template-structure)
- [Project metadata detection](#project-metadata-detection)
- [Quality guidelines](#quality-guidelines)
- [Edge cases](#edge-cases)
- [File layout](#file-layout)
- [Troubleshooting](#troubleshooting)
- [Related skills](#related-skills)

## Installation

```bash
npx skills add https://github.com/belsrc/skills --skill ticket-creator
```

## Quick Start

Ask for a ticket in plain language:

```
create a ticket: add --json flag to scan command for programmatic output
```

The skill spawns a sub-agent that researches your codebase, detects the project prefix and next ticket number, and generates a complete ticket with actionable acceptance criteria. No configuration required.

Multiple tickets in one request:

```
create tickets for:
1. fix crash on empty directories (high priority)
2. add rate limiting to API client
3. improve parser error messages
```

The skill spawns all tickets in parallel for efficiency.

## What it does

The skill transforms informal feature requests, bug reports, or task descriptions into formal project tickets. Each ticket includes metadata (type, priority, dependencies), a description explaining why the work matters, and specific acceptance criteria clear enough for someone else to implement without questions.

Two properties make this different from manually writing tickets:

- **Automatic context gathering.** The skill researches your codebase to write meaningful acceptance criteria rooted in what actually exists. It reads existing tickets, project documentation, tech stack indicators, and relevant source files. If `/opsx:explore` is available, it uses that for deeper investigation.
- **Parallel generation.** When creating multiple tickets, the skill spawns all sub-agents concurrently, each researching and generating independently. Result aggregation happens after all complete, with automatic renumbering if parallel agents suggest duplicates.

The skill detects project metadata automatically. It extracts the project prefix from existing tickets, git remotes, or `package.json`, and finds the next ticket number by scanning your tickets directory. Fallbacks handle projects without existing tickets gracefully.

## When to use

Trigger the skill when you want to formalize work:
- "create a ticket"
- "write a ticket"
- "make a ticket"
- "turn this into a ticket"
- You describe a feature/bug/task and want it structured

## Features

- **Automatic project detection** — Prefix from existing tickets, git remote, or `package.json`
- **Sequential numbering** — Finds next ticket number from your tickets directory
- **Parallel generation** — All tickets spawn concurrently, aggregate after completion
- **Context-aware acceptance criteria** — Researches codebase (docs, existing tickets, source files) to write specific, testable requirements
- **OpenSpec integration** — Uses `/opsx:explore` when available
- **Fallback support** — Degrades to serial processing when sub-agents unavailable
- **Quality defaults** — Infers type (Epic/Task/Enhancement) and priority (High/Medium/Low) from intent

## How it works

### 1. Intent Understanding

The skill extracts ticket details from your message. If ambiguous, it asks clarifying questions:
- What type of work? (Epic, Task, Enhancement)
- What priority? (High, Medium, Low)
- Any dependencies?

This step is conversational, not a form. You provide what you know, the skill infers defaults for the rest.

### 2. Parallel Sub-Agent Workflow

For each ticket, the skill spawns a sub-agent that:

1. **Gathers project context** via `/opsx:explore` (if available) or manual research:
   - Existing tickets (`.tickets/`, `docs/tickets/`, `tickets/`)
   - Project docs (`README.md`, `CLAUDE.md`, `AGENTS.md`)
   - Tech stack indicators (`package.json`, `Cargo.toml`, `go.mod`)
   - Relevant source files

2. **Detects project metadata:**
   - **Prefix**: From existing ticket patterns (`[FOO-123]`), git remote URL, or `package.json` name field
   - **Number**: Highest existing ticket number + 1

3. **Fills the template** with context-aware description and actionable acceptance criteria

4. **Returns the ticket** with detection notes (prefix source, numbering rationale, context sources)

All sub-agents run concurrently. In environments without sub-agent support, the skill falls back to serial processing.

### 3. Result Aggregation

Once all sub-agents complete:
- Collects generated tickets
- Renumbers sequentially if parallel agents suggested duplicates
- Presents all tickets with summary (count, prefix detected, priority distribution)

## Examples

See [SKILL.md](SKILL.md) for two complete examples with full ticket output:
1. Single feature request (JSON output flag with schema)
2. Multiple tickets in one request (bug fix + two enhancements)

## Ticket template structure

```markdown
### [PROJECT-NNN]: [Title]

Status: [Complete | Not Started | Closed | In Progress]
Type: [Epic | Task | Enhancement]
Priority: [High | Medium | Low]
Dependencies: [None | TICKET-ID (description)]

Description:

[1-3 paragraphs explaining what problem this solves, why it matters,
 and relevant codebase context]

Acceptance Criteria:

- [Specific, testable implementation requirements]
- [Validation/testing requirements]
- [Documentation requirements]
- [Integration/deployment considerations]
- [Edge cases to handle]
- [Performance requirements if applicable]

[Optional subsections: Technical Approach, Security Considerations, Migration Plan]
```

**Filling guidelines:**
- **Title**: Clear, actionable, 5-10 words
- **Status**: Defaults to "Not Started"
- **Type**: Inferred from intent (new feature = Enhancement/Epic, fix = Task, large initiative = Epic)
- **Priority**: Defaults to Medium if unclear
- **Dependencies**: "None" if not mentioned
- **Description**: What problem, why it matters, codebase context
- **Acceptance Criteria**: Specific, testable bullets covering implementation, validation, docs, integration, edge cases, performance

## Project metadata detection

### Prefix detection (priority order):

1. **Existing tickets** — `[FOO-123]` patterns in `.tickets/`, `docs/tickets/`, `tickets/`
2. **Git remote** — Repo name from remote URL, uppercased
3. **package.json** — The `name` field
4. **Placeholder** — `[PROJECT-NNN]` if none found

### Ticket numbering:

- Scans existing tickets for highest number
- Increments for next ticket
- Uses `NNN` placeholder if no tickets found

## Quality guidelines

- **Actionable criteria** — Clear enough for someone else to implement without questions
- **Balance detail** — Epics get more context than simple bug fixes
- **Specific verification** — "Unit tests cover X, Y, Z edge cases" not just "tests pass"
- **Capture motivation** — Explain why this work matters, not just what to do
- **Domain language** — Uses terminology from your codebase

## Edge cases

- **No git repo** — Uses placeholder prefix
- **Ambiguous intent** — Asks for clarification before processing
- **Partial information** — Fills defaults before delegating to sub-agents
- **Large epics** — May suggest breaking into multiple tickets
- **Sub-agent failures** — Reports errors and offers retry
- **Sequential numbering conflicts** — Renumbers after aggregation if parallel agents suggested duplicates
- **Environments without sub-agents** — Falls back to serial processing

## File layout

```
ticket-creator/
├── SKILL.md       # Core workflow, sub-agent prompts, template structure
└── README.md      # This file
```

## Troubleshooting

**Tickets use placeholder prefix `[PROJECT-NNN]`**  
Create at least one ticket manually with your desired prefix, or ensure your git remote URL contains the project name, or add a `name` field to `package.json`.

**Ticket numbers restart at `NNN`**  
Store existing tickets in: `.tickets/`, `docs/tickets/`, or `tickets/`. The skill scans these directories to detect the next number.

**Acceptance criteria feel generic**  
The skill researches your codebase automatically. If criteria are still generic, check that your project has documentation (README.md, CLAUDE.md) or existing tickets that provide domain context.

**Multiple tickets get the same number**  
Expected behavior when creating tickets in parallel. The skill automatically renumbers them sequentially after all sub-agents complete.

## Related skills

- **opsx:explore** — Used by ticket-creator for codebase research (optional)
- **engineering-council** — Can provide architectural guidance for complex tickets (optional)

# Changelog

## [1.1.0]

### Added
- OpenSpec awareness: both the main research workflow and the sub-agent prompt template now check for `openspec/` and read `openspec/specs/INDEX.md` (or `spec.md` files directly) to ground tickets in the current, canonical capability state instead of assumptions from skimming code
- In-flight `openspec/changes/` are checked for overlap with the ticket's intent, surfacing a potential match as a `Dependencies` entry instead of producing a duplicate or conflicting ticket
- New "Describe outcomes, not implementations" quality guideline: tickets should state *what* must change, not *how* to change it, since implementation-level details (specific files, functions, line numbers, step-by-step approach) go stale quickly as code shifts between ticket creation and pickup

### Changed
- Template's optional subsection reframed from open-ended "architecture decisions, or approach" to non-binding context (e.g., "Context for Implementer"), explicitly described as background rather than instructions
- Filling guidelines no longer suggest a "Technical Approach" subsection; call out that optional sections should stay descriptive of constraints/context, not prescriptive of implementation
- Example 2 ("Fix crash when scanning empty directories") had its prescriptive "Technical Approach" subsection (naming a specific file and code change) removed to match the new outcome-focused guidance

## [1.0.0] - Initial release
- Automatic project prefix and ticket number detection
- Parallel sub-agent fan-out for multi-ticket requests
- Structured template with Status, Type, Priority, Dependencies, Description, and Acceptance Criteria
- Context gathering from existing tickets, README/CLAUDE/AGENTS files, and tech stack indicators

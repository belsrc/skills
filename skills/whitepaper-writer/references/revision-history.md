# Revision History

## Detecting an Existing Whitepaper

Before starting exploration, the likely locations (scope root, `docs/`) MUST be checked for an existing whitepaper. If found:

1. It MUST be read in full before touching code — you need to know what it already claims so you can check each claim rather than re-deriving the whole document from nothing.
2. Its current revision number and date MUST be noted from its own `## Revision History` section (or `**Revision Date:**` header if there's no history section yet — meaning this would be its first documented revision).
3. Everything it says MUST be treated as a hypothesis to verify during exploration, not as ground truth to preserve. An update is not a diff-and-patch operation; it's a fresh verification pass that happens to have a strong prior.

## Determining What Changed

In order of reliability:

1. **`git log` since the prior revision's date**, scoped to the whitepaper's directory boundary, if the repo is a git checkout. This SHOULD be preferred when available — it gives an actual changelog to work from rather than inferring change from a diff of documentation states.
2. **A structural diff** between what the previous whitepaper documents and what fresh exploration found — new subsystems, removed subsystems, changed public APIs, new config options. This is the fallback when git history isn't available or doesn't cleanly map to the scope boundary.

Dates MUST NOT be guessed. If you can't establish when a change landed (no git history, no changelog, no version bump), the change MUST be described without a date rather than inventing one.

## Revision Entry Format

A new entry MUST be appended under `## Revision History`, newest first:

```markdown
### Revision <N> (<date>)

**Major Features Added:**

1. **<Feature Name>** (<date if known>)
   - <what changed, concretely>
   - <why it matters / what it replaces or extends>

**Architectural Changes:**

- **<Change Name>** (<date if known>): <what changed and why>

**Previous Revision:** Revision <N-1> (<prior date>)
```

Entries SHOULD be grouped by "Major Features Added" (new capability, new user-facing behavior) vs. "Architectural Changes" (internal restructuring, removed legacy paths, type system changes) — the same split the reference examples use, because a reader skimming revision history usually cares about one or the other, not both interleaved.

## First-Time Documentation

If there's no existing whitepaper, a Revision History section MUST NOT be manufactured for a document that has no history yet. A one-line `**Revision Date:** <date>` header is enough. The section appears starting with the first update.

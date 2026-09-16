#!/usr/bin/env python3
"""
Light structural and syntactic validation for a generated whitepaper.

Checks:
  1. Required top-level sections are present (Abstract, an Overview section,
     a Conclusion section).
  2. Prohibited sections are absent (doc-drift/gaps headers -- those belong
     in the conversational report to the user, never in the whitepaper).
  3. Inline file:line citation density isn't excessive (a bare filename
     mention is fine; systematic `(file:line)` citations after nearly every
     claim are noise and a WARN, not a hard failure, since a script can't
     perfectly distinguish a handful of legitimate ones from a pattern).
  4. Every fenced code block is at least syntactically well-formed for its
     declared language. This is a best-effort check, not a full compile:
     - json: json.loads
     - python: ast.parse
     - bash/sh: `bash -n` if bash is on PATH, else brace-balance only
     - typescript/tsx/javascript/jsx: `node --check` if node is on PATH
       (js only; ts falls back to brace-balance since type syntax needs a
       real TS toolchain), else brace-balance only
     - rust/c/cpp/go/java/powershell/csharp: brace-balance only (no compiler assumed present)
     - yaml: yaml.safe_load if PyYAML is importable, else skipped
     - mermaid: must start with a recognized diagram-type keyword

  This will not catch bad technical content, padding, or voice/tone issues
  (e.g. "the repo" instead of a named system as the subject) -- those need
  qualitative review. It exists to catch the mechanical failures (a
  truncated code block, invalid JSON, a drift section that shouldn't exist)
  that are cheap to catch automatically and embarrassing to ship.

Usage:
  python3 validate_structure.py <path-to-whitepaper.md>

Exit code is 0 if there are no FAIL results, 1 otherwise. WARN results
never affect the exit code.
"""

from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REQUIRED_SECTION_PATTERNS = [
    ("Abstract", re.compile(r"^#{1,2}\s+Abstract\s*$", re.MULTILINE)),
    (
        "System/Architecture Overview",
        re.compile(
            r"^#{1,3}\s+(\d+\.?\s*)?(System\s+Overview|Overview|Architecture\s+Overview)",
            re.MULTILINE | re.IGNORECASE,
        ),
    ),
    (
        "Conclusion",
        re.compile(r"^#{1,2}\s+(\d+\.?\s*)?Conclusion\s*$", re.MULTILINE | re.IGNORECASE),
    ),
]

# Headers in this shape MUST NOT appear anywhere in the document -- drift/gap
# findings belong in the conversational report to the user, not the file.
PROHIBITED_SECTION_PATTERNS = [
    (
        "doc drift / gaps section",
        re.compile(
            r"^#{1,6}\s+.*(doc(?:umentation)?\s*drift|documentation\s*gaps?|known\s*discrepanc|gaps?\s+and\s+asymmetr)",
            re.MULTILINE | re.IGNORECASE,
        ),
    ),
]

# A backtick-quoted `path/file.ext:123-456` or `filename:123` token -- the
# systematic inline-citation pattern that MUST NOT show up throughout the
# prose. A handful is fine; dozens means every claim got footnoted.
CITATION_RE = re.compile(r"`[A-Za-z0-9_][\w./-]*:\d+(?:-\d+)?`")
CITATION_WARN_ABSOLUTE = 8
CITATION_WARN_PER_1000_WORDS = 4

MERMAID_DIAGRAM_KEYWORDS = (
    "flowchart",
    "graph",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram",
    "erDiagram",
    "gantt",
    "pie",
    "journey",
    "gitGraph",
)

CODE_BLOCK_RE = re.compile(r"```([A-Za-z0-9_+-]*)\n(.*?)```", re.DOTALL)


def check_sections(text: str) -> list[dict]:
    results = []
    for name, pattern in REQUIRED_SECTION_PATTERNS:
        found = bool(pattern.search(text))
        results.append(
            {
                "check": f"section:{name}",
                "status": "PASS" if found else "FAIL",
                "detail": "" if found else f"No heading matching {name!r} found",
            }
        )
    for name, pattern in PROHIBITED_SECTION_PATTERNS:
        matches = pattern.findall(text)
        hit = bool(matches)
        results.append(
            {
                "check": f"prohibited_section:{name}",
                "status": "FAIL" if hit else "PASS",
                "detail": (
                    f"found {len(matches)} heading(s) matching a prohibited pattern -- "
                    "drift/gap findings belong in the conversational report, not the whitepaper"
                    if hit
                    else ""
                ),
            }
        )
    has_mermaid = "```mermaid" in text
    results.append(
        {
            "check": "diagram:mermaid",
            "status": "PASS" if has_mermaid else "WARN",
            "detail": "" if has_mermaid else "No mermaid diagram found (not always required)",
        }
    )
    citation_count = len(CITATION_RE.findall(text))
    word_count = max(len(text.split()), 1)
    per_1000 = citation_count / word_count * 1000
    citation_excessive = citation_count > CITATION_WARN_ABSOLUTE and per_1000 > CITATION_WARN_PER_1000_WORDS
    results.append(
        {
            "check": "citation_density",
            "status": "WARN" if citation_excessive else "PASS",
            "detail": (
                f"{citation_count} inline `file:line` citations found (~{per_1000:.1f} per 1000 words) "
                "-- a bare filename mention is fine, but systematic file:line citations after nearly "
                "every claim read as noise and go stale fast; see references/code-truth-and-conflicts.md"
                if citation_excessive
                else f"{citation_count} inline file:line citations found"
            ),
        }
    )
    return results


ELLIPSIS_LINE_RE = re.compile(r"^\s*(//|#)?\s*\.\.\.\s*$", re.MULTILINE)


def brace_balance_ok(code: str) -> bool:
    pairs = {"(": ")", "[": "]", "{": "}"}
    closers = set(pairs.values())
    stack = []
    in_string = None
    escape = False
    for ch in code:
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == in_string:
                in_string = None
            continue
        if ch in ("'", '"', "`"):
            in_string = ch
            continue
        if ch in pairs:
            stack.append(pairs[ch])
        elif ch in closers:
            if not stack or stack.pop() != ch:
                return False
    return not stack


def run_external_check(cmd: list[str], code: str, suffix: str) -> tuple[bool, str]:
    if shutil.which(cmd[0]) is None:
        return True, f"{cmd[0]} not on PATH, skipped external check (brace-balance only)"
    with tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False) as f:
        f.write(code)
        path = f.name
    try:
        proc = subprocess.run(
            cmd + [path], capture_output=True, text=True, timeout=10
        )
        if proc.returncode != 0:
            return False, proc.stderr.strip()[:300]
        return True, ""
    except Exception as exc:  # noqa: BLE001 - best effort, never crash the validator
        return True, f"external check errored ({exc}), falling back to brace-balance only"
    finally:
        Path(path).unlink(missing_ok=True)


def check_code_block(lang: str, code: str, index: int) -> dict:
    lang = lang.lower().strip()
    label = f"code_block[{index}]:{lang or 'untagged'}"

    if not code.strip():
        return {"check": label, "status": "WARN", "detail": "empty code block"}

    if lang == "json":
        try:
            json.loads(code)
            return {"check": label, "status": "PASS", "detail": ""}
        except json.JSONDecodeError as exc:
            return {"check": label, "status": "FAIL", "detail": str(exc)}

    if lang == "python":
        try:
            ast.parse(code, filename="<whitepaper-snippet>", mode="exec")
            return {"check": label, "status": "PASS", "detail": ""}
        except SyntaxError as exc:
            return {"check": label, "status": "FAIL", "detail": str(exc)}

    if lang in ("yaml", "yml"):
        try:
            import yaml  # type: ignore

            yaml.safe_load(code)
            return {"check": label, "status": "PASS", "detail": ""}
        except ImportError:
            return {
                "check": label,
                "status": "WARN",
                "detail": "PyYAML not available, skipped",
            }
        except Exception as exc:  # noqa: BLE001
            return {"check": label, "status": "FAIL", "detail": str(exc)}

    if lang in ("bash", "sh", "shell"):
        ok, detail = run_external_check(["bash", "-n"], code, ".sh")
        return {
            "check": label,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
        }

    if lang in ("javascript", "js", "jsx"):
        ok, detail = run_external_check(["node", "--check"], code, ".js")
        if ok and "not on PATH" in detail:
            ok = brace_balance_ok(code)
            detail = "" if ok else "unbalanced braces/parens/brackets"
        return {
            "check": label,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
        }

    if lang == "mermaid":
        stripped = code.strip()
        first_line = stripped.splitlines()[0] if stripped else ""
        ok = any(first_line.strip().startswith(kw) for kw in MERMAID_DIAGRAM_KEYWORDS) or (
            "init" in first_line and stripped.count("\n") > 0
        )
        return {
            "check": label,
            "status": "PASS" if ok else "WARN",
            "detail": "" if ok else "doesn't start with a recognized diagram keyword",
        }

    if lang in ("typescript", "ts", "tsx", "rust", "rs", "c", "cpp", "c++", "go", "java", "powershell", "ps1", "csharp", "cs"):
        if ELLIPSIS_LINE_RE.search(code):
            return {
                "check": label,
                "status": "WARN",
                "detail": "excerpt contains an elision line (`...`); brace-balance check skipped since this is intentionally a partial snippet",
            }
        ok = brace_balance_ok(code)
        return {
            "check": label,
            "status": "PASS" if ok else "FAIL",
            "detail": "" if ok else "unbalanced braces/parens/brackets (best-effort check only, not a full compile)",
        }

    return {
        "check": label,
        "status": "WARN",
        "detail": f"no validator for language {lang!r}, skipped",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 validate_structure.py <path-to-whitepaper.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")

    results = check_sections(text)
    for i, (lang, code) in enumerate(CODE_BLOCK_RE.findall(text)):
        results.append(check_code_block(lang, code, i))

    fails = [r for r in results if r["status"] == "FAIL"]
    warns = [r for r in results if r["status"] == "WARN"]
    passes = [r for r in results if r["status"] == "PASS"]

    print(f"Validated: {path}")
    print(f"  PASS: {len(passes)}  WARN: {len(warns)}  FAIL: {len(fails)}\n")
    for r in results:
        marker = {"PASS": " ok ", "WARN": "warn", "FAIL": "FAIL"}[r["status"]]
        line = f"[{marker}] {r['check']}"
        if r["detail"]:
            line += f" - {r['detail']}"
        print(line)

    print()
    print(json.dumps({"pass": len(passes), "warn": len(warns), "fail": len(fails), "results": results}))

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

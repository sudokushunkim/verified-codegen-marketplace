# verified-codegen

**Turn AI-generated code into verified-before-merge code.**

A language- and framework-neutral pipeline of 10 role-separated subagents. Instead of
accepting AI code as-is, every change is run past a **Destroyer** that intentionally hunts
failure cases and a **scenario + test quality gate** before it is accepted — and the pipeline
can never push or rewrite history on its own.

## Why
LLMs generate code fast, but can't guarantee it's correct. This plugin makes "AI writes it,
a verification process proves it" the default: role separation, an adversarial Destroyer stage,
a bounded feedback loop, and git-safety hooks.

## Pipeline
```
planner → architect → devops → (coder ∥ scenarist) → destroyer → fixer → scenarist(augment) → tester → reviewer → author
                                   ▲                                                              │
                                   └──────────────── issue found → restart from coder (≤3) ───────┘
```
**Coder and Scenarist run in parallel** — base test scenarios come from the spec, so they're
written while the code is written. After the Destroyer surfaces edge cases, the Scenarist
augments the scenario set and the Tester implements it.

## What's inside
- `skills/verified-codegen/` — the orchestration workflow (auto-triggers on build/implement requests).
- `agents/` — 10 subagents: planner, architect, devops, coder, scenarist, destroyer, fixer, tester, reviewer, author.
- `hooks/` — a PreToolUse git guard: **push / force-push / reset are blocked** (commits ok; use `revert`).
- `commands/verify-build.md` — `/verify-build <request>` to run the pipeline explicitly.

## Git safety (enforced)
`hooks/guard_git.py` denies `git push`, `git push --force`, and `git reset`. Requires `python`
on PATH. Commits, `revert`, and `worktree` are allowed.

## Language-neutral
The pipeline detects the repo's language, framework, package manager, linter/formatter, and test
framework first, then every agent works in that stack and follows its conventions.

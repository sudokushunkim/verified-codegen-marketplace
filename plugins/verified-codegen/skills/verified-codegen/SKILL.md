---
name: verified-codegen
description: "Verified-before-merge codegen pipeline. Runs a feature/implementation request through 10 role-separated subagents so AI-generated code is checked by a Destroyer (failure-case hunter) and a scenario+test quality gate before it is accepted. Use for any 'implement / build / add a feature / write an endpoint / design + implement / write service logic / create CRUD' request in any language or framework. Coder and Scenarist run in parallel. Do NOT use for simple questions or concept explanations."
---

# Verified Codegen Pipeline

A request to build or change code is handled by 10 specialist subagents so that
**AI-generated code is verified before it is accepted** — not shown as a suggestion,
but written into the real project files and put through a Destroyer and a test gate.

This pipeline is **language- and framework-neutral**. Detect the project's language,
framework, package manager, lint/format tool, and test framework from its files first,
then every agent works in *that* stack and follows *its* conventions.

## Core principles

- **Edit real files.** Read and modify the actual project files; don't paste code to the user.
- **Auto-advance.** Run the stages end to end without asking for confirmation between them.
- **Report at the end.** Deliver one change report when the pipeline finishes.
- **Bounded feedback loop.** If Destroyer or Tester finds an issue, restart from Coder. Max 3 loops; after that, deliver current state + unresolved issues.
- **Accumulate artifacts.** Each agent's output feeds the next and appears in the final report.
- **No over-engineering.** Keep code simple and readable. No speculative abstraction, patterns, or layers you don't need yet.
- **Git safety (enforced by hooks).** Commits are fine. **Never push, never force-push, never `reset`** — use `revert` to keep history. Use a **git worktree** per task when several branches of one repo are worked at once.
- **Preserve files.** Never blow away existing content; add/modify in place and keep the original newline style.

## Detect the stack first

Before stage 1, inspect the repo to establish:
- language(s) and framework(s) (manifest files, config, source layout)
- package manager / build tool
- linter + formatter (the language's standard)
- test framework and where tests live
- existing conventions (naming, module boundaries, error handling)

Every agent below maps its generic job onto this detected stack.

## Pipeline flow

```
planner → architect → devops → ┌─ coder (implementation) ──────┐
                                └─ scenarist (base scenarios) ──┘  (PARALLEL)
                                           │
                                           ▼
                             destroyer → fixer → scenarist (augment edge cases)
                                           │                    │
                                           ▼                    ▼
                                        tester → reviewer → author
                                           ▲
            issue found (destroyer/tester) └── restart from coder (max 3 loops)
```

### Parallel stage: Coder ∥ Scenarist

After `architect` and `devops`, launch **coder** and **scenarist** at the same time:

- **coder** implements the feature from the Planner/Architect/DevOps outputs.
- **scenarist** writes the **base** test scenarios (happy path, failure, full CRUD cycle,
  authorization/permission) — these derive from the *spec* (Planner/Architect), not from the
  code, so they can be authored in parallel while the code is being written.

They do not read each other's in-progress work. When both finish, continue to `destroyer`.
After `destroyer` surfaces edge cases, `scenarist` runs again briefly to **augment** the
scenario set with those edge cases before `tester` implements them.

> If the runtime cannot truly run two subagents at once, run `scenarist` immediately after
> dispatching `coder` and before `destroyer`; the point is that base scenarios never wait on code.

## Stages

1. **planner** — turn the request into a feature list, data-flow, interface/endpoint contracts, business rules, external dependencies.
2. **architect** — design the data model/schema, module boundaries, interface/DTO shapes, routing, and any needed patterns (cache, queue, events).
3. **devops** — apply config/env, dependency manifests, container/CI config, and cross-cutting middleware. Edit existing config surgically.
4. **coder** *(parallel)* — implement in the detected language/framework, following its conventions; keep controllers thin and domain logic separated; use the language's type system; document public surfaces.
5. **scenarist** *(parallel, then augment)* — author base scenarios from the spec, then augment with Destroyer's edge cases.
6. **destroyer** — hunt edge cases and failure modes (null/empty, boundaries, concurrency, authz bypass, N+1/perf, external failures, data-integrity). Issues → restart from coder.
7. **fixer** — enforce the language's style/lint conventions, naming, dead-code removal, constants, types, doc comments.
8. **tester** — implement the scenarios as real tests in the project's test framework (Arrange-Act-Assert, independent, parametrized). Logic gaps → restart from coder.
9. **reviewer** — quality/security/performance review with a 10-point score. Advisory only (no loop); high-severity items are flagged in the final report.
10. **author** — write docs: interface/API reference, schema/ERD in text, setup guide, usage examples, change summary.

Each agent's detailed brief lives in `agents/<name>.md`.

## Feedback loop

When **destroyer** or **tester** finds an issue:
1. Record issues clearly (id, description, severity).
2. Hand the list to **coder**; coder fixes.
3. Re-run destroyer → fixer → scenarist(augment) → tester → reviewer → author.
4. Count loops; **max 3**. On exceeding, deliver current state + the unresolved-issue list.

Track resolution across loops:
```
## Feedback loop history
### Loop 1 (Destroyer)
- D-001: [resolved] ...
### Loop 2 (Tester)
- T-001: [resolved] ...
```

## Final deliverable: change report

1. **Feature summary** (Planner)
2. **Design** (Architect — schema, module boundaries)
3. **File changes** — created / modified / deleted (path + what changed)
4. **Key logic highlights**
5. **Review summary** (Reviewer score + top items; high-severity warnings)
6. **Docs** (Author)
7. **Feedback-loop history** (only if a loop occurred)
8. **Next steps** (migrations, env vars, anything the user must run)

Deliver only this final report. Keep intermediate chatter out of it.

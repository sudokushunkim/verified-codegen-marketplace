# verified-codegen marketplace

A Claude Code / Cowork plugin marketplace hosting **verified-codegen** — a multi-agent
pipeline that turns AI-generated code into verified-before-merge code.

## Install
```
/plugin marketplace add <this-repo-url-or-path>
/plugin install verified-codegen@verified-codegen-marketplace
```
Then make a request like "add an endpoint that …" / "implement …", or run
`/verify-build <request>` explicitly.

## Layout
```
.claude-plugin/marketplace.json        # marketplace manifest
plugins/verified-codegen/              # the plugin
  .claude-plugin/plugin.json
  skills/verified-codegen/SKILL.md
  agents/*.md                          # 10 role subagents
  hooks/hooks.json, guard_git.py       # git-safety guard
  commands/verify-build.md
```

MIT licensed.

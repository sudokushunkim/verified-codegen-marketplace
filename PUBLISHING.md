# Publishing & registering this plugin

All plugin files are ready. Because the files were authored inside a sandbox,
re-initialize git on **your own machine** for a clean repo, then push to GitHub.

## 1. Clean re-init (run in Terminal on your Mac)
```bash
cd ~/Documents/Claude/Projects/이직/verified-codegen-marketplace
rm -rf .git                      # drop the sandbox-created repo (stray locks)
git init -b main
git add -A
git commit -m "feat: verified-codegen multi-agent pipeline plugin + marketplace"
```

## 2. Create the GitHub repo and push

**Option A — GitHub CLI (easiest):**
```bash
# one-time: brew install gh && gh auth login
gh repo create verified-codegen-marketplace --public --source=. --remote=origin --push
```

**Option B — web + git:**
1. Create a new PUBLIC repo on github.com named `verified-codegen-marketplace` (no README/license — you already have them).
2. Then:
```bash
git remote add origin https://github.com/<your-username>/verified-codegen-marketplace.git
git push -u origin main
```

## 3. Install the plugin (you, or anyone)

From Claude Code / Cowork:
```
/plugin marketplace add <your-username>/verified-codegen-marketplace
/plugin install verified-codegen@verified-codegen-marketplace
```
- `marketplace add` accepts `owner/repo`, a full Git URL, or a local path.
- After installing, restart the session if prompted so the skill, agents, and hook load.

### Use it
- Just ask: "implement …", "add an endpoint …", "build a feature that …" → the
  `verified-codegen` skill auto-triggers.
- Or run it explicitly: `/verify-build <your request>`.

## 4. Update later
```bash
# edit files, then:
git add -A && git commit -m "…" && git push
```
Bump `version` in `plugins/verified-codegen/.claude-plugin/plugin.json` for releases.
Users update with `/plugin marketplace update verified-codegen-marketplace`.

## Requirements
- The git-safety hook (`hooks/guard_git.py`) needs `python` on PATH (cross-platform).
- Tested behavior: blocks `git push`, `git push --force`, `git reset`; allows commit, revert, worktree.

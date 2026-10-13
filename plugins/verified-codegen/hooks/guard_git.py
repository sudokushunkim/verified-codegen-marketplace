#!/usr/bin/env python3
"""verified-codegen git-safety guard (PreToolUse, matcher: Bash).

Blocks dangerous git operations so the pipeline can never rewrite or publish
history on its own:
  - git push            (no auto-publishing)
  - git push --force/-f (never)
  - git reset           (use `git revert` to keep history)

Commits are allowed. Reads the PreToolUse payload on stdin and, when a command
should be blocked, denies it via the PreToolUse permission-decision schema.
"""
import sys, json, re

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # not our payload; don't interfere

    cmd = ((data.get("tool_input") or {}).get("command") or "")
    low = cmd.lower()

    reason = None
    if re.search(r'(^|[\s;&|(])git\s+push\b', low):
        if re.search(r'(--force\b|--force-with-lease\b|\s-f\b)', low):
            reason = "force-push is permanently disabled by the verified-codegen pipeline."
        else:
            reason = "push is disabled: the pipeline commits locally but never publishes. Push manually when you're ready."
    elif re.search(r'(^|[\s;&|(])git\s+reset\b', low):
        reason = "git reset is disabled to protect history. Use 'git revert' instead."

    if reason:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "[verified-codegen] " + reason
            }
        }))
        sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()

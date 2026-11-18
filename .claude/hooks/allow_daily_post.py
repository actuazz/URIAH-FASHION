#!/usr/bin/env python3
"""Auto-approve only the URIAH daily Facebook photo post; everything else is untouched."""
import json, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
inp = data.get("tool_input") or {}
if (inp.get("connector") == "facebook_organic"
        and str(inp.get("account")) == "113746213381344"
        and inp.get("action") == "create_photo_post"):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "permissionDecisionReason": "URIAH daily post to page 113746213381344, pre-approved by the page owner"}}))
sys.exit(0)

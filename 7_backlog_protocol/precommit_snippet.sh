# --- the backlog views cannot go stale -------------------------------------
#
# Paste this into the repo's pre-commit hook, above its final `exit`.
# It assumes the hook has already collected the staged file list, e.g.:
#     staged=$(git diff --cached --name-only --diff-filter=ACM)
# and is tracking failures in `$fail`. Adjust those two names to match.
#
# WHY THIS EXISTS. BACKLOG.html (and the optional BACKLOG.md) are generated from backlog.json
# and never edited by hand. A commit that changes the list and leaves the
# human-readable copies behind is how a backlog stops being believed: the file
# people actually read says something the canonical file no longer does, and
# nothing announces the difference.
#
# backlog.json is re-staged too, because the renderer corrects the
# `total_tasks` and `next_id` counters from the tasks array when they have
# drifted — and a correction that is not staged is undone by the next run.

if echo "$staged" | grep -q '^0_context/protocol/backlog\.json$'; then
  if python3 scripts/render_backlog.py >/dev/null; then
    git add 0_context/protocol/backlog.json 0_context/protocol/BACKLOG.html
    # BACKLOG.md is optional (render_backlog.py --md); re-stage it only if the repo keeps one.
    [ -f 0_context/protocol/BACKLOG.md ] && git add 0_context/protocol/BACKLOG.md
  else
    echo "BLOCKED: could not regenerate the backlog views from backlog.json." >&2
    fail=1
  fi
fi

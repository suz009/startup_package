Paste into the target repo's `CLAUDE.md`, under whatever heading holds the other protocols.
Adjust the documentation artefact named in the last bullet to whatever this project actually
shows its users — a help screen, a README, a runbook, a quick-start.

---

- Follow `0_context/protocol/BACKLOG_PROTOCOL.md` for all future work. The canonical list is
  `0_context/protocol/backlog.json`; `BACKLOG.md` and `BACKLOG.html` are **generated** by
  `python3 scripts/render_backlog.py` and must never be edited by hand. Every task is recorded
  twice — in the session summary where it arose, for context, and in the backlog, for
  visibility — and both are required. Regenerate the views before any commit that changes the
  JSON.
- **Search the backlog before writing a new task.** The question is not "what task describes
  this?" but "does a task already own this ground?" — amend the existing one rather than
  creating a second beside it.
- **Take the next task id from the highest id present in the array, plus one.** Never from
  `metadata.next_id`: it is maintained by hand, it drifts, and a reused id silently
  reattributes work to a task somebody has already referred to.
- Read `0_context/protocol/BACKLOG.md` at session start, sweep it at session start and end,
  and surface any `mvp`-priority open tasks that bear on the day's objectives.
- **Check [THE PROJECT'S USER-FACING DOCUMENTATION] at the start and end of every session**
  against what the project actually does. Nothing keeps it in step automatically, and
  documentation that lies is worse than none, because it is believed.

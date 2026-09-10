# Feature 5: Pre-Commit JSON Hook

**Audience:** an LLM agent (or a human) installing this feature into a new repo.

**What this feature gives the new repo:** a git pre-commit hook that blocks
any staged `.claude/*.json` file from being committed if the JSON is invalid.
Standalone-usable; designed as a belt-and-suspenders companion to Feature 4.

---

## Why this exists

In the parent repo, `.claude/settings.local.json` was force-tracked and got
malformed during a cross-machine merge (commit `8bee8a3`, 2026-04-22):
multi-line bash commands got split on `;`, `awk` quotes got double-doubled,
and a paren got dropped. Result: invalid JSON silently committed to git.
Claude Code then ignored the file (since it couldn't parse it), permission
prompts spiked, and the user had to manually reconstruct the file.

Feature 4's structural fix (untrack `.claude/`) prevents this scenario.
This feature is the catch-it-anyway safeguard.

---

## What the hook does

On every `git commit`:
1. Check whether any staged file matches `.claude/*.json`.
2. If yes, validate each with `python3 -m json.tool`.
3. If any is invalid, block the commit with a clear error message.
4. If all valid (or none staged), proceed normally.

---

## Files in this subfolder

| File | What it is | What to do with it |
|---|---|---|
| `README.md` | This file. | Read, then delete after install. |
| `pre-commit` | The hook script. | Copy to `<target>/.git/hooks/pre-commit`, `chmod +x`. |

---

## Install steps (LLM agent: execute these in order)

### Step 1 — Copy the hook
```bash
cp pre-commit <target>/.git/hooks/pre-commit
chmod +x <target>/.git/hooks/pre-commit
```

### Step 2 — Smoke-test
```bash
mkdir -p /tmp/_hooktest/.claude
echo '{"broken":' > /tmp/_hooktest/.claude/settings.local.json
cd /tmp/_hooktest
git init -q
cp <target>/.git/hooks/pre-commit .git/hooks/pre-commit
git add -f .claude/settings.local.json
git -c user.email=t@t -c user.name=t commit -m "test invalid json"
# Expected: ERROR: .claude/settings.local.json is not valid JSON. Pre-commit blocked.
rm -r /tmp/_hooktest
```

### Step 3 — Delete this subfolder
Once installed, delete from target repo.

---

## Limitations

- **Per-repo, not global.** `.git/hooks/` is a directory inside the repo's
  `.git/` folder; it is not committed and does not propagate when the repo
  is cloned. Each clone needs the hook reinstalled. To enforce
  organizationally, look at `core.hooksPath` (a git config that points all
  repos at a shared hooks directory).
- **Doesn't catch corruption that happens *during* a merge** (the merge
  produces uncommitted working-tree changes; the hook only fires on commit).
  If you `git pull`, the merge can produce malformed JSON in the working
  tree. Your safety net is then the architecture from Feature 4: with
  `.claude/*.json` untracked, there's no merge to corrupt them in the first
  place.
- **Validates only `.claude/*.json`.** Easy to extend — see the regex in the
  hook script. Suggested extension: validate any `.json` file under
  `0_context/`.

---

## Cross-feature notes

- **Feature 4 (Claude settings):** the structural fix that this hook
  defends. With Feature 4 in place, the conditions for this hook to ever
  fire are vanishingly rare (someone would have to `git add -f` a
  `.claude/*.json` file, undoing Feature 4's untracking). The hook is
  cheap insurance.

---

## How to know it worked

After install:
- `<target>/.git/hooks/pre-commit` exists and is executable.
- The smoke test in Step 2 produces the expected blocking message.
- Normal commits (no staged `.claude/*.json`) are unaffected.

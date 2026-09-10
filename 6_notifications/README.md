# Feature 6: VS Code / Desktop Notifications

**Audience:** an LLM agent (or a human) installing this feature into a new repo.

**What this feature gives:** a hook that fires a desktop notification
whenever Claude Code needs the user's attention (permission prompt,
elicitation dialog, idle timeout). So you don't have to keep checking
the terminal.

**Note on parent repo state:** during this feature's creation it was
discovered that `~/.claude/hooks/vscode-notify.sh` was *referenced* in
the global Claude Code settings but the script file did not actually
exist on disk — meaning notifications had not been firing for the user.
This package includes a working script.

---

## What this feature does

Three Claude Code notification events trigger a desktop alert:

| Event | When it fires |
|---|---|
| `permission_prompt` | Claude is asking permission to run a tool |
| `elicitation_dialog` | Claude needs user input via a dialog |
| `idle_prompt` | Claude has been waiting on the user for a while |

The hook script (`vscode-notify.sh`) translates the event into a desktop
notification using whichever mechanism is available on the platform.

---

## Files in this subfolder

| File | What it is | What to do with it |
|---|---|---|
| `README.md` | This file. | Read, then delete after install. |
| `vscode-notify.sh` | The hook script. Cross-platform: tries `notify-send`, then BurntToast (WSL→Windows), then terminal bell. | Install to `~/.claude/hooks/vscode-notify.sh`. |
| `hook_config_snippet.json` | The JSON hook block for `~/.claude/settings.json`. | Merge into `~/.claude/settings.json`. |

---

## Install steps (LLM agent: execute these in order)

### Step 1 — Install the script
```bash
mkdir -p ~/.claude/hooks
cp vscode-notify.sh ~/.claude/hooks/vscode-notify.sh
chmod +x ~/.claude/hooks/vscode-notify.sh
```

### Step 2 — Verify the script runs
```bash
~/.claude/hooks/vscode-notify.sh "Test notification" "This is a smoke test"
```
You should see a desktop notification (or hear a terminal bell as
fallback).

### Step 3 — Wire the hook into `~/.claude/settings.json`
Open `~/.claude/settings.json`. If it already has a `hooks` section
matching the snippet in `hook_config_snippet.json`, you're done. If not,
merge the snippet in (preserving any existing keys).

The snippet wires three events (`permission_prompt`, `elicitation_dialog`,
`idle_prompt`) all to the same script. You can drop any event you don't
want to be notified about.

### Step 4 — Reload Claude Code
Restart any active Claude Code sessions so the new hook config takes effect.

### Step 5 — Test in-context
In a Claude Code session, trigger a permission prompt (e.g. ask Claude to
run a not-pre-approved bash command). You should get a desktop
notification.

### Step 6 — Delete this subfolder
Once installed, delete from target repo.

---

## Platform notes

The script tries notification mechanisms in this order:
1. **`notify-send`** (Linux desktop, if `libnotify` is installed and a
   notification daemon like `dunst` / GNOME Shell / KDE Plasma is running).
2. **`osascript`** (macOS native).
3. **PowerShell BurntToast** (WSL2 → Windows, if BurntToast is installed:
   `Install-Module -Name BurntToast` from an admin PowerShell).
4. **Terminal bell** (`printf '\a'`) — last-ditch fallback. Visible only
   if your terminal is in focus.

### WSL2 specifics
- `notify-send` typically does NOT work out-of-the-box in WSL2 (no display
  server / no notification daemon).
- BurntToast via PowerShell is the most reliable WSL→Windows path. To set
  it up, run from an admin PowerShell on Windows:
  ```powershell
  Install-Module -Name BurntToast -Force
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
  Then test from WSL:
  ```bash
  powershell.exe -Command "New-BurntToastNotification -Text 'test'"
  ```

### macOS
`notify-send` won't work; `osascript` will. The script auto-detects.

### Linux native (not WSL)
Install `libnotify-bin` (Debian/Ubuntu) or your distro's equivalent so
`notify-send` is available. A notification daemon (`dunst`, GNOME Shell,
KDE Plasma) must also be running.

---

## Cross-feature notes

- **Feature 4 (Claude settings):** the hook config goes into the global
  `~/.claude/settings.json` from Feature 4. If you skipped Feature 4, you
  can put the hook block into any active Claude settings file (project or
  local), but global is the natural home since the script lives in
  `~/.claude/hooks/`.

---

## How to know it worked

After install:
- `~/.claude/hooks/vscode-notify.sh` exists and is executable.
- Manual test (`Step 2`) produces a visible/audible notification.
- `~/.claude/settings.json` contains the hook block referencing the script.
- In a fresh Claude Code session, triggering a permission prompt produces
  a desktop notification.

---

## Customization

The script accepts two args: `$1` = title, `$2` = message body. To change
the notification appearance (icon, urgency, sound), edit the relevant
branch of the script (`notify-send`, `osascript`, or BurntToast call).

To add new events: append more `Notification` matchers in
`~/.claude/settings.json`. Each can call the same script with a different
title to distinguish them in the notification:

```json
{
  "matcher": "tool_use_complete",
  "hooks": [{ "type": "command", "command": "~/.claude/hooks/vscode-notify.sh 'Tool done' 'Task complete'" }]
}
```

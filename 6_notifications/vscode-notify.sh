#!/usr/bin/env bash
# vscode-notify.sh — Cross-platform desktop notification helper.
# Used as a Claude Code hook. Tries multiple notification backends and
# falls back to a terminal bell.
#
# Usage:
#   vscode-notify.sh [TITLE] [MESSAGE]
#
# Defaults: TITLE="Claude Code", MESSAGE="needs your attention"

TITLE="${1:-Claude Code}"
MESSAGE="${2:-needs your attention}"

# 1) Linux notify-send (also works in some Linux desktops; usually NOT in WSL2)
if command -v notify-send >/dev/null 2>&1; then
  if notify-send "$TITLE" "$MESSAGE" 2>/dev/null; then
    exit 0
  fi
fi

# 2) macOS osascript
if command -v osascript >/dev/null 2>&1; then
  osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\"" 2>/dev/null && exit 0
fi

# 3) WSL2 → Windows via PowerShell BurntToast
if command -v powershell.exe >/dev/null 2>&1; then
  # Escape single quotes for PowerShell string literals
  ps_title=$(printf "%s" "$TITLE" | sed "s/'/''/g")
  ps_message=$(printf "%s" "$MESSAGE" | sed "s/'/''/g")
  powershell.exe -NoProfile -Command "New-BurntToastNotification -Text '$ps_title','$ps_message'" 2>/dev/null && exit 0
fi

# 4) Last-ditch: terminal bell
printf '\a'
exit 0

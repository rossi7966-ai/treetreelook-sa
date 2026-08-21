#!/bin/sh
# segment-commit-guard.sh — Stop hook:回合結束前未提交異動攔截。
# 承載 AI_Rules §6.3-3(段落存檔)之機械層;義務字面見該檔,本 hook 不另立規則。
INPUT=$(cat)
printf '%s' "$INPUT" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true' && exit 0
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  echo "回合結束攔截:工作樹有未提交異動。依 AI_Rules §6.3-3 先落段落 commit(或還原點 commit);收工紀錄依 §7-5 單獨提交。落完再結束回合。" >&2
  exit 2
fi
exit 0

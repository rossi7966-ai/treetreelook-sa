#!/usr/bin/env python3
"""MetaUI UIV 檢核入口(PREP-UI-1,info_level: Candidate)

Usage:
    python .metaui/UI_KIT/checks/run_checks.py --gate G0|G1|G2|all --scope <路徑> [--format text|json]

- scope 可為專案根或單一 F 模組目錄;預設當前目錄
- exit code(VerifyReportSchema §三): 0=無 fail/parse-error, 1=有 fail, 2=有 parse-error/工具錯誤
"""
import argparse
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uiv_common import Reporter, find_project_root, find_f_modules, find_all_f_dirs
from uiv_checks import CHECKS

GATES = {
    "G0": ["UIV-02", "UIV-04", "UIV-09"],
    "G1": ["UIV-01", "UIV-02", "UIV-03", "UIV-04", "UIV-08", "UIV-09", "UIV-12"],
    "G2": ["UIV-05", "UIV-06", "UIV-07", "UIV-11"],
}
GATES["all"] = ["UIV-0%d" % i for i in range(1, 10)] + ["UIV-11", "UIV-12"]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", choices=["G0", "G1", "G2", "all"], default="all")
    ap.add_argument("--scope", default=".")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    scope = os.path.abspath(args.scope)
    project = find_project_root(scope)
    if project is None:
        print("scope 上下層找不到 DesignSpecs/，無法定位專案根: %s" % scope)
        return 2
    repo_id = os.path.basename(project)
    rep = Reporter(repo_id)

    f_dirs = find_f_modules(scope, project)
    if not f_dirs:
        f_dirs = find_all_f_dirs(project)

    for pid in GATES[args.gate]:
        try:
            CHECKS[pid](rep, project, f_dirs)
        except Exception:
            rep.perror(pid, scope, "檢核自身異常: %s" % traceback.format_exc().strip().splitlines()[-1])

    out = rep.emit_text(args.gate, os.path.relpath(scope, project) or ".") if args.format == "text" \
        else rep.emit_json(args.gate, os.path.relpath(scope, project) or ".")
    print(out)
    return rep.exit_code()


if __name__ == "__main__":
    sys.exit(main())

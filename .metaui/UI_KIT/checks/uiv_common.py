#!/usr/bin/env python3
"""MetaUI UIV 檢核共用層(PREP-UI-1,info_level: Candidate)

報告格式: VerifyReportSchema v1.0(MetaCore TRAINER/CONTEXT/10_SHARED)
實作紀律: VerifyImplGuide v1.0 §四(分段解析容錯 / refs 排除 / fail 與 needs-review 分流)
"""
import os
import re
import json
from datetime import datetime, timezone
from html.parser import HTMLParser

SCHEMA_VERSION = "1.0"
SCHEMA_REF = "VerifyReportSchema v1.0 @ MetaCore 10_SHARED (PREP 期字面對齊,frozen-pin 待 Trainer 補登)"
IMPLEMENTATION_ID = "UI_KIT/checks v0.7 (PREP-UI-2)"
EXCLUDE_DIRS = {"refs", "temp-refs", "_templates", "templates", "node_modules", ".git", "_prep", ".metaui", ".metasa", ".claude"}
VOID_TAGS = {"br", "img", "input", "meta", "link", "hr", "area", "base", "col", "embed", "source", "track", "wbr"}

CLASS_ORDER = ["fail", "parse-error", "needs-review", "allowed-exception", "pass"]


class Reporter:
    def __init__(self, repo_id):
        self.repo_id = repo_id
        self.findings = []
        self._seq = {}

    def add(self, pattern_id, classification, target, detail="", **extra):
        n = self._seq.get(pattern_id, 0) + 1
        self._seq[pattern_id] = n
        f = {
            "result_id": "%s-%s-%04d" % (self.repo_id, pattern_id.replace("-", ""), n),
            "pattern_id": pattern_id,
            "classification": classification,
            "target": target,
            "detail": detail,
        }
        f.update(extra)
        self.findings.append(f)

    def fail(self, p, target, detail):
        self.add(p, "fail", target, detail)

    def ok(self, p, target, detail=""):
        self.add(p, "pass", target, detail)

    def review(self, p, target, review_reason):
        self.add(p, "needs-review", target, review_reason, review_reason=review_reason)

    def perror(self, p, target, detail):
        self.add(p, "parse-error", target, detail)

    def summary_status(self):
        cls = {f["classification"] for f in self.findings}
        if "parse-error" in cls:
            return "error"
        if "fail" in cls:
            return "fail"
        if "needs-review" in cls:
            return "needs-review"
        if "allowed-exception" in cls:
            return "pass-with-exceptions"
        return "pass"

    def exit_code(self):
        cls = {f["classification"] for f in self.findings}
        if "parse-error" in cls:
            return 2
        if "fail" in cls:
            return 1
        return 0

    def emit_text(self, gate, scope):
        lines = []
        lines.append("=== MetaUI UIV 檢核報告 ===")
        lines.append("repo_id: %s | gate: %s | scope: %s" % (self.repo_id, gate, scope))
        lines.append("schema_version: %s | %s" % (SCHEMA_VERSION, SCHEMA_REF))
        lines.append("implementation_id: %s" % IMPLEMENTATION_ID)
        lines.append("execution_timestamp: %s" % datetime.now(timezone.utc).isoformat(timespec="seconds"))
        lines.append("-" * 60)
        counts = {}
        for c in CLASS_ORDER:
            group = [f for f in self.findings if f["classification"] == c]
            counts[c] = len(group)
            show = group if c != "pass" else group  # pass 也列出(每檢核一筆彙總,不逐項)
            for f in show:
                lines.append("[%s] %s %s | %s" % (f["classification"], f["result_id"], f["target"], f["detail"]))
        lines.append("-" * 60)
        lines.append("counts: " + " / ".join("%s=%d" % (c, counts[c]) for c in CLASS_ORDER))
        lines.append("summary_status: %s" % self.summary_status())
        return "\n".join(lines)

    def emit_json(self, gate, scope):
        return json.dumps({
            "repo_id": self.repo_id,
            "schema_version": SCHEMA_VERSION,
            "schema_ref": SCHEMA_REF,
            "implementation_id": IMPLEMENTATION_ID,
            "execution_timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "gate": gate,
            "scope": scope,
            "results": self.findings,
            "summary_status": self.summary_status(),
        }, ensure_ascii=False, indent=2)


# ── 檔案系統 ──────────────────────────────────────────────

def read_text(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def find_project_root(scope):
    """scope 或其上層中含 DesignSpecs/ 者為專案根;找不到回 None。"""
    p = os.path.abspath(scope)
    while True:
        if os.path.isdir(os.path.join(p, "DesignSpecs")):
            return p
        parent = os.path.dirname(p)
        if parent == p:
            return None
        p = parent


def find_f_modules(scope, project_root):
    """回傳含 ui/ 的 F 模組目錄清單;scope 指向單一 F 目錄時只回它(即使尚無 ui/)。"""
    scope = os.path.abspath(scope)
    if os.path.basename(scope).startswith("F") and os.path.isdir(scope):
        return [scope]
    found = []
    walk_root = scope if os.path.isdir(scope) else project_root
    for root, dirs, _files in os.walk(walk_root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        if "ui" in dirs and re.match(r"F\d+", os.path.basename(root) or ""):
            found.append(root)
    return found


def find_all_f_dirs(project_root):
    """DesignSpecs 下所有 F## 目錄(不要求已有 ui/),供 G0 掃描。"""
    ds = os.path.join(project_root, "DesignSpecs")
    found = []
    for root, dirs, _files in os.walk(ds):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        base = os.path.basename(root)
        if re.match(r"F\d+_", base):
            found.append(root)
    return found


# ── Markdown 解析 ─────────────────────────────────────────

def parse_md_tables(text):
    """回傳所有 markdown 表格,各為 {headers:[...], rows:[[...],...]}。分段容錯。"""
    tables = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|?\s*$", lines[i + 1]):
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                rows.append(cells)
                j += 1
            tables.append({"headers": headers, "rows": rows})
            i = j
        else:
            i += 1
    return tables


def col_index(headers, *keywords):
    """依關鍵字尋欄位索引;關鍵字依序優先(先精確詞後寬鬆詞,避免「首訪路徑」搶「檔案路徑」);找不到回 -1。"""
    for kw in keywords:
        for idx, h in enumerate(headers):
            if kw in h:
                return idx
    return -1


def cell(row, idx):
    return row[idx].strip() if 0 <= idx < len(row) else ""


# ── 頁面 HTML 解析 ────────────────────────────────────────

class PageParser(HTMLParser):
    """收集 UIV 所需屬性;以堆疊追蹤 data-state 巢狀歸屬。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.metas = {}
        self.links = []          # {href, data_nav}
        self.stylesheets = []    # <link rel=stylesheet href>
        self.data_w = []
        self.data_term = []
        self.data_tbd = []
        self.states = []         # data-state 值(依出現序)
        self.state_na = {}       # 狀態 -> reason
        self.primary_by_state = {}
        self.primary_outside = 0
        self.style_blocks = []
        self.inline_styles = []
        self._stack = []         # (tag, state or None)
        self._in_style = False

    def _cur_state(self):
        for tag, st in reversed(self._stack):
            if st:
                return st
        return None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        state = a.get("data-state")
        if tag == "meta" and a.get("name"):
            self.metas[a["name"]] = a.get("content", "")
        if tag == "link" and a.get("rel") == "stylesheet":
            self.stylesheets.append(a.get("href", ""))
        if tag == "a":
            self.links.append({"href": a.get("href", ""), "data_nav": a.get("data-nav")})
        if "data-w" in a:
            self.data_w.append(a["data-w"])
        if "data-term" in a:
            self.data_term.append(a["data-term"])
        if "data-tbd" in a:
            self.data_tbd.append(a["data-tbd"])
        if "data-state-na" in a:
            self.state_na[a["data-state-na"]] = a.get("data-reason", "")
        if state:
            self.states.append(state)
        if a.get("data-action") == "primary":
            cur = state or self._cur_state()
            if cur:
                self.primary_by_state[cur] = self.primary_by_state.get(cur, 0) + 1
            else:
                self.primary_outside += 1
        if "style" in a:
            self.inline_styles.append(a["style"])
        if tag == "style":
            self._in_style = True
            self.style_blocks.append("")
        if tag not in VOID_TAGS:
            self._stack.append((tag, state))

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                break

    def handle_data(self, data):
        if self._in_style and self.style_blocks:
            self.style_blocks[-1] += data


def parse_page(path):
    p = PageParser()
    p.feed(read_text(path))
    return p

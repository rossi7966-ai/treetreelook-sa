#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MetaUI FlowMap 生成器(PREP-UI-2,info_level: Candidate)

把 10_UIFlow.md 的頁面登記表+mermaid 頁面流，連同頁面實掃結果，
煮成一張可點的「縮圖級 storyboard」:ui/00_FlowMap.html。

- 節點=登記表頁面卡(P## 編號+頁名+主任務+階段+縮圖;點卡開實頁，proto 優先)
- 邊=雙源對照:
    宣告邊 = mermaid 頁面流(設計意圖)
    實掃邊 = 頁面 <a data-nav> 連結(實作事實)
  分類規則:
    骨架邊 = nav/header/footer 祖先內的連結(全站導覽列/麵包屑/頁尾)——供宣告邊求證，不入差異
    逃生邊 = 僅出現於非 ideal 態(blank/loading/partial/error)的內容區連結——狀態設計，單獨列表
    雙源一致 / 骨架承載 / 宣告未實作 / 實掃未宣告(ideal 級)=對照結果，後二者為審查發現候選
- 縮圖:--capture 以 headless Edge 截取頁面初始畫面，嵌入 base64;無縮圖時灰佔位

R 層視覺輔件:每輪重生(縮圖非確定性)，不入 UIV-06 新鮮度;不得單獨作 pass/fail 依據。

Usage:
    python gen_flowmap.py --scope <F 模組目錄> [--capture] [--thumbs <目錄>] [--out <檔>]
"""
import argparse
import base64
import os
import re
import subprocess
import sys
import urllib.parse
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uiv_common import read_text, find_project_root, VOID_TAGS
from uiv_checks import registry_rows, flow_path, pages_of

HEADER = "生成物(R 層視覺輔件)，禁手改;重生成:python .metaui/UI_KIT/checks/gen_flowmap.py --scope <F 模組> --capture"

NODE_DEF_RE = re.compile(r'^\s*(\w+)\["([^"]+)"\]')
EDGE_RE = re.compile(r'^\s*(\w+)\s*(-->|-\.->)\s*(?:\|"([^"]*)"\|\s*)?(\w+)\s*$')
P_ID_RE = re.compile(r"^P\d+$")
SKELETON_TAGS = {"nav", "header", "footer"}
NON_IDEAL = {"blank", "loading", "partial", "error"}

# 卡片幾何(px;輸出 HTML 專屬，非頁面樣式，UIV-05 不轄)
CARD_W, CARD_H = 248, 236
EXT_W, EXT_H = 220, 72
GAP_X, GAP_Y, MARGIN = 128, 44, 40


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── mermaid 宣告邊 ────────────────────────────────────────

def parse_mermaid(flow_text):
    """回 (node_labels{id:label}, edges[{src,dst,label,dashed}])。"""
    blocks = re.findall(r"```mermaid(.*?)```", flow_text, re.S)
    labels, edges = {}, []
    for b in blocks:
        for ln in b.splitlines():
            m = NODE_DEF_RE.match(ln)
            if m:
                labels[m.group(1)] = m.group(2)
                continue
            m = EDGE_RE.match(ln)
            if m and not ln.strip().startswith("click"):
                edges.append({"src": m.group(1), "dst": m.group(4),
                              "label": m.group(3) or "", "dashed": m.group(2) == "-.->"})
    return labels, edges


# ── 頁面實掃邊 ────────────────────────────────────────────

class EdgeScanner(HTMLParser):
    """收集 <a data-nav>:目標/字面/是否骨架(nav·header·footer 祖先)/所在狀態。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found = []   # {nav, text, skel, state}
        self._stack = []  # (tag, state, is_skel)
        self._link = None

    def _ctx(self):
        state, skel = None, False
        for tag, st, sk in self._stack:
            if st:
                state = st
            if sk:
                skel = True
        return state, skel

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        state = a.get("data-state")
        if tag not in VOID_TAGS:
            self._stack.append((tag, state, tag in SKELETON_TAGS))
        if tag == "a" and a.get("data-nav"):
            st, skel = self._ctx()
            self._link = {"nav": a["data-nav"], "text": [], "skel": skel, "state": st or "(頁面層)"}

    def handle_endtag(self, tag):
        if tag == "a" and self._link is not None:
            self._link["text"] = re.sub(r"\s+", " ", " ".join(self._link["text"])).strip()
            self.found.append(self._link)
            self._link = None
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                break

    def handle_data(self, data):
        if self._link is not None:
            self._link["text"].append(data)


def scan_pages(pages):
    """回 (content{}, skeleton{}):{(src,key):{text,states}};key=('P',pid)/('EXT'，名)/('W99',)。"""
    content, skeleton = {}, {}
    for pg in pages:
        m = re.match(r"(P\d+)", os.path.basename(pg))
        if not m:
            continue
        src = m.group(1)
        sc = EdgeScanner()
        sc.feed(read_text(pg))
        for lk in sc.found:
            nav = lk["nav"]
            if nav.startswith("external:"):
                key = ("EXT", nav.split(":", 1)[1])
            elif nav == "W99":
                key = ("W99",)
            elif P_ID_RE.match(nav):
                if nav == src:
                    continue
                key = ("P", nav)
            else:
                continue
            bucket = skeleton if lk["skel"] else content
            rec = bucket.setdefault((src, key), {"text": lk["text"], "states": set()})
            rec["states"].add(lk["state"])
    return content, skeleton


# ── 雙源對照 ──────────────────────────────────────────────

def _ext_name_match(name, label):
    a, b = name.strip(), label.replace("外部:", "").strip()
    return a and b and (a in b or b in a)


def _find_hit(src, dst, node_labels, bucket, used):
    """在 bucket 中為宣告邊找對應實掃邊;命中回 key，否則 None。"""
    if P_ID_RE.match(dst):
        k = (src, ("P", dst))
        return k if k in bucket and k not in used else None
    lbl = node_labels.get(dst, dst)
    if dst.startswith("W99") or dst.startswith("GHOST"):
        k = (src, ("W99",))
        return k if k in bucket and k not in used else None
    cands = [k for k in bucket if k not in used and k[0] == src and k[1][0] == "EXT"]
    for k in cands:
        if _ext_name_match(k[1][1], lbl):
            return k
    return None


def match_edges(declared, content, skeleton, node_labels):
    """回 (rows, missing, undeclared, escapes)。
    rows[{src,dst,label,dashed,status}];status=both/skeleton/declared-only。
    外部邊名稱不中時，同 src 單一未匹配宣告×單一未匹配實掃=回退配對。"""
    used_c, used_s = set(), set()
    rows = []
    for e in declared:
        hit = _find_hit(e["src"], e["dst"], node_labels, content, used_c)
        status = "both"
        if hit:
            used_c.add(hit)
        else:
            hit = _find_hit(e["src"], e["dst"], node_labels, skeleton, used_s)
            if hit:
                used_s.add(hit)
                status = "skeleton"
            else:
                status = "declared-only"
        rows.append(dict(e, status=status))
    # 外部邊單一回退配對(名稱異寫救濟)
    for r in rows:
        if r["status"] != "declared-only" or P_ID_RE.match(r["dst"]):
            continue
        rem_decl = [x for x in rows if x["src"] == r["src"] and x["status"] == "declared-only"
                    and not P_ID_RE.match(x["dst"])]
        rem_scan = [k for k in content if k not in used_c and k[0] == r["src"] and k[1][0] == "EXT"]
        if len(rem_decl) == 1 and len(rem_scan) == 1:
            used_c.add(rem_scan[0])
            r["status"] = "both"
    undeclared, escapes = [], []
    for k, rec in sorted(content.items(), key=lambda x: (x[0][0], str(x[0][1]))):
        if k in used_c:
            continue
        src, key = k
        dst_disp = key[1] if key[0] == "P" else ("外部:" + key[1] if key[0] == "EXT" else "W99")
        item = {"src": src, "dst": dst_disp, "label": rec["text"], "states": sorted(rec["states"])}
        if rec["states"] & NON_IDEAL and not (rec["states"] - NON_IDEAL):
            escapes.append(item)   # 僅非 ideal 態=狀態設計的逃生邊
        else:
            undeclared.append(item)
    return rows, [r for r in rows if r["status"] == "declared-only"], undeclared, escapes


# ── 版面(BFS 欄位)─────────────────────────────────────────

def layout(reg_ids, declared):
    adj = {}
    for e in declared:
        if P_ID_RE.match(e["src"]) and P_ID_RE.match(e["dst"]):
            adj.setdefault(e["src"], []).append(e["dst"])
    root = reg_ids[0] if reg_ids else None
    depth = {root: 0} if root else {}
    q = [root] if root else []
    while q:
        cur = q.pop(0)
        for nxt in adj.get(cur, []):
            if nxt in reg_ids and nxt not in depth:
                depth[nxt] = depth[cur] + 1
                q.append(nxt)
    maxd = max(depth.values()) if depth else 0
    for pid in reg_ids:
        depth.setdefault(pid, maxd)
    return depth, max(depth.values()) if depth else 0


# ── 縮圖 ──────────────────────────────────────────────────

def find_edge_exe():
    cands = [os.environ.get("EDGE_PATH", ""),
             r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
             r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]
    for p in cands:
        if p and os.path.isfile(p):
            return p
    import shutil
    return shutil.which("msedge") or shutil.which("microsoft-edge")


def capture_thumbs(targets, thumbs_dir):
    exe = find_edge_exe()
    if not exe:
        print("⚠️ 找不到 Edge，略過截圖(可設 EDGE_PATH)")
        return
    os.makedirs(thumbs_dir, exist_ok=True)
    for pid, path in targets.items():
        out = os.path.abspath(os.path.join(thumbs_dir, "%s.png" % pid))
        url = "file:///" + urllib.parse.quote(os.path.abspath(path).replace("\\", "/"), safe="/:")
        try:
            subprocess.run([exe, "--headless", "--disable-gpu", "--hide-scrollbars",
                            "--window-size=1280,800", "--screenshot=%s" % out, url],
                           capture_output=True, timeout=60)
        except Exception as e:
            print("⚠️ %s 截圖失敗: %s" % (pid, e))


def thumb_b64(thumbs_dir, pid):
    p = os.path.join(thumbs_dir, "%s.png" % pid)
    if not os.path.isfile(p):
        return None
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


# ── HTML 輸出 ─────────────────────────────────────────────

def build_html(f_dir, project, rows_reg, declared, node_labels, matched_rows,
               missing, undeclared, escapes, skeleton_n, thumbs_dir):
    reg_ids = [r["p"] for r in rows_reg]
    reg = {r["p"]: r for r in rows_reg}
    depth, maxd = layout(reg_ids, declared)
    ext_ids = [n for n in node_labels if not P_ID_RE.match(n)]
    ext_col = maxd + 1

    cols = {}
    for pid in reg_ids:
        cols.setdefault(depth[pid], []).append(pid)
    pos = {}
    for c, ids in cols.items():
        for i, pid in enumerate(ids):
            pos[pid] = (MARGIN + c * (CARD_W + GAP_X), MARGIN + i * (CARD_H + GAP_Y), CARD_W, CARD_H)
    for i, nid in enumerate(ext_ids):
        pos[nid] = (MARGIN + ext_col * (CARD_W + GAP_X), MARGIN + i * (EXT_H + 28), EXT_W, EXT_H)
    canvas_w = MARGIN * 2 + ext_col * (CARD_W + GAP_X) + EXT_W
    canvas_h = MARGIN * 2 + max((len(ids) for ids in cols.values()), default=1) * (CARD_H + GAP_Y)
    canvas_h = max(canvas_h, MARGIN * 2 + len(ext_ids) * (EXT_H + 28))

    ui_dir = os.path.join(f_dir, "ui")
    tokens_rel = os.path.relpath(
        os.path.join(project, "DesignSpecs", "UIFoundation", "tokens.css"), ui_dir).replace("\\", "/")

    STATUS = {"both": ("var(--color-primary)", "m-both", ""),
              "skeleton": ("var(--color-divider)", "m-skel", ' stroke-dasharray="2 4"'),
              "declared-only": ("var(--color-error)", "m-miss", "")}

    svg = []
    for r in matched_rows:
        if r["src"] not in pos or r["dst"] not in pos:
            continue
        sx, sy, sw, sh = pos[r["src"]]
        tx, ty, tw, th = pos[r["dst"]]
        x1, y1 = sx + sw, sy + sh / 2
        x2, y2 = tx, ty + th / 2
        back = tx <= sx
        if back:
            y1 = sy + sh
            y2 = ty + th
            c1 = (sx + sw / 2, y1 + 90)
            c2 = (tx + tw / 2, y2 + 90)
            x1, x2 = sx + sw / 2, tx + tw / 2
        else:
            c1 = (x1 + 56, y1)
            c2 = (x2 - 56, y2)
        color, marker, forced_dash = STATUS[r["status"]]
        dash = forced_dash or (' stroke-dasharray="7 5"' if r["dashed"] else "")
        svg.append('<path d="M%.0f %.0f C %.0f %.0f, %.0f %.0f, %.0f %.0f" fill="none" stroke="%s" stroke-width="2"%s marker-end="url(#%s)"/>' % (
            x1, y1, c1[0], c1[1], c2[0], c2[1], x2, y2, color, dash, marker))
        if r["label"] and r["status"] != "skeleton":
            mx = (x1 + 3 * c1[0] + 3 * c2[0] + x2) / 8
            my = (y1 + 3 * c1[1] + 3 * c2[1] + y2) / 8
            svg.append('<text x="%.0f" y="%.0f" class="elabel" style="fill:%s">%s</text>' % (
                mx, my - 6, color, esc(r["label"])))

    cards = []
    for pid in reg_ids:
        r = reg[pid]
        x, y, w, h = pos[pid]
        base = os.path.basename(r["path"]) if r["path"] else ""
        proto_file = os.path.join(ui_dir, "pages", "proto", base)
        href = ("pages/proto/" + base) if base and os.path.isfile(proto_file) else (r["path"] or "#")
        b64 = thumb_b64(thumbs_dir, pid)
        img = ('<img src="data:image/png;base64,%s" alt="%s 縮圖">' % (b64, pid)) if b64 \
            else '<div class="noimg">縮圖未產出(--capture)</div>'
        cards.append(
            '<a class="card" style="left:%dpx;top:%dpx;width:%dpx" href="%s">'
            '%s<div class="body"><div class="pid">%s<span class="stage">%s</span></div>'
            '<div class="name">%s</div><div class="task">%s</div></div></a>' % (
                x, y, w, esc(href), img, esc(pid), esc(r["stage"]), esc(r["name"]), esc(r["task"])))
    for nid in ext_ids:
        x, y, w, h = pos[nid]
        cards.append('<div class="card ext" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
                     '<div class="pid">%s</div><div class="name">%s</div></div>' % (
                         x, y, w, h, esc(nid), esc(node_labels[nid])))

    def tbl(items, kind):
        if not items:
            return "<tr><td colspan='3'>(無)</td></tr>"
        out = []
        for it in items:
            third = esc(",".join(it.get("states", []))) if kind == "scan" else "宣告邊(mermaid)"
            out.append("<tr><td>%s → %s</td><td>%s</td><td>%s</td></tr>" % (
                esc(it["src"]), esc(it["dst"]), esc(it["label"]), third))
        return "\n".join(out)

    n_both = sum(1 for r in matched_rows if r["status"] == "both")
    n_skel_ok = sum(1 for r in matched_rows if r["status"] == "skeleton")
    html = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- %(header)s -->
<title>FlowMap 頁面串接綜覽(%(fbase)s)</title>
<link rel="stylesheet" href="%(tokens)s">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--typography-font-family-sans);background:var(--color-background);color:var(--color-text-body);padding:20px}
h1{font-size:var(--typography-font-size-head2);margin-bottom:6px}
.hint{font-size:var(--typography-font-size-body2);color:var(--color-subtitle);margin-bottom:14px;max-width:960px}
.legend{display:flex;gap:18px;flex-wrap:wrap;font-size:var(--typography-font-size-body2);margin-bottom:14px;align-items:center}
.legend .sw{display:inline-block;width:26px;height:0;border-top:3px solid;vertical-align:middle;margin-right:6px}
.canvas{position:relative;border:1px solid var(--color-divider);border-radius:var(--radius-m);overflow:auto;background:var(--color-surface)}
.inner{position:relative}
svg.wires{position:absolute;inset:0;pointer-events:none}
.elabel{font-size:11px;paint-order:stroke;stroke:var(--color-surface);stroke-width:4px}
.card{position:absolute;display:block;border:1px solid var(--color-divider);border-radius:var(--radius-m);background:var(--color-background);box-shadow:var(--shadow-card);text-decoration:none;color:inherit;overflow:hidden}
.card:hover{border-color:var(--color-primary)}
.card img{width:100%%;height:140px;object-fit:cover;object-position:top;display:block;border-bottom:1px solid var(--color-divider)}
.noimg{height:140px;display:flex;align-items:center;justify-content:center;background:var(--color-surface-variant);color:var(--color-placeholder);font-size:12px}
.body{padding:8px 10px}
.pid{font-weight:700;color:var(--color-primary);font-size:14px}
.stage{float:right;font-weight:400;font-size:11px;border:1px solid var(--color-divider);border-radius:var(--radius-xl);padding:1px 8px;color:var(--color-subtitle)}
.name{font-weight:700;font-size:14px;margin:2px 0}
.task{font-size:11px;color:var(--color-subtitle);line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card.ext{border-style:dashed;background:var(--color-surface-variant);padding:8px 10px}
.card.ext .pid{color:var(--color-subtitle);font-size:11px}
.card.ext .name{font-size:12px;font-weight:400}
h2{font-size:var(--typography-font-size-subtitle2);margin:20px 0 8px}
table{border-collapse:collapse;font-size:var(--typography-font-size-body2)}
td,th{border:1px solid var(--color-divider);padding:4px 10px;text-align:left}
th{background:var(--color-surface-variant)}
</style>
</head>
<body>
<h1>FlowMap 頁面串接綜覽(%(fbase)s)</h1>
<p class="hint">縮圖級 storyboard:點卡開實頁(proto 優先)。邊=宣告(mermaid)×實掃(data-nav)雙源對照;骨架邊(全站導覽/麵包屑/頁尾，%(skel)d 處)供宣告求證不入差異;僅非 ideal 態的內容連結=逃生邊(狀態設計)，單獨列表。R 層視覺輔件，不得單獨作 pass/fail 依據。</p>
<div class="legend">
<span><span class="sw" style="border-color:var(--color-primary)"></span>雙源一致 %(nboth)d</span>
<span><span class="sw" style="border-color:var(--color-divider)"></span>骨架承載 %(nskel)d</span>
<span><span class="sw" style="border-color:var(--color-error)"></span>宣告未實作 %(nmiss)d</span>
<span>實掃未宣告(表列)%(nextra)d</span>
<span>逃生邊(表列)%(nesc)d</span>
<span>虛線=宣告為次要邊(-.->)</span>
</div>
<div class="canvas"><div class="inner" style="width:%(cw)dpx;height:%(ch)dpx">
<svg class="wires" width="%(cw)d" height="%(ch)d">
<defs>
<marker id="m-both" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 z" fill="var(--color-primary)"/></marker>
<marker id="m-skel" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 z" fill="var(--color-divider)"/></marker>
<marker id="m-miss" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 z" fill="var(--color-error)"/></marker>
</defs>
%(svg)s
</svg>
%(cards)s
</div></div>
<h2>雙源差異表(審查發現候選;G1-R/Prototype-R 逐筆處置)</h2>
<table>
<tr><th colspan="3">宣告未實作(mermaid 有、頁面無——含骨架亦無)</th></tr>
<tr><th>邊</th><th>宣告字面</th><th>來源</th></tr>
%(miss_rows)s
<tr><th colspan="3">實掃未宣告(頁面 ideal 級內容連結有、mermaid 無)</th></tr>
<tr><th>邊</th><th>連結字面</th><th>所在狀態</th></tr>
%(extra_rows)s
<tr><th colspan="3">逃生邊(僅非 ideal 態;狀態設計，非旅程主張——覈對用)</th></tr>
<tr><th>邊</th><th>連結字面</th><th>所在狀態</th></tr>
%(esc_rows)s
</table>
</body>
</html>
""" % {
        "header": HEADER, "fbase": esc(os.path.basename(f_dir)), "tokens": esc(tokens_rel),
        "skel": skeleton_n, "nboth": n_both, "nskel": n_skel_ok, "nmiss": len(missing),
        "nextra": len(undeclared), "nesc": len(escapes),
        "cw": canvas_w, "ch": canvas_h, "svg": "\n".join(svg), "cards": "\n".join(cards),
        "miss_rows": tbl(missing, "decl"), "extra_rows": tbl(undeclared, "scan"),
        "esc_rows": tbl(escapes, "scan"),
    }
    return html, n_both, n_skel_ok


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", required=True, help="F 模組目錄")
    ap.add_argument("--capture", action="store_true", help="以 headless Edge 產縮圖")
    ap.add_argument("--thumbs", default=None, help="縮圖目錄(預設 ui/reviews/evidence/flowmap)")
    ap.add_argument("--out", default=None, help="輸出檔(預設 ui/00_FlowMap.html)")
    args = ap.parse_args()

    f_dir = os.path.abspath(args.scope)
    project = find_project_root(f_dir)
    if project is None:
        print("找不到專案根(DesignSpecs/)")
        return 2
    fp = flow_path(f_dir)
    if not os.path.isfile(fp):
        print("10_UIFlow.md 不存在: %s" % fp)
        return 2
    text = read_text(fp)
    rows_reg = registry_rows(text)
    if not rows_reg:
        print("找不到頁面登記表")
        return 2
    node_labels, declared = parse_mermaid(text)

    content, skeleton = scan_pages(pages_of(f_dir))
    skeleton_n = sum(len(rec["states"]) for rec in skeleton.values())
    matched_rows, missing, undeclared, escapes = match_edges(declared, content, skeleton, node_labels)

    thumbs_dir = args.thumbs or os.path.join(f_dir, "ui", "reviews", "evidence", "flowmap")
    if args.capture:
        targets = {}
        for r in rows_reg:
            base = os.path.basename(r["path"]) if r["path"] else ""
            if not base:
                continue
            proto_file = os.path.join(f_dir, "ui", "pages", "proto", base)
            styled_file = os.path.join(f_dir, "ui", r["path"])
            pick = proto_file if os.path.isfile(proto_file) else styled_file
            if os.path.isfile(pick):
                targets[r["p"]] = pick
        capture_thumbs(targets, thumbs_dir)

    html, n_both, n_skel_ok = build_html(f_dir, project, rows_reg, declared, node_labels,
                                         matched_rows, missing, undeclared, escapes,
                                         skeleton_n, thumbs_dir)
    out = args.out or os.path.join(f_dir, "ui", "00_FlowMap.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("已生成 %s|節點 %d(外部 %d)|宣告邊:一致 %d/骨架承載 %d/未實作 %d|實掃未宣告 %d|逃生邊 %d|骨架連結 %d 處" % (
        out, len(rows_reg), sum(1 for n in node_labels if not P_ID_RE.match(n)),
        n_both, n_skel_ok, len(missing), len(undeclared), len(escapes), skeleton_n))
    return 0


if __name__ == "__main__":
    sys.exit(main())

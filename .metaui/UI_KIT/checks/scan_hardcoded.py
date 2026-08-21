#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""brownfield 硬寫值掃描器(PREP-UI-2,info_level: Candidate;eco-pay 回件催生)

掃描消費端原始碼(css/scss/vue/html)中的硬寫 px 與 hex 色值,輸出頻次表與
token 映射建議(md)。定位=既有專案導入輔助工具,**不入 run_checks 閘門**;
建議欄僅供人工判定起點——同值一對多/同值異義=語意必須人工判定
(eco-pay 試點教訓:值比對不能決定映射)。

範圍與排除:
- 副檔名預設 css/scss/vue/html(--ext 可改)
- 排除目錄:node_modules/.git/dist/build/.nuxt/.output/coverage/vendor 等
- 排除生成物:檔頭含「生成物,禁手改」標記者(tokens.css 等=管線產物非硬寫)
- 0px 不計(無 token 需求);1px 建議欄註記邊框慣例(UIV-05 白名單)

Usage:
    python scan_hardcoded.py --root <消費端目錄> [--tokens <tokens.json>]
                             [--out <報告.md>] [--ext css,scss,vue,html]

exit code:0=完成(有無發現皆 0,輔助工具無閘門語意);2=參數/路徑錯誤
"""
import argparse
import collections
import json
import os
import re
import sys

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".nuxt", ".output",
             "coverage", "vendor", ".venv", "__pycache__"}
GENERATED_MARK = "生成物,禁手改"

PX_RE = re.compile(r"(?<![\w.\-])(\d+(?:\.\d+)?)px\b")
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def norm_hex(h):
    """#abc/#abcd → 六碼展開(丟 alpha);#aabbccdd → 丟 alpha。回小寫 #rrggbb 或 None。"""
    h = h.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    elif len(h) == 4:
        h = "".join(c * 2 for c in h[:3])
    elif len(h) == 8:
        h = h[:6]
    if len(h) != 6:
        return None
    return "#" + h


def load_token_maps(tokens_path):
    """tokens.json → (hex→[token名], px→[token名])。色彩含 color-dark(dark: 前綴)。"""
    with open(tokens_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    hex_map = collections.defaultdict(list)
    px_map = collections.defaultdict(list)

    def walk_colors(group, prefix):
        for key, val in group.items():
            if key.startswith("$") or not isinstance(val, dict):
                continue
            raw = val.get("$value")
            if isinstance(raw, str) and raw.startswith("#"):
                n = norm_hex(raw)
                if n:
                    hex_map[n].append(prefix + key)

    walk_colors(data.get("color", {}), "")
    walk_colors(data.get("color-dark", {}), "dark:")

    for grp in ("spacing", "radius"):
        for key, val in data.get(grp, {}).items():
            if key.startswith("$") or not isinstance(val, dict):
                continue
            m = re.match(r"^(\d+(?:\.\d+)?)px$", str(val.get("$value")))
            if m:
                px_map[float(m.group(1))].append("%s-%s" % (grp, key))
    return hex_map, px_map


def scan(root, exts):
    px_hits = collections.Counter()
    hex_hits = collections.Counter()
    px_files = collections.defaultdict(set)
    hex_files = collections.defaultdict(set)
    n_files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if os.path.splitext(fn)[1].lstrip(".").lower() not in exts:
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except OSError:
                continue
            if GENERATED_MARK in text[:400]:
                continue
            n_files += 1
            relp = os.path.relpath(path, root).replace(os.sep, "/")
            for m in PX_RE.finditer(text):
                v = float(m.group(1))
                if v == 0:
                    continue
                px_hits[v] += 1
                px_files[v].add(relp)
            for m in HEX_RE.finditer(text):
                n = norm_hex(m.group(0))
                if n:
                    hex_hits[n] += 1
                    hex_files[n].add(relp)
    return n_files, px_hits, px_files, hex_hits, hex_files


def fmt_px(v):
    return ("%g" % v) + "px"


def build_md(root, exts, n_files, px_hits, px_files, hex_hits, hex_files,
             hex_map, px_map, has_tokens):
    lines = [
        "# 硬寫值掃描報告(scan_hardcoded 產出)",
        "",
        "> 輔助工具產出,不入閘門;掃描時點快照,重跑即覆蓋。",
        "> 建議欄=映射起點——**同值一對多/同值異義=語意必須人工判定**(值比對不能決定映射)。",
        "",
        "- 掃描根:`%s`(副檔名:%s)" % (root, "/".join(sorted(exts))),
        "- 掃描檔數:%d(已排除 %s 與生成物標記檔)" % (n_files, "/".join(sorted(SKIP_DIRS))),
        "- px 硬寫:%d 種值,共 %d 處;hex 硬寫:%d 種色,共 %d 處"
        % (len(px_hits), sum(px_hits.values()), len(hex_hits), sum(hex_hits.values())),
        "",
        "## px 頻次表(0px 不計)",
        "",
        "| 值 | 次數 | 檔案例(≤3) | 建議 |",
        "|-----|------|-----------|------|",
    ]
    for v, cnt in px_hits.most_common():
        ex = "、".join("`%s`" % p for p in sorted(px_files[v])[:3])
        if not has_tokens:
            sug = "(未提供 tokens.json,僅頻次)"
        elif v in px_map:
            sug = "、".join("`--%s`" % t for t in px_map[v])
        elif v == 1:
            sug = "1px 邊框慣例(UIV-05 白名單,多半不需 token)"
        else:
            sug = "scale 外——候討論(就近改階或提回收)"
        lines.append("| %s | %d | %s | %s |" % (fmt_px(v), cnt, ex, sug))
    lines += [
        "",
        "## hex 頻次表(三/四/八碼已正規化為六碼,alpha 不比對)",
        "",
        "| 色值 | 次數 | 檔案例(≤3) | 候選 token | 備註 |",
        "|------|------|-----------|-----------|------|",
    ]
    for n, cnt in hex_hits.most_common():
        ex = "、".join("`%s`" % p for p in sorted(hex_files[n])[:3])
        if not has_tokens:
            cand, note = "(未提供 tokens.json,僅頻次)", "—"
        else:
            names = hex_map.get(n, [])
            if not names:
                cand, note = "無對應", "候回收通道或專案自定"
            else:
                cand = "、".join(
                    "`--color-%s`(dark)" % t[5:] if t.startswith("dark:")
                    else "`--color-%s`" % t for t in names)
                note = "**一對多:語意人判**" if len(names) > 1 else "—"
        lines.append("| `%s` | %d | %s | %s | %s |" % (n, cnt, ex, cand, note))
    return "\n".join(lines) + "\n"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--tokens")
    ap.add_argument("--out")
    ap.add_argument("--ext", default="css,scss,vue,html")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("掃描根不存在: %s" % root)
        return 2
    hex_map, px_map, has_tokens = {}, {}, False
    if args.tokens:
        if not os.path.isfile(args.tokens):
            print("tokens.json 不存在: %s" % args.tokens)
            return 2
        hex_map, px_map = load_token_maps(args.tokens)
        has_tokens = True
    exts = {e.strip().lower() for e in args.ext.split(",") if e.strip()}

    n_files, px_hits, px_files, hex_hits, hex_files = scan(root, exts)
    md = build_md(root, exts, n_files, px_hits, px_files, hex_hits, hex_files,
                  hex_map, px_map, has_tokens)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
        print("已輸出: %s(檔 %d/px %d 種/hex %d 種)"
              % (args.out, n_files, len(px_hits), len(hex_hits)))
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())

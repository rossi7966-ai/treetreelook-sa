#!/usr/bin/env python3
"""MetaUI token 生成器(PREP-UI-2 升級,info_level: Candidate)

tokens.json(DTCG 2025.10 巢狀格式,單一 SSOT)→ 生成 tokens.css + 00_TokenSheet.md。
生成物禁手改;新鮮度由 UIV-06 驗(重生成零 diff)。

支援:
- DTCG 巢狀群組(自動展平為 --群組-名)
- $type 群組繼承
- alias 引用({path.to.token} 語法,解析為實際值)
- color-dark 群組 → [data-theme=dark_mode] 選擇器

向下相容:偵測到 "tokens" 陣列時走舊格式路徑。

Usage:
    python gen_tokens.py --project <專案根>          # 生成/覆寫
    python gen_tokens.py --project <專案根> --check  # 只比對,不寫入
"""
import argparse
import json
import os
import re
import sys

HEADER = "生成物,禁手改;來源 UIFoundation/tokens.json,重生成用 UI_KIT/checks/gen_tokens.py"


def load_tokens(foundation):
    path = os.path.join(foundation, "tokens.json")
    if not os.path.isfile(path):
        return None, path
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), path


def is_token(obj):
    return isinstance(obj, dict) and "$value" in obj


def flatten_dtcg(data):
    """Walk DTCG nested structure, yield (css_name, raw_value, type, description, tier, group)."""
    def walk(obj, prefix, inherited_type):
        if not isinstance(obj, dict):
            return
        current_type = obj.get("$type", inherited_type)
        for key, val in obj.items():
            if key.startswith("$"):
                continue
            if is_token(val):
                css_name = "%s-%s" % (prefix, key) if prefix else key
                t = val.get("$type", current_type)
                desc = val.get("$description", "")
                ext = val.get("$extensions", {}).get("metaui", {})
                tier = ext.get("tier", "")
                yield (css_name, val["$value"], t or "", desc, tier, prefix or "(root)")
            elif isinstance(val, dict) and not key.startswith("$"):
                child_prefix = "%s-%s" % (prefix, key) if prefix else key
                yield from walk(val, child_prefix, current_type)
    yield from walk(data, "", None)


def resolve_aliases(tokens_flat, all_tokens_by_name):
    """Resolve {path} alias references to actual values."""
    alias_re = re.compile(r"^\{(.+)\}$")
    resolved = []
    for css_name, raw_value, typ, desc, tier, group in tokens_flat:
        if isinstance(raw_value, str):
            m = alias_re.match(raw_value)
            if m:
                ref_path = m.group(1).replace(".", "-")
                actual = all_tokens_by_name.get(ref_path, raw_value)
                resolved.append((css_name, actual, typ, desc, tier, group, raw_value))
                continue
        resolved.append((css_name, raw_value, typ, desc, tier, group, None))
    return resolved


def format_css_value(raw_value):
    if isinstance(raw_value, dict):
        parts = []
        for k in ("offsetX", "offsetY", "blur", "spread"):
            if k in raw_value:
                parts.append(str(raw_value[k]))
        if "color" in raw_value:
            parts.append(str(raw_value["color"]))
        return " ".join(parts)
    return str(raw_value)


def build_dtcg(data):
    light_groups = {k: v for k, v in data.items()
                    if not k.startswith("$") and k != "color-dark"}
    dark_group = data.get("color-dark", {})
    # dark=optional 宣告制:$modes 未含 dark → 不產 dark 區塊
    # (未宣告依 color-dark 有無推斷;判準與 uiv10 token_config 一致)
    modes = data.get("$modes") or (["light", "dark"] if dark_group else ["light"])
    if "dark" not in modes:
        dark_group = {}

    light_flat = list(flatten_dtcg(light_groups))
    all_by_name = {name: format_css_value(val) for name, val, *_ in light_flat}
    light_resolved = resolve_aliases(light_flat, all_by_name)

    dark_flat = list(flatten_dtcg({"color-dark": dark_group}))
    dark_tokens = []
    for css_name, raw_value, *rest in dark_flat:
        clean_name = css_name.replace("color-dark-", "color-")
        dark_tokens.append((clean_name, format_css_value(raw_value)))

    css_lines = ["/* %s */" % HEADER, ":root {"]
    for css_name, raw_value, typ, desc, tier, group, alias_ref in light_resolved:
        css_val = format_css_value(raw_value)
        css_lines.append("  --%s: %s;" % (css_name, css_val))
    css_lines.append("}")
    if dark_tokens:
        css_lines.append("[data-theme=dark_mode] {")
        for css_name, css_val in dark_tokens:
            css_lines.append("  --%s: %s;" % (css_name, css_val))
        css_lines.append("}")
    css = "\n".join(css_lines) + "\n"

    version = data.get("$extensions", {}).get("metaui", {}).get("version", "unknown")
    md_lines = [
        "---",
        "file: DesignSpecs/UIFoundation/00_TokenSheet.md",
        "role: token_sheet_generated",
        "summary: %s" % HEADER,
        "---",
        "# Token 對照表(生成物)",
        "",
        "> 來源:tokens.json v%s" % version,
        "> 使用規則:元件/頁面只准引 semantic tier;primitive 只供 alias 引用(F-2)",
        "",
        "| token | 群組 | 型別 | 值 | 層級 | 說明 |",
        "|-------|------|------|-----|------|------|",
    ]
    for css_name, raw_value, typ, desc, tier, group, alias_ref in light_resolved:
        css_val = format_css_value(raw_value)
        alias_note = " → `%s`" % alias_ref if alias_ref else ""
        md_lines.append("| `--%s` | %s | %s | `%s`%s | %s | %s |" % (
            css_name, group, typ, css_val, alias_note, tier, desc))
    if dark_tokens:
        md_lines.append("")
        md_lines.append("## Dark Mode 覆寫")
        md_lines.append("")
        md_lines.append("| token | 值 |")
        md_lines.append("|-------|----|")
        for css_name, css_val in dark_tokens:
            md_lines.append("| `--%s` | `%s` |" % (css_name, css_val))
    md = "\n".join(md_lines) + "\n"

    return {"tokens.css": css, "00_TokenSheet.md": md}


def build_legacy(data):
    """舊格式(metaui-tokens-v0)向下相容。"""
    tokens = data.get("tokens", [])
    name_re = re.compile(r"^[a-z0-9][a-z0-9-]*$")
    bad = [t.get("name", "?") for t in tokens if not name_re.match(t.get("name", ""))]
    if bad:
        raise ValueError("token 名稱不合法: " + ", ".join(bad))

    css_lines = ["/* %s */" % HEADER, ":root {"]
    for t in tokens:
        css_lines.append("  --%s: %s;" % (t["name"], t["value"]))
    css_lines.append("}")
    css = "\n".join(css_lines) + "\n"

    md_lines = [
        "---",
        "file: DesignSpecs/UIFoundation/00_TokenSheet.md",
        "role: token_sheet_generated",
        "summary: %s" % HEADER,
        "---",
        "# Token 對照表(生成物)",
        "",
        "> 來源:tokens.json(%s)" % data.get("source_kit", "未標"),
        "",
        "| token | 類別 | 值 | 來源 |",
        "|-------|------|-----|------|",
    ]
    for t in tokens:
        md_lines.append("| `--%s` | %s | `%s` | %s |" % (
            t["name"], t.get("category", ""), t["value"], t.get("source", "")))
    md = "\n".join(md_lines) + "\n"
    return {"tokens.css": css, "00_TokenSheet.md": md}


def build(data):
    """UIV-06 入口:接受已解析的 tokens.json dict,回傳 {filename: content}。"""
    if "tokens" in data:
        return build_legacy(data)
    return build_dtcg(data)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    foundation = os.path.join(os.path.abspath(args.project), "DesignSpecs", "UIFoundation")
    data, src = load_tokens(foundation)
    if data is None:
        print("tokens.json 不存在: %s" % src)
        return 2

    try:
        if "tokens" in data:
            outputs = build_legacy(data)
        else:
            outputs = build_dtcg(data)
    except (ValueError, KeyError) as e:
        print("tokens.json 內容錯誤: %s" % e)
        return 2

    dirty = []
    for name, content in outputs.items():
        path = os.path.join(foundation, name)
        current = None
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                current = f.read()
        if current != content:
            dirty.append(name)
            if not args.check:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(content)

    if args.check:
        if dirty:
            print("STALE: " + ", ".join(dirty))
            return 1
        print("FRESH: 生成物與 tokens.json 一致")
        return 0
    print("已生成: " + ", ".join(outputs) + ("(異動: %s)" % ", ".join(dirty) if dirty else "(無異動)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

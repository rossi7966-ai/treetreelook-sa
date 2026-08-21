#!/usr/bin/env python3
"""Design.md 資料段生成器(PREP-UI-2,info_level: Candidate)

tokens.json + 20_Components.md → Design.md
- YAML front matter:色彩/字型/圓角/間距 hard token
- 數據段:自動生成(色彩表/字型表/元件摘要)
- 敘事段:以 <!-- NARRATIVE:key --> 標記,若既有 Design.md 已填內容則保留不覆寫

Usage:
    python gen_design_md.py --project <專案根>
    python gen_design_md.py --project <專案根> --check
"""
import argparse
import json
import os
import re
import sys

HEADER = "資料段為生成物(來源:tokens.json);敘事段(NARRATIVE 標記區)=人工審定內容,生成器保留不覆寫"


def load_json(path):
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_tokens(data, group, key_filter=None):
    g = data.get(group, {})
    result = []
    for k, v in g.items():
        if k.startswith("$"):
            continue
        if key_filter and not key_filter(k):
            continue
        if isinstance(v, dict) and "$value" in v:
            ext = v.get("$extensions", {}).get("metaui", {})
            result.append({
                "name": k,
                "value": v["$value"],
                "desc": v.get("$description", ""),
                "tier": ext.get("tier", ""),
            })
    return result


def build_yaml_front_matter(data):
    lines = ["---"]
    lines.append("file: DesignSpecs/UIFoundation/Design.md")
    lines.append("role: design_document")
    lines.append("task: PREP-UI-2")
    lines.append("origin: PREP-UI 前置準備產出")
    lines.append("info_level: Candidate")
    ext = data.get("$extensions", {}).get("metaui", {})
    lines.append("ds_version: %s" % ext.get("version", "0.1.0"))
    lines.append("provenance: DS@%s" % ext.get("version", "0.1.0"))
    lines.append("narrative_status: 敘事段=人工審定;資料段=gen_design_md 生成")

    colors = extract_tokens(data, "color")
    lines.append("colors:")
    for c in colors:
        val = c["value"]
        if isinstance(val, str) and val.startswith("{"):
            continue
        lines.append("  %s: \"%s\"" % (c["name"], val))

    typo = data.get("typography", {})
    lines.append("typography:")
    ff = typo.get("font-family", {})
    if "sans" in ff and "$value" in ff["sans"]:
        lines.append("  font-family: \"%s\"" % ff["sans"]["$value"])
    fs = typo.get("font-size", {})
    lines.append("  sizes:")
    for k, v in fs.items():
        if k.startswith("$"):
            continue
        if isinstance(v, dict) and "$value" in v:
            lines.append("    %s: \"%s\"" % (k, v["$value"]))
    fw = typo.get("font-weight", {})
    lines.append("  weights:")
    for k, v in fw.items():
        if k.startswith("$"):
            continue
        if isinstance(v, dict) and "$value" in v:
            lines.append("    %s: %s" % (k, v["$value"]))

    radii = extract_tokens(data, "radius")
    lines.append("rounded:")
    for r in radii:
        lines.append("  %s: \"%s\"" % (r["name"], r["value"]))

    spacings = extract_tokens(data, "spacing")
    lines.append("spacing:")
    for s in spacings:
        lines.append("  step-%s: \"%s\"" % (s["name"], s["value"]))

    lines.append("---")
    return "\n".join(lines)


def build_color_section(data):
    lines = ["## Styles — Color"]
    lines.append("")
    lines.append("> 使用規則:元件/頁面只准引 semantic tier token;primitive 僅供 alias 引用(F-2)")
    lines.append("")
    lines.append("### Primitive Colors(Light Mode)")
    lines.append("")
    lines.append("| token | 值 | 說明 |")
    lines.append("|-------|----|------|")
    prims = extract_tokens(data, "color", lambda k: not k.startswith("text-") and k not in ("error","success","info","error-container","success-container","info-container"))
    for t in prims:
        if isinstance(t["value"], str) and t["value"].startswith("{"):
            continue
        lines.append("| `{colors.%s}` | `%s` | %s |" % (t["name"], t["value"], t["desc"]))

    lines.append("")
    lines.append("### Semantic Colors(元件應引用此層)")
    lines.append("")
    lines.append("| token | 指向 | 說明 |")
    lines.append("|-------|------|------|")
    sems = extract_tokens(data, "color", lambda k: k in ("text-heading","text-body","error","success","info","error-container","success-container","info-container"))
    for t in sems:
        val = t["value"]
        if isinstance(val, str) and val.startswith("{"):
            lines.append("| `{colors.%s}` | `%s` | %s |" % (t["name"], val, t["desc"]))
        else:
            lines.append("| `{colors.%s}` | `%s` | %s |" % (t["name"], val, t["desc"]))

    dark = data.get("color-dark", {})
    # dark=optional 宣告制:$modes 未含 dark → 不產 Dark 覆寫表
    # (未宣告依 color-dark 有無推斷;判準與 uiv10 token_config 一致)
    modes = data.get("$modes") or (["light", "dark"] if dark else ["light"])
    if "dark" not in modes:
        dark = {}
    if dark:
        lines.append("")
        lines.append("### Dark Mode 覆寫")
        lines.append("")
        lines.append("| token | Light 值 | Dark 值 |")
        lines.append("|-------|---------|---------|")
        light_colors = {t["name"]: t["value"] for t in extract_tokens(data, "color")}
        for k, v in dark.items():
            if k.startswith("$"):
                continue
            if isinstance(v, dict) and "$value" in v:
                lv = light_colors.get(k, "—")
                if isinstance(lv, str) and lv.startswith("{"):
                    lv = "(alias)"
                lines.append("| `{colors.%s}` | `%s` | `%s` |" % (k, lv, v["$value"]))

    return "\n".join(lines)


def build_typography_section(data):
    typo = data.get("typography", {})
    lines = ["## Styles — Typography"]
    lines.append("")
    ff = typo.get("font-family", {})
    if "sans" in ff and "$value" in ff["sans"]:
        lines.append("**Font family**: `%s`" % ff["sans"]["$value"])
    lh = typo.get("line-height", {})
    if "default" in lh and "$value" in lh["default"]:
        lines.append("**Line height**: %s" % lh["default"]["$value"])
    lines.append("**Letter spacing**: fontSize × 0.02")
    lines.append("")
    lines.append("| 級別 | token | 值 | px |")
    lines.append("|------|-------|----|-----|")
    fs = typo.get("font-size", {})
    for k, v in fs.items():
        if k.startswith("$") or not isinstance(v, dict):
            continue
        desc = v.get("$description", "")
        lines.append("| %s | `{typography.font-size.%s}` | `%s` | %s |" % (k, k, v.get("$value", ""), desc))

    lines.append("")
    lines.append("| 權重 | token | 值 |")
    lines.append("|------|-------|----|")
    fw = typo.get("font-weight", {})
    for k, v in fw.items():
        if k.startswith("$") or not isinstance(v, dict):
            continue
        lines.append("| %s | `{typography.font-weight.%s}` | %s |" % (k, k, v.get("$value", "")))

    return "\n".join(lines)


def build_spacing_section(data):
    lines = ["## Styles — Spacing & Radius"]
    lines.append("")
    lines.append("### Spacing Scale（4pt grid）")
    lines.append("")
    lines.append("| step | token | 值 |")
    lines.append("|------|-------|----|")
    for t in extract_tokens(data, "spacing"):
        lines.append("| %s | `{spacing.%s}` | `%s` |" % (t["name"], t["name"], t["value"]))
    lines.append("")
    lines.append("### Border Radius")
    lines.append("")
    lines.append("| 名稱 | token | 值 | 說明 |")
    lines.append("|------|-------|----|------|")
    for t in extract_tokens(data, "radius"):
        lines.append("| %s | `{radius.%s}` | `%s` | %s |" % (t["name"], t["name"], t["value"], t["desc"]))
    return "\n".join(lines)


def build_component_summary(project_root):
    comp_path = os.path.join(project_root, "DesignSpecs", "UIFoundation", "20_Components.md")
    if not os.path.isfile(comp_path):
        return "## Components\n\n> 元件規範見 20_Components.md（檔案尚未建立）"
    lines = ["## Components"]
    lines.append("")
    lines.append("> 詳見 [20_Components.md](20_Components.md)——此處僅列分類摘要")
    lines.append("")
    lines.append("| 類別 | 現有元件數 | 代表元件 |")
    lines.append("|------|-----------|---------|")
    categories = [
        ("Form", "15", "BaseInput, BaseSelect, BaseDatepicker"),
        ("Action", "9", "BaseButton, ScrollToTopButton"),
        ("Navigation", "4", "HeaderBar, BreadCrumbs, BaseTab"),
        ("Feedback", "6", "BaseAlert, BaseDialog, BaseTooltip"),
        ("Content", "4", "BaseCard, BaseExpansion, BasePopover"),
        ("Data", "1", "BaseTable"),
        ("Layout", "3", "BaseDivider, BasePanel"),
        ("Status", "3", "BaseChip, StatusChip"),
        ("GIS", "1", "MapPane"),
    ]
    for cat, count, examples in categories:
        lines.append("| %s | %s | %s |" % (cat, count, examples))
    return "\n".join(lines)


def parse_existing_narratives(design_md_path):
    narratives = {}
    if not os.path.isfile(design_md_path):
        return narratives
    with open(design_md_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(
        r"<!-- NARRATIVE:(\w+) -->\n(.*?)(?=\n<!-- /NARRATIVE:\1 -->)",
        re.DOTALL
    )
    for m in pattern.finditer(content):
        key = m.group(1)
        body = m.group(2).strip()
        if body and body != "（待 Fable/UI 審定稿）":
            narratives[key] = body
    return narratives


def narrative_slot(key, existing, default="（待 Fable/UI 審定稿）"):
    body = existing.get(key, default)
    return "<!-- NARRATIVE:%s -->\n%s\n<!-- /NARRATIVE:%s -->" % (key, body, key)


def build_design_md(data, project_root):
    design_path = os.path.join(project_root, "DesignSpecs", "UIFoundation", "Design.md")
    existing = parse_existing_narratives(design_path)

    parts = []
    parts.append(build_yaml_front_matter(data))
    parts.append("")
    parts.append("# MetaUI Design Document")
    parts.append("")
    parts.append("> %s" % HEADER)
    parts.append("")

    parts.append("## Overview")
    parts.append("")
    parts.append(narrative_slot("overview", existing))
    parts.append("")

    parts.append("## 設計原則摘要")
    parts.append("")
    parts.append("> 完整版見 [10_Principles.md](10_Principles.md)")
    parts.append("")
    parts.append(narrative_slot("principles", existing))
    parts.append("")

    parts.append(build_color_section(data))
    parts.append("")
    parts.append(build_typography_section(data))
    parts.append("")
    parts.append(build_spacing_section(data))
    parts.append("")

    shadows = extract_tokens(data, "shadow")
    if shadows:
        parts.append("## Styles — Shadow")
        parts.append("")
        parts.append("| 名稱 | token | 值 |")
        parts.append("|------|-------|----|")
        for t in shadows:
            v = t["value"]
            if isinstance(v, dict):
                vs = "%s %s %s %s %s" % (v.get("offsetX",""), v.get("offsetY",""), v.get("blur",""), v.get("spread",""), v.get("color",""))
            else:
                vs = str(v)
            parts.append("| %s | `{shadow.%s}` | `%s` |" % (t["name"], t["name"], vs.strip()))
        parts.append("")

    parts.append(build_component_summary(project_root))
    parts.append("")

    parts.append("## Patterns")
    parts.append("")
    parts.append(narrative_slot("patterns", existing))
    parts.append("")

    parts.append("## 反模式（Never Do）")
    parts.append("")
    parts.append("- **Never** hardcode hex/rgb 色值——一律引用 token（UIV-05 機器檢核）")
    parts.append("- **Never** 在元件/頁面層直接引用 primitive tier token（如 `{colors.red1}`）——改引 semantic（如 `{colors.error}`）")
    parts.append("- **Never** 手改 tokens.css / 00_TokenSheet.md / Design.md 資料段——這些是生成物,改 tokens.json 後重生成")
    parts.append("- **Never** 在 dark mode 判斷中使用 `prefers-color-scheme`——使用 `[data-theme=dark_mode]` 選擇器")
    parts.append("")
    parts.append(narrative_slot("anti_patterns", existing))
    parts.append("")

    parts.append("## Responsive")
    parts.append("")
    bps = extract_tokens(data, "breakpoint")
    if bps:
        parts.append("| 名稱 | token | 值 |")
        parts.append("|------|-------|----|")
        for t in bps:
            parts.append("| %s | `{breakpoint.%s}` | `%s` |" % (t["name"], t["name"], t["value"]))
    parts.append("")
    parts.append(narrative_slot("responsive", existing))
    parts.append("")

    parts.append("## Known Gaps")
    parts.append("")
    parts.append("- 動畫/Transition 細節:僅有 fast(0.2s) / slow(0.5s) 兩級,缺 easing curve 分類")
    parts.append("- A11y:色彩對比度未全表機械驗證(WCAG 2.1 AA)")
    parts.append("- 0.75rem(12px)字級:出現於 BaseSelect 但不在 typography scale 內——待確認是否納入或標為例外")
    parts.append("- GIS 元件:僅 MapPane 存在;圖例/圖層控制/坐標顯示=擴充候選(觸發依 00_Blueprint)")
    parts.append("- Figma 變數同步:人工、單向 Figma→repo;漂移偵測=checks/uiv10_figma_diff.py(具名依賴 MCP 讀回,不入閘門子集)")
    parts.append("- Brand 多品牌:MVP 假設單品牌,overrides 擴充槽保留名字不實作")
    parts.append("- Dark mode subtitle 層級消失:subtitle 和 text 的 dark mode 覆寫值皆為 `#ffffff`,副標題在深色模式下與正文無區分——弱化值=設計師決定項;建議帶青灰調呼應品牌,錨點 `#a9b6b4`(於 `#2f2e31` 上對比約 7:1),範圍 `#9fb0ad`~`#c0cac8`;text 純白眩光疑慮可一併評估(業界慣例 87~90% 白,如 `#e6ecea`)")
    parts.append("")

    return "\n".join(parts) + "\n"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    project = os.path.abspath(args.project)
    foundation = os.path.join(project, "DesignSpecs", "UIFoundation")
    tokens_path = os.path.join(foundation, "tokens.json")

    if not os.path.isfile(tokens_path):
        print("tokens.json 不存在: %s" % tokens_path)
        return 2

    with open(tokens_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    content = build_design_md(data, project)
    design_path = os.path.join(foundation, "Design.md")

    if args.check:
        if not os.path.isfile(design_path):
            print("STALE: Design.md 不存在")
            return 1
        with open(design_path, "r", encoding="utf-8") as f:
            current = f.read()
        if current != content:
            print("STALE: Design.md 資料段與 tokens.json 不一致")
            return 1
        print("FRESH: Design.md 資料段與 tokens.json 一致")
        return 0

    with open(design_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("已生成: Design.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())

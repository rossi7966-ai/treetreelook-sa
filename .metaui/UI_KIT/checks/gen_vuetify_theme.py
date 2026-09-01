#!/usr/bin/env python3
"""Vuetify theme 生成器(PREP-UI-2,info_level: Candidate)

tokens.json → vuetify.theme.json(Vuetify 3 createVuetify({ theme }) 設定樣張)

雙軌共存設計:
  tokens.css    → --color-*     (DS 正規名，gen_tokens.py 生成)
  Vuetify theme → --v-theme-*   (Vuetify 慣例，本檔生成)
兩軌同值同源(tokens.json)，工程師可用任一命名空間;
DS 規範以 tokens.css 的 --color-* 為正規引用名。

Vuetify built-in color keys(primary/secondary/error/success/info/
background/surface/surface-variant)直接對映。
非 built-in 的 token(如 primary-emphasis/subtitle/stroke)
註冊為 Vuetify custom colors，工程師可在元件上 color="primary-emphasis"。

Usage:
    python gen_vuetify_theme.py --project <專案根>
    python gen_vuetify_theme.py --project <專案根> --check
"""
import argparse
import json
import os
import sys

HEADER = (
    "生成物，禁手改;來源 UIFoundation/tokens.json，"
    "重生成用 UI_KIT/checks/gen_vuetify_theme.py"
)

VUETIFY_BUILTINS = {
    "primary", "secondary", "error", "success", "info", "warning",
    "background", "surface", "surface-variant",
    "on-primary", "on-secondary", "on-error", "on-success", "on-info",
    "on-warning", "on-background", "on-surface", "on-surface-variant",
}


def load_tokens(foundation):
    path = os.path.join(foundation, "tokens.json")
    if not os.path.isfile(path):
        return None, path
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), path


def extract_colors(color_group):
    primitives = {}
    aliases = {}
    for key, val in color_group.items():
        if key.startswith("$") or not isinstance(val, dict) or "$value" not in val:
            continue
        raw = val["$value"]
        if isinstance(raw, str) and raw.startswith("{"):
            aliases[key] = raw
        elif isinstance(raw, str):
            primitives[key] = raw

    resolved = dict(primitives)
    alias_map = {}
    for key, ref in aliases.items():
        ref_key = ref.strip("{}").split(".")[-1]
        if ref_key in primitives:
            resolved[key] = primitives[ref_key]
            alias_map[key] = ref_key

    return resolved, alias_map


def build_vuetify_theme(data):
    color_group = data.get("color", {})
    dark_group = data.get("color-dark", {})
    # dark=optional 宣告制:$modes 未含 dark → 不產 dark_mode 主題
    # (未宣告依 color-dark 有無推斷;判準與 uiv10 token_config 一致)
    modes = data.get("$modes") or (["light", "dark"] if dark_group else ["light"])
    dark_enabled = "dark" in modes
    if not dark_enabled:
        dark_group = {}

    light_colors, alias_map = extract_colors(color_group)

    dark_overrides = {}
    for key, val in dark_group.items():
        if key.startswith("$") or not isinstance(val, dict) or "$value" not in val:
            continue
        dark_overrides[key] = val["$value"]

    dark_primitives = {k: v for k, v in light_colors.items() if k not in alias_map}
    dark_primitives.update(dark_overrides)
    dark_colors = dict(dark_primitives)
    for alias_key, ref_key in alias_map.items():
        dark_colors[alias_key] = dark_primitives.get(ref_key, light_colors.get(alias_key, ""))

    mapping = []
    for key in light_colors:
        entry = {
            "token": "color.%s" % key,
            "vuetify_key": key,
            "type": "built-in" if key in VUETIFY_BUILTINS else "custom",
            "light": light_colors[key],
        }
        if key in dark_overrides:
            entry["dark"] = dark_overrides[key]
        if key in alias_map:
            entry["alias_of"] = alias_map[key]
        mapping.append(entry)

    ext = data.get("$extensions", {}).get("metaui", {})
    version = ext.get("version", "unknown")

    themes = {
        "light": {
            "dark": False,
            "colors": light_colors,
        }
    }
    if dark_enabled:
        themes["dark_mode"] = {
            "dark": True,
            "colors": dark_colors,
        }

    return {
        "$generated": HEADER,
        "$version": version,
        "defaultTheme": "light",
        "themes": themes,
        "$mapping": mapping,
        "$notes": {
            "dual_track": (
                "tokens.css(--color-*) 與 Vuetify(--v-theme-*) 雙軌共存，同值同源。"
                "DS 規範以 --color-* 為正規引用名"
            ),
            "emphasis_not_darken": (
                "使用 color=\"primary-emphasis\" 而非 Vuetify 自動生成的 "
                "primary-darken-1(F-5 裁決:darken/lighten→emphasis/soft)"
            ),
            "semantic_only": (
                "元件應引用 semantic tier(error/success/info)，"
                "不直接引用 primitive(red1/green1/blue1)(F-2 裁決)"
            ),
            "usage": (
                "import theme from './vuetify.theme.json';\n"
                "createVuetify({ theme: { "
                "defaultTheme: theme.defaultTheme, "
                "themes: theme.themes } })"
            ),
        }
    }


def build(data):
    """UIV-06 entry point."""
    theme = build_vuetify_theme(data)
    content = json.dumps(theme, indent=2, ensure_ascii=False) + "\n"
    return {"vuetify.theme.json": content}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    project = os.path.abspath(args.project)
    foundation = os.path.join(project, "DesignSpecs", "UIFoundation")
    data, src = load_tokens(foundation)
    if data is None:
        print("tokens.json 不存在: %s" % src)
        return 2

    try:
        outputs = build(data)
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
        print("FRESH: vuetify.theme.json 與 tokens.json 一致")
        return 0
    print("已生成: " + ", ".join(outputs) + ("(異動: %s)" % ", ".join(dirty) if dirty else "(無異動)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

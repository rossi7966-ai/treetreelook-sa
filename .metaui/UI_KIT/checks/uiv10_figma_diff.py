#!/usr/bin/env python3
"""UIV-10 原型:Figma Variables 讀回 JSON ↔ tokens.json 漂移偵測。

具名依賴:輸入之 Figma 讀回 JSON 由 MCP(use_figma Plugin API 全量讀回)產出,
本腳本不自行連線 Figma——故不入 run_checks 閘門子集,手動或維護流程調用。

用法:
    python uiv10_figma_diff.py --figma <readback.json> --tokens <tokens.json>

比對四面:名(terminal name 雙向)/值(light)/alias 指向/mode 值(dark_mode)。
範圍:color/color-dark/typography.font-size/font-weight/spacing/radius;
shadow/z-index/breakpoint/layout/transition/focus 屬 repo 側,不要求 Figma 持有。
宣告例外:subtitle 之 dark 值待設計師定,Figma 暫留 light 值 → allowed-exception。

dark mode=optional(宣告制):tokens.json 頂層 `$modes` 宣告(如 ["light"]);
未宣告時依 color-dark 群組有無推斷。未含 "dark" → dark 相關比對全數不適用。
集合名可配置:tokens.json `$extensions.metaui.figma_collections`
{"color"/"typography"/"spacing": "<集合名>"},未設=MetaUI Color/Typography/Spacing。
font-weight 型別容錯:Figma 端 STRING 字重名(Bold/Medium…)映射為數值後比對。
exit code:0=無 fail,1=有 fail,2=輸入解析失敗。
"""
import argparse
import io
import json
import sys

DECLARED_EXCEPTIONS = {
    ("subtitle", "dark_mode"): "dark 弱化值待設計師定,Figma 暫留 light 值",
}

FONT_WEIGHT_NAMES = {
    "thin": 100, "hairline": 100, "extralight": 200, "ultralight": 200,
    "light": 300, "regular": 400, "normal": 400, "medium": 500,
    "semibold": 600, "demibold": 600, "bold": 700,
    "extrabold": 800, "ultrabold": 800, "black": 900, "heavy": 900,
}


def weight_num(v):
    """字重值→數值;STRING 字重名映射,無法解析回 None。"""
    try:
        return float(v)
    except (TypeError, ValueError):
        name = str(v).strip().lower().replace(" ", "")
        return float(FONT_WEIGHT_NAMES[name]) if name in FONT_WEIGHT_NAMES else None


def token_config(tok):
    """回 (modes, collections):$modes 宣告制(未宣告依 color-dark 推斷)+集合名配置。"""
    modes = tok.get("$modes")
    if not modes:
        modes = ["light", "dark"] if tok.get("color-dark") else ["light"]
    coll = tok.get("$extensions", {}).get("metaui", {}).get("figma_collections", {})
    return modes, {
        "color": coll.get("color", "MetaUI Color"),
        "typography": coll.get("typography", "MetaUI Typography"),
        "spacing": coll.get("spacing", "MetaUI Spacing"),
    }


def rem_px(v):
    s = str(v)
    if s.endswith("rem"):
        return float(s[:-3]) * 16
    if s.endswith("px"):
        return float(s[:-2])
    return float(s)


def load_figma(path):
    data = json.load(io.open(path, encoding="utf-8"))
    m = {}
    for c in data["collections"]:
        for v in c["vars"]:
            m[(c["name"], v["name"].split("/")[-1])] = v
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--figma", required=True)
    ap.add_argument("--tokens", required=True)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        fig = load_figma(args.figma)
        tok = json.load(io.open(args.tokens, encoding="utf-8"))
    except Exception as e:
        print("[parse-error] UIV-10 輸入解析失敗: %s" % e)
        return 2

    fails, exceptions, passes = [], [], 0
    modes, colls = token_config(tok)
    dark_required = "dark" in modes
    c_color, c_typo, c_space = colls["color"], colls["typography"], colls["spacing"]

    def check(cond, msg):
        nonlocal passes
        if cond:
            passes += 1
        else:
            fails.append(msg)

    color = {k: v for k, v in tok["color"].items() if isinstance(v, dict) and "$value" in v}
    dark = {k: v["$value"].lower() for k, v in tok.get("color-dark", {}).items()
            if isinstance(v, dict) and "$value" in v}
    prims = {k: v for k, v in color.items() if not v["$value"].startswith("{")}
    aliases = {k: v["$value"].strip("{}").split(".")[-1] for k, v in color.items()
               if v["$value"].startswith("{")}

    for name, spec in prims.items():
        fv = fig.get((c_color, name))
        if not fv:
            fails.append("色彩缺席: %s 不在 Figma %s" % (name, c_color))
            continue
        check(fv["values"].get("light", "").lower() == spec["$value"].lower(),
              "light 值漂移: %s Figma=%s tokens=%s" % (name, fv["values"].get("light"), spec["$value"]))
        if not dark_required:
            continue
        expect_dark = dark.get(name, spec["$value"].lower())
        got_dark = str(fv["values"].get("dark_mode", "")).lower()
        if got_dark != expect_dark:
            if (name, "dark_mode") in DECLARED_EXCEPTIONS:
                exceptions.append("%s dark=%s(tokens=%s)——%s"
                                  % (name, got_dark, expect_dark, DECLARED_EXCEPTIONS[(name, "dark_mode")]))
            else:
                fails.append("dark 值漂移: %s Figma=%s tokens=%s" % (name, got_dark, expect_dark))
        else:
            passes += 1

    alias_modes = ("light", "dark_mode") if dark_required else ("light",)
    for name, target in aliases.items():
        fv = fig.get((c_color, name))
        if not fv:
            fails.append("alias 缺席: %s" % name)
            continue
        for mode in alias_modes:
            got = fv["values"].get(mode)
            got_target = got.get("alias", "").split("/")[-1] if isinstance(got, dict) else str(got)
            check(got_target == target, "alias 指向漂移: %s[%s] Figma→%s tokens→%s" % (name, mode, got_target, target))

    for name, spec in tok["typography"]["font-size"].items():
        if not isinstance(spec, dict) or "$value" not in spec:
            continue
        fv = fig.get((c_typo, name))
        check(fv is not None and float(list(fv["values"].values())[0]) == rem_px(spec["$value"]),
              "font-size 漂移/缺席: %s" % name)
    for name, spec in tok["typography"]["font-weight"].items():
        if not isinstance(spec, dict) or "$value" not in spec:
            continue
        fv = fig.get((c_typo, name))
        got_w = weight_num(list(fv["values"].values())[0]) if fv else None
        check(fv is not None and got_w is not None and got_w == float(spec["$value"]),
              "font-weight 漂移/缺席: %s" % name)
    for cat in ("spacing", "radius"):
        for name, spec in tok[cat].items():
            if not isinstance(spec, dict) or "$value" not in spec:
                continue
            fv = fig.get((c_space, name))
            check(fv is not None and float(list(fv["values"].values())[0]) == rem_px(spec["$value"]),
                  "%s 漂移/缺席: %s" % (cat, name))

    known = {t for pair in (prims, aliases) for t in pair}
    for (cname, term), _v in fig.items():
        if cname == c_color and term not in known:
            fails.append("Figma 多出未登記色彩變數: %s" % term)

    print("=== UIV-10 Figma↔tokens 漂移偵測(原型) ===")
    print("modes: %s%s | collections: %s / %s / %s"
          % ("+".join(modes), "" if dark_required else "(dark 檢核不適用)", c_color, c_typo, c_space))
    for f in fails:
        print("[fail] %s" % f)
    for e in exceptions:
        print("[allowed-exception] %s" % e)
    print("counts: fail=%d / allowed-exception=%d / pass=%d" % (len(fails), len(exceptions), passes))
    print("summary_status: %s" % ("fail" if fails else ("pass-with-exceptions" if exceptions else "pass")))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

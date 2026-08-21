#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MetaUI checks 迴歸自測(外稽 20260712 A2;PREP-UI-2,info_level: Candidate)

固定樣本包=「檢核器必須抓到的病」:外稽 PoC 三繞過面(var fallback/命名色與
現代色彩函數/外掛 stylesheet)+R12 去 AI 感合成病句+B4 三樣本(同名 data-state
重複/data-nav↔href 脫鉤)。斷言型:樣本未被抓到=exit 1。

紀律:改 checks/ 任一檔必跑本檔(SOP 字面=checks/README);樣本只增不減
(誤殺移除須留紀錄);新 bug 修復=先加樣本再修(regression-first)。

Usage:
    python selftest.py        # exit 0=全過
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_copy
import gen_design_md
import gen_tokens
import gen_vuetify_theme
import uiv_checks
from uiv_common import Reporter

UIV10 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uiv10_figma_diff.py")

FAILED = []


def expect(name, cond):
    print("[%s] %s" % ("PASS" if cond else "MISS", name))
    if not cond:
        FAILED.append(name)


def fails_of(rep, pattern_id=None):
    return [f for f in rep.findings if f["classification"] == "fail" and (pattern_id is None or f["pattern_id"] == pattern_id)]


def reviews_of(rep, pattern_id):
    return [f for f in rep.findings if f["classification"] == "needs-review" and f["pattern_id"] == pattern_id]


POC_PAGE = """<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="pageid" content="P99"><meta name="stage" content="styled">
<meta name="primary-action" content="測試主行動">
<link rel="stylesheet" href="../../../DesignSpecs/UIFoundation/tokens.css">
<link rel="stylesheet" href="extra.css">
<style>
  .a { color: var(--undefined-token, #ff0000); }          /* 繞過面1:fallback hex */
  .b { color: tomato; background: oklch(0.7 0.1 200); border-color: darkred; }  /* 繞過面2 */
</style></head><body>
<div data-state="ideal"><h1>PoC 測試頁</h1>
<a href="P99_poc.html" data-nav="P99" data-action="primary">前往下一頁</a></div>
<div data-state="ideal"><p>同名狀態重複宣告(B4)</p></div>
<div data-state="error"><p>err</p><a href="#" data-nav="P98" data-action="primary">修復去</a></div>
</body></html>"""

EXTRA_CSS = ".c { color: #123456; padding: 37px; background: rgb(1,2,3); }  /* 繞過面3 */"

CLEAN_CSS_SAMPLE = """
  .ok { color: var(--color-text); background: transparent; white-space: nowrap;
        padding: var(--spacing-4); border: 1px solid var(--color-divider); }
"""

AF_SAMPLE = "在數位轉型的時代下,我們深信極致體驗。你是否還在等?讓我們一起賦能。這不是工具,而是一站式平台,不僅省時,更能無縫接軌。"

# ── UIV-10 樣本(dark=optional 宣告制+font-weight 型別容錯+集合名配置) ──
T10_TOKENS_LIGHT = {
    "color": {"primary": {"$value": "#123456"}},
    "typography": {"font-size": {"body1": {"$value": "1rem"}},
                   "font-weight": {"bold-w": {"$value": 700}}},
    "spacing": {"1": {"$value": "4px"}},
    "radius": {"sm": {"$value": "4px"}},
}
T10_FIGMA_LIGHT = {"collections": [
    {"name": "MetaUI Color", "vars": [{"name": "primary", "values": {"light": "#123456"}}]},
    {"name": "MetaUI Typography", "vars": [
        {"name": "body1", "values": {"light": 16}},
        {"name": "bold-w", "values": {"light": "Bold"}}]},
    {"name": "MetaUI Spacing", "vars": [
        {"name": "1", "values": {"light": 4}},
        {"name": "sm", "values": {"light": 4}}]},
]}


def run_uiv10(tmp, tokens, figma):
    tp = os.path.join(tmp, "tok.json")
    fp = os.path.join(tmp, "fig.json")
    with open(tp, "w", encoding="utf-8") as f:
        json.dump(tokens, f)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(figma, f)
    r = subprocess.run([sys.executable, UIV10, "--figma", fp, "--tokens", tp],
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # ── 純函數層:UIV-05 css_hardcodes ──
    hits = uiv_checks.css_hardcodes(POC_PAGE.split("<style>")[1].split("</style>")[0])
    expect("A2-1 fallback 內 hex 抓到", any("#ff0000" in h for h in hits))
    expect("A2-2 oklch() 抓到", any("oklch" in h for h in hits))
    expect("A2-2 命名色 tomato/darkred 抓到", any("tomato" in h.lower() for h in hits) and any("darkred" in h.lower() for h in hits))
    expect("A2-4 乾淨樣本零誤殺(transparent/white-space)", uiv_checks.css_hardcodes(CLEAN_CSS_SAMPLE) == [])
    ext_hits = uiv_checks.css_hardcodes(EXTRA_CSS)
    expect("A2-3 外掛表內容:hex+px+rgb 抓到", any("#123456" in h for h in ext_hits) and any("37px" in h for h in ext_hits))

    # ── 純函數層:去 AI 感(R12 樣本回歸) ──
    expect("AF-04 核心詞", any(w in AF_SAMPLE for w in gen_copy.AF04_CORE_WORDS))
    expect("AF-04 擴充詞", bool(gen_copy.AF04_HINT_RE.search(AF_SAMPLE)))
    expect("AF-05 時代開場", bool(gen_copy.AF05_ERA_RE.match(AF_SAMPLE)))
    expect("AF-09 設問", bool(gen_copy.AF09_RHETORIC_RE.match("你是否還在等?")))
    expect("AF-11 假互動", bool(gen_copy.AF11_FAKE_RE.search(AF_SAMPLE)))
    expect("AF-01 對比句", any(rx.search(AF_SAMPLE) for rx in gen_copy.AF01_CONTRAST_RES))
    expect("AF-02 遞進句", bool(gen_copy.AF02_ESCALATE_RE.search(AF_SAMPLE)))
    expect("AF-07 三聯句(clause 計數)", gen_copy.af07_triad("提供查詢、下載、串接。") is not None)
    expect("AF-07 四項不誤列", gen_copy.af07_triad("氣溫、雨量、風速、日照。") is None)
    expect("AF-07 開放枚舉不誤列", gen_copy.af07_triad("災防、保險、農事等任務。") is None)

    # ── 盤古之白反轉(拍板者裁定 2026-08-07:中英數之間不留空格) ──
    expect("PW-1 中英數間混入空格=抓到", bool(gen_copy.CJK_ALNUM_SPACE_RE.search("查詢 API 金鑰共 120 筆")))
    expect("PW-2 緊鄰無空格=乾淨", not gen_copy.CJK_ALNUM_SPACE_RE.search("查詢API金鑰共120筆"))

    # ── 整合層:臨時專案跑 uiv05/uiv03/uiv02 ──
    tmp = tempfile.mkdtemp(prefix="metaui_selftest_")
    try:
        foundation = os.path.join(tmp, "DesignSpecs", "UIFoundation")
        pages = os.path.join(tmp, "DesignSpecs", "F99_poc", "ui", "pages")
        os.makedirs(foundation)
        os.makedirs(pages)
        open(os.path.join(foundation, "tokens.css"), "w", encoding="utf-8").write(":root { --color-text: #000; }\n")
        open(os.path.join(tmp, "DesignSpecs", "03_Structure.md"), "w", encoding="utf-8").write(
            "# 結構\n\n| 節點ID | 名稱 | 狀態 | 路徑 |\n|--------|------|------|------|\n")
        open(os.path.join(pages, "P99_poc.html"), "w", encoding="utf-8").write(POC_PAGE)
        open(os.path.join(pages, "extra.css"), "w", encoding="utf-8").write(EXTRA_CSS)
        f99 = os.path.join(tmp, "DesignSpecs", "F99_poc")

        rep = Reporter("selftest")
        uiv_checks.uiv05(rep, tmp, [f99])
        expect("UIV-05 頁內 hardcode=fail", any("hardcode" in f["detail"] for f in fails_of(rep, "UIV-05")))
        expect("UIV-05 外掛表 hardcode=fail", any("外掛 stylesheet" in f["detail"] for f in fails_of(rep, "UIV-05")))

        rep2 = Reporter("selftest")
        uiv_checks.uiv03(rep2, tmp, [f99])
        expect("UIV-03 同名 data-state 重複=fail(B4)", any("重複宣告" in f["detail"] for f in fails_of(rep2, "UIV-03")))

        rep3 = Reporter("selftest")
        uiv_checks.uiv02(rep3, tmp, [f99])
        expect("UIV-02 nav↔href 脫鉤=needs-review(B4)", any("脫鉤" in f["detail"] for f in reviews_of(rep3, "UIV-02")))

        # ── UIV-10:dark=optional 宣告制+font-weight 容錯+集合名配置(eco-pay 回件) ──
        expect("T10-1 light-only 專案(無 color-dark)不驗 dark=pass",
               run_uiv10(tmp, T10_TOKENS_LIGHT, T10_FIGMA_LIGHT) == 0)
        expect("T10-2 font-weight STRING(Bold vs 700)容錯=pass",
               run_uiv10(tmp, T10_TOKENS_LIGHT, T10_FIGMA_LIGHT) == 0)
        tok_dark = dict(T10_TOKENS_LIGHT)
        tok_dark["color-dark"] = {"primary": {"$value": "#abcdef"}}
        expect("T10-3 宣告 dark 但 Figma 缺 dark 值=fail(咬合不鬆)",
               run_uiv10(tmp, tok_dark, T10_FIGMA_LIGHT) == 1)
        tok_coll = json.loads(json.dumps(T10_TOKENS_LIGHT))
        tok_coll["$extensions"] = {"metaui": {"figma_collections": {
            "color": "Proj Color", "typography": "Proj Typography", "spacing": "Proj Spacing"}}}
        fig_coll = json.loads(json.dumps(T10_FIGMA_LIGHT))
        for c in fig_coll["collections"]:
            c["name"] = c["name"].replace("MetaUI", "Proj")
        expect("T10-4 集合名配置(Proj *)=pass", run_uiv10(tmp, tok_coll, fig_coll) == 0)
        fig_drift = json.loads(json.dumps(T10_FIGMA_LIGHT))
        fig_drift["collections"][0]["vars"][0]["values"]["light"] = "#654321"
        expect("T10-5 light 值漂移=fail(原有咬合)", run_uiv10(tmp, T10_TOKENS_LIGHT, fig_drift) == 1)

        # ── UIV-07:DS 層報告歸屬+來源報告欄多名容錯(eco-pay 回件分流 5) ──
        ds_reviews = os.path.join(foundation, "reviews")
        os.makedirs(ds_reviews)
        f99_reviews = os.path.join(f99, "ui", "reviews")
        os.makedirs(f99_reviews)
        open(os.path.join(ds_reviews, "R90_TokenSync.md"), "w", encoding="utf-8").write(
            "# DS 層報告\n\n| 發現 | 嚴重度 |\n|------|--------|\n| UIX-901 對位缺鍵 | 🔴 |\n")
        open(os.path.join(ds_reviews, "R92_Drift.md"), "w", encoding="utf-8").write(
            "# DS 層報告\n\n| 發現 | 嚴重度 |\n|------|--------|\n| 漂移一筆(樣本故意未配編號) | 🟡 |\n")
        open(os.path.join(f99_reviews, "R91_G0.md"), "w", encoding="utf-8").write("# F 模組報告\n")
        open(os.path.join(foundation, "90_IssueLedger.md"), "w", encoding="utf-8").write(
            "# 議題帳\n\n| UIX | 來源報告 | 狀態 |\n|-----|---------|------|\n"
            "| UIX-901 | R90_TokenSync、R91_G0 | open |\n"
            "| UIX-902 | R99_Missing | open |\n")
        rep7 = Reporter("selftest")
        uiv_checks.uiv07(rep7, tmp, [f99])
        f7 = fails_of(rep7, "UIV-07")
        expect("T07-1 DS 層報告(UIFoundation/reviews)納掃:🟡 未配 UIX=fail",
               any("未配 UIX" in f["detail"] and "UIFoundation/reviews" in f["target"] for f in f7))
        expect("T07-2 DS 層 🔴 配 UIX 且在帳=不誤報",
               not any("UIX-901" in f["detail"] for f in f7))
        expect("T07-3 來源報告欄多名(、分隔)逐名解析=不誤報",
               not any("R90_TokenSync" in f["detail"] or "R91_G0" in f["detail"] for f in f7))
        expect("T07-4 缺席報告 R99_Missing 仍 fail(咬合不鬆)",
               any("R99_Missing" in f["detail"] for f in f7))

        # ── scan_hardcoded 煙霧樣本(brownfield 導入輔助工具;不入閘門仍自證) ──
        scanner = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_hardcoded.py")
        sroot = os.path.join(tmp, "scan_fixture")
        os.makedirs(os.path.join(sroot, "node_modules"))
        open(os.path.join(sroot, "a.scss"), "w", encoding="utf-8").write(
            ".x { margin: 16px; padding: 37px; color: #176466; border: 1px solid #FC890C; }")
        open(os.path.join(sroot, "node_modules", "skip.css"), "w", encoding="utf-8").write(
            ".n { margin: 99px; }")
        stok = os.path.join(tmp, "scan_tokens.json")
        with open(stok, "w", encoding="utf-8") as f:
            json.dump({"color": {"primary": {"$value": "#176466"},
                                 "chart-1": {"$value": "#176466"},
                                 "secondary": {"$value": "#fc890c"}},
                       "spacing": {"5": {"$value": "16px"}},
                       "radius": {"s": {"$value": "4px"}}}, f)
        sout = os.path.join(tmp, "scan_report.md")
        rs = subprocess.run([sys.executable, scanner, "--root", sroot,
                             "--tokens", stok, "--out", sout],
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        rmd = open(sout, "r", encoding="utf-8").read() if os.path.isfile(sout) else ""
        expect("T11s-1 掃描器 exit 0+報告產出", rs.returncode == 0 and "16px" in rmd)
        expect("T11s-2 px 命中 scale=建議 --spacing-5", "--spacing-5" in rmd)
        expect("T11s-3 px scale 外=候討論", "37px" in rmd and "候討論" in rmd)
        expect("T11s-4 hex 大小寫正規化命中(#FC890C→secondary)", "--color-secondary" in rmd)
        expect("T11s-5 同值一對多=語意人判備註", "一對多:語意人判" in rmd)
        expect("T11s-6 node_modules 排除(99px 不入表)", "99px" not in rmd)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ── 生成器側 $modes 宣告制(eco-pay 併版回報 R2:三支生成器與 uiv10 同判準) ──
    TG = {"$modes": ["light"],
          "color": {"primary": {"$value": "#123456"}},
          "color-dark": {"primary": {"$value": "#abcdef"}},
          "spacing": {"1": {"$value": "4px"}}}
    out_light = gen_tokens.build(TG)
    expect("TG-1 宣告 light-only:tokens.css/TokenSheet 不產 dark 區塊",
           "dark_mode" not in out_light["tokens.css"]
           and "Dark Mode 覆寫" not in out_light["00_TokenSheet.md"])
    expect("TG-2 宣告 light-only:vuetify.theme 不產 dark_mode 主題",
           "dark_mode" not in gen_vuetify_theme.build(TG)["vuetify.theme.json"])
    expect("TG-3 宣告 light-only:Design.md 色彩段不產 Dark 覆寫表",
           "Dark Mode 覆寫" not in gen_design_md.build_color_section(TG))
    TG_dual = json.loads(json.dumps(TG))
    TG_dual["$modes"] = ["light", "dark"]
    expect("TG-4 宣告雙 mode:三生成器照產 dark",
           "dark_mode" in gen_tokens.build(TG_dual)["tokens.css"]
           and "dark_mode" in gen_vuetify_theme.build(TG_dual)["vuetify.theme.json"]
           and "Dark Mode 覆寫" in gen_design_md.build_color_section(TG_dual))
    TG_infer = json.loads(json.dumps(TG))
    del TG_infer["$modes"]
    expect("TG-5 未宣告+有 color-dark:推斷產 dark(向後相容)",
           "dark_mode" in gen_tokens.build(TG_infer)["tokens.css"])

    print("-" * 50)
    if FAILED:
        print("selftest FAIL:%d 樣本未被抓到 → %s" % (len(FAILED), " / ".join(FAILED)))
        return 1
    print("selftest PASS(檢核器對固定樣本包全數咬合)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

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
import gen_digest
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


def css_has(hits, needle):
    return any(needle in h for h in hits)


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

# ── UIV-05 樣本(UIX-007/UIX-008，案源 moa-weather R02_G2:首個 styled 頁踩出) ──
# 同一頁同時放:合法斷點、非 token 斷點、條件式 rem 繞道、宣告區 rem 盲區、
# 官方載體與非官方外掛表。未修版=768px 也擋(斷點路全死)且 rem 完全不報。
V5_PAGE = """<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="pageid" content="P97"><meta name="stage" content="styled">
<meta name="primary-action" content="測試主行動">
<link rel="stylesheet" href="../../../UIFoundation/tokens.css">
<link rel="stylesheet" href="../../../UIFoundation/placeholder.css">
<link rel="stylesheet" href="site.css">
<style>
  @media (max-width: 768px) { .a { gap: var(--spacing-3); } }   /* 合法:等於 breakpoint token */
  @media (max-width: 820px) { .b { gap: var(--spacing-3); } }   /* 非 token 值 */
  @media (max-width: 48rem) { .c { gap: var(--spacing-3); } }   /* 無 rem 斷點 token 可用 */
  .d { grid-template-columns: repeat(auto-fit, minmax(min(100%,14rem), 1fr)); }  /* rem 盲區 */
</style></head><body>
<div data-state="ideal"><h1>斷點測試頁</h1>
<a href="P97_media.html" data-nav="P97" data-action="primary">下一頁</a></div>
</body></html>"""

V5_FOUNDATION_CSS = """.ph-slot { gap: var(--spacing-3);
  border: 1px dashed var(--color-divider); min-height: var(--imagery-ph-min-h); }
"""

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


# ── gen_digest 樣本(UIX-003/UIX-004，案源 moa-weather R00_G0) ──
# 一個 F 模組裡同時放:句中引用、已解鎖(刪除線)宣告、廢除節點之 TBD、
# 相鄰兩條 TBD 只有後者有預設假設。未修版會把這些全當未決項列出。
DG_STRUCTURE = """# 結構

##### F01_digest
| 節點ID | 名稱 | 狀態 | 層級 | 實體檔案路徑 |
|--------|------|------|------|-------------|
| M09-F01-W01 | 活躍節點 | S4_SYNC_DONE | 業務流程 | nodes/M09-F01-W01_活躍節點.md |
| M09-F01-W02 | 已廢除節點 | **DEPRECATED** | 業務流程 | nodes/M09-F01-W02_已廢除節點.md |
| M09-F01-W03 | 未展開節點 | PLANNED | - | 尚未建立 |
| M09-F01-W99 | Out-of-Scope佔位符 | RESERVED | - | nodes/M09-F01-W99_OutOfScope.md |
""" + "".join("| M09-F01-W%02d | 未展開節點%d | PLANNED | - | 尚未建立 |\n" % (i, i)
              for i in range(4, 20))

DG_SCOPE = """# 範疇

## Epic 清單

| EP## | Epic 名稱 | 對應 M-F | 業務目標 |
|------|----------|---------|---------|
| EP01 | 活躍 Epic | M09-F01 | 對應節點仍在展開中。 |
| ~~EP02~~ | ~~已廢除 Epic~~ ⛔已廢除 | ~~M09-F01~~ | 節點已併入他處。 |
| EP03 | 未展開 Epic | M09-F01 | 對應節點全為 PLANNED。 |
| ~~EP04~~ | ~~另一個已廢除 Epic~~ ⛔已廢除 | ~~M09-F01~~ | 併入 EP01。 |
"""

DG_NODE_W01 = """---
node_id: M09-F01-W01
epic: EP01_活躍 Epic
status: S4_SYNC_DONE
---
# 規格節點

## 業務規則
- 規則一:實際網址字串見 `[!TBD-W01-01]`(實作層，不影響版面與行為設計)。

## 開放問題與決策紀錄
- `[!TBD-W01-01]` 甲項未定。
  > 🔒 **解鎖條件**:待外部單位回覆。
- `[!TBD-W01-02]` 乙項未定。
  > 💡 **預設假設**:假設乙。
- ~~`[!TBD-W01-03]`~~ **已解鎖**:丙項已於 DEC 拍板。
"""

DG_NODE_W02 = """---
node_id: M09-F01-W02
epic: EP02_已廢除 Epic
status: DEPRECATED
---
# 規格節點

## 開放問題與決策紀錄
- `[!TBD-W02-01]` 丁項未定。
  > 💡 **預設假設**:假設丁。
"""

DG_NODE_W99 = """---
node_id: M09-F01-W99
status: RESERVED
---
# Out-of-Scope佔位符
"""


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

        # ── UIV-07 掃描面固定全 repo + 佔位跨分隔符(2026-08-20 案源:moa PR#84/#85、NP UIX-015) ──
        f98 = os.path.join(tmp, "DesignSpecs", "F98_other")
        os.makedirs(os.path.join(f98, "ui", "reviews"))
        open(os.path.join(f98, "ui", "reviews", "R01_G1.md"), "w", encoding="utf-8").write(
            "# 他模組獨有報告\n")
        open(os.path.join(foundation, "90_IssueLedger.md"), "w", encoding="utf-8").write(
            "# 議題帳\n\n| UIX | 來源報告 | 狀態 |\n|-----|---------|------|\n"
            "| UIX-903 | R01_G1 | open |\n"
            "| UIX-904 | ⟪RWD/A11y 規則補建輪次·未立 R 報告⟫ | open |\n")
        rep7b = Reporter("selftest")
        uiv_checks.uiv07(rep7b, tmp, [f99])          # 故意只給 f99，報告卻在 f98
        f7b = fails_of(rep7b, "UIV-07")
        expect("T07-5 帳上他模組獨有報告(R01_G1)，以單模組 scope 呼叫不誤報",
               not any("R01_G1" in f["detail"] for f in f7b))
        expect("T07-6 佔位含分隔符(⟪RWD/A11y…⟫)不被拆成假報告名",
               not any("A11y" in f["detail"] for f in f7b))

        # ── UIV-12:尚未開工(無 ui/)之 F 模組不報 G0 缺席(NP 14 筆誤報案源) ──
        f97 = os.path.join(tmp, "DesignSpecs", "F97_notstarted")
        os.makedirs(f97)
        rep12 = Reporter("selftest")
        uiv_checks.uiv12(rep12, tmp, [f97])
        expect("T12-1 無 ui/ 之 F 模組=不適用，不報 G0 缺席",
               not fails_of(rep12, "UIV-12"))
        rep12b = Reporter("selftest")
        uiv_checks.uiv12(rep12b, tmp, [f98])          # 有 ui/ 但無 R##_G0
        expect("T12-2 有 ui/ 但缺 G0 報告=仍 fail(咬合不鬆)",
               any("G0 報告" in f["detail"] for f in fails_of(rep12b, "UIV-12")))

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

    # ── UIV-05:@media 條件式與官方載體(UIX-007/UIX-008) ──
    v5tmp = tempfile.mkdtemp(prefix="metaui_selftest_uiv05_")
    try:
        v5f = os.path.join(v5tmp, "DesignSpecs", "UIFoundation")
        v5p = os.path.join(v5tmp, "DesignSpecs", "F97_v5", "ui", "pages")
        os.makedirs(v5f)
        os.makedirs(v5p)
        with open(os.path.join(v5f, "tokens.json"), "w", encoding="utf-8") as f:
            json.dump({"breakpoint": {"tablet": {"$value": "768px"}}}, f)
        open(os.path.join(v5f, "tokens.css"), "w", encoding="utf-8").write(":root { --spacing-3: 12px; }\n")
        open(os.path.join(v5f, "placeholder.css"), "w", encoding="utf-8").write(V5_FOUNDATION_CSS)
        open(os.path.join(v5p, "site.css"), "w", encoding="utf-8").write(V5_FOUNDATION_CSS)
        open(os.path.join(v5p, "P97_media.html"), "w", encoding="utf-8").write(V5_PAGE)

        rep5 = Reporter("selftest")
        uiv_checks.uiv05(rep5, v5tmp, [os.path.join(v5tmp, "DesignSpecs", "F97_v5")])
        f5 = " ".join(f["detail"] for f in fails_of(rep5, "UIV-05"))
        r5 = " ".join(f["detail"] for f in reviews_of(rep5, "UIV-05"))

        expect("V5-1 條件式 px 等於 breakpoint token=不擋", "768px" not in f5)
        expect("V5-2 條件式 px 非 token 值=fail", "820px(條件式" in f5)
        expect("V5-2b em 與 rem 都算相對長度",
               uiv_checks.css_rem_literals("@media (max-width:40em){.a{width:2rem}}") == ["40em", "2rem"])
        expect("V5-3 條件式 rem=needs-review 不擋閘(無 rem 斷點 token 可用)",
               "48rem" in r5 and "48rem" not in f5)
        expect("V5-4 宣告區 rem=needs-review 非 fail",
               "相對長度單位" in r5 and "14rem" in r5 and "14rem" not in f5)
        expect("V5-5 UIFoundation 官方載體不報白名單外", "placeholder.css" not in r5)
        expect("V5-6 非官方外掛表照報白名單外", "site.css(非 UIFoundation" in r5)

        # 純函數層:白名單來源與盲區邊界
        bps = uiv_checks.breakpoint_values(v5tmp)
        expect("V5-7 白名單取自 tokens.json breakpoint", bps == {"768"})
        expect("V5-8 專案無 breakpoint token=條件式維持零容忍",
               any("768px(條件式" in h for h in uiv_checks.css_hardcodes("@media (max-width:768px){.a{gap:0}}", set())))
        expect("V5-9 條件式豁免不外溢到宣告區",
               any(h == "768px" for h in uiv_checks.css_hardcodes(".a { padding: 768px; }", {"768"})))
        expect("V5-10 官方載體夾 hardcode 一樣 fail(白名單非免死金牌)",
               css_has(uiv_checks.css_hardcodes(".x{color:#123456}", {"768"}), "#123456"))
    finally:
        shutil.rmtree(v5tmp, ignore_errors=True)

    # ── gen_digest:TBD 宣告位與閥值活躍面(UIX-003/UIX-004) ──
    dtmp = tempfile.mkdtemp(prefix="metaui_selftest_digest_")
    try:
        f_dir = os.path.join(dtmp, "DesignSpecs", "M09_x", "F01_digest")
        os.makedirs(os.path.join(f_dir, "nodes"))
        specs = os.path.join(dtmp, "DesignSpecs")
        for rel, body in [("03_Structure.md", DG_STRUCTURE), ("02_Scope.md", DG_SCOPE)]:
            open(os.path.join(specs, rel), "w", encoding="utf-8").write(body)
        for rel, body in [("M09-F01-W01_活躍節點.md", DG_NODE_W01),
                          ("M09-F01-W02_已廢除節點.md", DG_NODE_W02),
                          ("M09-F01-W99_OutOfScope.md", DG_NODE_W99)]:
            open(os.path.join(f_dir, "nodes", rel), "w", encoding="utf-8").write(body)

        names = gen_digest.node_names(dtmp, "M09-F01")
        metas = gen_digest.node_meta(f_dir)
        tbds = gen_digest.tbd_inventory(f_dir, names, metas)
        ids = [x[0] for x in tbds]
        al = " ".join(gen_digest.alarms(dtmp, f_dir, "M09-F01", names, metas))

        expect("DG-1 宣告位:句中引用不重複計入", ids == ["TBD-W01-01", "TBD-W01-02"])
        expect("DG-2 已解鎖(刪除線)宣告不列為未決", "TBD-W01-03" not in ids)
        expect("DG-3 已廢除節點之 TBD 不列", "TBD-W02-01" not in ids)
        expect("DG-4 描述取宣告位而非句中殘字", tbds and tbds[0][1] == "甲項未定")
        expect("DG-5 預設假設不跨列串味", tbds and tbds[0][2] == "" and "假設乙" in tbds[1][2])
        expect("DG-6 閥值只數活躍 Epic(廢除/無活躍節點者不計)",
               "Epic 活躍 1／登記 4" in al and "EP02(已廢除)" in al
               and "EP04(已廢除)" in al and "EP03(無活躍節點)" in al)
        expect("DG-7 閥值只數活躍節點(DEPRECATED/PLANNED/W99 不計)",
               "業務節點 活躍 1／登記 19" in al and "DEPRECATED:W02" in al and "PLANNED:W03/W04" in al)
        expect("DG-8 長清單收斂但總數不藏", "等 17 個" in al)
        expect("DG-9 死項撐不起閥值:登記 4 Epic／19 節點但活躍面不觸發", "建議評估" not in al)
    finally:
        shutil.rmtree(dtmp, ignore_errors=True)

    print("-" * 50)
    if FAILED:
        print("selftest FAIL:%d 樣本未被抓到 → %s" % (len(FAILED), " / ".join(FAILED)))
        return 1
    print("selftest PASS(檢核器對固定樣本包全數咬合)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

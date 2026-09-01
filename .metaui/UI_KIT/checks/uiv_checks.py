#!/usr/bin/env python3
"""MetaUI UIV-01~09 檢核實作(PREP-UI-1,info_level: Candidate)

各檢核的檢查對象/方法/預期/失敗處置見 checks/README.md 清冊。
誠實邊界:語意判斷不假機械化，拋 needs-review(VerifyReportSchema §六)。
"""
import os
import re

from uiv_common import (
    read_text, parse_md_tables, col_index, cell, parse_page, find_all_f_dirs,
)

P_RE = re.compile(r"\bP\d{2,}\b")
NODE_RE = re.compile(r"\b(M\d+-F\d+-W\d+)\b")
TBD_RE = re.compile(r"\[!(TBD-[^\]\s]+)\]")
PLACEHOLDER = "⟪"
# 佔位整段(含閉合)。佔位內若含分隔符，逐段拆解會使後半段失去 ⟪ 而誤判為真報告名
# (2026-08-20 案源:NP UIX-015 來源欄 ⟪RWD/A11y 規則補建輪次·未立 R 報告⟫)。
PLACEHOLDER_SPAN_RE = re.compile(r"⟪[^⟫]*⟫")


# ── 資料收集 ──────────────────────────────────────────────

def flow_path(f_dir):
    return os.path.join(f_dir, "ui", "10_UIFlow.md")


def pages_of(f_dir):
    d = os.path.join(f_dir, "ui", "pages")
    if not os.path.isdir(d):
        return []
    return sorted(os.path.join(d, x) for x in os.listdir(d) if x.endswith(".html"))


def proto_pages_of(f_dir):
    """產品視圖(45_PrototypeView):ui/pages/proto/*.html;納 01/02/04/05/08/09/11，五態 03 不適用。"""
    d = os.path.join(f_dir, "ui", "pages", "proto")
    if not os.path.isdir(d):
        return []
    return sorted(os.path.join(d, x) for x in os.listdir(d) if x.endswith(".html"))


def registry_rows(flow_text):
    """從 10_UIFlow.md 取頁面登記表 → list of dict;找不到回 None。"""
    for t in parse_md_tables(flow_text):
        h = t["headers"]
        pi = col_index(h, "P##", "P#")
        if pi < 0:
            continue
        return [{
            "p": cell(r, pi),
            "name": cell(r, col_index(h, "頁面名", "頁面")),
            "w": cell(r, col_index(h, "承載")),
            "task": cell(r, col_index(h, "主任務")),
            "primary": cell(r, col_index(h, "primary")),
            "stage": cell(r, col_index(h, "階段")),
            "path": cell(r, col_index(h, "檔案路徑", "路徑")),
        } for r in t["rows"] if cell(r, pi)]
    return None


def page_id_of(path, parsed):
    m = re.match(r"(P\d+)", os.path.basename(path))
    fid = m.group(1) if m else None
    mid = parsed.metas.get("pageid")
    return fid, mid


def structure_nodes(project):
    """03_Structure.md → (登記節點 id 集， 路徑欄清單 [(id, path, status)]);檔缺回 (None, None)。"""
    p = os.path.join(project, "DesignSpecs", "03_Structure.md")
    if not os.path.isfile(p):
        return None, None
    text = read_text(p)
    ids = set(NODE_RE.findall(text))
    rows = []
    for t in parse_md_tables(text):
        h = t["headers"]
        ni = col_index(h, "節點ID", "節點")
        pi = col_index(h, "實體檔案路徑", "路徑")
        si = col_index(h, "狀態")
        if ni < 0 or pi < 0:
            continue
        for r in t["rows"]:
            rows.append((cell(r, ni), cell(r, pi), cell(r, si)))
    return ids, rows


def glossary_terms(project):
    p = os.path.join(project, "DesignSpecs", "00_Glossary.md")
    if not os.path.isfile(p):
        return None
    terms = set()
    for t in parse_md_tables(read_text(p)):
        for r in t["rows"]:
            v = cell(r, 0)
            if v and not v.startswith("<!--") and not v.startswith("DEC-"):
                terms.add(v)
    return terms


def open_tbds(f_dir):
    """F 模組 nodes/*.md 與 *REVIEW*.md 內仍存在的 TBD 標記。回 (全集， 節點→TBD 映射)。"""
    ids, by_node = set(), {}
    nodes_dir = os.path.join(f_dir, "nodes")
    if os.path.isdir(nodes_dir):
        for x in os.listdir(nodes_dir):
            if x.endswith(".md"):
                found = set(TBD_RE.findall(read_text(os.path.join(nodes_dir, x))))
                if found:
                    # 檔名如 M01-F01-W01_名稱.md:W01 後接底線，\b 會失效，改錨定於行首
                    m = re.match(r"(M\d+-F\d+-W\d+)", x)
                    if m:
                        by_node[m.group(1)] = found
                    ids |= found
    for x in os.listdir(f_dir):
        if x.endswith(".md") and "REVIEW" in x.upper():
            ids |= set(TBD_RE.findall(read_text(os.path.join(f_dir, x))))
    return ids, by_node


def rel(project, path):
    try:
        return os.path.relpath(path, project).replace("\\", "/")
    except ValueError:
        return path


# ── UIV-01 頁面登記對齊 ───────────────────────────────────

def uiv01(rep, project, f_dirs):
    P = "UIV-01"
    for f in f_dirs:
        fp, pages = flow_path(f), pages_of(f)
        if not os.path.isfile(fp):
            if pages:
                for pg in pages:
                    rep.fail(P, rel(project, pg), "頁面存在但無 10_UIFlow.md 登記表(私建，違先登記後產檔)")
            continue
        rows = registry_rows(read_text(fp))
        if rows is None:
            rep.perror(P, rel(project, fp), "找不到頁面登記表(P## 欄)")
            continue
        reg = {r["p"]: r for r in rows}
        seen = {}
        for pg in pages:
            parsed = parse_page(pg)
            fid, mid = page_id_of(pg, parsed)
            pid = fid or mid
            if not pid:
                rep.fail(P, rel(project, pg), "檔名與 meta 均無 P## 編號")
                continue
            seen[pid] = pg
            if fid and mid and fid != mid:
                rep.fail(P, rel(project, pg), "檔名 %s 與 meta pageid %s 不一致" % (fid, mid))
            if pid not in reg:
                rep.fail(P, rel(project, pg), "%s 未在登記表登記(私建)" % pid)
        for pid, r in reg.items():
            target = os.path.normpath(os.path.join(f, "ui", r["path"])) if r["path"] else ""
            if not r["path"] or not os.path.isfile(target):
                rep.fail(P, rel(project, fp), "%s 已登記但檔案未產出/路徑無效: %s" % (pid, r["path"] or "(空)"))
        # 產品視圖對齊(45_PrototypeView 規則 6/7):階段=prototype ↔ proto 檔雙向
        protos = proto_pages_of(f)
        seen_proto = set()
        for pg in protos:
            parsed = parse_page(pg)
            fid, mid = page_id_of(pg, parsed)
            pid = fid or mid
            if not pid:
                rep.fail(P, rel(project, pg), "proto 檔名與 meta 均無 P## 編號")
                continue
            seen_proto.add(pid)
            if pid not in reg:
                rep.fail(P, rel(project, pg), "proto %s 未在登記表登記(私建)" % pid)
            elif "prototype" not in reg[pid]["stage"]:
                rep.fail(P, rel(project, pg), "proto %s 存在但登記表階段=%s(未同步為 prototype)" % (pid, reg[pid]["stage"] or "(空)"))
            elif reg[pid]["path"] and os.path.basename(pg) != os.path.basename(reg[pid]["path"]):
                rep.fail(P, rel(project, pg), "proto 檔名 %s 與審查視圖 %s 不同名(45 規則 7)" % (
                    os.path.basename(pg), os.path.basename(reg[pid]["path"])))
            if parsed.metas.get("stage") != "prototype":
                rep.fail(P, rel(project, pg), "proto 頁 meta stage=%s(須 prototype)" % (parsed.metas.get("stage") or "(空)"))
        for pid, r in reg.items():
            if "prototype" in r["stage"] and pid not in seen_proto:
                rep.fail(P, rel(project, fp), "%s 階段=prototype 但 proto 檔未產出(pages/proto/)" % pid)
        rep.ok(P, rel(project, f), "登記 %d 頁 / 實體 %d 頁 / proto %d 頁比對完成" % (len(reg), len(pages), len(protos)))


# ── UIV-02 規格錨定與連結完整 ─────────────────────────────

def uiv02(rep, project, f_dirs):
    P = "UIV-02"
    node_ids, node_rows = structure_nodes(project)
    if node_ids is None:
        rep.perror(P, "DesignSpecs/03_Structure.md", "檔案缺席，錨定無從驗證(殘缺部署?)")
        return
    # G0 面:03_Structure 路徑欄實體存在性(對齊 VP-01 索引對齊精神)
    for nid, npath, status in node_rows or []:
        if not npath or "尚未建立" in npath or "PLANNED" in status.upper() or status == "-":
            continue
        if not os.path.isfile(os.path.join(project, "DesignSpecs", npath)):
            rep.fail(P, "03_Structure.md", "%s 登記路徑不存在: %s" % (nid, npath))
    for f in f_dirs:
        fp = flow_path(f)
        if os.path.isfile(fp):
            text = read_text(fp)
            rows = registry_rows(text) or []
            reg_p = {r["p"] for r in rows}
            mermaid = "\n".join(re.findall(r"```mermaid(.*?)```", text, re.S))
            for pid in set(P_RE.findall(mermaid)):
                if pid not in reg_p:
                    rep.fail(P, rel(project, fp), "flow 節點 %s 未在登記表" % pid)
            for m in re.finditer(r'click\s+\S+\s+"([^"]+)"', mermaid):
                t = os.path.normpath(os.path.join(f, "ui", m.group(1)))
                if not os.path.isfile(t):
                    rep.fail(P, rel(project, fp), "click 路徑不存在: %s" % m.group(1))
            for w in set(NODE_RE.findall("\n".join(r["w"] for r in rows))):
                if w not in node_ids:
                    rep.fail(P, rel(project, fp), "登記表承載節點 %s 未在 03_Structure 登記" % w)
        for pg in pages_of(f) + proto_pages_of(f):
            parsed = parse_page(pg)
            for w in parsed.data_w:
                if w and w not in node_ids:
                    rep.fail(P, rel(project, pg), "data-w=%s 未在 03_Structure 登記(範本殘留亦屬違規)" % w)
            for lk in parsed.links:
                nav, href = lk["data_nav"], lk["href"]
                if not nav:
                    rep.fail(P, rel(project, pg), "連結未型別化(缺 data-nav): href=%s" % (href or "(空)"))
                    continue
                if nav.startswith("P"):
                    if href.endswith(".html"):
                        t = os.path.normpath(os.path.join(os.path.dirname(pg), href))
                        if not os.path.isfile(t):
                            rep.fail(P, rel(project, pg), "data-nav=%s 目標檔不存在: %s" % (nav, href))
                    else:
                        rep.review(P, rel(project, pg), "data-nav=%s 而 href=%s 非 .html——宣告與連結脫鉤，是否合法(如錨點佔位)屬 R 層(外稽 20260712 B4)" % (nav, href or "(空)"))
                elif nav.startswith("external:") or nav == "W99":
                    pass
                else:
                    rep.fail(P, rel(project, pg), "data-nav 型別不明: %s(須 P##/external:名/W99)" % nav)
    rep.ok(P, rel(project, project), "錨定與連結掃描完成(節點登記 %d 筆)" % len(node_ids))


# ── UIV-03 五態覆蓋 ───────────────────────────────────────

REQUIRED_STATES = {"blank", "loading", "partial", "error", "ideal"}


def uiv03(rep, project, f_dirs):
    P = "UIV-03"
    total = 0
    for f in f_dirs:
        for pg in pages_of(f):
            total += 1
            parsed = parse_page(pg)
            have = set(parsed.states)
            na = set(parsed.state_na)
            for s, reason in parsed.state_na.items():
                if not reason.strip() or PLACEHOLDER in reason:
                    rep.fail(P, rel(project, pg), "data-state-na=%s 缺具體理由(data-reason)" % s)
            dup = have & na
            if dup:
                rep.fail(P, rel(project, pg), "狀態同時宣告 data-state 與 data-state-na: %s" % ", ".join(sorted(dup)))
            multi = sorted({s for s in have if parsed.states.count(s) > 1})
            if multi:
                rep.fail(P, rel(project, pg), "同名 data-state 重複宣告: %s(一狀態一區塊;外稽 20260712 B4)" % ", ".join(multi))
            missing = REQUIRED_STATES - have - na
            if missing:
                rep.fail(P, rel(project, pg), "五態缺席: %s(補區塊或以 data-state-na+理由標 N/A)" % ", ".join(sorted(missing)))
    rep.ok(P, rel(project, project), "五態覆蓋掃描完成(%d 頁)" % total)


# ── UIV-04 術語對齊 ───────────────────────────────────────

def uiv04(rep, project, f_dirs):
    P = "UIV-04"
    terms = glossary_terms(project)
    if terms is None:
        rep.perror(P, "DesignSpecs/00_Glossary.md", "檔案缺席，術語無從比對(殘缺部署?)")
        return
    used = 0
    for f in f_dirs:
        for pg in pages_of(f) + proto_pages_of(f):
            for t in parse_page(pg).data_term:
                used += 1
                if t and PLACEHOLDER not in t and t not in terms:
                    rep.fail(P, rel(project, pg), "data-term=%s 不在 00_Glossary(術語漂移或字典缺登)" % t)
    rep.ok(P, rel(project, project), "術語比對完成(字典 %d 條 / 頁面標記 %d 處);可見文字模糊比對屬 R 層" % (len(terms), used))


# ── UIV-05 樣式 lint(styled 階段)──────────────────────────

PX_WHITELIST = {"0", "1"}
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
FUNC_RE = re.compile(r"\b(?:rgb|rgba|hsl|hsla|oklch|oklab|lab|lch|hwb|color)\(")
PX_RE = re.compile(r"\b(\d+(?:\.\d+)?)px\b")
VAR_RE = re.compile(r"var\([^)]*\)")
# 外稽 20260712 A2 補洞:var() fallback 段先掃再剝/顏色函數家族補齊/命名色/外掛表連帶掃
VAR_FALLBACK_RE = re.compile(r"var\(\s*[^,)]+,([^)]+)\)")
CSS_NAMED_COLORS = {
    "black", "silver", "gray", "grey", "white", "maroon", "red", "purple", "fuchsia",
    "green", "lime", "olive", "yellow", "navy", "blue", "teal", "aqua", "orange",
    "tomato", "gold", "pink", "brown", "coral", "salmon", "crimson", "indigo",
    "violet", "khaki", "beige", "ivory", "azure", "lavender", "darkred", "darkblue",
    "darkgreen", "darkgray", "darkgrey", "lightgray", "lightgrey", "lightblue",
    "lightgreen", "skyblue", "steelblue", "rebeccapurple",
}
# transparent/currentColor/inherit=合法關鍵字非色值，不入表(誤殺防護)
NAMED_IN_VALUE_RE = re.compile(r"(?<![-\w])([a-zA-Z]{3,})(?![-\w(])")
# @media/@container 條件式:CSS 規範不允許條件式消費 var()，零容忍會讓 --breakpoint-*
# 變成無法使用的資產(案源=moa UIX-007)。故條件式另案處理——只認等於某個
# --breakpoint-* token 值的 px，語意仍受 token 控管。
AT_COND_RE = re.compile(r"@(?:media|container)[^{;]*", re.I)
COND_PX_RE = re.compile(r"\b(\d+(?:\.\d+)?)px\b")
# 相對長度單位字面(rem/em)=掃描盲區(同案源):治理意義同 px 硬寫值，但目前無對應
# token 分類可替代——宣告區沒有「欄位最小寬度」類 token，條件式也沒有 rem 斷點
# token。缺替代路徑就判 fail 等於再造一個 UIX-007，故一律列 needs-review 交 R 層
# (候選登記見 checks/README 成長迴路;實證需求=eco-pay 7 頁 48rem/64rem 斷點)。
REM_RE = re.compile(r"\b(\d+(?:\.\d+)?)(r?em)\b")
# UIFoundation 底下的 .css=DS 層官方載體(tokens.css 生成物、placeholder.css 佔位契約),
# 不報「白名單外」;內容照掃，官方載體一樣不准夾 hardcode(案源=moa UIX-008)。
FOUNDATION_REL = os.path.join("DesignSpecs", "UIFoundation")


def breakpoint_values(project):
    """tokens.json 的 --breakpoint-* 值集合(純數字字串)，供 @media 條件式白名單。

    專案沒定義 breakpoint token 時回空集合=條件式維持零容忍——沒有 token 就沒有
    可控語意，不能因為「反正 var() 用不了」就把 px 全放行。
    """
    src = os.path.join(project, FOUNDATION_REL, "tokens.json")
    if not os.path.isfile(src):
        return set()
    try:
        import json as _json
        data = _json.loads(read_text(src))
    except Exception:
        return set()
    out = set()
    for v in (data.get("breakpoint") or {}).values():
        if isinstance(v, dict) and "$value" in v:
            m = PX_RE.search(str(v["$value"]))
            if m:
                out.add(m.group(1))
    return out


def css_rem_literals(css_raw):
    """回傳相對長度單位字面(rem/em)，宣告區與 @media 條件式一併計。"""
    return ["%s%s" % t for t in REM_RE.findall(VAR_RE.sub("var()", css_raw))]


def css_hardcodes(css_raw, breakpoints=None):
    """回傳 hardcode 值清單:hex/顏色函數/px(白名單外)/命名色;var() fallback 段先掃再剝。

    @media/@container 條件式另案:只認等於 --breakpoint-* token 值的 px(見 AT_COND_RE 註);
    條件式內的 rem/em 不在此列，走 css_rem_literals 的 needs-review 面。
    """
    hits = []
    allowed = set(breakpoints or ())
    for m in AT_COND_RE.finditer(css_raw):
        for val in COND_PX_RE.findall(m.group(0)):
            if val not in allowed and val not in PX_WHITELIST:
                hits.append("%spx(條件式須用 --breakpoint-* 的值)" % val)
    css_raw = AT_COND_RE.sub("@media ", css_raw)
    for m in VAR_FALLBACK_RE.finditer(css_raw):
        fb = m.group(1)
        hits += HEX_RE.findall(fb) + [x + "(" for x in FUNC_RE.findall(fb)]
        hits += ["%spx" % v for v in PX_RE.findall(fb) if v not in PX_WHITELIST]
        hits += ["fallback:" + w for w in NAMED_IN_VALUE_RE.findall(fb) if w.lower() in CSS_NAMED_COLORS]
    css = VAR_RE.sub("var()", css_raw)
    hits += HEX_RE.findall(css) + FUNC_RE.findall(css)
    hits += ["%spx" % v for v in PX_RE.findall(css) if v not in PX_WHITELIST]
    values_text = " ".join(re.findall(r":([^;{}]*)", css))
    hits += [w for w in NAMED_IN_VALUE_RE.findall(values_text) if w.lower() in CSS_NAMED_COLORS]
    return hits


def is_foundation_css(project, path):
    """DS 層官方載體判定:落在 DesignSpecs/UIFoundation/ 底下的樣式表。"""
    base = os.path.normpath(os.path.join(project, FOUNDATION_REL)) + os.sep
    return os.path.normpath(path).startswith(base)


def uiv05(rep, project, f_dirs):
    P = "UIV-05"
    bps = breakpoint_values(project)
    styled = 0
    proto = 0
    for f in f_dirs:
        for pg in pages_of(f) + proto_pages_of(f):
            parsed = parse_page(pg)
            stage = parsed.metas.get("stage")
            if stage not in ("styled", "prototype"):
                continue
            if stage == "prototype":
                proto += 1
            else:
                styled += 1
            if not any("tokens.css" in s for s in parsed.stylesheets):
                rep.fail(P, rel(project, pg), "styled 頁未連結 tokens.css")
            rem_hits = []
            for s in parsed.stylesheets:
                t = os.path.normpath(os.path.join(os.path.dirname(pg), s))
                if not os.path.isfile(t):
                    rep.fail(P, rel(project, pg), "stylesheet 連結不可解析: %s" % s)
                    continue
                if os.path.basename(t) == "tokens.css":
                    continue          # 生成物=值的來源，不掃自己
                ext_css = read_text(t)
                ext_hits = css_hardcodes(ext_css, bps)
                rem_hits += css_rem_literals(ext_css)
                if ext_hits:
                    sample = ", ".join(sorted(set(ext_hits))[:6])
                    rep.fail(P, rel(project, pg), "外掛 stylesheet %s 含 hardcode %d 處(樣本: %s)" % (s, len(ext_hits), sample))
                elif not is_foundation_css(project, t):
                    rep.review(P, rel(project, pg), "外掛 stylesheet %s(非 UIFoundation 官方載體)——內容本輪無 hardcode，是否合法組態屬 R 層" % s)
            page_css = "\n".join(parsed.style_blocks + parsed.inline_styles)
            hardcode = css_hardcodes(page_css, bps)
            rem_hits += css_rem_literals(page_css)
            if hardcode:
                sample = ", ".join(sorted(set(hardcode))[:8])
                rep.fail(P, rel(project, pg), "hardcode 值 %d 處(樣本: %s);一律改 var(--token),fallback 段同禁" % (len(hardcode), sample))
            if rem_hits:
                sample = ", ".join(sorted(set(rem_hits))[:6])
                rep.review(P, rel(project, pg), "相對長度單位字面(rem/em)%d 處(樣本: %s)——治理意義同 px 硬寫值，惟目前無對應 token 分類可替代(宣告區無欄寬類 token、條件式無 rem 斷點 token)，本輪交 R 層判讀;候選登記見 checks/README(補齊分類後轉 fail)" % (len(rem_hits), sample))
    rep.ok(P, rel(project, project), "樣式 lint 完成(styled 頁 %d / proto 頁 %d;wire 頁不適用;fallback/命名色/外掛表納掃;@media 條件式認 --breakpoint-* 值 %d 個;rem/em 字面列 needs-review)" % (styled, proto, len(bps)))


# ── UIV-06 生成物新鮮度 ───────────────────────────────────

def uiv06(rep, project, f_dirs):
    P = "UIV-06"
    foundation = os.path.join(project, "DesignSpecs", "UIFoundation")
    src = os.path.join(foundation, "tokens.json")
    if not os.path.isfile(src):
        rep.review(P, "DesignSpecs/UIFoundation/tokens.json",
                   "tokens.json 缺席——G2 無 token 基準，整閘 ⚪(40_TokenPipeline);未採用 token 管線的專案屬正常組態(是否採用歸 R 層)")
        return
    import json as _json
    import gen_tokens
    try:
        data = _json.loads(read_text(src))
        outputs = gen_tokens.build(data)
    except Exception as e:
        rep.perror(P, rel(project, src), "tokens.json 解析/生成失敗: %s" % e)
        return
    for name, content in outputs.items():
        path = os.path.join(foundation, name)
        if not os.path.isfile(path):
            rep.fail(P, rel(project, path), "生成物缺席，執行 gen_tokens.py")
        elif read_text(path) != content:
            rep.fail(P, rel(project, path), "生成物過期(與 tokens.json 重生成結果不一致)，禁手改、請重生成")
    try:
        import gen_design_md
        design_content = gen_design_md.build_design_md(data, project)
        design_path = os.path.join(foundation, "Design.md")
        if os.path.isfile(design_path):
            if read_text(design_path) != design_content:
                rep.fail(P, rel(project, design_path), "Design.md 資料段過期(與 tokens.json 重生成結果不一致)，執行 gen_design_md.py")
        else:
            rep.review(P, rel(project, design_path), "Design.md 缺席——採用設計文件的專案請執行 gen_design_md.py;未採用則屬正常組態(是否採用歸 R 層)")
    except ImportError:
        pass
    except Exception as e:
        rep.perror(P, rel(project, foundation), "Design.md 新鮮度比對失敗: %s" % e)
    try:
        import gen_vuetify_theme
        vt_outputs = gen_vuetify_theme.build(data)
        for name, content in vt_outputs.items():
            path = os.path.join(foundation, name)
            if not os.path.isfile(path):
                rep.review(P, rel(project, path), "生成物缺席——Vuetify 專案請執行 gen_vuetify_theme.py;非 Vuetify 專案屬正常組態(是否採用歸 R 層)")
            elif read_text(path) != content:
                rep.fail(P, rel(project, path), "生成物過期，執行 gen_vuetify_theme.py")
    except ImportError:
        pass
    except Exception as e:
        rep.perror(P, rel(project, foundation), "vuetify.theme.json 新鮮度比對失敗: %s" % e)
    rep.ok(P, rel(project, foundation), "生成物新鮮度比對完成")


# ── UIV-07 報告↔議題帳同步 ────────────────────────────────

UIX_RE = re.compile(r"\bUIX-\d{3,}\b")
SEV_RE = re.compile(r"[🔴🟡]")


def uiv07(rep, project, f_dirs):
    P = "UIV-07"
    ledger_path = os.path.join(project, "DesignSpecs", "UIFoundation", "90_IssueLedger.md")
    ledger_ids, ledger_srcs = set(), []
    if os.path.isfile(ledger_path):
        ltext = read_text(ledger_path)
        ledger_ids = set(UIX_RE.findall(ltext))
        for t in parse_md_tables(ltext):
            si = col_index(t["headers"], "來源報告", "來源")
            ui = col_index(t["headers"], "UIX")
            for r in t["rows"]:
                if cell(r, ui).startswith("UIX-"):
                    ledger_srcs.append((cell(r, ui), cell(r, si)))
    report_names = set()
    found_sev = 0
    # 掃描面固定全 repo:議題帳本身是全 repo 一本，報告面若隨 --scope 收窄，
    # 帳上屬於他模組的來源報告會被誤判為「不存在」(2026-08-20 案源:moa PR#84/#85,
    # 任何模組一產出獨有報告名即全 repo 紅)。找不到時退回 f_dirs。
    scan_dirs = find_all_f_dirs(project) or f_dirs
    review_dirs = [("ui/reviews", os.path.join(f, "ui", "reviews")) for f in scan_dirs]
    # DS 層報告歸屬:token 管線類報告不屬任何 F 模組(eco-pay 回件分流 5)
    review_dirs.append(("UIFoundation/reviews",
                        os.path.join(project, "DesignSpecs", "UIFoundation", "reviews")))
    for label, rdir in review_dirs:
        if not os.path.isdir(rdir):
            continue
        for x in sorted(os.listdir(rdir)):
            if not x.endswith(".md"):
                continue
            report_names.add(os.path.splitext(x)[0])
            for t in parse_md_tables(read_text(os.path.join(rdir, x))):
                for r in t["rows"]:
                    line = " | ".join(r)
                    if SEV_RE.search(line):
                        found_sev += 1
                        ids = UIX_RE.findall(line)
                        if not ids:
                            rep.fail(P, "%s/%s" % (label, x), "🔴/🟡 發現未配 UIX 編號(未入帳)")
                        for i in ids:
                            if i not in ledger_ids:
                                rep.fail(P, "%s/%s" % (label, x), "%s 不在議題帳(漏登)" % i)
    for uix, src in ledger_srcs:
        # 來源報告欄允許多報告名(跨輪沿革;、,;+/ 分隔;eco-pay 回件分流 5)
        for name in re.split(r"[、,;+/]", PLACEHOLDER_SPAN_RE.sub("", src)):
            base = re.sub(r"\.md$", "", name.strip())
            if base and base not in report_names and PLACEHOLDER not in name:
                rep.fail(P, rel(project, ledger_path), "%s 來源報告 %s 不存在" % (uix, base))
    if found_sev and not os.path.isfile(ledger_path):
        rep.fail(P, "DesignSpecs/UIFoundation/90_IssueLedger.md", "有 🔴/🟡 發現但議題帳不存在")
    rep.ok(P, rel(project, project), "報告↔議題帳同步比對完成(嚴重發現 %d 筆 / 帳上 %d 號);掃描面=各 F 模組 ui/reviews/+UIFoundation/reviews/(DS 層歸屬)，來源報告欄可列多名;誠實邊界:僅掃報告表格行，散文段 UIX 樣式歸 R 層(外稽 20260712 B4)" % (found_sev, len(ledger_ids)))


# ── UIV-08 主軸一致性 ─────────────────────────────────────

DEC_RE = re.compile(r"\bDEC-[A-Z0-9-]+\b")


def uiv08(rep, project, f_dirs):
    P = "UIV-08"
    for f in f_dirs:
        fp = flow_path(f)
        if not os.path.isfile(fp):
            continue
        text = read_text(fp)
        axis = re.search(r"導覽主軸", text)
        if not axis:
            rep.fail(P, rel(project, fp), "缺「導覽主軸」宣告節")
        elif not DEC_RE.search(text):
            rep.fail(P, rel(project, fp), "導覽主軸未引用 DEC 依據(00_Glossary 區塊B)")
        for r in registry_rows(text) or []:
            for k, label in (("task", "主任務"), ("primary", "primary action")):
                if not r[k] or PLACEHOLDER in r[k]:
                    rep.fail(P, rel(project, fp), "%s 的 %s 欄未填(空欄不得開畫)" % (r["p"], label))
        for pg in pages_of(f):
            parsed = parse_page(pg)
            pa = parsed.metas.get("primary-action", "")
            if not pa or PLACEHOLDER in pa:
                rep.fail(P, rel(project, pg), "meta primary-action 未填")
            for s in set(parsed.states):
                n = parsed.primary_by_state.get(s, 0)
                if n == 0:
                    rep.fail(P, rel(project, pg), "狀態 %s 缺主行動(data-action=primary)" % s)
                elif n > 1:
                    rep.fail(P, rel(project, pg), "狀態 %s 有 %d 個 primary(搶焦，主行動須唯一)" % (s, n))
        for pg in proto_pages_of(f):
            parsed = parse_page(pg)
            pa = parsed.metas.get("primary-action", "")
            if not pa or PLACEHOLDER in pa:
                rep.fail(P, rel(project, pg), "proto 頁 meta primary-action 未填")
            n = parsed.primary_outside + sum(parsed.primary_by_state.values())
            if n != 1:
                rep.fail(P, rel(project, pg), "proto 頁 primary 數=%d(產品視圖單態，全頁恰一主行動)" % n)
    rep.ok(P, rel(project, project), "主軸一致性掃描完成;「視覺強弱是否如宣告」屬 G1-R 判斷")


# ── UIV-09 TBD 對齊 ───────────────────────────────────────

def uiv09(rep, project, f_dirs):
    P = "UIV-09"
    for f in f_dirs:
        spec_tbds, by_node = open_tbds(f)
        pages = pages_of(f)
        if not pages:
            if spec_tbds:
                rep.ok(P, rel(project, f), "G0 盤點:未決 TBD %d 條(%s)——供 IA 阻塞判定" % (
                    len(spec_tbds), ", ".join(sorted(spec_tbds)[:6]) + ("…" if len(spec_tbds) > 6 else "")))
            continue
        for pg in pages:
            parsed = parse_page(pg)
            cited = set(t for t in parsed.data_tbd if PLACEHOLDER not in t)
            for t in cited:
                if t not in spec_tbds:
                    rep.fail(P, rel(project, pg), "data-tbd=%s 不在未決清單(已決殘留或編造)" % t)
            node_open = set()
            for w in parsed.data_w:
                node_open |= by_node.get(w, set())
            uncited = node_open - cited
            if uncited and not cited:
                rep.review(P, rel(project, pg),
                           "承載節點有未決 TBD(%s)而頁面無任何佔位標記;佔位是否缺席屬語意判斷" % ", ".join(sorted(uncited)[:4]))
        # 產品視圖完稿門檻(45_PrototypeView 規則 5):proto 對佔位零容忍
        for pg in proto_pages_of(f):
            parsed = parse_page(pg)
            if parsed.data_tbd:
                rep.fail(P, rel(project, pg), "proto 含 data-tbd(%s)——完稿門檻:以假設代決補完並登 90_Backfill" % ", ".join(parsed.data_tbd[:4]))
            if PLACEHOLDER in read_text(pg):
                rep.fail(P, rel(project, pg), "proto 含 ⟪⟫ 佔位字元——完稿門檻不過(45 規則 5)")
    rep.ok(P, rel(project, project), "TBD 對齊掃描完成(proto 完稿門檻含)")


# ── UIV-11 文案 lint(30_UXWriting V 層)────────────────────

def uiv11(rep, project, f_dirs):
    P = "UIV-11"
    import gen_copy
    total = 0
    for f in f_dirs:
        pages = pages_of(f) + proto_pages_of(f)
        if not pages:
            continue
        for pg in pages:
            total += 1
            d = gen_copy.extract_page(pg)
            tgt = rel(project, pg)
            for act in d["actions"]:
                if act["text"] in gen_copy.BARE_ACTIONS:
                    rep.fail(P, tgt, "模糊/裸動詞行動文案「%s」(狀態 %s)——改為具體結果(30_UXWriting §三禁清單)" % (act["text"], act["state"]))
                elif gen_copy.cta_core_len(act["text"]) > 12:
                    rep.fail(P, tgt, "行動文案過長「%s」(>12 字，狀態 %s)——CTA 以 1~5 字為理想" % (act["text"], act["state"]))
            for nv in d["nav_counts"]:
                if nv["links"] > 7:
                    rep.fail(P, tgt, "導航項目 %d 個(狀態 %s)——主導航上限 7 項(#10 選項精簡)" % (nv["links"], nv["state"]))
            for ph in d["placeholders"]:
                if ph["text"].startswith(gen_copy.PLACEHOLDER_IMPERATIVE):
                    rep.fail(P, tgt, "指令型 placeholder「%s」——改提供範例(30_UXWriting §六)" % ph["text"])
            if "lorem" in d["all_text"].lower():
                rep.fail(P, tgt, "lorem 佔位殘留(擬真資料紀律)")
            for st, txt in d["state_text_joined"].items():
                hits = []
                for m in gen_copy.CJK_ALNUM_SPACE_RE.finditer(txt):
                    frag = txt[max(0, m.start() - 4):m.end() + 4].replace("\n", "␤")
                    if frag not in hits:
                        hits.append(frag)
                if hits:
                    rep.fail(P, tgt, "中英數間混入空格(盤古之白)%d 處(狀態 %s;樣本:%s)——不留空格(30_UXWriting §九，拍板者裁定)" % (len(hits), st, " / ".join(hits[:4])))
            sts = set(d["states"])
            if "loading" in sts and len(re.findall(r"[一-鿿]", d["state_text_joined"].get("loading", ""))) < 4:
                rep.fail(P, tgt, "loading 態缺說明文字(骨架載入(Skeleton)需帶一行說明，不得只有灰塊)")
            for stname, need in (("error", "「怎麼修」行動元素"), ("blank", "「下一步」行動元素")):
                if stname in sts and not any(a["state"] == stname for a in d["actions"]):
                    rep.fail(P, tgt, "%s 態缺%s" % (stname, need))
            # 去 AI 感機檢(30_UXWriting §十一;AntiAIFlavor v0.1 蒸餾快照 2026-07-12)
            for st, txt in d["state_text_joined"].items():
                words = [w for w in gen_copy.AF04_CORE_WORDS if w in txt]
                if words:
                    rep.fail(P, tgt, "空泛大詞「%s」(狀態 %s)——換具體機制描述或刪(§十一 AF-04 核心詞，全層)" % ("、".join(words), st))
            for pr in d["prose"]:
                frag, st = pr["text"], pr["state"]
                if gen_copy.AF05_ERA_RE.match(frag) or gen_copy.AF05_MID_RE.search(frag):
                    rep.fail(P, tgt, "大時代開場(狀態 %s):「%s」——改具體資料錨(§十一 AF-05)" % (st, frag[:40]))
                if gen_copy.AF09_RHETORIC_RE.match(frag):
                    rep.fail(P, tgt, "修辭設問開場(狀態 %s):「%s」——散文層改直述，問句歸標題(§十一 AF-09)" % (st, frag[:40]))
                if gen_copy.AF11_FAKE_RE.search(frag):
                    rep.fail(P, tgt, "假互動句(狀態 %s):「%s」——刪或改直述(§十一 AF-11)" % (st, frag[:40]))
        sheet = os.path.join(f, "ui", "00_CopySheet.md")
        expected = gen_copy.build_sheet(f)
        if not os.path.isfile(sheet):
            rep.review(P, rel(project, sheet), "00_CopySheet.md 未生成——G2-R 文案審以本表為入口;執行 gen_copy.py")
        elif read_text(sheet) != expected:
            rep.fail(P, rel(project, sheet), "00_CopySheet.md 過期(與重生成結果不一致)，禁手改、請重生成")
        # 00_Digest 新鮮度(外稽 20260712 A3 轉正:拍板者吸收介面+回件 diff 基準，不得零防線)
        import gen_digest
        dig = os.path.join(f, "ui", "00_Digest.md")
        try:
            dig_expected = gen_digest.build(project, f)
        except Exception as e:
            rep.perror(P, rel(project, dig), "00_Digest 重生成比對失敗: %s" % e)
            dig_expected = None
        if dig_expected is not None:
            if not os.path.isfile(dig):
                rep.review(P, rel(project, dig), "00_Digest.md 未生成——拍板者吸收介面+回件 diff 基準;執行 gen_digest.py")
            elif read_text(dig) != dig_expected:
                rep.fail(P, rel(project, dig), "00_Digest.md 過期(與重生成結果不一致)，禁手改、請重生成")
    rep.ok(P, rel(project, project), "文案 lint 完成(%d 頁，含去 AI 感機檢);語氣/三段式/日期單位/AF 句式與擴充詞判讀歸 G2-R(佇列=00_CopySheet)" % total)


# ── UIV-12 G0 IA 對照段存在斷言(G1 前置)──────────────────

IA_HEADING_RE = re.compile(r"^#{2,}\s*IA 原則對照", re.M)


def _ia_section_filled(text):
    """回 (狀態， 訊息):ok=含已填 IA 對照表;no-section/empty/placeholder=各失敗型。"""
    m = IA_HEADING_RE.search(text)
    if not m:
        return "no-section", "缺「IA 原則對照」段"
    section = text[m.end():]
    nxt = re.search(r"^#{1,2}\s", section, re.M)
    if nxt:
        section = section[:nxt.start()]
    rows = [ln for ln in section.splitlines()
            if ln.strip().startswith("|") and not re.match(r"^\s*\|[\s:|-]+\|?\s*$", ln)]
    data_rows = rows[1:] if rows else []
    filled = [ln for ln in data_rows if PLACEHOLDER not in ln]
    if not data_rows:
        return "empty", "「IA 原則對照」段無對照表列"
    if not filled:
        return "placeholder", "「IA 原則對照」表全為範本佔位，未實際對照"
    return "ok", "IA 原則對照段存在且已填(%d/%d 列)" % (len(filled), len(data_rows))


def uiv12(rep, project, f_dirs):
    P = "UIV-12"
    if not f_dirs:
        rep.ok(P, ".", "無 F 模組，不適用")
        return
    checked = 0
    for f in f_dirs:
        # 尚未開工(無 ui/)=未進 UI 產線，G1 前置不適用。
        # 不跳過的話，pre-UI repo 從專案根跑會對每個已登記 F 模組報缺席(NP 14 筆誤報)。
        if not os.path.isdir(os.path.join(f, "ui")):
            continue
        checked += 1
        rdir = os.path.join(f, "ui", "reviews")
        g0_reports = sorted(x for x in os.listdir(rdir)
                            if re.match(r"R\d+.*G0.*\.md$", x)) if os.path.isdir(rdir) else []
        if not g0_reports:
            rep.fail(P, rel(project, f), "G0 報告(R##_G0)缺席，G1 不得啟動(先完成 G0 並產出 IA 原則對照段)")
            continue
        verdicts = [(x,) + _ia_section_filled(read_text(os.path.join(rdir, x))) for x in g0_reports]
        hit = next((v for v in verdicts if v[1] == "ok"), None)
        if hit:
            rep.ok(P, rel(project, os.path.join(rdir, hit[0])), hit[2])
        else:
            last = verdicts[-1]
            rep.fail(P, rel(project, os.path.join(rdir, last[0])),
                     "%s,G1 不得啟動(G0 報告 %d 份均無已填 IA 段)" % (last[2], len(verdicts)))
    if not checked:
        rep.ok(P, ".", "無已開工 F 模組(皆無 ui/)，不適用")


CHECKS = {
    "UIV-01": uiv01, "UIV-02": uiv02, "UIV-03": uiv03,
    "UIV-04": uiv04, "UIV-05": uiv05, "UIV-06": uiv06,
    "UIV-07": uiv07, "UIV-08": uiv08, "UIV-09": uiv09,
    "UIV-11": uiv11, "UIV-12": uiv12,
}

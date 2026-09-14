#!/usr/bin/env python3
"""MetaUI 規格導讀生成器(PREP-UI-1,info_level: Candidate)

把 MetaSA 產出(Strategy/Scope/Structure/L3/nodes)煮成一頁人話導讀:
這模組是什麼、誰會用、旅程怎麼走(W 編號自動翻譯成節點名)、
還沒決定的事(TBD+預設假設)、結構警報。

生成物，禁手改;SA 檔一改重跑即同步(與 gen_tokens 同哲學)。

TBD 只採「宣告位」，閥值只數「活躍」——兩者皆以 SA 側唯一真理表為準，
生成器不自行臆測(案源=moa-weather UIX-003／UIX-004,R00_G0)。
內容確定性:不含時戳，供 UIV-11 以重生成比對驗新鮮度(與 gen_copy 同課;
生成日看 git——外稽 20260712 A3 修正)。

Usage:
    python gen_digest.py --scope <F 模組目錄>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uiv_common import read_text, parse_md_tables, col_index, cell, find_project_root

NODE_RE = re.compile(r"\b(M\d+-F\d+-W\d+)\b")
# TBD 宣告位:整行以列表項起頭之 `[!TBD-xxx]`。句中引用(相依性宣告、下游影響、
# 已解鎖之 DEC 行)只是提及，不是宣告，不重複計入(UIX-003)。
TBD_DECL_RE = re.compile(r"^[ \t]*[-*+][ \t]+`\[!(TBD-[^\]\s]+)\]`[ \t]*(.*)$", re.M)
# 宣告區塊終點=下一個頂層區塊(列表項/編號項/標題/表格列/水平線)。同一 TBD 的
# 解鎖條件、下游影響、預設假設皆為縮排續行，故不誤切;預設假設只在自己的區塊內
# 找，不再吃到下一條的(UIX-003 欄位串味)。
TBD_BLOCK_END_RE = re.compile(r"^(?:[-*+][ \t]|\d+\.[ \t]|#{1,6}[ \t]|\||---[ \t]*$)", re.M)
ASSUME_RE = re.compile(r"預設假設\*{0,2}[:：]\s*(.+)")
FM_RE = re.compile(r"\ufeff?---\r?\n(.*?)\r?\n---\r?\n", re.S)
FM_STATUS_RE = re.compile(r"^status:[ \t]*(.+?)[ \t]*$", re.M)
FM_EPIC_RE = re.compile(r"^epic:[ \t]*(.+?)[ \t]*$", re.M)
EP_ID_RE = re.compile(r"EP\d+")
# 非活躍狀態:不計入拆分閥值、其 TBD 不列(口徑=moa DEC-SCOPE-005;案源 UIX-004)
INACTIVE_STATES = ("DEPRECATED", "PLANNED", "RESERVED", "OBSOLETE", "CANCELLED")
HEADER = "生成物，禁手改;來源=同專案 SA 產出，重生成用 UI_KIT/checks/gen_digest.py"


def norm_state(s):
    """狀態欄字面正規化:去 markdown 強調與反引號後大寫(`**DEPRECATED**` → DEPRECATED)。"""
    return re.sub(r"[*~`\s]", "", s or "").upper()


def is_active(state):
    """空狀態=未知，當活躍處理:寧可多報一則警報，不靜默漏掉一個節點。"""
    s = norm_state(state)
    return not any(k in s for k in INACTIVE_STATES)


def inactive_kind(state):
    s = norm_state(state)
    for k in INACTIVE_STATES:
        if k in s:
            return k
    return "UNKNOWN"


def brief(ids, limit=8):
    """清單過長時只列前幾個，但總數照報——收斂是為了可讀，不是把數量藏起來。"""
    return "/".join(ids) if len(ids) <= limit else "/".join(ids[:limit]) + "…等 %d 個" % len(ids)


def table_cell(s):
    """表格欄位淨化:壓平換行、跳脫直槓，免得一個欄位把整列表格撐爛。"""
    return re.sub(r"\s*\n\s*", " ", (s or "").strip()).replace("|", "\\|")


def node_meta(f_dir):
    """nodes/*.md frontmatter → {節點ID: {status, epic, path}}。

    節點↔Epic 的機械連結取自節點檔自身宣告(`epic:`)，不從 L3 主線反推——
    主線寫不寫是 D1 進度問題，不等於該 Epic 已廢除或未展開。
    """
    out = {}
    nodes_dir = os.path.join(f_dir, "nodes")
    if not os.path.isdir(nodes_dir):
        return out
    for x in sorted(os.listdir(nodes_dir)):
        if not x.endswith(".md"):
            continue
        path = os.path.join(nodes_dir, x)
        fm = FM_RE.match(read_text(path))
        fm = fm.group(1) if fm else ""
        m = re.match(r"(M\d+-F\d+-W\d+)", x)
        st = FM_STATUS_RE.search(fm)
        ep = FM_EPIC_RE.search(fm)
        ep = EP_ID_RE.search(ep.group(1)) if ep else None
        out[m.group(1) if m else x] = {
            "status": st.group(1) if st else "",
            "epic": ep.group(0) if ep else "",
            "path": path,
        }
    return out


def section_text(text, title):
    m = re.search(r"^##+\s*%s.*?$(.*?)(?=^##|\Z)" % re.escape(title), text, re.S | re.M)
    if not m:
        return ""
    return "\n".join(l.strip() for l in m.group(1).strip().splitlines() if l.strip() and not l.strip().startswith("<!--"))


def node_names(project, f_id):
    """03_Structure → {W id: (名稱， 狀態)}(全案，不限 F)。"""
    p = os.path.join(project, "DesignSpecs", "03_Structure.md")
    names = {}
    if not os.path.isfile(p):
        return names
    for t in parse_md_tables(read_text(p)):
        ni = col_index(t["headers"], "節點ID", "節點")
        mi = col_index(t["headers"], "名稱")
        si = col_index(t["headers"], "狀態")
        if ni < 0 or mi < 0:
            continue
        for r in t["rows"]:
            nid = cell(r, ni)
            if NODE_RE.fullmatch(nid):
                names[nid] = (cell(r, mi), cell(r, si))
    return names


def humanize_chain(chain_text, names):
    """`[W01] -> [W02]` → 「節點名 → 節點名」。查不到名者保留編號。"""
    ids = NODE_RE.findall(chain_text)
    if not ids:
        return chain_text.strip("`") or "(無)"
    return " → ".join(names.get(i, (i,))[0] or i for i in ids)


def epic_journeys(f_dir, names):
    """L3 映射表 → [(EP, Epic 名， 起點， 終點， 主線人話)]。"""
    for x in os.listdir(f_dir):
        if re.match(r"F\d+_L3_", x):
            text = read_text(os.path.join(f_dir, x))
            out = []
            for m in re.finditer(r"###\s*Epic[:：]\s*(EP\d+)[-—](.+?)$(.*?)(?=^###|\Z)", text, re.S | re.M):
                ep, name, body = m.group(1), m.group(2).strip(), m.group(3)
                def grab(label):
                    g = re.search(r"%s[:：]\s*(.+)" % label, body)
                    return g.group(1).strip() if g else ""
                main = re.search(r"主線[:：]\s*(.+)", body)
                out.append({
                    "ep": ep, "name": name,
                    "start": grab("旅程起點"), "end": grab("旅程終點"),
                    "chain": humanize_chain(main.group(1), names) if main else grab("主線") or "(本期不展開)",
                })
            return out
    return []


def scope_tables(project, f_token):
    p = os.path.join(project, "DesignSpecs", "02_Scope.md")
    epics, roles = [], []
    if not os.path.isfile(p):
        return epics, roles
    for t in parse_md_tables(read_text(p)):
        h = t["headers"]
        if col_index(h, "EP##", "Epic") >= 0 and col_index(h, "業務目標") >= 0:
            ei, ni, gi, mi = col_index(h, "EP"), col_index(h, "Epic 名稱", "名稱"), col_index(h, "業務目標"), col_index(h, "對應")
            for r in t["rows"]:
                if not f_token or f_token in cell(r, mi):
                    epics.append((cell(r, ei), cell(r, ni), cell(r, gi)))
        if col_index(h, "角色 ID", "角色ID") >= 0:
            ii, ni, si = col_index(h, "角色"), col_index(h, "角色名稱", "名稱"), col_index(h, "權限範圍", "範圍")
            for r in t["rows"]:
                roles.append((cell(r, ii), cell(r, ni), cell(r, si)))
    return epics, roles


def tbd_inventory(f_dir, names, metas=None):
    """nodes/*.md → [(TBD id, 一句話， 預設假設， 節點)];只列真正未決者。

    三道過濾(UIX-003):①只採宣告位，同一 TBD 在他處被引用不再重複列;
    ②已廢除/未展開節點(DEPRECATED/PLANNED/RESERVED)之 TBD 不列;
    ③預設假設限在該 TBD 自身區塊內擷取，不跨列串味。
    節點狀態以 03_Structure 唯一真理表為準，缺席時退回節點檔 frontmatter。
    """
    metas = node_meta(f_dir) if metas is None else metas
    out, seen = [], set()
    for nid in sorted(metas):
        meta = metas[nid]
        if not is_active((names.get(nid) or ("", ""))[1] or meta["status"]):
            continue
        text = read_text(meta["path"])
        for m in TBD_DECL_RE.finditer(text):
            tid = m.group(1)
            if tid in seen:
                continue
            seen.add(tid)
            end = TBD_BLOCK_END_RE.search(text, m.end())
            block = text[m.end():end.start()] if end else text[m.end():]
            assume = ASSUME_RE.search(block)
            out.append((tid,
                        table_cell(m.group(2).strip().rstrip("。")),
                        table_cell(assume.group(1).strip() if assume else ""),
                        nid))
    return out


def alarms(project, f_dir, f_token, names, metas=None):
    """04_FuncMap 拆分觸發條件的機械面;閥值只數活躍面(UIX-004)。

    已廢除(DEPRECATED)與未展開(PLANNED/RESERVED)的節點與 Epic 一律不計入——
    用一個可能永不啟用的項目去撐強制拆分條件，閥值會每次重跑都紅一次。
    W99 佔位符不計。計數基準逐項列出，人工可覆算。
    """
    metas = node_meta(f_dir) if metas is None else metas
    epics, _ = scope_tables(project, f_token)

    registered, active, dropped = [], [], {}
    for nid, (_, state) in names.items():
        if not f_token or not nid.startswith(f_token + "-") or nid.endswith("-W99"):
            continue
        state = state or (metas.get(nid) or {}).get("status", "")
        registered.append(nid)
        if is_active(state):
            active.append(nid)
        else:
            dropped.setdefault(inactive_kind(state), []).append(nid.rsplit("-", 1)[-1])

    linked = any(m["epic"] for m in metas.values())
    active_eps, ep_dropped = [], []
    for ep_cell, ep_name, _ in epics:
        eid = EP_ID_RE.search(ep_cell or "")
        eid = eid.group(0) if eid else (ep_cell or "").strip("~ ")
        if "~~" in (ep_cell or "") or "廢除" in (ep_name or "") or "作廢" in (ep_name or ""):
            ep_dropped.append("%s(已廢除)" % eid)
        elif not linked or any((metas.get(x) or {}).get("epic") == eid for x in active):
            active_eps.append(eid)
        else:
            ep_dropped.append("%s(無活躍節點)" % eid)

    out = []
    if len(active_eps) > 3:
        out.append("活躍 Epic 數 %d > 3 → 建議評估 F 模組拆分" % len(active_eps))
    if len(active) > 15:
        out.append("活躍業務節點數 %d > 15 → 建議評估 Epic 細分" % len(active))
    basis = "計數基準:Epic 活躍 %d／登記 %d" % (len(active_eps), len(epics))
    if ep_dropped:
        basis += "(不計 %s)" % "、".join(ep_dropped)
    basis += ";業務節點 活躍 %d／登記 %d" % (len(active), len(registered))
    if dropped:
        basis += "(不計 %s)" % "、".join("%s:%s" % (k, brief(v)) for k, v in sorted(dropped.items()))
    basis += ";W99 佔位符不計"
    if epics and not linked:
        basis += ";節點檔未宣告 epic，Epic 面僅排除已廢除者"
    out.append(basis)
    out.append("跨 RBAC 閉環屬語意判斷，由 G0-R 人工確認(機器不裝懂)")
    return out


def build(project, f_dir):
    f_base = os.path.basename(f_dir)
    f_token = ""
    m = re.match(r"(F\d+)_", f_base)
    m2 = re.search(r"(M\d+)_", os.path.basename(os.path.dirname(f_dir)))
    if m and m2:
        f_token = "%s-%s" % (m2.group(1), m.group(1))
    names = node_names(project, f_token)
    metas = node_meta(f_dir)
    epics, roles = scope_tables(project, f_token)
    journeys = epic_journeys(f_dir, names)
    tbds = tbd_inventory(f_dir, names, metas)
    goal = section_text(read_text(os.path.join(project, "DesignSpecs", "01_Strategy.md")), "專案目標") \
        if os.path.isfile(os.path.join(project, "DesignSpecs", "01_Strategy.md")) else ""

    L = []
    L.append("<!-- %s -->" % HEADER)
    L.append("# %s — 一頁導讀" % f_base)
    L.append("")
    if goal:
        L.append("## 這個專案在做什麼")
        L.append(goal)
        L.append("")
    if epics:
        L.append("## 本模組承載的價值(Epic)")
        for e in epics:
            # 已廢除者來源欄位自帶刪除線，再包一層 ** 會讓 markdown 巢狀錯亂
            L.append(("- %s %s:%s" if "~~" in (e[0] or "") else "- **%s %s**:%s") % e)
        L.append("")
    if roles:
        L.append("## 誰會用")
        for r in roles:
            L.append("- **%s %s**:%s" % r)
        L.append("")
    if journeys:
        L.append("## 使用者旅程(編號已翻譯成人話)")
        for j in journeys:
            L.append("### %s %s" % (j["ep"], j["name"]))
            if j["start"]:
                L.append("- 從哪開始:%s" % j["start"])
            if j["end"]:
                L.append("- 走到哪算完:%s" % j["end"])
            L.append("- 主線:%s" % j["chain"])
        L.append("")
    if tbds:
        L.append("## 還沒決定的事(%d 條;哪些卡畫面由 G0 報告判定)" % len(tbds))
        L.append("")
        L.append("| TBD | 是什麼 | 目前的預設假設 | 節點 |")
        L.append("|-----|--------|---------------|------|")
        for t in tbds:
            L.append("| %s | %s | %s | %s |" % t)
        L.append("")
    al = alarms(project, f_dir, f_token, names, metas)
    if al:
        L.append("## 結構警報(轉交 SA 參考)")
        for a in al:
            L.append("- %s" % a)
        L.append("")
    return "\n".join(L) + "\n"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", required=True, help="F 模組目錄")
    args = ap.parse_args()
    f_dir = os.path.abspath(args.scope)
    project = find_project_root(f_dir)
    if project is None:
        print("找不到專案根(DesignSpecs/)")
        return 2
    out_dir = os.path.join(f_dir, "ui")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "00_Digest.md")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(build(project, f_dir))
    print("已生成: %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""MetaUI 規格導讀生成器(PREP-UI-1,info_level: Candidate)

把 MetaSA 產出(Strategy/Scope/Structure/L3/nodes)煮成一頁人話導讀:
這模組是什麼、誰會用、旅程怎麼走(W 編號自動翻譯成節點名)、
還沒決定的事(TBD+預設假設)、結構警報。

生成物,禁手改;SA 檔一改重跑即同步(與 gen_tokens 同哲學)。
內容確定性:不含時戳,供 UIV-11 以重生成比對驗新鮮度(與 gen_copy 同課;
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
TBD_LINE_RE = re.compile(r"`\[!(TBD-[^\]\s]+)\]`\s*(.*)")
HEADER = "生成物,禁手改;來源=同專案 SA 產出,重生成用 UI_KIT/checks/gen_digest.py"


def section_text(text, title):
    m = re.search(r"^##+\s*%s.*?$(.*?)(?=^##|\Z)" % re.escape(title), text, re.S | re.M)
    if not m:
        return ""
    return "\n".join(l.strip() for l in m.group(1).strip().splitlines() if l.strip() and not l.strip().startswith("<!--"))


def node_names(project, f_id):
    """03_Structure → {W id: (名稱, 狀態)}(全案,不限 F)。"""
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
    """L3 映射表 → [(EP, Epic 名, 起點, 終點, 主線人話)]。"""
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


def tbd_inventory(f_dir):
    """nodes/*.md → [(TBD id, 一句話, 預設假設, 節點)]。"""
    out = []
    nodes_dir = os.path.join(f_dir, "nodes")
    if not os.path.isdir(nodes_dir):
        return out
    for x in sorted(os.listdir(nodes_dir)):
        if not x.endswith(".md"):
            continue
        text = read_text(os.path.join(nodes_dir, x))
        nid = re.match(r"(M\d+-F\d+-W\d+)", x)
        nid = nid.group(1) if nid else x
        for m in TBD_LINE_RE.finditer(text):
            tail = text[m.end():m.end() + 400]
            assume = re.search(r"預設假設\*\*[:：]\s*(.+)", tail)
            out.append((m.group(1), m.group(2).strip().rstrip("。"), assume.group(1).strip() if assume else "", nid))
    return out


def alarms(project, f_dir, f_token, names):
    """04_FuncMap 拆分觸發條件的機械面。"""
    epics, _ = scope_tables(project, f_token)
    w_count = sum(1 for nid in names if f_token and f_token in nid and "W99" not in nid)
    out = []
    if len(epics) > 3:
        out.append("Epic 數 %d > 3 → 建議評估 F 模組拆分" % len(epics))
    if w_count > 15:
        out.append("W 節點數 %d > 15 → 建議評估 Epic 細分" % w_count)
    out.append("跨 RBAC 閉環屬語意判斷,由 G0-R 人工確認(機器不裝懂)")
    return out


def build(project, f_dir):
    f_base = os.path.basename(f_dir)
    f_token = ""
    m = re.match(r"(F\d+)_", f_base)
    m2 = re.search(r"(M\d+)_", os.path.basename(os.path.dirname(f_dir)))
    if m and m2:
        f_token = "%s-%s" % (m2.group(1), m.group(1))
    names = node_names(project, f_token)
    epics, roles = scope_tables(project, f_token)
    journeys = epic_journeys(f_dir, names)
    tbds = tbd_inventory(f_dir)
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
            L.append("- **%s %s**:%s" % e)
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
    al = alarms(project, f_dir, f_token, names)
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

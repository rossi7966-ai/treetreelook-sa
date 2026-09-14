#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MetaUI 文案清單生成器(PREP-UI-2,info_level: Candidate)

把 F 模組 pages/*.html 的可見文案機械抽取成單檔 ui/00_CopySheet.md:
頁 × 狀態 × 元素文案總表+AI-R 檢核佇列(V 層不可判項)+人工覆核提示。
排除方法論鷹架(wire-meta/wire-foot/style/script)。
三級分工:V=UIV-11 機械判定;AI-R=G2-R 讀本表佇列逐條判讀;Human-R=覆核欄。
去 AI 感(30_UXWriting §十一;AntiAIFlavor v0.1 蒸餾快照 2026-07-12):
散文層=非 action/heading/placeholder 之可見文字(分層計算);
AF-01/02 句式、AF-04 擴充詞、段首「隨著」入 AI-R 佇列;核心 fail 項歸 UIV-11;
AF-07 三聯句(散文層+標題層)入佇列——AF-R4 含 (d) 問，通過仍優先非三聯改寫(v0.4.2)。

生成物，禁手改;頁面一改重跑即同步(與 gen_tokens 同哲學)。
內容確定性:不含時戳，供 UIV-11 以重生成比對驗新鮮度。

Usage:
    python gen_copy.py --scope <F 模組目錄>
"""
import argparse
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uiv_common import read_text, VOID_TAGS

# 盤古之白偵測:中英數之間「不留」空格(拍板者裁定 2026-08-07;30_UXWriting §九)
CJK_ALNUM_SPACE_RE = re.compile(r"[一-鿿] +[A-Za-z0-9]|[A-Za-z0-9] +[一-鿿]")
DATE_RE = re.compile(r"\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|\b\d{1,2}:\d{2}\b")
DESTRUCTIVE_RE = re.compile(r"^(刪除|移除|清除|重設)")
BARE_ACTIONS = {"確定", "OK", "Ok", "ok", "好", "刪除", "移除", "清除",
                "提交", "送出", "繼續", "下一步", "點擊這裡"}
PLACEHOLDER_IMPERATIVE = ("請輸入", "請填寫", "在此")

# ── 去 AI 感(30_UXWriting §十一;AntiAIFlavor v0.1 蒸餾快照 2026-07-12)──
# 核心詞【U】=UIV-11 全層 fail;擴充詞(draft，含「一站」變體)=AI-R 佇列。
AF04_CORE_WORDS = ("無縫", "極致", "卓越", "深信", "致力於", "前瞻性", "全方位")
AF04_HINT_RE = re.compile(r"賦能|抓手|閉環|頂層設計|助力|智慧化|(?<!下)一站")
# 大時代開場:時代/浪潮/背景 開頭與「為迎合/迎接」變體=fail;段首「隨著」=佇列(氣象因果句合法)。
AF05_ERA_RE = re.compile(r"^在.{1,12}的(時代|浪潮|背景)下")
AF05_MID_RE = re.compile(r"為(迎合|迎接).{1,12}(時代|浪潮|趨勢)")
AF05_SUIZHE_RE = re.compile(r"^隨著")
AF09_RHETORIC_RE = re.compile(r"^(什麼是.{1,20}[??]|你是否)")
AF11_FAKE_RE = re.compile(r"你可能會問|讓我們一起")
# 三聯句(AF-07 判讀式;v0.4.2 生成期降位):子句計數法(regex 於中文無詞界環境
# 可被回溯繞過——首掃實證兩型漏抓/誤列，改程式判斷)。
AF07_CLAUSE_SPLIT_RE = re.compile(r"[,,。;::!?!?\n]|——")
AF07_LAST_OPEN_RE = re.compile(r"[與及或等]")


def af07_triad(text):
    """回傳恰三項頓號並列之子句(無則 None):子句內恰 2 頓號、各段 1~12 字;
    末段含 與/及/或(=四項)或 等(=開放枚舉)不算。"""
    for clause in AF07_CLAUSE_SPLIT_RE.split(text):
        if clause.count("、") != 2:
            continue
        segs = [s.strip() for s in clause.split("、")]
        if all(0 < len(s) <= 12 for s in segs) and not AF07_LAST_OPEN_RE.search(segs[-1]):
            return clause.strip()
    return None
AF01_CONTRAST_RES = (
    re.compile(r"並?不是[^。!?\n]{1,30}而是"),
    re.compile(r"不在於[^。!?\n]{1,30}而在於"),
    re.compile(r"你以為[^。!?\n]{1,30}其實"),
    re.compile(r"表面上?[^。!?\n]{1,30}(深層|實則)"),
    re.compile(r"與其說[^。!?\n]{1,30}不如說"),
    re.compile(r"真正(重要|關鍵)?的[^。!?\n]{1,20}是"),
    re.compile(r"不應僅[^。!?\n]{1,30}而應"),
    re.compile(r"不再只?是[^。!?\n]{1,30}而是"),
    re.compile(r"並非單純[^。!?\n]{1,30}而是"),
    re.compile(r"(不止|不限於)[^。!?\n]{1,30}(更|而)"),
)
AF02_ESCALATE_RE = re.compile(r"不僅[^。!?\n]{1,30}(更|還|也)")

PAREN_RE = re.compile(r"[(（][^)）]*[)）]")
SKIP_CLASSES = {"wire-meta", "wire-foot"}
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
HEADER_NOTE = "生成物，禁手改;重生成:python .metaui/UI_KIT/checks/gen_copy.py --scope <F 模組>"
AUTHORITY = "authority: generated-summary——與頁面原文衝突以頁面為準，不得單獨作 pass/fail 依據"


def _clean(s):
    return re.sub(r"\s+", " ", s).strip()


class CopyParser(HTMLParser):
    """收集可見文案:行動元素/標題逐則，其餘文字按狀態歸桶(片段以換行分隔)。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.actions = []      # {state, tag, primary, text}
        self.headings = []     # {state, tag, text}
        self.state_frags = {}  # state -> [fragment]
        self.states = []       # data-state 出現序
        self.na = {}           # state -> reason
        self.placeholders = []  # {state, text}
        self.nav_counts = []    # {state, links}
        self.prose = []         # {state, text} 散文層片段(非 action/heading 內;分層計算)
        self._stack = []       # {tag, state, skip}
        self._nav_links = []   # 每層 <nav> 的 <a> 計數
        self._action = None
        self._heading = None

    def _cur_state(self):
        for fr in reversed(self._stack):
            if fr["state"]:
                return fr["state"]
        return "(頁面層)"

    def _skipping(self):
        return any(fr["skip"] for fr in self._stack)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set((a.get("class") or "").split())
        state = a.get("data-state")
        if "data-state-na" in a:
            self.na[a["data-state-na"]] = a.get("data-reason", "")
        if state:
            self.states.append(state)
        skip = tag in ("style", "script") or bool(classes & SKIP_CLASSES)
        if tag in ("input", "textarea") and a.get("placeholder") and not (skip or self._skipping()):
            self.placeholders.append({"state": self._cur_state() if not state else state,
                                      "text": _clean(a["placeholder"])})
        if tag not in VOID_TAGS:
            self._stack.append({"tag": tag, "state": state, "skip": skip})
        if skip or self._skipping():
            return
        if tag == "nav":
            self._nav_links.append({"state": self._cur_state(), "links": 0})
        if tag == "button" or tag == "a":
            if tag == "a" and self._nav_links:
                self._nav_links[-1]["links"] += 1
            self._action = {"state": self._cur_state(), "tag": tag,
                            "primary": a.get("data-action") == "primary", "parts": []}
        elif tag in HEADING_TAGS:
            self._heading = {"state": self._cur_state(), "tag": tag, "parts": []}

    def handle_endtag(self, tag):
        if tag == "nav" and self._nav_links:
            self.nav_counts.append(self._nav_links.pop())
        if (tag == "button" or tag == "a") and self._action is not None:
            text = _clean(" ".join(self._action["parts"]))
            if text:
                self.actions.append({"state": self._action["state"], "tag": tag,
                                     "primary": self._action["primary"], "text": text})
            self._action = None
        if tag in HEADING_TAGS and self._heading is not None:
            text = _clean(" ".join(self._heading["parts"]))
            if text:
                self.headings.append({"state": self._heading["state"], "tag": tag, "text": text})
            self._heading = None
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i]["tag"] == tag:
                del self._stack[i:]
                break

    def handle_data(self, data):
        if self._skipping():
            return
        t = _clean(data)
        if not t:
            return
        self.state_frags.setdefault(self._cur_state(), []).append(t)
        if self._action is not None:
            self._action["parts"].append(t)
        if self._heading is not None:
            self._heading["parts"].append(t)
        if self._action is None and self._heading is None:
            self.prose.append({"state": self._cur_state(), "text": t})


def extract_page(path):
    p = CopyParser()
    p.feed(read_text(path))
    joined = {st: "\n".join(frags) for st, frags in p.state_frags.items()}
    return {
        "actions": p.actions,
        "headings": p.headings,
        "state_text_joined": joined,
        "states": p.states,
        "na": p.na,
        "placeholders": p.placeholders,
        "nav_counts": p.nav_counts,
        "prose": p.prose,
        "all_text": "\n".join(x for v in joined.values() for x in v.splitlines()),
    }


def cta_core_len(text):
    """CTA 有效字數:剝除括注後計 CJK+英數字元。"""
    core = PAREN_RE.sub("", text)
    return len(re.findall(r"[一-鿿A-Za-z0-9]", core))


def _esc(s):
    return s.replace("|", "\\|")


def build_sheet(f_dir):
    pages_dir = os.path.join(f_dir, "ui", "pages")
    pages = sorted(os.path.join(pages_dir, x) for x in os.listdir(pages_dir)
                   if x.endswith(".html")) if os.path.isdir(pages_dir) else []
    proto_dir = os.path.join(pages_dir, "proto")
    if os.path.isdir(proto_dir):
        pages += sorted(os.path.join(proto_dir, x) for x in os.listdir(proto_dir)
                        if x.endswith(".html"))
    lines = ["# 文案清單(%s)" % os.path.basename(f_dir), "",
             "> %s" % HEADER_NOTE,
             "> %s" % AUTHORITY, ""]
    queue = []
    if not pages:
        lines.append("(無頁面)")
    for pg in pages:
        d = extract_page(pg)
        base = os.path.relpath(pg, pages_dir).replace("\\", "/")
        lines += ["## %s" % base, "", "| 狀態 | 元素 | 文案 |", "|------|------|------|"]
        for h in d["headings"]:
            lines.append("| %s | %s | %s |" % (h["state"], h["tag"], _esc(h["text"])))
        for act in d["actions"]:
            el = act["tag"] + ("[primary]" if act["primary"] else "")
            lines.append("| %s | %s | %s |" % (act["state"], el, _esc(act["text"])))
        for ph in d["placeholders"]:
            lines.append("| %s | input[placeholder] | %s |" % (ph["state"], _esc(ph["text"])))
        for st, reason in sorted(d["na"].items()):
            lines.append("| %s | (N/A) | %s |" % (st, _esc(reason)))
        for stname in ("blank", "loading", "error"):
            txt = d["state_text_joined"].get(stname, "")
            if txt:
                lines += ["", "**%s 態全文**:%s" % (stname, _esc(_clean(txt)))]
        lines.append("")
        etext = _clean(d["state_text_joined"].get("error", ""))
        if etext:
            queue.append("[%s/error] 三段式與語氣判讀:「%s」" % (base, etext[:90]))
        for m in sorted(set(DATE_RE.findall(d["all_text"]))):
            queue.append("[%s] 日期時間格式統一判讀:「%s」" % (base, m))
        for act in d["actions"]:
            if DESTRUCTIVE_RE.match(act["text"]) and act["text"] not in BARE_ACTIONS:
                queue.append("[%s] 破壞性行動後果重述判讀:「%s」" % (base, act["text"]))
        # 去 AI 感佇列(30_UXWriting §十一;V 層不可判，過 AF-R1 三問/機制搭配判斷)
        for pr in d["prose"]:
            frag = pr["text"]
            if any(rx.search(frag) for rx in AF01_CONTRAST_RES):
                queue.append("[%s/%s] AF-01 對比句判讀(AF-R1 三問):「%s」" % (base, pr["state"], frag[:60]))
            if AF02_ESCALATE_RE.search(frag):
                queue.append("[%s/%s] AF-02 遞進句判讀(AF-R1 三問):「%s」" % (base, pr["state"], frag[:60]))
            if AF05_SUIZHE_RE.match(frag):
                queue.append("[%s/%s] AF-05 段首「隨著…」判讀(氣象因果句合法/大時代開場改寫):「%s」" % (base, pr["state"], frag[:60]))
            tri = af07_triad(frag)
            if tri:
                queue.append("[%s/%s] AF-07 三聯句判讀(AF-R4 含(d)問，通過仍優先非三聯改寫):「%s」" % (base, pr["state"], tri[:60]))
        for h in d["headings"]:
            tri = af07_triad(h["text"])
            if tri:
                queue.append("[%s/%s] AF-07 三聯句判讀(散文式標籤;AF-R4 含(d)問):「%s」" % (base, h["state"], tri[:60]))
        af04_seen = []
        for m in AF04_HINT_RE.finditer(d["all_text"]):
            w = m.group(0)
            if w in af04_seen:
                continue
            af04_seen.append(w)
            ctx = d["all_text"][max(0, m.start() - 8):m.end() + 8].replace("\n", "␤")
            queue.append("[%s] AF-04 擴充詞「%s」判讀(無具體機制搭配即改寫):「…%s…」" % (base, w, ctx))
    lines += ["## AI-R 檢核佇列(V 層不可判項，G2-R 逐條判讀)", ""]
    lines += ["- " + q for q in queue] if queue else ["- (本輪無)"]
    lines += ["", "## 人工覆核提示", "",
              "- AI-R 佇列判讀結果:🔴🟡 入 90_IssueLedger 待 UI 拍板者裁決;🟢 逕改後重跑。", ""]
    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", required=True, help="F 模組目錄")
    args = ap.parse_args()
    f_dir = os.path.abspath(args.scope)
    out = os.path.join(f_dir, "ui", "00_CopySheet.md")
    content = build_sheet(f_dir)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("已生成 %s(%d 行)" % (out, len(content.splitlines())))
    return 0


if __name__ == "__main__":
    sys.exit(main())

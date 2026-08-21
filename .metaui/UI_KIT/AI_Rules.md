---
file: .metaui/UI_KIT/AI_Rules.md
role: ui_ai_rules
info_level: Candidate
origin: PREP-UI 前置準備產出(PREP-UI-1)
version: v0.3 (2026-08-09;引用鏈補同事協作協定承接通則=00_START_UI/SOP.md)
last_updated: 2026-08-09
summary:
  role: UI 側 AI(Coach/Runner)在專案 repo 的行為守則
  scope: 讀寫邊界/產製紀律/檢核紀律/引用鏈/議題紀律/停止條件
  audience:
    - Coach
    - Runner
---

# UI AI 行為守則

## 身份

你是專案 repo 內的 UI 側 AI:Coach(Chat 介面,引導拍板者)或 Runner(Coding Session,讀寫實體檔案)。三閘門模型(G0 規格就緒 / G1 結構定案 / G2 樣式合規)與 V/R 雙層是你的工作骨架,SOP 見 UI_KIT 10~50。

## 讀寫邊界

- **可寫**:各 F 模組 `ui/`(10_UIFlow.md / pages/ / reviews/)、`DesignSpecs/UIFoundation/`
- **唯讀**:DesignSpecs 其餘一切(SA 職權:00~04 全域檔、W 節點、L2/L3/L4)——發現 SA 側問題只登錄轉介,不修
- **禁改生成物**:tokens.css / 00_TokenSheet.md 由 gen_tokens.py 生成,手改即違規(UIV-06 會抓)

## 產製紀律

1. **先登記後產檔**:頁面先在 10_UIFlow.md 登記 P## 才可建檔(對齊 03_Structure 節點紀律)
2. **wire 階段禁表現層**:灰階、框線、系統字;禁品牌色、圓角、陰影、動畫、web font
3. **TBD 禁虛構**:依賴未決 TBD 的內容一律佔位呈現+`data-tbd` 錨定;嚴禁編造具體文案、清單、數字充當已決
4. **連結型別化**:所有導覽連結帶 `data-nav="P##|external:名稱|W99"`;裸 `href="#"` 即違規
5. **每態唯一主行動**:每個 `data-state` 區塊內恰一個 `data-action="primary"`,對齊登記表主任務
6. **擬真資料**:內容用貼近領域的擬真資料,不用 lorem ipsum

## 檢核紀律

- 每個閘門先跑 V:`python .metaui/UI_KIT/checks/run_checks.py --gate G# --scope <路徑>`
- 報告 V 段貼**真實 stdout 原文**,不轉述、不美化
- fail 不辯解:能修即修,不能修立案入議題帳
- 數值判斷(px / hex / 間距)一律歸 V 層,R 層禁止目測估算數值

## 引用鏈(每閘必經)

每個閘門開工前,先讀齊該列「必讀」指針所指載體;檢核依 V/AI-R/Human-R 三級分工。

| 時機 | 必讀(指針) | V(機器) | AI-R(判斷) | Human-R(人工) |
|------|-----------|---------|-----------|--------------|
| 接手/G0 | ui/00_Digest(生成輔助)+UIFoundation/10_Principles 標【G0 適用】條目+DesignSpecs/00_Glossary | run_checks --gate G0 | 10_SpecReview 五問+IA 原則對照 | 阻塞 TBD 由 UI 拍板者裁決 |
| G1 結構 | 10_Principles【紅線】三條+UIFoundation/20_Components+UIFoundation/Design.md 反模式段 | run_checks --gate G1(含 R00 IA 對照段存在斷言) | 30_ReviewRun 紅線對照+五態+視覺強弱 | 🔴 由 UI 拍板者裁決 |
| G2 樣式 | UI_KIT/40_TokenPipeline+UIFoundation tokens 生成物+Design.md 敘事段+UIFoundation/30_UXWriting | run_checks --gate G2 | 30_ReviewRun 反模式對照+原則覆驗(地圖單源=10_Principles)+00_CopySheet 佇列判讀 | 樣式驗收 |
| 維護(主軸 A) | UI_KIT/40_TokenPipeline 維護鏈紀律 | gen_* --check | 變更影響檢視 | 設計師發佈;UI 拍板者裁決 |

- 三級分工通則:V 承擔可判定項;AI-R 承擔有規則需語感項;Human-R 承擔價值與事實判斷;每級只上送上一級不可判項。新資產一律按本表掛載,不另立檢核動線。
- 同事協作協定=`00_START_UI/SOP.md`(常時義務,非閘門時機):其對同事之字面承諾(開工句/收工/准駁/還原點)由 AI 承接——收到「收工」照其協定寫紀錄並隨工作提交;計畫准駁與還原點照其敘述兌現;單包部署時本條同樣成立。
- 本表僅指針:規範本文以所指載體為準,衝突時以載體為準。00_Digest 為生成輔助,不得單獨作 pass/fail 依據。
- DS 定義口徑單源:MetaUI 主 repo `TRAINER/UI_FuncIndex.md`(部署包不含該檔,回主 repo 查)。
- 本表行數上限 12 列;超限即拆分為獨立載體。
- 變更管理:本表修訂由拍板者核准;觸發=DS 資產(UI_KIT/UIFoundation 載體)新增或廢除;修訂時同步檢視 checks/README 閘門子集是否對應。
- 回溯傳播:DS 資產破壞性變更(token 更名或刪除/原則增刪/元件語彙變更)→盤點受影響已過閘專案→重跑對應閘門 V 子集,或登 90_IssueLedger 待處理。

## 議題紀律

- 報告 R 段 🔴🟡 發現必入 `UIFoundation/90_IssueLedger.md`(UIV-07 會驗)
- 結案不自證:需下一輪對應閘門 V 重跑通過或 R 覆核
- 拆面 out 面向(無障礙 / 前端程式品質 / 效能)不審不展開;偶遇問題記「範圍外轉介」一行

## 停止條件

- 導覽主軸無 DEC 依據 → 停,請拍板者先立 DEC(進 00_Glossary 區塊B)
- G0 的 IA 阻塞 TBD 未裁決 → 不得開畫
- 規格輸入缺席(如缺 03_Structure)→ 以 parse-error 呈報,不硬猜
- 涉及 SA 檔修改需求 → 僅登錄轉介,SA pass 管道處理

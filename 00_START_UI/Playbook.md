---
file: 00_START_UI/Playbook.md
role: ui_playbook
info_level: Candidate
origin: PREP-UI 前置準備產出(PREP-UI-1)
version: v0.1 (2026-07-05)
last_updated: 2026-07-05
summary: UI 情境卡操作手冊(對位 SA_DEPLOY 同名檔，檔名對稱=UI 2026-07-05 Q1 拍板)。五張卡對應 UI_KIT 五支 SOP，附指令句。
---

# UI 情境卡

> 用法:複製指令句給 AI(Coach / Runner)，替換焦點模組。SOP 細節在 `.metaui/UI_KIT/`。

| 卡 | 情境 | 指令句 | SOP |
|----|------|--------|-----|
| U0 | 開畫前，確認 SA 規格畫得下去 | 『執行規格就緒檢核 焦點模組:M0X/F0X』 | 10_SpecReview.md |
| U1 | 畫 UI flow 與 wire 線框 | 『執行線框產製 焦點模組:M0X/F0X』 | 20_FlowPages.md |
| U2 | 審查(G1 結構 / G2 樣式) | 『執行 G1 審查 焦點模組:M0X/F0X』 | 30_ReviewRun.md |
| U3 | 取 token、上樣式 | 『執行 token 套用 焦點模組:M0X/F0X』 | 40_TokenPipeline.md |
| U4 | 議題同步與結案 | 『同步議題帳 焦點模組:M0X/F0X』 | 50_IssueFlow.md |

## 常用查核句

- 『跑 G1 檢核 焦點模組:M0X/F0X』→ AI 執行 run_checks 並貼原文結果
- 『目前開放議題』→ AI 讀 `DesignSpecs/UIFoundation/90_IssueLedger.md` 摘要
- 『開畫前還缺哪些決策』→ AI 讀最近 R00_G0 報告的決策清單節

## 順序鐵律

U0 過閘才 U1;G1 過閘才 U3。跳關 = 檢核會擋(閘門 HOLD)，不是 AI 不配合。

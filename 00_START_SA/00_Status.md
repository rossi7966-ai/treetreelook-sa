---
file: 00_START_SA/00_Status.md
role: project_status_dashboard
status: TEMPLATE_EMPTY
version: v0.3 (2026-07-18)
last_updated: 2026-07-18
summary: SA 駕駛艙——30 秒掌握當前要做什麼。實際內容由 Coach 在專案開案時填入。(v0.2:MS-T051 I-94 onboarding 配套——範本擴充 Coach 接手清單 + Coach 交接日誌兩區塊,對應 I-94 Q4 落地)
---
# 專案執行狀態駕駛艙

> 用途:SA 開啟此檔時,30 秒內知道目前流程位置、下一步動作、待回應問題。
> 維護:Coach 每次推進流程後同步更新。

## 當前位置
- 流程階段:<!-- R1 / R2 / D1 / D1.5 / D2,擇一 -->
- 焦點模組:<!-- 當前 SYS / SS / M / F 路徑 -->
- 上次更新:<!-- YYYY-MM-DD -->

## 下一步動作
<!-- Coach 在此明示 SA 該做什麼 -->

## 待 SA 回應問題
<!-- Coach 列出需要 SA 拍板的事項 -->

## 階段完成度
<!-- 各 W## 節點狀態彙整,從 03_Structure.md 同步 -->

---

## Coach 接手清單

> 給 Coach 開新 chat 時讀取的當前專案狀態。由 Runner 經 AGENT_TASK 更新,Coach / SA 不直接編輯。

- **專案簡稱**:[填值,Coach chat 命名用]
- **當前焦點 SYS**:[SYS##_系統名稱]
- **當前焦點 M**:[M##_業務模組]
- **當前焦點 F**:[F##_功能名稱]
- **當前流程階段**:[R1 / R2 / D1 / D1.5 / D2 / CR]
- **Coach 第 N 代**:[數字,初始為 1]
- **最近一次穩定狀態 commit**:[hash,異常處理退回安全點用]

## Coach 交接日誌

> 上代 Coach Session 結尾交接 Part 1 結構化日誌寫入區。歷代累積,最新在上。

(歷代日誌條目以時間倒序排列,初始狀態為空)

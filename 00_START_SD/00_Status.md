---
file: 00_START_SD/00_Status.md
role: project_status_dashboard
status: TEMPLATE_EMPTY
info_level: Candidate
origin: PREP-SD 前置準備產出(PREP-SD-2)
version: v0.1
last_updated: 2026-08-09
summary: SD駕駛艙——30秒掌握當前要做什麼。實際內容由SD Coach在專案開案時填入。
---
# SD 執行狀態駕駛艙

> 用途:SD開啟此檔時,30秒內知道目前流程位置、下一步動作、待拍板問題。
> 維護:Coach每次推進流程後同步更新。
> 同事協作協定:同夾`SOP.md`(開工句/收工/准駁/還原點)——AI須承接其對同事之字面承諾。

## 當前位置
- 流程階段:<!-- Handoff / Introspect / Profile / Modeling / Contract / Generate / Check,擇一(對應SD_KIT 10/12/15/20/30/40/90) -->
- 入口模式:<!-- 綠地(SA接手) / 棕地(DB逆向),擇一 -->
- 焦點範圍:<!-- 當前資料集 / 模組 / API族 -->
- 採用層級:<!-- L0 / L1 / L2 / L3(見採用梯度) -->
- 上次更新:<!-- YYYY-MM-DD -->

## 下一步動作
<!-- Coach在此明示SD該做什麼 -->

## 待SD拍板問題
<!-- 決策卡升級的請示卡、GapRegister待解鎖項 -->

## 檢核狀態
<!-- 最近一次檢核腳本stdout摘要:fail數 / needs-review數 -->

---

## Coach 接手清單

> 給Coach開新chat時讀取的當前專案狀態。

- **專案簡稱**:[填值]
- **入口模式**:[綠地/棕地]
- **當前焦點**:[資料集/模組]
- **當前流程階段**:[階段]
- **Coach第N代**:[數字,初始為1]
- **最近一次穩定狀態commit**:[hash]

## Coach 交接日誌

> 歷代累積,最新在上。(初始為空)

---
version: v1.4 (2026-06-03)
last_updated: 2026-06-03
changed_by: Claude Code
summary: 新增SYS層掃描指令；新增跨SYS搬移與SubSystem歸屬變更規則；修復議題[I-12/I-13](補丁：命名定案批次一)(補丁：命名定案批次三)(補丁：SA_KIT目錄建立)(v1.4:MS-T045 X3B1 棒——frontmatter §十一 弱治理對齊,追加歷史補丁指針)(歷史補丁見 git history)
---
# 角色與任務
你是一個資深DevOps與系統架構師，運行環境為Code(Runner)。
任務：安全執行功能模組的「重新命名」、「拆分」或「下架歸檔」，並透過「人工對映+自動掃描」雙重機制確保架構追溯性。

## 🛑 前提確認(閘控機制)
執行本腳本前，必須先確認已完成以下任一項：
1. 已執行 `10_ReqAnalysis.md`(變更分析模式)，確認拆分後的模組邊界與US/W##歸屬。
2. 或由SA主動提供US與W##的新歸屬對映表。
若未完成上述任一項，請拒絕執行並輸出：「⚠️ 違反治理原則：請先透過10_ReqAnalysis.md釐清模組拆分後的規格邊界與節點歸屬，再執行重構。」

# 前置準備：定義重構對映表(Mapping)
當我要求重構時，我會提供對映關係。例如：
- [歸檔] `F02_Portal` -> `_archive/F02_Portal`
- [拆分/改名] `F02_Portal` -> `F02_Shell` 與 `F03_Catalog`

# 執行指令(嚴格遵守順序)

## 1. 依賴路徑全域掃描(Dry-Run)
在垂直原子化架構下，實體搬移極易導致 `/nodes/W##_xxx.md` 內的相對路徑與跳轉連結失效。必須嚴格掃描。
1. 在終端機執行：
```
# 同時搜尋M層與F層的所有引用
grep -rn "{舊SYS模組ID}" DesignSpecs/
grep -rn "{舊M模組ID}" DesignSpecs/
grep -rn "{舊F模組ID}" DesignSpecs/
grep -rn "{舊SYS模組ID}/{舊M模組ID}" DesignSpecs/
grep -rn "{舊M模組ID}-{舊F模組ID}" DesignSpecs/
```
⚠️ 層級ID搜尋說明：需分別搜尋M層ID、F層ID與完整複合ID(M##-F##)，
因為三種格式在不同位置可能獨立出現。
2. 建立一份暫時的 `refactor_plan.md`，列出：
   - 準備移動/改名的實體資料夾與檔案(含所有 `/nodes/` 內的原子檔)。
   - 需要修改跨模組連結(`[某字](../F0X.../...)`)、YAML Header與Markdown雙向導覽列的外部/內部檔案清單與行號。
3. **強制停頓**：輸出「✅ 依賴掃描完成，清單如 `refactor_plan.md`。請在清單中為每條需要更新的連結填入『新的目標路徑(含正確錨點)』，完成後輸入『**執行替換**』」。等待我填寫與確認。

## 2. 實體遷移與依賴替換(收到「執行替換」後啟動)
1. **實體操作**：使用檔案系統工具(或bash指令)進行資料夾與檔案的重新命名或搬移(如移至 `_archive/`)。

**M層搬移特殊規則**：
- 若搬移的是整個F模組(跨M遷移)：
  1. 實體移動目錄至目標M層下
  2. 更新該F模組所有節點單檔的YAML Header中的`module_id`欄位
  3. 更新所有節點單檔的檔名前綴(舊M##-F## → 新M##-F##)
  4. 更新來源M層與目標M層的`M##_overview.md`功能模組表格
- 若搬移的是整個M層(M層改名或拆分)：
  需同時更新旗下所有F模組目錄內的節點單檔YAML Header與檔名，
  工作量大，強制在`refactor_plan.md`中列出受影響的節點單檔總數，
  等待SA確認後再執行。

- 若搬移的是整個M層至不同SYS（跨SYS搬移）：
  1. 實體移動目錄至目標SYS層下
  2. 更新該M層`M##_overview.md` YAML的`parent_system`欄位
  3. 若原SYS有SubSystem且M層屬於某SS：
     同步更新原SS##_overview.md（移除M層）與目標SYS的SS##_overview.md（加入M層）
  4. 更新來源SYS與目標SYS的`SYS##_overview.md`包含M層清單
  5. 更新03_Structure.md，將M層區塊從原SYS標題移至目標SYS標題下

- 若SubSystem歸屬變更（M層不搬移實體目錄，只改SS歸屬）：
  1. 更新`M##_overview.md` YAML的`parent_subsystem`欄位
  2. 更新原SS##_overview.md（移除M層）
  3. 更新目標SS##_overview.md（加入M層）
  4. 更新03_Structure.md的父層標題歸屬
  5. 實體目錄不變，不需要搬移檔案

2. **全域依賴替換**：嚴格依照我在 `refactor_plan.md` 中指定的新路徑，精準替換所有檔案中的連結字串。特別留意 `/nodes/*.md` 內部的 `向上對齊` 與 `流程定位` 雙向連結。
3. **中樞與全域地圖更新**：
   - 更新 `03_Structure.md`，標註舊模組狀態為 `ARCHIVED` 或更新為新模組名稱，並處理對應的 `W##` 佔位符。
   - 打開 `04_FuncMap.md`，手動/批次將被移除模組的Mermaid樹狀分支標註為灰階或將名稱註記為 `[DEPRECATED]`。

## 3. 終端機Linter防呆驗證(強制執行)
嚴禁靠猜測確認結果，必須使用工具進行靜態分析。
1. 在終端機執行以下指令，深入掃描所有微型單檔的內部連結有效性：
   `npx markdown-link-check -q "DesignSpecs/**/*.md"`
2. **驗證結果處置**：
   - 若終端機回報 `[✖]`(Dead links)：主動修復漏改或改錯的Markdown檔案(特別是 `/nodes/` 裡的)，然後重新掃描，直到全數通過。
   - 若終端機回報全數 `[✓]`：執行下一步。
> ⚠️ **Linter侷限性宣告**：`markdown-link-check` 僅能驗證「檔案實體路徑」是否存在，無法驗證 `#錨點` 與純文字標記的 `[W##]` 是否正確。這部分的完整性驗證將依賴人工與Phase 2覆蓋率檢查。

## 4. 輸出DoD報告
1. 刪除暫存的 `refactor_plan.md`。
2. 輸出：「✅ 模組重構完成。所有節點單檔與全域路徑已更新並通過 `markdown-link-check` 驗證。接下來請使用 `30_DraftSync.md` 針對受影響的新模組執行Phase 2，以驗證 `W##` 與功能架構樹的最新覆蓋率與完整性。」
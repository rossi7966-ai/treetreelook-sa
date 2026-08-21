---
file: DesignSpecs/UIFoundation/10_Principles.md
role: design_principles
task: PREP-UI-2
origin: PREP-UI 前置準備產出
info_level: Candidate
version: 0.6.1
last_updated: 2026-07-12
summary: MetaUI 設計原則十條。Shneiderman 6 條+認知定律 4 條;紅線級 3 條(1/3/5)為 G1-R 必查;【G0 適用】4 條(1/8/9/10)為 G0「IA 原則對照」必查;閘門地圖(G0/G1-R/G2-R 覆驗)以本檔為單源,30_ReviewRun 與引用鏈回指。
---

# MetaUI 設計原則

> **來源**:Shneiderman 8 Golden Rules of Interface Design + Laws of UX
> **選取標準**:與 MetaUI 雙場景(GIS 圖台前台 + 後台管理)最相關者
> **優先級**:標【紅線】者(1 一致性、3 回饋、5 錯誤預防)為 G1-R 審查必查項,
> 違反即 🔴;其餘為建議級,違反視情節 🟡/🟢。
> **G0 掛載**:標【G0 適用】者(1 一致性、8 資訊分組、9 遵循慣例、10 選項精簡)為 G0
> 「IA 原則對照」必查條目——對照標的=03_Structure 節點組織、L2 頁面拓樸、導覽軸。

## 閘門地圖(單源=本檔;30_ReviewRun 與 AI_Rules 引用鏈回指,不另立清單)

| 原則 | G0 IA 對照 | G1-R 結構審 | G2-R 覆驗(渲染後) |
|------|-----------|------------|------------------|
| 1 一致性【紅線】 | ✓ 命名/模式 | ✓ 元件語彙與行為 | ✓ 跨頁視覺一致 |
| 2 通用可用性 | ✓ 入口級雙讀者(首訪懂價值/回訪有捷徑) | ✓ 新手引導/專家捷徑 | — |
| 3 回饋【紅線】 | — | ✓ 五態回饋完備 | — |
| 4 階段完成感 | — | ✓ 流程步序與確認 | — |
| 5 錯誤預防【紅線】 | — | ✓ 錯誤路徑與修復指引 | — |
| 6 可逆性 | — | ✓ 逃生/撤銷/重設 | — |
| 7 目標要大要近 | — | — | ✓ 目標大小與距離感知 |
| 8 資訊分組(組塊化) | ✓ 結構分群 | ✓ 版面分段 | — |
| 9 遵循慣例 | ✓ 導覽拓樸 | — | ✓ 慣例感知(像不像使用者熟悉的樣子) |
| 10 選項精簡 | ✓ 導覽軸/選單量 | ✓ 單一畫面主行動唯一 | — |

G2-R 覆驗欄=樣式落地後對**渲染結果**再看一次的條目;執行步驟見 30_ReviewRun。
渲染後全譜易用性覆核(Nielsen 十項)=30_ReviewRun 承載,逐項映射回本檔原則,不另立原則清單。

---

## 原則十條

### 1.【紅線】【G0 適用】一致性(Consistency)
**出處**:Shneiderman #1 — Strive for consistency

在同類操作中維持一致的視覺與互動模式。相同語意的操作用相同元件、相同色彩 token、相同位置。

**MetaUI 情境**:前台圖台的「儲存」與後台管理的「儲存」使用同一 BaseButton primary 變體,避免使用者在兩個場景間切換時產生認知落差。

---

### 2. 通用可用性(Universal Usability)
**出處**:Shneiderman #2 — Seek universal usability

支援不同經驗層級的使用者。新手有引導,專家有捷徑。

**MetaUI 情境**:GIS 圖台提供初次使用引導(tooltip 標示圖層操作),同時保留鍵盤快捷鍵供專業測量人員使用。

---

### 3.【紅線】回饋(Informative Feedback)
**出處**:Shneiderman #3 — Offer informative feedback

每個操作都應有適當的系統回饋。頻繁操作回饋可簡潔,重大操作回饋須明確。

**MetaUI 情境**:資料篩選立即反映在地圖標記數量(簡潔);刪除保留地資料前以 BaseDialog 二次確認(明確)。

---

### 4. 階段完成感(Closure)
**出處**:Shneiderman #4 — Design dialogs to yield closure

將複雜操作分成有明確起點與終點的步驟序列,每步完成後給予確認。

**MetaUI 情境**:後台資料匯入流程:選檔→預覽→確認→完成(每步有狀態指示,完成後顯示匯入筆數)。

---

### 5.【紅線】錯誤預防(Error Prevention)
**出處**:Shneiderman #5 — Prevent errors

設計系統使嚴重錯誤不可能發生。偵測到錯誤時提供簡單、建設性的修復指引。

**MetaUI 情境**:表單即時驗證(BaseInput error 狀態 + ValidationList);必填欄位以紅色星號標示;刪除操作不可 undo 時強制二次確認。

---

### 6. 可逆性(Easy Reversal of Actions)
**出處**:Shneiderman #6 — Permit easy reversal of actions

盡可能讓操作可撤銷,降低使用者的焦慮感。

**MetaUI 情境**:地圖量測標記可逐步 undo;篩選條件可一鍵重設;表格排序可還原。

---

### 7. 目標要大要近(Fitts's Law)
**出處**:Laws of UX — Fitts's Law

觸及目標的時間與目標大小和距離成函數。頻繁使用的操作應該大且近。

**MetaUI 情境**:地圖操作工具列固定於可及位置;ScrollToTopButton 尺寸足夠(圓形 FAB);表格行列操作按鈕靠近資料行。

---

### 8.【G0 適用】資訊分組(Miller's Law・組塊化)
**出處**:Laws of UX — Miller's Law

工作記憶有限,但重點不是「7」這個數字,而是**組塊化(chunking)**:把資訊組成有意義的群,使用者就能處理更多。
(注意:「選單不得超過 7 項」是本定律的著名誤用——選項數量問題見第 10 條 Hick's Law。)

**MetaUI 情境**:長表單用 FieldWrap 依業務語意分段(申請人資料/土地資訊/附件),而非一長串欄位;BaseTable 欄位分組表頭;坐標、案號等長字串以視覺分節呈現(如 `TW97 X: 250,000`)。

---

### 9.【G0 適用】遵循慣例(Jakob's Law)
**出處**:Laws of UX — Jakob's Law

使用者將大部分時間花在其他網站上,他們期望你的網站運作方式與已知網站相同。

**MetaUI 情境**:遵循 Vuetify/Material Design 慣例(drawer 左開、FAB 右下、toast 頂部);BreadCrumbs 放在頁面頂部 header 下方。

---

### 10.【G0 適用】選項精簡(Hick's Law)
**出處**:Laws of UX — Hick's Law

決策時間隨選項數量與複雜度增加。減少同時呈現的選擇,或用漸進揭露分層。

**MetaUI 情境**:導覽主項精簡聚焦(分類過多時併類,而非硬塞);圖台工具列只常駐高頻工具,進階量測/分析工具收合於「更多」;表單的下拉選項超過十餘項時提供搜尋過濾(BaseSelect);每個畫面主行動唯一(與 Design.md 反模式「同畫面雙主行動」互鎖)。

---

## 舊稱對照(讀舊報告用)

R03~R05 報告沿用原譯名(費茲/米勒/雅各/希克)與「啟發式」稱法;報告為不可變紀錄
不回改,新舊對照以編號 #7~#10 與「易用性原則」定名為準。

---
file: DesignSpecs/UIFoundation/20_Components.md
role: component_spec_skeleton
task: PREP-UI-2
origin: PREP-UI 前置準備產出
info_level: Candidate
version: 0.3.1 (2026-08-20)
last_updated: 2026-08-20
summary: 元件規範骨架+標準六欄模板(anatomy/states/usage 含 when-not/code 對應/a11y/tokens 消耗表)+互動態視覺語彙共用基準(hover/focus/disabled/error/selected 之視覺與 token)。9 大類;既有條目逐步補齊至六欄。元件/頁面只准引 semantic tier token(F-2)。
---

# MetaUI 元件規範(骨架版)

> **分類依據**:Adobe Spectrum + GOV.UK Design System 業界分類
> **使用規則**:元件/頁面只准引 semantic tier token;primitive 僅供 alias 引用(F-2)
> **邊界規則**:行動回饋(alert/toast)歸 Feedback;純狀態展示(badge/chip)歸 Status;空類不湊件

---

## 元件文件標準欄位(六欄)

逐元件文件依下列欄位撰寫;既有骨架條目逐步補齊至六欄。

| 欄位 | 內容 | 檢核接點 |
|------|------|---------|
| anatomy 解剖 | 組成部件與包裝層(Vuetify/Base*) | G1 結構審 |
| states 狀態 | 狀態矩陣(default/hover/focus/disabled/loading/error 依元件取用) | UIV-03 五態紀律 |
| usage 使用時機 | when-to 與 when-not(決策導向) | 30_ReviewRun 選型判準 |
| code 對應 | Vuetify/Base* 元件名與 props 要點 | 前端 repo 對映 |
| a11y 無障礙 | 鍵盤/焦點/ARIA 要求 | 藍圖節點 a11y.builtin 必填欄 |
| tokens 消耗表 | 引用之 token 清單(semantic tier) | UIV-05;uiv10 對齊 |

元件文字內容以指針連 30_UXWriting，不複製字面。

---

## 互動態視覺語彙(states 欄共用基準)

> 各元件 states 欄宣告「有哪些態」;本節定義「每種態長什麼樣」的共用基準，
> 元件條目只寫與基準不同的差異。值一律引 semantic token(F-2)。

| 態 | 共用視覺基準 | token |
|----|-------------|-------|
| hover | 面型元件=底色轉容器層/卡片面轉次要面;線型與文字型=加主色邊框或淡底 | `--color-primary-container`(淡底)/`--color-primary`(邊框)/`--color-surface-variant`(卡片面) |
| focus | 外環(focus ring)，不以底色變化替代;表單欄位=邊框轉主色+加粗 | `--color-primary-soft`(外環)/`--color-primary`(欄位邊框) |
| disabled | 降飽和+禁用游標，保留輪廓 | `--color-disabled` |
| error | 邊框與提示轉錯誤語意色 | `--color-error` |
| selected/checked | 主色實底，或主色底線(Tab=2px 底線+Medium 字重;未選=1px divider 底線) | `--color-primary`/`--color-primary-container`/`--color-divider` |
| 控制項尺寸 | 表單控制高 43px(Button/Select/DatePicker 對齊)、Switch 軌 44×24 鈕 20、IconButton 40×40 | 尺寸未 token 化;43 不在間距表=候 token 化裁決(43 vs 44 網格)，現值住本節 |

> **本表範圍=元件互動態，不涵蓋頁面五態**(2026-08-20 補註，案源=moa R02_G2)。
> 上表 `error` 指元件層的錯誤回饋(欄位驗證失敗、上傳失敗、必填未勾)，故轉 `--color-error`。
> UIV-03 五態裡的 `error` 是**頁面資料取不到**，語意由 30_UXWriting §四 錯誤三段式
> (哪裡錯→為什麼→怎麼修)承載，**不塗警示色**——整面轉紅會被讀成警示元件，
> 且與警特報三級(50_GisCartography §三)的警戒語言互相稀釋。
> 頁面層要不要用色由 G2-R 個案判斷，本表不預設。

---

## 1. Form

表單類元件——使用者資料輸入的核心互動層。

### 1.1 BaseInput

- **何時用**:單行文字輸入(文字/數字/email 等)
- **解剖**:VTextField 包裝 → label + input + hint/error message
- **狀態**:default / focus / error / disabled
- **token 引用**:`--color-text-body`(文字), `--color-stroke`(邊框), `--color-error`(錯誤態), `--color-disabled`(停用態), `--color-surface`(底色)

### 1.2 BaseTextarea

- **何時用**:多行文字輸入
- **解剖**:VTextarea 包裝 → label + textarea + character count
- **狀態**:default / focus / error / disabled
- **token 引用**:同 BaseInput

### 1.3 BaseCheckbox / BaseCheckboxGroup

- **何時用**:多選(單一或群組)
- **解剖**:VCheckbox 包裝 → checkbox + label;群組版含全選(CheckboxWithSelectAll)
- **狀態**:unchecked / checked / indeterminate / disabled / error(必填未勾)
- **token 引用**:`--color-primary`(勾選色), `--color-error`(必填標記)

### 1.4 BaseRadio / BaseRadioGroup

- **何時用**:單選
- **解剖**:VRadioGroup 包裝 → radio circles + labels
- **狀態**:unselected / selected / disabled
- **token 引用**:`--color-primary`(選中色)

### 1.5 BaseSelect / BaseCombobox

- **何時用**:下拉選擇(BaseSelect)或可搜尋下拉(BaseCombobox)
- **解剖**:VAutocomplete 包裝 → input + dropdown menu + chip 群組(多選時)
- **狀態**:default / focus / open / selected / disabled
- **token 引用**:`--color-surface`(底色), `--color-primary`(選中高亮), `--shadow-popover`(下拉陰影)

### 1.6 BaseDatepicker

- **何時用**:日期選擇
- **解剖**:flatpickr 整合 → input + calendar popup
- **狀態**:default / open / selected / inRange / disabled / today
- **token 引用**:`--color-primary`(選中日), `--color-primary-soft`(範圍底色), `--radius-m`(日曆圓角)

### 1.7 PasswordInput

- **何時用**:密碼輸入(含顯示/隱藏切換)
- **解剖**:BaseInput 包裝 + 眼睛 icon toggle
- **狀態**:masked / visible / error
- **token 引用**:同 BaseInput

### 1.8 FileUploadButton / FilePreviewer

- **何時用**:檔案上傳與預覽
- **解剖**:upload button + file list / preview panel
- **狀態**:idle / uploading / uploaded / error
- **token 引用**:`--color-primary`(按鈕), `--color-error`(上傳失敗)

### 1.9 BaseLabel / FieldWrap

- **何時用**:表單欄位標籤與佈局包裝
- **解剖**:label text + required marker(*) / field + label + hint + error slot
- **狀態**:default / required / error
- **token 引用**:`--color-text-body`(標籤), `--color-error`(必填星號)

### 1.10 CaptchaInput / ReCaptcha

- **何時用**:驗證碼輸入(自訂或 Google reCAPTCHA)
- **解剖**:圖片驗證碼 + input / Google reCAPTCHA widget
- **狀態**:default / verified / expired / error

---

## 2. Action

觸發操作的互動元件。

### 2.1 BaseButton

- **何時用**:主要操作觸發
- **解剖**:VBtn 包裝 → icon(optional) + label + ripple
- **變體**:primary(實心) / lighten(淺底) / outlined(描邊) / text(純文字)
- **狀態**:default / hover / active / focus-visible / disabled / loading
- **token 引用**:`--color-primary`(primary 變體), `--color-primary-soft`(lighten 變體), `--color-text-body`(text 變體), `--focus-visible`(focus ring)

### 2.2 BaseIconButton

- **何時用**:純圖示操作(空間受限場景)
- **解剖**:VBtn icon 模式 → icon + tooltip
- **狀態**:同 BaseButton
- **token 引用**:同 BaseButton

### 2.3 BaseButtonDelete / Edit / Review / View

- **何時用**:表格/卡片行列的常用操作捷徑
- **解剖**:BaseIconButton 特化 → 預設 icon + tooltip text
- **狀態**:同 BaseIconButton

### 2.4 BaseButtonToggle

- **何時用**:互斥選項群組(如檢視模式切換)
- **解剖**:VBtnToggle 包裝 → button group
- **狀態**:selected / unselected / disabled

### 2.5 ScrollToTopButton

- **何時用**:長頁面回到頂部
- **解剖**:圓形浮動按鈕(FAB 風格) → icon
- **狀態**:default / hover(brightness) / active(scale) / focus-visible
- **token 引用**:`--color-primary`(底色), `--radius-xl`(999px pill), `--z-index-to-top`

---

## 3. Navigation

頁面/區塊導覽元件。

### 3.1 HeaderBar

- **何時用**:全站頂部導覽列
- **解剖**:sticky header → logo + title + nav actions
- **狀態**:default / responsive(375/768/1280 斷點)
- **token 引用**:`--color-primary-emphasis`(底色), `--layout-header-height`, `--z-index-header`

### 3.2 BreadCrumbs

- **何時用**:多層頁面路徑指示
- **解剖**:VBreadcrumbs 包裝 → home icon + path segments + divider
- **狀態**:default / hover(underline) / responsive
- **token 引用**:`--color-primary`(home icon), `--color-text-body`(路徑文字)

### 3.3 BaseTab

- **何時用**:同頁分頁切換
- **解剖**:VTabs 包裝 → tab items + indicator
- **狀態**:active / inactive / disabled
- **token 引用**:`--color-primary`(active indicator)

### 3.4 BasePagination

- **何時用**:分頁資料翻頁
- **解剖**:頁碼列 + 上一頁/下一頁
- **狀態**:default / active page / disabled(首/末頁)

> **擴充候選**:SideNav, Stepper, Link

---

## 4. Feedback

系統對使用者操作的回應;行動回饋(alert/toast)歸此類(邊界規則見檔頭)。

### 4.1 BaseAlert

- **何時用**:頁面內嵌式通知(可關閉)
- **解剖**:VAlert 包裝 → icon + message + close button
- **狀態**:info / success / warning / error
- **token 引用**:`--color-info`/`--color-success`/`--color-secondary`/`--color-error`(依狀態)

### 4.2 StaticAlert

- **何時用**:靜態提示(不可關閉)
- **解剖**:VAlert 覆寫(去背景) → icon + message
- **狀態**:同 BaseAlert(無 close)

### 4.3 BaseDialog

- **何時用**:模態對話框(確認/取消操作)
- **解剖**:VDialog 包裝 → title + content slot + action buttons(cancel/save)
- **狀態**:open / closed / persistent(點外不關)
- **token 引用**:`--color-surface`(底色), `--shadow-dialog`, `--radius-m`, `--z-index-dialog`

### 4.4 BaseTooltip

- **何時用**:hover/focus 時的輔助說明
- **解剖**:觸發元素 + tooltip bubble(TooltipBubble)
- **狀態**:hidden / visible
- **token 引用**:`--z-index-tooltip`, `--shadow-popover`

### 4.5 BaseLoading / FetchLoading / LoadingDialog

- **何時用**:操作中等候指示(元件級/全域 API/對話框式)
- **解剖**:spinner/circular progress + optional message / 全域遮罩(FetchLoading) / dialog + spinner(LoadingDialog)
- **狀態**:loading / idle
- **token 引用**:`--color-primary`(spinner), `--z-index-fetch-loading`(全域遮罩), `--z-index-backdrop`

### 4.6 GlobalComponents

- **何時用**:全域掛載(Alert + Dialog + Loading 的 singleton 實例)
- **解剖**:app 根層 teleport → BaseAlert + BaseDialog + FetchLoading

> **擴充候選**:Toast, ProgressBar, Banner

---

## 5. Content

內容展示與組織。

### 5.1 BaseCard

- **何時用**:資訊卡片容器
- **解剖**:VCard 包裝 → header slot + body slot + footer slot
- **狀態**:default / elevated / flat
- **token 引用**:`--color-surface`(底色), `--shadow-card`, `--radius-s`

### 5.2 BaseExpansion

- **何時用**:可折疊內容區塊
- **解剖**:VExpansionPanel 包裝 → header(toggle) + content
- **狀態**:collapsed / expanded / disabled

### 5.3 BasePopover

- **何時用**:點擊觸發的浮動內容面板
- **解剖**:trigger + floating panel(header + body)
- **狀態**:hidden / visible / focus-visible
- **token 引用**:`--shadow-popover`, `--radius-m`, `--z-index-popover`

### 5.4 EmptyTbody

- **何時用**:表格/列表無資料時的空狀態
- **解剖**:empty icon + message + pagination slot
- **狀態**:empty

> **擴充候選**:Accordion(group), Avatar, Carousel

---

## 6. Data

資料展示與操作。

### 6.1 BaseTable

- **何時用**:結構化資料展示(原生 table)
- **解剖**:thead(headers) + tbody(rows) + optional operate column
- **狀態**:default / empty(→EmptyTbody) / sortable / bordered
- **token 引用**:`--color-divider`(表格線), `--color-surface-variant`(斑馬紋底色)

> **擴充候選**:Tree view, List, DataTable(VDataTable 包裝)

---

## 7. Layout

頁面佈局與空間組織。

### 7.1 BaseDivider

- **何時用**:區塊間視覺分隔
- **解剖**:VDivider 包裝 → horizontal/vertical line
- **token 引用**:`--color-divider`

### 7.2 BasePanel / RwdPanel

- **何時用**:內容面板 / 響應式面板(含折疊)
- **解剖**:container + header + content slot / responsive container + toggle
- **狀態**:expanded / collapsed(RwdPanel)
- **token 引用**:`--color-surface`(底色)

> **擴充候選**:Grid system, Spacer

---

## 8. Status

純狀態展示;badge/chip 歸此類(邊界規則見檔頭)。

### 8.1 BaseChip

- **何時用**:標籤/分類展示
- **解剖**:pill 形狀 → label text
- **狀態**:default
- **token 引用**:`--radius-xl`(pill), `--color-background`(底色)

### 8.2 StatusChip / StatusTag

- **何時用**:狀態指示(審核/上架/停用等)
- **解剖**:chip/tag + color variant(依狀態類型)
- **狀態**:由業務邏輯決定(如:審核中/通過/退回)
- **token 引用**:`--color-info`/`--color-success`/`--color-error`(依狀態映射)

> **擴充候選**:Badge, Indicator

---

## 9. GIS(Map)

地理資訊系統特色元件。MetaUI 團隊核心領域。

### 9.1 MapPane

- **何時用**:地圖顯示面板
- **解剖**:map container + controls slot
- **狀態**:loading / interactive / error
- **token 引用**:`--z-index-map`(圖層基準)

> **擴充候選(觸發依 00_Blueprint GIS 節點)**:圖例(Legend), 圖層控制(LayerControl), 坐標顯示(CoordinateDisplay), 比例尺(ScaleBar)

---

## 附錄:元件統計

| 類別 | 現有元件數 | 擴充候選 |
|------|-----------|---------|
| Form | 15 | Number input, Search input, Toggle switch, Color/Time picker, Drag & drop |
| Action | 9 | ActionMenu, ActionBar, FAB |
| Navigation | 4 | SideNav, Stepper, Link |
| Feedback | 6 | Toast, ProgressBar, Banner |
| Content | 4 | Accordion(group), Avatar, Carousel |
| Data | 1 | Tree view, List, DataTable |
| Layout | 3 | Grid system, Spacer |
| Status | 3 | Badge, Indicator |
| GIS | 1 | Legend, LayerControl, CoordinateDisplay, ScaleBar |
| **合計** | **46** | — |

> 51 個掃描元件中 5 個為內部/全域掛載(TooltipBubble, ValidationList, GlobalComponents, TogglePanelButton, ToggleRwdPanelButton)，不獨立列入規範。

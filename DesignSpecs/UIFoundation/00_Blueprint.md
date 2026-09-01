---
file: DesignSpecs/UIFoundation/00_Blueprint.md
role: ds_blueprint
info_level: Candidate
origin: PREP-UI 前置準備產出
version: v0.1.1 (2026-07-18)
last_updated: 2026-07-18
summary:
  role: DS 藍圖=結構分類單源(節點鍵×標記×權威載體×消費者/觸發)
  scope: DS 內容分類軸。權屬單源=TRAINER/FolderOwnership;業務入口=TRAINER/UI_FuncIndex;排程屬路線載體，本檔不承載波次
  audience:
    - 專案成員
    - AI 管線
---

# MetaUI Design System 藍圖

> 本檔承載 DS 的結構分類:節點鍵、必要/可擴充標記、權威載體、消費者與觸發條件。
> 規範本文一律住權威載體，本檔只登記結構。
> 外部 DS 研究僅作分類參照;必要性判斷以三閘門、政府 GIS 場景與現有工具鏈為準。

## 一、標記判準

| 標記 | 名稱 | 判準 |
|------|------|------|
| ■ | 必要(依賴軌) | 三閘門或 DS 維護流程現行實際依賴;且缺失導致決策不可追溯、品質不可驗證或跨專案不一致。消費者欄列出依賴者 |
| ◆ | 必要(差異化軌) | 拍板者裁定之差異化主體(政府 GIS 場景);必要性來源=裁決，建置依觸發欄 |
| □ | 可擴充 | 依觸發條件啟動;觸發條件寫成可查驗徵兆，未觸發不建置 |

標記變更屬大改，層級與判準變更屬結構級(分級見 00_Philosophy 治理節)。

## 二、分類樹(導覽視圖)

層帶:L0~L5=內容層(DS 說什麼)|L6~L8=營運層(DS 怎麼運轉)|L5=橫切面(子項載體在他層)。
樹與 §三 表同檔維護;兩者不一致時以表為準。引用節點一律用節點鍵，L 序號僅供顯示。

```
metaui-ds
├─ L0 philosophy 理念
│   ├─ vision 願景與使命 ■
│   ├─ principles 原則與閘門地圖 ■
│   └─ boundary 邊界與階段標記 ■
├─ L1 foundations 基礎
│   ├─ tokens tokens SSOT 與生成管線 ■
│   ├─ color 色彩(雙層+深淺模式) ■
│   ├─ typography 字階與排版 ■
│   ├─ space-shape 間距/圓角/陰影/z-index ■
│   ├─ grid 版面網格與斷點 □
│   ├─ gis-cartography GIS 圖徵與分級設色 ◆
│   ├─ icons 圖示規範 □
│   ├─ motion 動效 □
│   ├─ imagery 圖像與插畫 □
│   └─ i18n 國際化 □
├─ L2 components 元件
│   ├─ spec 元件規範(六欄模板) ■
│   ├─ figma-library Figma 統一元件庫(上游) ■
│   ├─ code code 元件(下游採用) ■
│   ├─ storybook Storybook 故事同步 □
│   └─ code-connect 設計↔程式對映 □
├─ L3 patterns 情境
│   ├─ core 表單/空態/危險操作/回饋 ■
│   ├─ states 載入/唯讀/停用 □
│   ├─ admin 後台版型(列表/詳情) □
│   ├─ gis-interaction GIS 互動(圖層/量測/繪製/坐標) ◆
│   └─ dataviz 資料視覺化與圖表 □
├─ L4 content 內容
│   ├─ ux-writing UX Writing 規範 ■
│   ├─ glossary 術語(專案層) ■
│   ├─ glossary-base 術語(DS 基底層) □
│   └─ voice-tone 語氣矩陣 □
├─ L5 a11y 無障礙(橫切面)
│   ├─ builtin 元件內建合規 ■
│   ├─ contrast 對比機器驗 □
│   └─ audit 外部審查軌 ■
├─ L6 quality 品質檢核
│   ├─ gates 三閘門與三級漏斗 ■
│   ├─ checks 檢核規則語意與報告 schema ■
│   ├─ issues 報告鏈與議題帳 ■
│   └─ drift 漂移偵測與處置 ■
├─ L7 governance 治理
│   ├─ ownership 權屬與軸線 ■
│   ├─ change 變更流程(三級判準) ■
│   ├─ backprop 回溯傳播 ■
│   ├─ versioning 版本與棄用 □
│   └─ metrics 採用度量 □
└─ L8 tooling 工具鏈
    ├─ figma Figma 操作與維護鏈 ■
    ├─ generators 生成管線 gen_* ■
    ├─ runner 檢核執行器 ■
    ├─ deploy 部署(整包進駐) ■
    ├─ deploy-script 部署腳本化 □
    └─ ai-collab AI 協作規範 ■
```

## 三、節點權威表(權威記錄)

路徑縮寫:UI_KIT=`UI_DEPLOY/.metaui/UI_KIT`;UIF=`UI_DEPLOY/DesignSpecs/UIFoundation`。
「未建」=權威載體尚不存在;□ 節點於觸發成立並經裁決後建置。

### L0 philosophy 理念

| 節點鍵 | 項目 | 標記 | 權威載體 | 消費者(■◆)/觸發(□) |
|--------|------|------|---------|---------------------|
| philosophy.vision | 願景與使命 | ■ | UIF/00_Philosophy.md | 變更分級與爭議上送的裁決基準 |
| philosophy.principles | 原則(取捨式)與閘門地圖 | ■ | UIF/00_Philosophy.md(四條)+UIF/10_Principles.md(十條+地圖) | UI_KIT/30_ReviewRun G1-R/G2-R 原則覆驗;UIV-08 |
| philosophy.boundary | 邊界與階段標記 | ■ | UIF/00_Philosophy.md 邊界節+本檔標記欄 | 可擴充項啟動裁決 |

### L1 foundations 基礎

| 節點鍵 | 項目 | 標記 | 權威載體 | 消費者(■◆)/觸發(□) |
|--------|------|------|---------|---------------------|
| foundations.tokens | tokens SSOT 與生成管線 | ■ | UIF/tokens.json+UI_KIT/40_TokenPipeline.md | UIV-05/06;gen_tokens/gen_design_md/gen_vuetify_theme |
| foundations.color | 色彩(primitive/semantic 雙層+深淺模式) | ■ | UIF/tokens.json | UIV-06;uiv10 mode 面;G2-R 渲染覆驗 |
| foundations.typography | 字階與排版 | ■ | UIF/tokens.json | UIV-05/06 |
| foundations.space-shape | 間距/圓角/陰影/z-index | ■ | UIF/tokens.json | UIV-05/06 |
| foundations.grid | 版面網格與斷點 | □ | 未建;敘事基準=UIF/Design.md responsive 段 | 觸發=斷點值 token 化需求(第二個 RWD 場景進 G1) |
| foundations.gis-cartography | GIS 圖徵與分級設色 | ◆ | UIF/50_GisCartography.md(v0.1;互動歸 patterns.gis-interaction) | 建置觸發=首個含圖台頁面的專案進 G1(2026-08-18 成立，UII-031) |
| foundations.icons | 圖示規範 | □ | UIF/40_Iconography.md(v0.1)+對照契約 UIF/assets/;素材=Figma kit ICON 頁 | 觸發=kit ICON 頁項目變動，或補件元件需引用圖示(2026-08-18 成立，UII-031) |
| foundations.motion | 動效 | □ | transition token 兩級(值存 tokens.json);規範未建 | 觸發=過場/載入互動元件進元件規範 |
| foundations.imagery | 圖像與插畫 | □ | UIF/45_Imagery.md(v0.1)+佔位樣式 UIF/assets/ | 觸發=空狀態或導引插畫需求進 G0(2026-08-18 成立，UII-031) |
| foundations.i18n | 國際化 | □ | 未建 | 觸發=政府案合約含雙語驗收條款 |

### L2 components 元件

| 節點鍵 | 項目 | 標記 | 權威載體 | 消費者(■◆)/觸發(□) |
|--------|------|------|---------|---------------------|
| components.spec | 元件規範(六欄模板) | ■ | UIF/20_Components.md | G1 結構審;30_ReviewRun 選型判準 |
| components.figma-library | Figma 統一元件庫(上游) | ■ | Figma kit(發佈權=設計師) | uiv10 讀回 diff;40_TokenPipeline 單向紀律 |
| components.code | code 元件(下游採用) | ■ | 前端 repo;theme 接點=UIF/vuetify.theme.json | gen_vuetify_theme+UIV-06(採用型:缺席=needs-review) |
| components.storybook | Storybook 故事同步 | □ | 前端 Storybook | 觸發=stories token 化補丁派發，或新元件補件開工 |
| components.code-connect | 設計↔程式對映 | □ | 未建 | 觸發=kit library 發佈完成+首個元件對映需求 |

### L3 patterns 情境

| 節點鍵 | 項目 | 標記 | 權威載體 | 消費者(■◆)/觸發(□) |
|--------|------|------|---------|---------------------|
| patterns.core | 表單/空態/危險操作/回饋 | ■ | UIF/Design.md patterns 段 | G1 結構審;30_ReviewRun 反模式對照 |
| patterns.states | 載入/唯讀/停用狀態 | □ | 未建 | 觸發=表格或表單元件規範開工 |
| patterns.admin | 後台版型(資源列表/詳情) | □ | 未建 | 觸發=第二個後台專案進 G0 |
| patterns.gis-interaction | GIS 互動(圖層/量測/繪製/坐標) | ◆ | 未建;domain=gis | 建置觸發=首個含量測或繪製需求的專案進 G0 |
| patterns.dataviz | 資料視覺化與圖表 | □ | 未建;讓色紀律=UIF/Design.md | 觸發=首個統計圖表需求進 G0;domain=gis 相鄰 |

### L4 content 內容

| 節點鍵 | 項目 | 標記 | 權威載體 | 消費者(■◆)/觸發(□) |
|--------|------|------|---------|---------------------|
| content.ux-writing | UX Writing 規範 | ■ | UIF/30_UXWriting.md | UIV-11;gen_copy;G2 AI-R 佇列 |
| content.glossary | 術語(專案層) | ■ | 專案側 00_Glossary.md | UIV-04;10_SpecReview 輸入 |
| content.glossary-base | 術語(DS 基底層) | □ | 未建 | 觸發=兩個專案的 Glossary 出現交集術語 |
| content.voice-tone | 語氣矩陣 | □ | 未建 | 觸發=UI_DEPLOY 進駐第二條產品線 repo |

### L5 a11y 無障礙(橫切面:子項載體在他層，按面索引)

| 節點鍵 | 項目 | 標記 | 權威載體 | 消費者(■◆)/觸發(□) |
|--------|------|------|---------|---------------------|
| a11y.builtin | 元件內建合規 | ■ | UIF/20_Components.md a11y 欄(L2 載體) | 六欄模板必填欄 |
| a11y.contrast | 對比機器驗 | □ | 未建 | 觸發=對比檢核腳本進 checks/ 清冊 |
| a11y.audit | 外部審查軌 | ■ | Freego(外部工具);報告歸專案 ui/reviews/ | 必要性來源=政府案驗收要求 |

### L6 quality 品質檢核(制度與判定)

| 節點鍵 | 項目 | 標記 | 權威載體 | 消費者(■◆)/觸發(□) |
|--------|------|------|---------|---------------------|
| quality.gates | 三閘門與三級漏斗(V/AI-R/Human-R) | ■ | UI_KIT/AI_Rules.md(引用鏈)+10/20/30 SOP | 每案 G0→G1→G2 走用 |
| quality.checks | 檢核規則語意與報告 schema | ■ | UI_KIT/checks/README.md(清冊)+templates 報告模板 | run_checks 閘門子集 |
| quality.issues | 報告鏈與議題帳 | ■ | UI_KIT/templates+50_IssueFlow.md+專案側 90_IssueLedger.md | UIV-07 雙向一致 |
| quality.drift | 漂移偵測與處置 | ■ | UI_KIT/40_TokenPipeline.md 維護鏈節 | uiv10 diff+宣告例外機制 |

### L7 governance 治理

| 節點鍵 | 項目 | 標記 | 權威載體 | 消費者(■◆)/觸發(□) |
|--------|------|------|---------|---------------------|
| governance.ownership | 權屬與軸線 | ■ | TRAINER/FolderOwnership.md(權屬單源);業務入口=TRAINER/UI_FuncIndex.md;內容分類=本檔 | 結構性變動前置閘控 |
| governance.change | 變更流程(三級判準) | ■ | UI_KIT/AI_Rules.md 變更管理節(機制)+UIF/00_Philosophy.md 治理節(判準) | 每次載體變更走用 |
| governance.backprop | 回溯傳播 | ■ | UI_KIT/AI_Rules.md 引用鏈條款 | 破壞性變更觸發 |
| governance.versioning | 版本與棄用 | □ | DS@version 欄位既有;條款未建 | 觸發=首次破壞性 token 變更 |
| governance.metrics | 採用度量 | □ | 未建;指標清單=檢核通過率/例外數/hardcode 攔截數/設計返工率/DS 資產採用率 | 觸發=第三個專案進駐 |

### L8 tooling 工具鏈(執行工具)

| 節點鍵 | 項目 | 標記 | 權威載體 | 消費者(■◆)/觸發(□) |
|--------|------|------|---------|---------------------|
| tooling.figma | Figma 操作與維護鏈(變數/元件/MCP) | ■ | UI_KIT/40_TokenPipeline.md 維護鏈與沙盒紀律 | uiv10 輸入產製;單向 Figma→repo |
| tooling.generators | 生成管線 gen_*(五支) | ■ | UI_KIT/checks/ | UIV-06 新鮮度;--check |
| tooling.runner | 檢核執行器 | ■ | UI_KIT/checks/run_checks.py+uiv10_figma_diff.py | 閘門子集執行 |
| tooling.deploy | 部署(整包進駐) | ■ | UI_DEPLOY 容器(整包複製，外殼消失) | FolderOwnership 部署單元定義 |
| tooling.deploy-script | 部署腳本化 | □ | 未建 | 觸發=第三次手動部署作業 |
| tooling.ai-collab | AI 協作規範 | ■ | UI_KIT/AI_Rules.md+40_TokenPipeline 沙盒紀律 | 執行者每回合遵循 |

## 四、使用規則

- 查找:功能→節點鍵→權威載體;規範本文只住載體，本檔不承載。
- 增刪節點或改分類=結構級變更;改標記=大改(分級判準見 00_Philosophy 治理節)。
- □ 觸發成立時:登議題帳→提案→裁決後建置，同 commit 更新標記與載體欄。
- 階段自陳由標記承載:■◆=現行依賴或裁定，□=未觸發;本檔不寫波次與日期。

## 五、業界分類對照(22 類→節點)

對照基準=六家(Material 3/Spectrum/Carbon/Polaris/Fluent 2/GOV.UK)聯集。

| # | 業界類別 | 節點 | 註 |
|---|---------|------|-----|
| 1 | 理念/原則/價值觀 | philosophy.* | |
| 2 | 入門分軌(Get started) | 不入樹 | 部署外殼(00_START_UI)承擔，權屬歸 FolderOwnership |
| 3 | Foundations 基礎 | foundations.* | IA 歸 SA 側(跨 repo 分工)，不入本樹 |
| 4 | 視覺樣式(Styles) | foundations.color/typography/space-shape/icons/motion | 聲音規範=有意剔除(場景無) |
| 5 | Design tokens | foundations.tokens | |
| 6 | 元件+文件欄位 | components.spec | |
| 7 | Patterns 情境 | patterns.* | |
| 8 | Content/UX Writing | content.* | |
| 9 | Accessibility | a11y.* | |
| 10 | 國際化/雙向文字 | foundations.i18n | 雙向文字=有意剔除(中文場景) |
| 11 | 資料視覺化 | patterns.dataviz | |
| 12 | 地圖/空間規範 | foundations.gis-cartography+patterns.gis-interaction | 差異化軌(◆):六家僅 Carbon 有圖表型地圖，互動 GIS 均無 |
| 13 | Icons 資產庫 | foundations.icons | |
| 14 | 多平台 | 不入樹 | 有意剔除:單平台 Web(Vuetify)，邊界節明文 |
| 15 | 治理:貢獻流程 | governance.change | |
| 16 | 治理:版本/棄用 | governance.versioning | |
| 17 | 治理:採用度量 | governance.metrics | |
| 18 | 社群/生態系 | 不入樹 | 有意剔除:規模不適用 |
| 19 | 遷移指南 | governance.versioning | 附屬:交接文件遷移清單隨版本條款成長 |
| 20 | AI 介面規範 | tooling.ai-collab | 六家僅 Carbon 有 AI 介面章;AI 產線規範(檢核/漏斗/沙盒)為本系統自有章 |
| 21 | 設計工具鏈 | tooling.figma/generators/runner | |
| 22 | 研究/證據文化 | quality.issues | 議題帳+報告鏈+獨立審查承擔 |

## 六、視圖與外殼歸位

- UIF/Design.md=跨節點生成敘事視圖，不作節點;其各段落以所屬節點的載體欄出現。
- 00_START_UI(Status/Guide/Playbook)=部署操作外殼，不入分類樹;權屬歸 FolderOwnership。
- SOP 附屬素材(UI_KIT/references/、templates/)隨其所屬 SOP 節點，不獨立設節點。

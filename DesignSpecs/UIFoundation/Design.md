---
file: DesignSpecs/UIFoundation/Design.md
role: design_document
task: PREP-UI-2
origin: PREP-UI 前置準備產出
info_level: Candidate
ds_version: 0.3.1
provenance: DS@0.3.1
narrative_status: 敘事段=人工審定;資料段=gen_design_md 生成
colors:
  primary: "#176466"
  primary-emphasis: "#0a3738"
  primary-soft: "#d9efef"
  primary-container: "#eef4f3"
  secondary: "#fc890c"
  secondary-emphasis: "#6b4823"
  secondary-soft: "#ffecd8"
  secondary-container: "#fff8eb"
  tertiary: "#554677"
  tertiary-emphasis: "#2e2545"
  tertiary-soft: "#e6e1f0"
  tertiary-container: "#f1eef7"
  on-primary: "#ffffff"
  on-secondary: "#212b2b"
  on-tertiary: "#ffffff"
  on-primary-container: "#212b2b"
  on-secondary-container: "#212b2b"
  on-tertiary-container: "#212b2b"
  text: "#212b2b"
  subtitle: "#4c5858"
  placeholder: "#757575"
  background: "#ffffff"
  surface: "#fbfdfb"
  surface-variant: "#f3f7fa"
  primary-bright: "#39959b"
  hero-bg: "#12403f"
  hero-bg-deep: "#0a2b2a"
  hero-text: "#f2f9f8"
  hero-muted: "#9cc5c1"
  band-soft: "#eef6f5"
  divider: "#bfc8c6"
  stroke: "#8e9190"
  disabled: "#d8d8d8"
  red1: "#cd3033"
  red1-container: "#fff9f9"
  green1: "#138251"
  green1-container: "#f8fffc"
  blue1: "#0168ee"
  blue1-container: "#f3f8ff"
  orange1: "#b45309"
  orange1-container: "#fff4e5"
  on-error: "#ffffff"
  on-success: "#ffffff"
  on-info: "#ffffff"
  on-warning: "#ffffff"
  on-error-container: "#212b2b"
  on-success-container: "#212b2b"
  on-info-container: "#212b2b"
  on-warning-container: "#212b2b"
typography:
  font-family: "roboto, Noto Sans TC, sans-serif"
  sizes:
    display1: "2.75rem"
    display2: "2rem"
    head1: "1.75rem"
    head2: "1.5rem"
    subtitle1: "1.25rem"
    subtitle2: "1.125rem"
    body1: "1rem"
    body2: "0.875rem"
  weights:
    bold: 700
    medium: 500
    regular: 400
rounded:
  s: "4px"
  m: "8px"
  l: "20px"
  xl: "999px"
spacing:
  step-1: "2px"
  step-2: "4px"
  step-3: "8px"
  step-4: "12px"
  step-5: "16px"
  step-6: "20px"
  step-7: "24px"
  step-8: "32px"
  step-9: "48px"
  step-10: "64px"
  step-11: "96px"
---

# MetaUI Design Document

> 資料段為生成物(來源:tokens.json);敘事段(NARRATIVE 標記區)=人工審定內容,生成器保留不覆寫

## Overview

<!-- NARRATIVE:overview -->
MetaUI 是崧旭資訊為政府 GIS 資料服務打造的設計系統,服務兩種場景:**圖台前台**(地圖為主畫布的查詢與導覽)與**後台管理**(表格與表單密集的資料維運)。技術基底為 Vuetify 3,元件以 Base* 包裝層承載——換的是 token 值,不是工程師的寫法。

視覺性格:**沉穩的資料底色,單一的行動電壓**。品牌主色是低飽和的深青 `{colors.primary}`(#176466),承載身分與結構(header、主導覽、選取態);高飽和的橙 `{colors.secondary}`(#fc890c)是全系統唯一的強調電壓,只給主行動與關鍵焦點,一個畫面一次。文字用近黑的青灰 `{colors.text}`(#212b2b)落在近白的綠調表面 `{colors.surface}`(#fbfdfb)上,不用純黑。字體 Roboto + Noto Sans TC,標題階距克制(head1 僅 28px):這是資料工具,不是行銷頁,層級靠留白與分組,不靠字號吼。

**GIS 系統的特殊紀律——UI 讓色**:主色低飽和不是偶然。地圖圖層、專題渲染與資料視覺化才是彩度的主人,介面鉻件(chrome)必須在色彩上退位,否則工具會跟資料搶戲。這條紀律解釋了整個色彩系統的克制。

形狀語言三階:輸入與按鈕 `{rounded.s}`(4px)、卡片容器 `{rounded.m}`(8px)、標籤與 pill `{rounded.xl}`;陰影僅三級(card/popover/dialog),平面為預設,浮起才有影。間距走 4pt 網格(`{spacing.1}`~`{spacing.8}`,2~32px)。**Dark mode 是一等公民**:以 `[data-theme=dark_mode]` 屬性切換(非媒體查詢),長時間監控作業的護眼需求內建於 token 模式表。
<!-- /NARRATIVE:overview -->

## 設計原則摘要

> 完整版見 [10_Principles.md](10_Principles.md)

<!-- NARRATIVE:principles -->
十條原則,兩個層級:**紅線級三條**——一致性(同語意同元件同 token)、回饋(每個操作有下文)、錯誤預防(嚴重錯誤設計成不可能發生)——審查時違反即 🔴,不放行。其餘七條為建議級:通用可用性(新手有引導、專家有捷徑)、閉合感(多步流程有明確起終點)、可逆性(能 undo 就 undo)、目標要大要近(Fitts,常用的做大放近)、資訊分組(Miller,組塊化而非「不超過七項」)、遵循慣例(Jakob,跟隨 Vuetify/Material 慣例,不發明新互動)、選項精簡(Hick,減少同時選項,進階功能漸進揭露)。

設計期先看 Shneiderman 六條把結構做對;審查期 G1-R 用易用性原則結構六條對結構,G2-R 渲染後用 Nielsen 十大易用性原則全譜覆核——同一套認知科學,三個施力時機。
<!-- /NARRATIVE:principles -->

## Styles — Color

> 使用規則:元件/頁面只准引 semantic tier token;primitive 僅供 alias 引用(F-2)

### Primitive Colors(Light Mode)

| token | 值 | 說明 |
|-------|----|------|
| `{colors.primary}` | `#176466` | 品牌主色 |
| `{colors.primary-emphasis}` | `#0a3738` | 主色強調(原 primary-darken,F-5 改名) |
| `{colors.primary-soft}` | `#d9efef` | 主色柔和(原 primary-lighten,F-5 改名) |
| `{colors.primary-container}` | `#eef4f3` | 主色容器背景 |
| `{colors.secondary}` | `#fc890c` | 品牌輔色 |
| `{colors.secondary-emphasis}` | `#6b4823` | 輔色強調(原 secondary-darken,F-5 改名;dark mode 值由 mode 表切換) |
| `{colors.secondary-soft}` | `#ffecd8` | 輔色柔和(原 secondary-lighten,F-5 改名;dark mode 值由 mode 表切換) |
| `{colors.secondary-container}` | `#fff8eb` | 輔色容器背景 |
| `{colors.tertiary}` | `#554677` | 品牌第三色槽(結構回收:eco-pay 回件案源;試點回收起始值,專案可覆蓋;白字對比 8.3 過 AAA;圖表序列色屬另一語意,不與品牌角色共用鍵) |
| `{colors.tertiary-emphasis}` | `#2e2545` | 第三色強調(同構 primary/secondary 家族 -emphasis;試點回收起始值,專案可覆蓋) |
| `{colors.tertiary-soft}` | `#e6e1f0` | 第三色柔和(對 text 對比 11.3;試點回收起始值,專案可覆蓋) |
| `{colors.tertiary-container}` | `#f1eef7` | 第三色容器背景(對 text 對比 12.7;試點回收起始值,專案可覆蓋) |
| `{colors.on-primary}` | `#ffffff` | primary 底上前景(對比 6.9 過 AA;與 Vuetify theme on-* 慣例同名=消費端對接點;試點回收起始值,專案可覆蓋) |
| `{colors.on-secondary}` | `#212b2b` | secondary 底上前景(亮底深字慣例,對比 6.0 過 AA;secondary 無 dark 覆寫,本鍵不隨 mode 翻轉;試點回收起始值,專案可覆蓋) |
| `{colors.on-tertiary}` | `#ffffff` | tertiary 底上前景(對比 8.3;試點回收起始值,專案可覆蓋) |
| `{colors.on-primary-container}` | `#212b2b` | primary-container 底上前景(深字,對比 13.1;on-* 補遺=容器淺底配深字,與 on-primary 白字不可代用;試點回收起始值,專案可覆蓋) |
| `{colors.on-secondary-container}` | `#212b2b` | secondary-container 底上前景(深字,對比 13.8;試點回收起始值,專案可覆蓋) |
| `{colors.on-tertiary-container}` | `#212b2b` | tertiary-container 底上前景(深字,對比 12.7;試點回收起始值,專案可覆蓋) |
| `{colors.text}` | `#212b2b` | 文字基色(F-1 裁決:title #373b3c 與 font #212b2b 合併,取較深值) |
| `{colors.subtitle}` | `#4c5858` | 副標題文字色 |
| `{colors.placeholder}` | `#757575` | 佔位文字色 |
| `{colors.background}` | `#ffffff` | 頁面底色(F-3 裁決:原 white 拆分,頁面底→background) |
| `{colors.surface}` | `#fbfdfb` | 卡片/元件面色 |
| `{colors.surface-variant}` | `#f3f7fa` | 次要面色(F-4 裁決:原 container 改名,避免與 M3 -container 後綴衝突) |
| `{colors.primary-bright}` | `#39959b` | 亮調主色(展示層:飾線/圖形/hover 大字用,非內文文字色——AA 依用途驗算;試點回收起始值,專案可覆蓋) |
| `{colors.hero-bg}` | `#12403f` | 展示層 hero 深色帶底(45_PrototypeView 展示層槽;試點回收起始值,專案可覆蓋) |
| `{colors.hero-bg-deep}` | `#0a2b2a` | 展示層 hero 漸層深端/頁尾底(試點回收) |
| `{colors.hero-text}` | `#f2f9f8` | 展示層 hero 上主文字(對 hero-bg 對比 10.7 過 AAA;試點回收) |
| `{colors.hero-muted}` | `#9cc5c1` | 展示層 hero 上次要文字(對 hero-bg 對比 6.1 過 AA;試點回收) |
| `{colors.band-soft}` | `#eef6f5` | 展示層淺色段帶底(淺深節奏用;對 text 對比 >13;試點回收) |
| `{colors.divider}` | `#bfc8c6` | 分隔線色 |
| `{colors.stroke}` | `#8e9190` | 邊框/描邊色 |
| `{colors.disabled}` | `#d8d8d8` | 停用狀態色 |
| `{colors.red1}` | `#cd3033` | 紅色 primitive(F-2:只供 alias 引用,元件不直接使用) |
| `{colors.red1-container}` | `#fff9f9` |  |
| `{colors.green1}` | `#138251` | 綠色 primitive |
| `{colors.green1-container}` | `#f8fffc` |  |
| `{colors.blue1}` | `#0168ee` | 藍色 primitive |
| `{colors.blue1-container}` | `#f3f8ff` |  |
| `{colors.orange1}` | `#b45309` | 橘色 primitive(警戒語意保留區;試點回收起始值——對齊 CWA 警戒色階慣例,CTA 不得用橘) |
| `{colors.orange1-container}` | `#fff4e5` |  |
| `{colors.on-error}` | `#ffffff` | error 底上前景(light 對 red1 對比 5.2 過 AA;dark 隨 red1 提亮翻轉深字;試點回收起始值,專案可覆蓋) |
| `{colors.on-success}` | `#ffffff` | success 底上前景(light 對 green1 對比 4.8 過 AA;dark 隨 green1 提亮翻轉深字;試點回收起始值,專案可覆蓋) |
| `{colors.on-info}` | `#ffffff` | info 底上前景(對 blue1 對比 5.0 過 AA;blue1 無 dark 覆寫,本鍵不翻轉;試點回收起始值,專案可覆蓋) |
| `{colors.on-warning}` | `#ffffff` | warning 底上前景(light 對 orange1 對比 5.0 過 AA;dark 隨 orange1 提亮翻轉深字;試點回收起始值,專案可覆蓋) |
| `{colors.on-error-container}` | `#212b2b` | error-container 底上前景(深字,對比 14.0;on-* 補遺;試點回收起始值,專案可覆蓋) |
| `{colors.on-success-container}` | `#212b2b` | success-container 底上前景(深字,對比 14.3;試點回收起始值,專案可覆蓋) |
| `{colors.on-info-container}` | `#212b2b` | info-container 底上前景(深字,對比 13.6;試點回收起始值,專案可覆蓋) |
| `{colors.on-warning-container}` | `#212b2b` | warning-container 底上前景(深字,對比 13.4;試點回收起始值,專案可覆蓋) |

### Semantic Colors(元件應引用此層)

| token | 指向 | 說明 |
|-------|------|------|
| `{colors.text-heading}` | `{color.text}` | 標題文字色(F-1 semantic alias) |
| `{colors.text-body}` | `{color.text}` | 內文文字色(F-1 semantic alias) |
| `{colors.error}` | `{color.red1}` | 錯誤語意色(F-2 semantic alias → red1) |
| `{colors.error-container}` | `{color.red1-container}` |  |
| `{colors.success}` | `{color.green1}` | 成功語意色(F-2 semantic alias → green1) |
| `{colors.success-container}` | `{color.green1-container}` |  |
| `{colors.info}` | `{color.blue1}` | 資訊語意色(F-2 semantic alias → blue1) |
| `{colors.info-container}` | `{color.blue1-container}` |  |

### Dark Mode 覆寫

| token | Light 值 | Dark 值 |
|-------|---------|---------|
| `{colors.primary}` | `#176466` | `#57cbcf` |
| `{colors.primary-container}` | `#eef4f3` | `#131315` |
| `{colors.secondary-emphasis}` | `#6b4823` | `#ffecd8` |
| `{colors.secondary-soft}` | `#ffecd8` | `#6b4823` |
| `{colors.text}` | `#212b2b` | `#ffffff` |
| `{colors.subtitle}` | `#4c5858` | `#ffffff` |
| `{colors.background}` | `#ffffff` | `#2f2e31` |
| `{colors.surface}` | `#fbfdfb` | `#2f2e31` |
| `{colors.surface-variant}` | `#f3f7fa` | `#1a1a1a` |
| `{colors.disabled}` | `#d8d8d8` | `#3f3f3f` |
| `{colors.red1}` | `#cd3033` | `#f96063` |
| `{colors.green1}` | `#138251` | `#54c594` |
| `{colors.orange1}` | `#b45309` | `#ffaf54` |
| `{colors.band-soft}` | `#eef6f5` | `#16302f` |
| `{colors.on-primary}` | `#ffffff` | `#0a3738` |
| `{colors.on-primary-container}` | `#212b2b` | `#ffffff` |
| `{colors.on-error}` | `#ffffff` | `#212b2b` |
| `{colors.on-success}` | `#ffffff` | `#212b2b` |
| `{colors.on-warning}` | `#ffffff` | `#212b2b` |

## Styles — Typography

**Font family**: `roboto, Noto Sans TC, sans-serif`
**Line height**: 1.5
**Letter spacing**: fontSize × 0.02

| 級別 | token | 值 | px |
|------|-------|----|-----|
| display1 | `{typography.font-size.display1}` | `2.75rem` | 44px(展示層 hero 主標;試點回收) |
| display2 | `{typography.font-size.display2}` | `2rem` | 32px(展示層段帶標題;試點回收) |
| head1 | `{typography.font-size.head1}` | `1.75rem` | 28px |
| head2 | `{typography.font-size.head2}` | `1.5rem` | 24px |
| subtitle1 | `{typography.font-size.subtitle1}` | `1.25rem` | 20px |
| subtitle2 | `{typography.font-size.subtitle2}` | `1.125rem` | 18px |
| body1 | `{typography.font-size.body1}` | `1rem` | 16px(基準) |
| body2 | `{typography.font-size.body2}` | `0.875rem` | 14px |

| 權重 | token | 值 |
|------|-------|----|
| bold | `{typography.font-weight.bold}` | 700 |
| medium | `{typography.font-weight.medium}` | 500 |
| regular | `{typography.font-weight.regular}` | 400 |

## Styles — Spacing & Radius

### Spacing Scale（4pt grid）

| step | token | 值 |
|------|-------|----|
| 1 | `{spacing.1}` | `2px` |
| 2 | `{spacing.2}` | `4px` |
| 3 | `{spacing.3}` | `8px` |
| 4 | `{spacing.4}` | `12px` |
| 5 | `{spacing.5}` | `16px` |
| 6 | `{spacing.6}` | `20px` |
| 7 | `{spacing.7}` | `24px` |
| 8 | `{spacing.8}` | `32px` |
| 9 | `{spacing.9}` | `48px` |
| 10 | `{spacing.10}` | `64px` |
| 11 | `{spacing.11}` | `96px` |

### Border Radius

| 名稱 | token | 值 | 說明 |
|------|-------|----|------|
| s | `{radius.s}` | `4px` |  |
| m | `{radius.m}` | `8px` |  |
| l | `{radius.l}` | `20px` |  |
| xl | `{radius.xl}` | `999px` | pill |

## Styles — Shadow

| 名稱 | token | 值 |
|------|-------|----|
| card | `{shadow.card}` | `0px 4px 6px -2px rgba(0,0,0,0.1)` |
| popover | `{shadow.popover}` | `0px 4px 8px 0px rgba(0,0,0,0.2)` |
| dialog | `{shadow.dialog}` | `0px 11px 15px 0px rgba(0,0,0,0.2)` |

## Components

> 詳見 [20_Components.md](20_Components.md)——此處僅列分類摘要

| 類別 | 現有元件數 | 代表元件 |
|------|-----------|---------|
| Form | 15 | BaseInput, BaseSelect, BaseDatepicker |
| Action | 9 | BaseButton, ScrollToTopButton |
| Navigation | 4 | HeaderBar, BreadCrumbs, BaseTab |
| Feedback | 6 | BaseAlert, BaseDialog, BaseTooltip |
| Content | 4 | BaseCard, BaseExpansion, BasePopover |
| Data | 1 | BaseTable |
| Layout | 3 | BaseDivider, BasePanel |
| Status | 3 | BaseChip, StatusChip |
| GIS | 1 | MapPane |

## Patterns

<!-- NARRATIVE:patterns -->
先立五個模式骨架(模式庫擴充依 00_Blueprint 觸發制),每條都可在審查時逐項對照:

1. **表單模式**:label 上置;即時驗證,錯誤用 `{colors.error}` + BaseInput error 態 + 欄下訊息(說哪裡錯、怎麼修);必填以星號標示;整表**送出主行動唯一**,次要動作(取消/暫存)視覺降階。
2. **空狀態模式**(對齊五態 blank):比照 EmptyTbody 範式——說明「為什麼是空的」+ 給一個下一步行動,禁止只留白或只放一行「無資料」。
3. **危險操作模式**:不可逆操作(刪除、覆蓋)→ BaseDialog 二次確認,確認鈕用 `{colors.error}`、預設焦點在取消;可逆操作不設確認,改提供 undo(對齊原則 #6)。
4. **回饋模式**:輕操作(篩選、排序)→ 介面即時變化即為回饋;寫入操作 → toast/alert,成功 `{colors.success}`、失敗 `{colors.error}` 並保留使用者輸入;多步流程 → 步驟指示器 + 完成畫面含結果摘要(匯入 N 筆)。
5. **圖台佈局模式**:地圖是主畫布,控制面板浮於側緣、窄幅收為抽屜;UI chrome 用中性色 + `{colors.primary}`,**彩度讓給圖層資料**;圖例與坐標常駐但低視覺權重;量測/繪製工具進行中須有明確的「進行中」態與逐步 undo。
<!-- /NARRATIVE:patterns -->

## 反模式（Never Do）

- **Never** hardcode hex/rgb 色值——一律引用 token（UIV-05 機器檢核）
- **Never** 在元件/頁面層直接引用 primitive tier token（如 `{colors.red1}`）——改引 semantic（如 `{colors.error}`）
- **Never** 手改 tokens.css / 00_TokenSheet.md / Design.md 資料段——這些是生成物,改 tokens.json 後重生成
- **Never** 在 dark mode 判斷中使用 `prefers-color-scheme`——使用 `[data-theme=dark_mode]` 選擇器

<!-- NARRATIVE:anti_patterns -->
以下為判斷級反模式(機器抓不到,審查者要抓):

- **Never** 同一畫面出現兩個 `{colors.secondary}` 橙色主行動——橙是唯一強調電壓,一個畫面一次;搶焦即失焦。
- **Never** 在地圖畫布周邊使用高飽和 chrome 色與圖層資料搶色——UI 讓色是 GIS 系統的底線紀律。
- **Never** 用 `{colors.disabled}` 表達「唯讀內容」——disabled 是「行動不可用」,唯讀是「內容不可改」,語意不同、樣式不得混用。
- **Never** 因為 styled 畫面「看起來完成」而跳過或放水結構審查——審美-可用性效應會遮蔽結構問題,G1 未過不得因美觀放行(這正是 wire 先行的理由)。
<!-- /NARRATIVE:anti_patterns -->

## Responsive

| 名稱 | token | 值 |
|------|-------|----|
| xs-mobile | `{breakpoint.xs-mobile}` | `375px` |
| tablet | `{breakpoint.tablet}` | `768px` |
| laptop | `{breakpoint.laptop}` | `1280px` |
| desktop | `{breakpoint.desktop}` | `1440px` |
| xl-desktop | `{breakpoint.xl-desktop}` | `1920px` |

<!-- NARRATIVE:responsive -->
斷點策略依兩場景分工:**後台以 laptop(1280px)為設計基準**——表格與地圖並存的最小舒適寬,desktop/xl 只放寬留白與欄距,不增生佈局;**tablet(768px)是現場作業的關鍵斷點**——巡查、會勘等戶外情境以平板為主力,此檔位必須完整可操作,觸控目標 ≥ 44px(戶外、手套情境再放大);xs-mobile(375px)服務前台查詢,後台在此檔位允許唯讀降級,不強求所有維運操作可用。

收合規則:降欄不重排(欄數隨斷點遞減,列邏輯不變);圖台在窄幅時地圖全幅化、控制面板轉為抽屜;資料表格窄幅時凍結首欄橫向捲動,不折行擠壓。
<!-- /NARRATIVE:responsive -->

## Known Gaps

- 動畫/Transition 細節:僅有 fast(0.2s) / slow(0.5s) 兩級,缺 easing curve 分類
- A11y:色彩對比度未全表機械驗證(WCAG 2.1 AA)
- 0.75rem(12px)字級:出現於 BaseSelect 但不在 typography scale 內——待確認是否納入或標為例外
- GIS 元件:僅 MapPane 存在;圖例/圖層控制/坐標顯示=擴充候選(觸發依 00_Blueprint)
- Figma 變數同步:人工、單向 Figma→repo;漂移偵測=checks/uiv10_figma_diff.py(具名依賴 MCP 讀回,不入閘門子集)
- Brand 多品牌:MVP 假設單品牌,overrides 擴充槽保留名字不實作
- Dark mode subtitle 層級消失:subtitle 和 text 的 dark mode 覆寫值皆為 `#ffffff`,副標題在深色模式下與正文無區分——弱化值=設計師決定項;建議帶青灰調呼應品牌,錨點 `#a9b6b4`(於 `#2f2e31` 上對比約 7:1),範圍 `#9fb0ad`~`#c0cac8`;text 純白眩光疑慮可一併評估(業界慣例 87~90% 白,如 `#e6ecea`)


---
file: DesignSpecs/UIFoundation/40_Iconography.md
role: iconography_guide
info_level: Candidate
origin: PREP-UI 前置準備產出(PREP-UI-2)
version: v0.1.1 (2026-08-19;基底套件 MDI 獲設計師認可入註)
last_updated: 2026-08-19
summary: 圖示規範——基底套件與授權(MDI+yr.no 補位)/尺寸階與格線(token 綁定)/顏色紀律(currentColor+semantic)/氣象碼↔icon 兩段式契約(CWA Wx 1~42 全碼，fallback 規則)/無障礙(decorative 與 informative 分流)。自繪風格個性=Known Gaps 候設計師。
---

# 圖示規範

> 白話:在氣象資料工具裡，icon 不是裝飾，是資料介面——使用者掃一眼 icon
> 就該知道「今天什麼天氣」，不用讀字。因此 icon 的選用與對應關係是資料契約，
> 進版控，跟 tokens 同等治理。

## 一、三原則

1. **語意優先**:每個 icon 對應一個明確語意(天氣現象、操作、狀態)，
   同語意同 icon，全站唯一;禁同 icon 表兩義、兩 icon 表一義。
2. **不自創符號語言**:氣象現象用全民已有認知的符號(太陽、雲、雨滴、閃電)，
   對齊中央氣象署生活氣象 App 的既有心智模型，降學習成本。
3. **成套一致**:同一畫面內線寬、圓角、視覺重量一致——基底套件內選件，
   禁混搭第二套線性風格;缺件依 §五 補位順序，不逕自混入他套。

## 二、基底套件與授權

| 順位 | 套件 | 授權 | 用途 | 引入 |
|------|------|------|------|------|
| 1 | Material Design Icons(Pictogrammers) | Apache-2.0 | 通用操作/狀態/氣象子集 | Vuetify 原生生態(`@mdi/font` 或 `@mdi/js` 按需) |
| 2 | yr.no weather icons(MET Norway) | MIT | 氣象現象補位(MDI 缺件時) | 靜態 SVG 資產，逐件入 `assets/` |
| 3 | 自繪 | — | 前二者皆缺或需品牌個性時 | 候設計師輪，入 Figma kit ICON 頁後鏡像 |

- 新 icon 入包前逐件登記:名稱、來源、授權、對應語意(落 `assets/README.md` 清單)。
- prototype(靜態 HTML)引用方式=inline SVG path，不掛字型檔;前端 repo 走 Vuetify 慣例。

## 三、尺寸與格線

- 格線基準=24px(MDI 原生格線);縮放只取尺寸階，禁任意值。
- 尺寸階(token 綁定，tokens.json `icon` 群組):

| token | 值 | 用途 |
|-------|-----|------|
| `--icon-size-s` | 16px | 行內輔助(輸入框內、表格格內) |
| `--icon-size-m` | 20px | 按鈕內、清單項 |
| `--icon-size-l` | 24px | 獨立操作、導航 |
| `--icon-size-xl` | 32px | 空狀態、氣象現象主顯示 |

- 點擊目標:icon 本體可小，可點區域 ≥40×40(對齊 20_Components BaseIconButton 40×40)。

## 四、顏色紀律

- 預設=`currentColor` 繼承文字色，icon 隨語境變色，不各自帶色。
- 需獨立設色時只准 semantic token(F-2 紀律;UIV-05 掃 hardcode)。
- 警戒類 icon(警特報、異常狀態)限 `warning`/`error` 語意色——
  橘=警戒語意保留區(tokens orange1 條款)，非警戒內容禁用。

## 五、氣象碼↔icon 對照(兩段式契約)

模式借鑑 yr.no/MET Norway:API 代碼→icon 以資料契約對應，前端零判斷。
本站資料源=中央氣象署開放資料，天氣現象代碼(Wx)1~42。

- **兩段式**:`Wx 代碼 → canonical 天氣類別 → icon 名`。
  代碼層隨資料源換版，canonical 層穩定，icon 層隨套件/自繪演進——三層解耦。
- **契約載體**=`assets/weather-icon-map.json`(單一事實源，前端與 prototype 皆消費它)。
- **canonical 類別十類**:clear/fair/cloudy/overcast/rain/thunder/sleet/snow/fog
  +日夜變體規則(clear、fair 於夜間時段換 night 變體;日夜由時段推導，代碼不承載)。
- **分類規則**(機械可判，寫入契約檔):描述含「雷」→thunder;否則含「雪」→
  (雨或雪→sleet，純雪→snow);否則含「雨」→rain;否則含「霧」→fog;
  否則依天空階(晴/晴時多雲/多雲/陰)。
- **fallback 規則**:未對照代碼一律落 `cloudy` 並記 needs-review——
  部分覆蓋在構造上安全，不因缺碼破版。
- 代碼源=氣象署「預報 XML 產品預報因子欄位中文說明表」(107.12.20 製表版);
  代碼 40 官方表無(38→39→41 跳號)，契約檔照實登記。

## 六、無障礙

- **裝飾性** icon(旁邊已有等義文字)=`aria-hidden="true"`，不進讀屏。
- **承載資訊**的 icon 必附 `aria-label`，用詞循 00_Glossary(UIV-04 詞彙紀律同源)。
- icon-only 按鈕必帶 tooltip+`aria-label`(20_Components BaseIconButton 慣例，本章重申)。
- 氣象現象 icon 屬承載資訊類:label=canonical 類別的中文詞(契約檔 `label` 欄)。

## 七、消費端現況

20_Components 既有引用位:BaseInput(眼睛 toggle)、BaseButton(optional icon)、
BaseIconButton、tooltip 特化、FAB、Breadcrumbs(home)、Alert、EmptyState。
以上全數改循本章尺寸階與顏色紀律;新元件引用 icon 時本章為前置規範。

## 八、檢核掛載

- V:UIV-05(顏色 hardcode)既有涵蓋;「圖像/icon 槽佔位完備」=候選檢核
  (checks/README 候選登記，立案權=Trainer)。
- R:G1 結構審引用本章(icon 語意唯一性、套件一致性屬判讀項)。

## Known Gaps

- 基底套件 MDI 已獲設計師認可(2026-08-19);自繪風格個性(線寬、圓角、品牌感)
  候設計師回鍋輪定義，現行=基底套件原樣。
- Figma kit ICON 頁鏡像=DS 定型後一批補齊(55_FigmaFileRules 紀律)。
- 氣象自繪件(若基底套件語意不足)候設計師回鍋輪。

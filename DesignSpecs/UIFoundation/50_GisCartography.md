---
file: DesignSpecs/UIFoundation/50_GisCartography.md
role: gis_cartography_guide
info_level: Candidate
origin: PREP-UI 前置準備產出(PREP-UI-2)
version: v0.1 (2026-08-18;foundations.gis-cartography 首建(◆ 差異化軌);底圖讓色+分級設色 token 化+站點圖徵+圖例骨架)
last_updated: 2026-08-18
summary: GIS 圖徵與分級設色規範——底圖讓色(低彩度底圖，飽和色留給資料層)/分級設色三組收 tokens 級(雨量藍階 sequential 六級/溫度冷暖 diverging 七級/警特報三級對齊語意保留區)/站點圖徵與選取態/圖例規格/標註 halo 可讀性。互動(圖層/量測/繪製)歸 patterns.gis-interaction，未建不入本章。
---

# GIS 圖徵與分級設色

> 白話:圖台是政府 GIS 場景的差異化核心(00_Blueprint ◆ 軌)。地圖上的顏色
> 不是配色是編碼——深藍=雨大、紅=警戒，使用者用顏色讀數據。因此分級設色
> 收進 tokens 治理，改色=改資料語言，走變更流程，不是換皮。

## 一、範圍

- 本章管**靜態圖面**:底圖處理、資料層設色、站點圖徵、圖例、標註。
- 互動(圖層切換、量測、繪製、坐標)=patterns.gis-interaction(未建，觸發另計)。
- 統計圖表讓色=patterns.dataviz 相鄰(Design.md 讓色紀律同源)。

## 二、底圖讓色

- 底圖=背景不是主角:低彩度(灰階或淡色系)，飽和色全數讓給資料層。
- 底圖上不得出現與分級設色、警戒色同色相的地圖元素(誤讀風險)。
- 深色模式底圖=Known Gaps(候 dark 輪定案);現行 light 單軌。

## 三、分級設色(tokens 0.4.0 `color.rain`/`color.temp`/`color.alert`)

三組語意色階，值=色盲安全起始值(ColorBrewer sequential/diverging 譜系)，
專案可覆蓋;方向與級距語意對齊中央氣象署既有圖例慣例(全民已有認知，
不自創資料語言);官方圖例精確色碼之對齊覆核=Known Gaps。

| 組 | 型 | token | 用途 |
|----|-----|-------|------|
| 雨量 | sequential 六級 | `--color-rain-1`(淺)~`--color-rain-6`(深) | 累積雨量、降雨機率面量圖 |
| 溫度 | diverging 七級 | `--color-temp-cold-3`~`--color-temp-mid`~`--color-temp-warm-3` | 溫度分布、距平 |
| 警特報 | 三級 | `--color-alert-advisory`(黃)/`--color-alert-warning`(→orange1)/`--color-alert-severe`(→red1) | 警特報面與徽章 |

- 警特報二、三級=alias 至既有警戒語意保留區(orange1/red1)，不另生色——
  警戒語言全站唯一(40_TokenPipeline on- 綁定條款同理)。
- **分級離散優先**於連續色帶:級距邊界明確可讀，圖例可逐級對照。
- 級距數超出 token 級數時=需求進帳再擴，不逕自插值。

## 四、站點圖徵

- 預設 marker=`--color-gis-station`(→primary);選取=`--color-gis-station-active`(→secondary);
  異常/停測狀態循語意色(error/disabled)。
- 尺寸階循 icon 尺寸 token(40_Iconography §三);點擊目標 ≥40×40。
- 密集區群聚(cluster)顯示計數 chip，色循 primary 系;展開規則歸互動章(未建)。

## 五、圖例

- 必附:單位、級距邊界值、無資料表示法(無資料≠零值，分開表示)。
- 字階 body2 以上;圖例底=`surface` 加 `divider` 框，浮於圖面(z-index `panel`)。
- 分級色塊與邊界值逐級並列，不用連續漸層條。

## 六、標註可讀性

- 圖面文字標註一律帶 halo(`--color-gis-halo` 白暈)確保任意底圖上可讀。
- 字階 body2 以上;地名/站名用詞循 00_Glossary。

## 七、檢核掛載

- V:UIV-05(hardcode)涵蓋圖面 CSS;分級設色 token 化後 UIV-06 新鮮度鏈自動涵蓋。
- R:底圖讓色、級距語意、圖例完備=G1/G2 判讀項;首個實圖台頁進 G1 時本章隨案精修。

## Known Gaps

- 互動規範(圖層/量測/繪製/坐標)=patterns.gis-interaction 未建。
- 深色模式底圖與圖徵翻轉未定(現行 light 單軌)。
- 氣象署官方圖例精確色碼對齊覆核(現行=譜系與方向對齊，值為色盲安全起始值)。
- 站點資料的「前期產出如何納入登入後功能」屬專案側整合議題(團隊處理)，
  非本章範圍;其結論若產生新圖徵需求，循觸發制進帳。

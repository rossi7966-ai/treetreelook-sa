---
file: .metaui/UI_KIT/45_PrototypeView.md
role: ui_sop_prototype_view
info_level: Candidate
origin: PREP-UI 前置準備產出(PREP-UI-2)
version: v0.2.2 (2026-07-12)
last_updated: 2026-07-12
summary: 產品視圖(prototype)產線 SOP。三階產線宣告(wire→styled 審查視圖→prototype 產品視圖)、產製規則八條(僅 ideal/品牌 chrome/100% token/同結構同連結/文案完稿門檻)、V 檢核納管、展示層 token 擴充槽、Figma 鏡像紀律(code prototype=SSOT,鏡像文案=原文轉植禁自創事實);對 SA 與外部溝通一律以滿意的產品視圖為載體。
---

# 45|產品視圖產線(Prototype)

> 白話:styled 審查視圖是「給審查者看的」——五態堆疊、狀態標頭、TBD 斜紋、連接點徽章
> 都是制度鷹架,看起來永遠像工程圖。產品視圖是「給利害關係人看的」——同一套結構、
> 同一套 token,拿掉鷹架、補完文案、加上品牌門面,單就視覺已是準上線產品。
> 對 SA 回報與對外溝通,一律以拍板者滿意的產品視圖為載體。

## 三階產線(單一結構,三種視圖)

| 階段 | 載體 | 服務對象 | 產製 SOP |
|------|------|---------|---------|
| wire | pages/P##.html(stage=wire) | 結構審(G1-R):灰階下層級自明 | 20_FlowPages |
| styled 審查視圖 | 同檔演進(stage=styled) | 樣式合規(G2-R):五態+錨定+機器檢核 | 40_TokenPipeline |
| prototype 產品視圖 | pages/proto/P##.html(stage=prototype) | 驗收與對外溝通:吸引力+文案完稿 | 本檔+30_ReviewRun Prototype-R |

三者同源:結構與連結拓樸以 styled 為準,prototype 不得增刪資訊節點。
審查視圖永久保留(五態與制度證據載體),prototype 疊加其上,不取代。

## 前置

該頁 G2 已 PASS(styled 全綠)。文案未完稿不阻擋開工,但完稿門檻(規則 5)不過不得交驗收。

## 產製規則

1. **僅 ideal 態**:無 data-state 區塊、無 wire-meta/wire-foot/狀態標頭;
   五態證據由審查視圖承載,prototype 呈現產品單一實況。
2. **品牌 chrome 與展示層**:品牌 header(識別+主導覽)+頁尾(機關/聯絡/授權);
   hero 與分段帶(band)使用展示層 token(hero-bg/band-soft/display 字階);
   連接點徽章不顯示(制度元素,歸審查視圖)。
3. **100% token**:UIV-05 紀律全額適用(prototype 納檢);漸層/深色帶之色停一律
   `var(--token)`,禁 hex/rgb/px 字面(白名單同 styled)。
4. **同結構同連結**:資訊區塊與連結拓樸承 styled,去制度元素≠去內容;
   `data-w`/`data-term`/`data-nav` 錨定全數保留(不可見治理);頁間連結指向 proto/ 同名頁。
5. **文案完稿門檻**(交驗收前提):
   - 禁 `data-tbd` 與 ⟪⟫ 佔位(UIV-09 對 proto 零容忍)——未決內容以**假設代決文案**
     補完,逐筆登 90_Backfill(DEC-ASM),推翻只換內容不動結構;
   - 00_CopySheet 含 proto 全量(gen_copy 自動納入);
   - UIV-11 全譜適用;AI-R 佇列於 Prototype-R 逐條判讀(30_UXWriting §十)。
6. **登記表同步**:該頁 階段 欄改 `prototype`(UIV-01 據此驗 proto 檔存在);
   檔案路徑欄仍指審查視圖。
7. **命名對齊**:proto 檔名=審查視圖同名(pages/proto/P##_名.html);
   meta pageid/stage/primary-action 照填(stage=prototype)。
8. **範圍紀律**:prototype 只換視圖不改決策——要改結構回 G1,要改 token
   改 tokens.json 重生成(40_TokenPipeline),不得在 proto 層私調。

## V 檢核與交審

```
python .metaui/UI_KIT/checks/run_checks.py --gate G2 --scope <F 模組路徑>
python .metaui/UI_KIT/checks/gen_flowmap.py --scope <F 模組路徑> --capture
```

proto 頁納入 UIV-01/02/04/05/08/09/11(UIV-03 五態不適用:單態視圖);
FlowMap 縮圖自動優先取 proto 頁。修至無 fail → proto 截圖(單態)→
交 30_ReviewRun Prototype-R(吸引力/探索潛力/文案完稿判讀)。

## 展示層 token(tokens.json 擴充槽)

- color:`hero-bg` / `hero-bg-deep` / `hero-text` / `hero-muted` / `band-soft` /
  `primary-bright`(裝飾與大字用,非內文文字色——AA 依用途驗算)
- typography:`font-size.display1` / `font-size.display2`、`line-height.display`
- spacing:9/10/11(48/64/96px,band 垂直呼吸)
- layout:`content-width`(內容欄寬)

專案未擴充展示層時,prototype 以既有 token 組裝(hero 用 primary-emphasis 等),
不得因此 hardcode;展示層擴充=改 tokens.json 重生成,與一般 token 同紀律。

## Figma 鏡像(55_FigmaFileRules 配套)

- **SSOT 宣告**:code prototype(pages/proto/)=產品視圖的唯一真理來源;
  Figma 檔=**設計師可編輯鏡像**,供設計師接手迭代與跨職能溝通,不回寫 code——
  鏡像側的視覺決策要生效,走 Figma→tokens.json 單向維護鏈(40_TokenPipeline)。
- 佈建與寫入紀律=55_FigmaFileRules(頁面骨架/AI 隔離區/初始佈建例外/版本紀錄);
  variables 對齊驗收=`checks/uiv10_figma_diff` diff=0。
- 對齊抽查:鏡像頁 vs proto 頁同構(資訊節點與連結拓樸無增刪),隨 Prototype-R 抽查;
  鏡像落後 code 不阻塞閘門(鏡像=溝通載體,非審查載體)。
- **鏡像文案紀律**:樣張文案=code proto **原文轉植**,禁改寫、
  禁自創事實(公告/數據/來源說明尤甚——鏡像上的杜撰會被利害關係人當真);
  同構抽查含**文案抽比**:hero lede/卡片描述/規格列值 至少各一組對原文。

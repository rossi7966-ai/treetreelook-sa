---
file: .metaui/UI_KIT/45_PrototypeView.md
role: ui_sop_prototype_view
info_level: Candidate
origin: PREP-UI 前置準備產出(PREP-UI-2)
version: v0.4 (2026-09-08;增規則 9 產品視圖必備項+展示層工法(選用)段;--gate G2 正為 --gate all(G2 闘子集跑不到 proto 七支中五支);展示層預設路徑改為「無專屬 DS 即整組抄母版」;前版 v0.3 (2026-08-19;規則2 增 hero 氛圍照工法=照片+品牌色罩，條款掛 45_Imagery §五))
last_updated: 2026-09-08
summary: 產品視圖(prototype)產線 SOP。三階產線宣告(wire→styled 審查視圖→prototype 產品視圖)、產製規則八條(僅 ideal/品牌 chrome/100% token/同結構同連結/文案完稿門檻)、V 檢核納管、展示層 token 擴充槽、Figma 鏡像紀律(code prototype=SSOT，鏡像文案=原文轉植禁自創事實);對 SA 與外部溝通一律以滿意的產品視圖為載體。
---

# 45|產品視圖產線(Prototype)

> 白話:styled 審查視圖是「給審查者看的」——五態堆疊、狀態標頭、TBD 斜紋、連接點徽章
> 都是制度鷹架，看起來永遠像工程圖。產品視圖是「給利害關係人看的」——同一套結構、
> 同一套 token，拿掉鷹架、補完文案、加上品牌門面，單就視覺已是準上線產品。
> 對 SA 回報與對外溝通，一律以拍板者滿意的產品視圖為載體。

## 三階產線(單一結構，三種視圖)

| 階段 | 載體 | 服務對象 | 產製 SOP |
|------|------|---------|---------|
| wire | pages/P##.html(stage=wire) | 結構審(G1-R):灰階下層級自明 | 20_FlowPages |
| styled 審查視圖 | 同檔演進(stage=styled) | 樣式合規(G2-R):五態+錨定+機器檢核 | 40_TokenPipeline |
| prototype 產品視圖 | pages/proto/P##.html(stage=prototype) | 驗收與對外溝通:吸引力+文案完稿 | 本檔+30_ReviewRun Prototype-R |

三者同源:結構與連結拓樸以 styled 為準，prototype 不得增刪資訊節點。
審查視圖永久保留(五態與制度證據載體),prototype 疊加其上，不取代。

## 前置

該頁 G2 已 PASS(styled 全綠)。文案未完稿不阻擋開工，但完稿門檻(規則 5)不過不得交驗收。

## 產製規則

1. **僅 ideal 態**:無 data-state 區塊、無 wire-meta/wire-foot/狀態標頭;
   五態證據由審查視圖承載，prototype 呈現產品單一實況。
2. **品牌 chrome 與展示層**:品牌 header(識別+主導覽)+頁尾(機關/聯絡/授權);
   hero 與分段帶(band)使用展示層 token(hero-bg/band-soft/display 字階);
   連接點徽章不顯示(制度元素，歸審查視圖)。
   hero 得用氛圍照背景(來源條件與授權登記=DesignSpecs/UIFoundation/45_Imagery §五):
   照片上必壓品牌色罩——色罩以 `color-mix()` 於 hero-bg 系 token 構成(token 衍生，
   非 hardcode)，文字對比循 hero-text 驗 AA，攝影者頁面標註。
3. **100% token**:UIV-05 紀律全額適用(prototype 納檢);漸層/深色帶之色停一律
   `var(--token)`，禁 hex/rgb/px 字面(白名單同 styled)。
4. **同結構同連結**:資訊區塊與連結拓樸承 styled，去制度元素≠去內容;
   `data-w`/`data-term`/`data-nav` 錨定全數保留(不可見治理);頁間連結指向 proto/ 同名頁。
5. **文案完稿門檻**(交驗收前提):
   - 禁 `data-tbd` 與 ⟪⟫ 佔位(UIV-09 對 proto 零容忍)——未決內容以**假設代決文案**
     補完，逐筆登 90_Backfill(DEC-ASM)，推翻只換內容不動結構;
   - 00_CopySheet 含 proto 全量(gen_copy 自動納入);
   - UIV-11 全譜適用;AI-R 佇列於 Prototype-R 逐條判讀(30_UXWriting §十)。
6. **登記表同步**:該頁 階段 欄改 `prototype`(UIV-01 據此驗 proto 檔存在);
   檔案路徑欄仍指審查視圖。
7. **命名對齊**:proto 檔名=審查視圖同名(pages/proto/P##_名.html);
   meta pageid/stage/primary-action 照填(stage=prototype)。
8. **範圍紀律**:prototype 只換視圖不改決策——要改結構回 G1，要改 token
   改 tokens.json 重生成(40_TokenPipeline)，不得在 proto 層私調。

9. **產品視圖必備項**(AI_Rules 產製紀律 7 之展開；案源=設計師七點回饋 2026-08-19
   + 設計師視覺工法板 2026-09-07，拍板者 2026-09-08 裁採用):
   ① **去鷹架**:規則 1 所列制度元素一律不出現。
   ② **去線框改陰影**:區塊層級不靠粗框分割，改以面與光影承載——
   `--shadow-card`(元件級)或 `--shadow-ambient-s/m/l`(展示層漫射階)。
   **線寬本身不規定**——用不用框、幾 px，屬設計師與前端自治(2026-09-07 裁定；
   線寬不納 token、依前端 Storybook 現況)；本款只規定**層級不得僅靠框線而來**。
   **實務註**:`surface`(#fbfdfb)對 `background`(#ffffff)幾乎同色，
   無框卡片若陰影又淡會整張消失——無框卡片必落 `band-soft`／`surface-variant` 底或帶 ambient 階。
   ③ **主次分區**:同頁區塊不得等重——設定／結果、主／次以留白(spacing 9~11)、
   底色帶(`band-soft`)與字階(display2 vs head／subtitle)分區，**不以 ①②③ 編號代替層級**。
   ④ **可點性**:可導覽之卡片／清單項**整塊**為 `<a data-nav>`，帶 hover 浮起
   (陰影升一階，位移走 `calc(-1 * var(--spacing-n))`——**直寫 `-8px` 會被 UIV-05 拓**)
   與 focus 樣式(`--focus-visible`)。
   ⑤ **圖像不以文字或佔位代替**:G1 審定之圖像槽(地圖、插畫、照片、圖例色塊、介面截圖)
   必為實件——**禁佔位槽、禁以文字描述代替圖、禁 ●○▨ 文字符號代替色塊**。
   實件形式依 `45_Imagery` 四分法與 §五 授權條件；地圖頁依 `50_GisCartography` 三階呈現節。
   ⑥ **品牌 chrome**:規則 2 之 header 與頁尾為**必備非選配**。
   工具頁(非入口級)**不套 hero 大圖**，產品感來自「圖是真的、卡片有層次、可點的看起來可點」三件。

   **六項全備才交 Prototype-R。缺項=黃級起跳，⑤ 缺項=紅級**(等同完稿門檻)。

## V 檢核與交審

```
python .metaui/UI_KIT/checks/run_checks.py --gate all --scope <F 模組路徑>
python .metaui/UI_KIT/checks/gen_flowmap.py --scope <F 模組路徑> --capture
```

proto 頁納入 UIV-01/02/04/05/08/09/11(UIV-03 五態不適用:單態視圖);
FlowMap 縮圖自動優先取 proto 頁。修至無 fail → proto 截圖(單態)→
交 30_ReviewRun Prototype-R(吸引力/探索潛力/文案完稿判讀)。

## 展示層 token(tokens.json 擴充槽)

- color:`hero-bg` / `hero-bg-deep` / `hero-text` / `hero-muted` / `band-soft` /
  `primary-bright`(裝飾與大字用，非內文文字色——AA 依用途驗算)
- typography:`font-size.display1` / `font-size.display2`、`line-height.display`
- spacing:9/10/11(48/64/96px,band 垂直呼吸)
- layout:`content-width`(內容欄寬)

專案展示層槽位之預設路徑，依有無專屬 DS 二分:

- **無專屬 DS**(未自母版分支 tokens.json，或與部署包母版同值):
  展示層槽位**整組照抄母版**——上列 color 六鍵、display 字階、spacing 9~11、
  `content-width`、`shadow.ambient-*` 皆已在母版 tokens.json，部署包自帶即為基準；
  只改品牌鍵(primary 家族／secondary／hero-bg／hero-bg-deep，**改 X 必重算 on-X**)後重生成。
  **不得以「既有 token 組裝」代替展示層**(hero 拿 `primary-emphasis` 充數即為此病)，亦不得 hardcode。
- **有專屬 DS**:展示層擴充=改專案 tokens.json 重生成，與一般 token 同紀律；
  缺槽位者自母版補鍵，值可覆蓋。

> **母版新增之鍵不會自動到達專案**——換包射程明文「`DesignSpecs/` 非範本檔零觸」。
> 引用母版新鍵前先確認專案 `tokens.css` 有該鍵；沒有就依 40_TokenPipeline 下發節合併重生成。
> (UIV-05 **不驗 `var()` 名的存在性**，引錯不會 fail，畫面直接空白。)

## 展示層工法(選用)

> **適用面**=自產頁(`pages/` 三階)與前端手刻客製區塊(參考級)。
> **Vuetify 原生元件之線寬／hover／active／尺寸依 2026-09-07 裁定不納 token、
> 以前端 Storybook 為準，本節不反向規定。**

以下為選用工法，**不入必備項**，也不入機檢；採用與否屬 R 層判讀。
案源=設計師視覺工法板(2026-09-07)。

| 工法 | 做法 | token 指針與約束 |
|---|---|---|
| **跨層交疊** | 元件穿透底部幾何塊；次要卡片以負間距懸浮於主視覺邊緣 | 負位移走 `calc(-1 * var(--spacing-n))`；`--shadow-ambient-m`。**窄幅要取消交疊**(降欄不重排)；不得遮蔽資訊節點 |
| **大曲率幾何底板** | 大圓角至藥丸型區塊作局部承載底板 | `--radius-l`(20px)／`--radius-xl`(pill)。**段落級底板若需 >20px，向設計師取值後開新階，不自行補值** |
| **微型浮動標籤與指示器** | 主體周圍穿插極小獨立元件，形成視覺節奏 | `--radius-xl`+body2；`--z-index-panel`。**標籤必承載系統事實或狀態**(更新時間、站數、狀態)，**純裝飾不放**——否則撞「資料優於裝飾」與 TBD 禁虛構 |
| **數據錯點** | 關鍵量化指標放大作為掃視記憶點 | `font-size.display1`。**限系統事實且標來源**；編造數字撞產製紀律 3。**評分卡、重疊頭像、已下載人數等社會背書不入**——受眾為機關專業人員，且假頭像撞 45_Imagery §五 禁假人物擺拍 |
| **Cardlets 微卡片** | 大表單拆成相互獨立的微型卡片，單一卡片只講一件事 | **限資訊展示，輸入表單不適用**——每張 cardlet 各帶 CTA 會撞 UIV-08「全頁恰一 primary」，而它擋得對；表單模式優先 |

## Figma 鏡像(55_FigmaFileRules 配套)

- **SSOT 宣告**:code prototype(pages/proto/)=產品視圖的唯一真理來源;
  Figma 檔=**設計師可編輯鏡像**，供設計師接手迭代與跨職能溝通，不回寫 code——
  鏡像側的視覺決策要生效，走 Figma→tokens.json 單向維護鏈(40_TokenPipeline)。
- 佈建與寫入紀律=55_FigmaFileRules(頁面骨架/AI 隔離區/初始佈建例外/版本紀錄);
  variables 對齊驗收=`checks/uiv10_figma_diff` diff=0。
- 對齊抽查:鏡像頁 vs proto 頁同構(資訊節點與連結拓樸無增刪)，隨 Prototype-R 抽查;
  鏡像落後 code 不阻塞閘門(鏡像=溝通載體，非審查載體)。
- **鏡像文案紀律**:樣張文案=code proto **原文轉植**，禁改寫、
  禁自創事實(公告/數據/來源說明尤甚——鏡像上的杜撰會被利害關係人當真);
  同構抽查含**文案抽比**:hero lede/卡片描述/規格列值 至少各一組對原文。

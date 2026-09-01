---
file: .metaui/UI_KIT/checks/README.md
role: uiv_checks_manifest
info_level: Candidate
origin: PREP-UI 前置準備產出(PREP-UI-1)
version: v0.13 (2026-08-20;UIV-05 開 @media 條件式 breakpoint 白名單+rem 字面轉 needs-review+UIFoundation 官方載體不報白名單外，案源=moa UIX-007/008;前版 v0.12=gen_digest 兩修、v0.11=UIV-07/12 scope 三修)
last_updated: 2026-08-20
summary: UIV 檢核清冊與使用說明。十一支檢核(01~09+11+12)×四要素;prototype 產品視圖(pages/proto/)納 01/02/04/05/08/09/11;UIV-07 掃描面含 UIFoundation/reviews/(DS 層報告歸屬)+來源報告欄多名容錯;UIV-11 含去 AI 感機檢與 00_CopySheet/00_Digest 新鮮度;報告依 VerifyReportSchema v1.0,exit code 與五態分類同 VP 體系;生成器六支(tokens/digest/design_md/vuetify_theme/copy/flowmap;digest 之 TBD 只認宣告位、閥值只數活躍面)+selftest 迴歸自測+scan_hardcoded 導入輔助掃描器(不入閘門);成長迴路含候選登記。
---

# UIV 機器檢核清冊

> 定位:把「可判定的事」從 LLM 判斷抽離成腳本(V 層)。R 層(判斷審查)見 30_ReviewRun.md。
> 規格鏈:VerifyReportSchema v1.0 + VerifyImplGuide v1.0(MetaCore 10_SHARED 字面對齊;frozen-pin 登記=母版治理層 TRAINER/Issues)。

## 使用

```
python .metaui/UI_KIT/checks/run_checks.py --gate G0|G1|G2|all --scope <專案根或F模組> [--format text|json]
python .metaui/UI_KIT/checks/gen_tokens.py --project <專案根> [--check]
python .metaui/UI_KIT/checks/gen_design_md.py --project <專案根> [--check]
python .metaui/UI_KIT/checks/gen_vuetify_theme.py --project <專案根> [--check]
python .metaui/UI_KIT/checks/gen_digest.py --scope <F 模組>      # 生成 ui/00_Digest.md 一頁導讀
                                                                  # TBD 只採宣告位(整行以列表項起頭之 `[!TBD-xx]`)，句中引用不重複計入;
                                                                  # 拆分閥值只數活躍面，DEPRECATED/PLANNED/RESERVED 與 W99 不計入，計數基準隨警報列出
python .metaui/UI_KIT/checks/gen_copy.py --scope <F 模組>        # 生成 ui/00_CopySheet.md 文案清單
python .metaui/UI_KIT/checks/gen_flowmap.py --scope <F 模組> --capture  # 生成 ui/00_FlowMap.html 縮圖級 storyboard(宣告×實掃雙源對照;R 層輔件不入 UIV-06)
python .metaui/UI_KIT/checks/selftest.py                          # 檢核器迴歸自測(改 checks 必跑;樣本只增不減)
python .metaui/UI_KIT/checks/scan_hardcoded.py --root <消費端目錄> [--tokens <tokens.json>] [--out <報告.md>]
                                                                  # brownfield 硬寫值掃描(px/hex 頻次+映射建議;輔助工具不入閘門，語意映射必人工判定)
```

- 閘門子集:G0=02/04/09(對 SA 產出)、G1=01~04+08+09+12、G2=05~07+11
- **prototype 產品視圖**(pages/proto/,45_PrototypeView):納 01(登記表 階段=prototype 雙向)/02/04/05(stage=prototype 同紀律)/08(全頁恰一 primary)/09(data-tbd 與 ⟪⟫ 零容忍=完稿門檻)/11;UIV-03 五態不適用(單態視圖)
- exit code:0=綠、1=有 fail、2=有 parse-error;needs-review 與 allowed-exception 不影響 exit code
- 報告 stdout **原文貼入**審查報告 V 段，不轉述

## 檢核清冊(四要素)

| ID | 檢查對象 | 檢查方法 | 預期結果 | 失敗處置 |
|----|---------|---------|---------|---------|
| UIV-01 | 頁面登記對齊 | 10_UIFlow 登記表 ↔ pages/*.html 雙向比對(含 meta pageid) | 無孤兒頁、無未產檔登記 | 閘門 HOLD |
| UIV-02 | 規格錨定與連結 | data-w ∈ 03_Structure;flow P## ∈ 登記表;click/href 可解析;data-nav 型別化，裸 href="#" 零容忍;03_Structure 路徑欄實體存在(G0 面) | 全數命中、零死鏈 | 閘門 HOLD |
| UIV-03 | 五態覆蓋 | 每頁 data-state ∪ data-state-na(附理由)= 五態，不得重複宣告 | 覆蓋完整 | 議題帳 🟡 候選 |
| UIV-04 | 術語對齊 | data-term ⊆ 00_Glossary 表格首欄 | 全數命中 | 議題帳 🟡 候選 |
| UIV-05 | 樣式 lint | styled 頁:tokens.css 連結可解析;剝除 var() 後掃 hex/rgb/hsl/px(白名單 0/1px)。**`@media`／`@container` 條件式另案**——CSS 規範不允許條件式消費 `var()`，故只認等於某個 `--breakpoint-*` token 值的 px(專案未定義該類 token 時維持零容忍);**rem/em 字面**(宣告區與條件式皆同)列 needs-review——治理意義同 px 硬寫值，惟尚無對應 token 分類可替代，判 fail 等於再造一次同型阻塞，見候選登記。外掛表:`tokens.css` 為值的來源不掃自己，其餘一律掃內容，`DesignSpecs/UIFoundation/` 底下者視為 DS 官方載體不報「白名單外」 | 零 hardcode | 閘門 HOLD |
| UIV-06 | 生成物新鮮度 | tokens.json 重生成 ↔ tokens.css / 00_TokenSheet.md / Design.md 資料段 / vuetify.theme.json 零 diff;採用型生成物(Design.md/vuetify.theme.json)缺席=needs-review(是否採用歸 R 層)，存在才驗 | 一致 | 閘門 HOLD(重生成) |
| UIV-07 | 報告↔議題帳 | 報告 🔴🟡 行有 UIX 且在帳上;帳上來源報告存在(欄可列多名，、,;+/ 分隔=跨輪沿革);掃描面=**全 repo** 各 F 模組 ui/reviews/+UIFoundation/reviews/(DS 層報告歸屬，token 管線類報告的家);議題帳為全 repo 一本，故報告面不隨 --scope 收窄——收窄會使帳上他模組的來源報告誤判為不存在 | 雙向一致 | 補登後過閘 |
| UIV-08 | 主軸一致性 | flow 主軸宣告+DEC 引用;登記表主任務/primary 無空欄;每頁每態恰一 primary | 命中且唯一 | 閘門 HOLD |
| UIV-09 | TBD 對齊 | data-tbd ↔ 節點/REVIEW 未決 TBD 雙向;G0 無頁面時輸出 TBD 盤點 | 一致 | 🟡 候選;佔位缺席=needs-review |
| UIV-11 | 文案 lint(30_UXWriting V 層) | 模糊詞與裸動詞行動文案/CTA 字數/導航項數/指令型 placeholder/盤古之白偵測(中英數間不留空格，2026-08-07 拍板反轉)/loading 說明文字/error·blank 態行動元素/lorem 殘留/去 AI 感機檢(AF-04 核心詞全層;AF-05/09/11 散文層)/00_CopySheet 與 00_Digest 新鮮度(缺席=needs-review) | 零違規且表新鮮 | 閘門 HOLD;語氣與 AF 佇列判讀歸 G2-R(佇列=00_CopySheet) |
| UIV-12 | G0 IA 對照段存在(G1 前置) | ui/reviews/ 內 R##_G0 報告存在+至少一份含「IA 原則對照」段且至少一列已填(非 ⟪ 佔位);**無 ui/ 之 F 模組=尚未開工，不適用**(不報缺席) | 存在且已填 | 閘門 HOLD(G1 不得啟動) |

## 誠實邊界(不假機械化，拋 needs-review 或歸 R 層)

- BDD 情境 → flow 路徑的語意走通(20_FlowPages 步驟 2 由 AI 逐條比對)
- 可見文字的模糊術語漂移(UIV-04 只驗 data-term 精確比對)
- 「視覺強弱是否如主軸宣告」(UIV-08 只驗唯一性，強弱歸 G1-R)
- 佔位是否該出現(UIV-09 對「節點有 TBD 而頁無佔位」拋 needs-review)
- 語氣三原則/錯誤三段式措辭/日期單位語意(UIV-11 只驗結構與格式;判讀項出 00_CopySheet AI-R 佇列歸 G2-R)
- 行內元素切斷的中英交界(UIV-11 盤古之白偵測以文字片段為界，跨片段混入的空格不保證全捕)
- TBD 是否真的還沒決定(gen_digest 只認宣告位與節點狀態欄;節點檔解鎖後未加刪除線標記者仍會列出，屬 SA 側同步問題，不由生成器猜)
- 斷點值選得對不對(UIV-05 只驗「是不是某個 `--breakpoint-*` 的值」，選 768 還是 1280 屬版面判斷歸 G2-R)
- rem/em 字面該不該存在(機檢只列出，替代路徑未備齊前不作 pass/fail;見候選登記)
- 拆分閥值該不該調(生成器只按 >3／>15 報數並揭露基準，門檻本身與是否真要拆歸 SA;口徑先例=moa `DEC-SCOPE-005`)

## 成長迴路

R 層同型發現 ≥3 次(見 50_IssueFlow)→ 在此清冊登錄候選新 UIV，由 Trainer 立案。
新增檢核=uiv_checks.py 加函式 + CHECKS 註冊 + 本清冊補列 + 對應閘門子集更新。

### 候選登記(立案權=Trainer)

候選未落地前，引用處操作語意=跳過並記 needs-review，不作 pass/fail。

| 候選 | 來源 | 內容 |
|------|------|------|
| UIV-10 Figma↔tokens 漂移偵測 | 40_TokenPipeline 維護鏈 3 | **原型已落 `checks/uiv10_figma_diff.py`**:比對名/值/alias/mode 四面。具名依賴=輸入 JSON 須由 MCP(use_figma 全量讀回)產出，腳本不自行連 Figma，故不入 run_checks 閘門子集;立案時再定調用節奏 |
| 感知重複色偵測 | foundations.color(00_Blueprint) | primitive 色彩兩兩 ΔE 過近(肉眼難辨)時拋 needs-review，防重複語意色增生 |
| 部署載體字面 lint | TRAINER/Issues UII-013 | 部署與治理載體寫入前掃禁用句法(樣本來源=DraftRevRule §一 原則 6/7)+日期/波次/時序占位徵兆;命中=needs-review 交人工。未落地前，字面複核走獨立審查席(不自查) |
| on-X↔X 對比驗算 | eco-pay 併版回報 R1(40_TokenPipeline 回收節 on- 綁定條款) | color 群組同時存在 X 與 on-X(含 *-container 對)時，解析 alias 後驗 WCAG 對比 ≥4.5(light 必驗;宣告 dark 者 dark 亦驗);<4.5=fail。防專案覆蓋 base 色沿用母版 on- 基線(實證=on-warning 白字壓亮橘 1.97，現行機檢不報) |
| 圖像槽佔位完備 | 45_Imagery §三/§七(UII-031,DS 推進 P0) | 頁面 hero/圖像槽=實資產或合規佔位(`class="ph-slot"`+`data-ph`)，二擇一零空槽;機檢可判 class 與 data 屬性存在性;「該不該有槽」歸 G1 結構審 |
| 相對長度單位 token 化(rem/em 轉 fail) | moa UIX-007(R02_G2 首個 styled 頁)+eco-pay 既有頁 | 現況:`rem`/`em` 字面列 needs-review 不擋閘，因無對應 token 分類可替代(RAM 版面的最小欄寬只能寫長度值;`@media` 條件式也沒有 rem 斷點 token)。立案需求兩項=①補「欄位/容器最小寬度」類 token(`layout` 群既有 `content-width` 可為家)②決定 `--breakpoint-*` 要不要出 rem 對照鍵。實證用例已足:moa P01 用 14rem/22rem 撐 RAM 欄寬，eco-pay 7 頁用 48rem/64rem 當斷點。定分類後再把 rem/em 併入 fail 面——**不先立分類就轉 fail 會把版面路一起堵死，等於再造一次 UIX-007** |

已畢業候選:00_Digest 新鮮度→UIV-11 承載(過期=fail/缺席=needs-review)。

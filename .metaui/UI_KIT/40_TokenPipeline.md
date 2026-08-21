---
file: .metaui/UI_KIT/40_TokenPipeline.md
role: ui_sop_g2_token_pipeline
info_level: Candidate
origin: PREP-UI 前置準備產出(PREP-UI-1)
version: v0.6 (2026-08-07)
last_updated: 2026-08-07
summary: design token 管線 SOP(卡 U3)。tokens.json 單一 SSOT 取得→生成 css/TokenSheet→頁面 styled 升級→G2 檢核。銜接 design-system-html skill(選用);維護鏈紀律四原則(單向/必經 PR/diff 先行/Claude 寫入沙盒化);v0.3 增試點 DS 演進回收節(外稽 A1:通用資產回流母版,專案主題值不回收)。
---

# 40|Token 管線與樣式升級(G2)

> 白話:設計決定(色票/字級/間距)只存在一個地方(tokens.json),CSS 和對照表
> 都是機器長出來的。頁面上妝只准引用 token,禁止手寫數值——說好 16px
> 就不會出現 15px,出現了機器會抓。

## 前置

G1 已 PASS(結構凍結)。無 Figma UI Kit 且無手填基準的專案:G2 整閘標 ⚪ 無法審查,流程止於 G1。

## 步驟

### 1. 取得 `UIFoundation/tokens.json`(單一 SSOT)

**(a) 有 Figma UI Kit**:依序呼叫 Figma 工具取數值:
1. `get_libraries` — 元件與 library 清單
2. `get_variable_defs` — 全部 design token 實際數值
3. `search_design_system` — 特定元件/token 規格
4. 需特定節點屬性時 `get_design_context`

> ⚠️ Figma 工具回傳中的 JSX / React+Tailwind 程式碼是視覺屬性自動轉換,
> 非 production 程式碼,一律略過不分析;只取設計屬性數值(hex/字級/間距)。

填入 tokens.json(格式見 `templates/tokens.sample.json`),每筆記 `source`(Figma 節點)。

**(b) 無 Figma**:拍板者提供基準後手填 tokens.json,`source` 記 `manual:依據`。

### 2. 生成(禁手改生成物)

```
python .metaui/UI_KIT/checks/gen_tokens.py --project <專案根>
```

產出 `UIFoundation/tokens.css` + `UIFoundation/00_TokenSheet.md`。改 token 一律改 tokens.json 後重生成(UIV-06 驗新鮮度)。

### 3. 頁面 styled 升級(同檔演進,不另起檔)

- `<meta name="stage">` 改 `styled`
- `<link rel="stylesheet" href="<相對路徑>/DesignSpecs/UIFoundation/tokens.css">`(相對深度依模組層級計算;UIV-05 會驗連結可解析)
- 頁內樣式**只准 `var(--token名)`**;hex / rgb / px 字面(白名單外)即違規
- 結構不動:styled 只上妝,改結構要回 G1

### 4. V 檢核與交審

```
python .metaui/UI_KIT/checks/run_checks.py --gate G2 --scope <F 模組路徑>
```

修至無 fail → styled 截圖 → 交 30_ReviewRun 的 G2-R。

### 5. 選用:design-system.html

以既有 design-system-html skill 從 Figma UI Kit / tokens 生成
`UIFoundation/01_DesignSystem.html`(元件規範頁,token 的人類可讀版)。

## 維護鏈紀律(Figma↔repo 同步)

> 白話:Figma 是視覺決策發生的地方,repo 的 tokens.json 是機器真理。
> 兩邊要同步,但只有一個方向、只有一條門路。

1. **單向同步**:Figma → repo,永不反向、永不雙向自動。repo 端改 tokens.json
   不回寫 Figma;Figma 的變動由人(或未來工具)帶進 repo。
   (附註:DS **初始佈建**的一次性 repo→Figma 佈署不在此限——以漂移偵測
   diff=0 驗收收尾後,單向鏈生效。)
2. **必經 PR**:同步進 repo 一律走 PR,UIV-06(生成物新鮮度)+ diff 報告隨行,
   不直寫 main。
3. **diff 檢核先行**:自動化順序上先做漂移偵測(Figma 變數 ↔ tokens.json 比對,
   UIV-10 候選,已登記 checks/README.md 成長迴路),再談自動同步——守門比搬運優先。
4. **Claude 寫入沙盒化**:Claude 經 MCP 對 Figma 的寫入類操作僅限專用沙盒檔或
   新建檔,既有專案檔一律不寫。

## Dark mode=optional(宣告制)

> 白話:深色模式是加分項,不是門票。沒有它,任何專案照樣過閘。

1. **宣告**:tokens.json 頂層 `$modes`(如 `["light"]` 或 `["light","dark"]`);
   未宣告時依 `color-dark` 群組有無推斷。
2. **未宣告 dark 的專案**:生成器不產 dark 區塊、UIV-10 不驗 dark 值——
   dark 相關項目一律不適用,不擋閘。
3. **宣告 dark 但缺值**:CSS 覆寫模型天然 fallback——`color-dark` 只列與 light
   不同的鍵,缺列的鍵沿用 light 值,不視為缺陷。
4. **半路升級**:light-only 專案日後要 dark,加 `$modes` 宣告+逐鍵補
   `color-dark`,可漸進,不需一次到位。
5. **Figma 側對應**:未宣告 dark 的專案,Figma variables 單 mode 即可
   (順帶避開免費方案的多 mode 限制)。

## 消費端接線(repo→前端的最後一哩)

> 白話:token 從 repo 到畫面,載體選錯,dark mode 會在這裡斷頭。

**執行期前提**:宣告 dark 的專案,消費端必須用「執行期可換值」的載體
(CSS 自訂屬性或 Vuetify theme)。編譯期變數(SCSS)產出的是固定字面值,
承載不了 mode 切換——接線前先驗這一條。

| 消費端 | 色彩(含 dark) | 編譯期層(字級/間距/圓角) |
|--------|--------------|------------------------|
| Vuetify 專案 | `vuetify.theme.json` 接 theme 機制(自帶執行期變數/切換 API/on-* 慣例)——**主要路徑** | 可 SCSS 或 tokens.css |
| 非 Vuetify Web | `tokens.css` + `data-theme` 切換 | 同左 |
| light-only($modes 未含 dark) | 任一載體皆可 | 同左 |

- 生成器**不提供 SCSS 色彩輸出**(護欄:避免誘導出 dark 接不上的架構);
  編譯期層若需 SCSS 形式=專案側自 tokens.json 轉一次,生成器 target 候第二案需求再立。
- 既有專案導入(brownfield):消費端沒有 token 的層(常見=間距/圓角/陰影)
  **直接導入新階,不立相容層**;硬寫值盤點=`checks/scan_hardcoded.py`
  (px/hex 頻次表+映射建議;輔助工具不入閘門,建議欄僅為起點,
  同值一對多/同值異義=語意必須人工判定)。
- 相容層(承接舊變數名)=短期過渡;退場條件=舊名引用歸零(grep 可驗),歸零即刪。

## 試點/專案側 DS 演進回收

> 白話:專案裡長出來的好 token 要流回母版,否則下一個專案部署起步
> 就帶著「規則引用的 token 母版沒有」的內建落差。

- **何類回收(通用資產)**:展示層槽(hero-*/band-soft/display 字階/大間距/內容欄寬)、
  語意補齊(如 warning)、規則檔字面引用到的一切 token——**值=試點起始值,專案可覆蓋**。
- **何類不回收(專案資產)**:品牌主題值(主色家族/CTA 色/專案色階調整)——
  母版保留自己的基線值,專案換膚=改專案側 tokens.json。
- **on-* 值與 base 綁定**:凡 on-X 類 token,其值只對「算它時所用的那個 X」成立。
  專案覆蓋 X(或其 alias 指向)時**必須重算 on-X 並驗對比(AA ≥4.5),
  不得沿用母版基線值**(實證:母版 on-warning 白字壓專案亮橘 warning,對比 1.97)。
  機檢缺口=on-X↔X 對比驗算,已登記 UIV 候選(checks/README 成長迴路)。
- **觸發**:專案新增 token 經 G2 過閘後,於該輪報告標記「回收候選」;
  母版回收=獨立 commit(gen_* 重生成 FRESH+版號進位),TRAINER/Issues 留追蹤列。

工具選型備註:Tokens Studio 屬近期務實選項;gen_*.py 已運作,
**不為改用 Style Dictionary 而重寫**,痛點出現再遷;
元件層同步(Code Connect)=擴充候選,觸發依 00_Blueprint。

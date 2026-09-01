---
file: .metaui/UI_KIT/55_FigmaFileRules.md
role: ui_sop_figma_file_rules
info_level: Candidate
origin: PREP-UI 前置準備產出(PREP-UI-2)
version: v0.1.1 (2026-07-12)
last_updated: 2026-07-12
summary: Figma 檔案頁面管理規則(Concept A 落地)。頁面骨架 11 頁、命名文法、封面狀態標籤、AI 隔離區(Sketches)、Master 版本紀錄、初始佈建例外(新建 DS 檔經拍板者授權佈建 variables/元件，diff=0+設計師接管後回歸唯讀)。
---

# 55|Figma 檔案管理規則(Concept A 配套)

> 白話:Claude 寫進 Figma 的一切，落在哪一頁、叫什麼名字、誰之後能動，
> 都照這份規則——設計師打開檔案，一眼就知道哪些是 AI 產出、哪些是定稿。
> 依據=設計師指定「Figma設計文件管理研究」Concept A;
> 與 40_TokenPipeline 維護鏈紀律 4(寫入僅限沙盒/複本/新建檔)疊加適用。

## 一、頁面骨架(MetaUI 寫入檔一律遵循)

Concept A 五分類(Master/Research/Resource/Sketches/Done)+團隊 emoji 慣例:

| 順序 | 頁名 | 分類 | 內容規則 |
|------|------|------|---------|
| 1 | `cover` | — | 檔名/開發版本/日期/功能描述/狀態標籤(準備好開發・確認中・已取消) |
| 2 | `📖 Master｜版本概覽` | Master | 版本迭代追蹤表(日期/版本/變更摘要/負責人);與 repo tokens.json `$version` 對齊 |
| 3 | `-----` | 分隔 | 空頁，純分節 |
| 4 | `📍 Resource｜元件庫-後台` | Resource | 元件本體(kit 複本沿用既有 📍後台 — UI Kit 頁) |
| 5 | `📍 Resource｜元件庫-前台` | Resource | 同上(前台) |
| 6 | `🔍 Resource｜ICON` | Resource | icon 元件 |
| 7 | `📚 Resource｜規範` | Resource | token 色板/字級表/間距表(可由 AI 生成對照 frame)+品牌規範連結 |
| 8 | `-----` | 分隔 | |
| 9 | `✏️ Sketches｜AI 產出區` | Sketches | **AI 隔離頁:Claude 生成的一切 frame 先落此頁，經設計師確認後由人搬移**;頁首放置說明文字 |
| 10 | `🔬 Research｜研究` | Research | 訪談/易用性測試/筆記(可空頁保留) |
| 11 | `✅ Done｜定稿` | Done | 產品介面/流程圖/最終解決方案(設計師搬入，AI 不直寫) |

> 既有檔改造時:保留原頁內容，僅補缺頁與正名——不重排設計師的元件版面。

## 二、命名文法與狀態標記

- 頁名=`emoji 分類｜用途`;分類詞彙固定五選一(Master/Research/Resource/Sketches/Done)
- 進度標記:執行版本檔沿用 `✅`(完成)/`⚒️`(進行中)前綴;
  kit/DS 檔頁面不掛進度(元件庫無「完成態」，以發佈為準)
- 封面狀態標籤三選一:`準備好開發`/`確認中`/`已取消`——狀態變更時同步更新封面
- Starred:高頻頁(元件庫/版本概覽)加星，對齊 Concept A「以階段建立 Starred」

## 三、管理規則(誰能動什麼)

| 區域 | 設計師 | AI(Claude) |
|------|--------|-----------|
| cover / Master | 維護 | 可代寫版本紀錄列(經指示或依本檔版本紀錄紀律) |
| Resource(元件庫/規範) | 維護 | **唯讀**;例外僅二:複本檔正名(經拍板者授權)/初始佈建(見四) |
| Sketches｜AI 產出區 | 檢視/搬移 | **唯一可自由寫入頁** |
| Research / Done | 維護 | 唯讀 |

- 檔案層紀律(40_TokenPipeline 維護鏈 4):AI 寫入僅限專用沙盒檔/經拍板者授權之複本檔/新建檔，
  既有專案檔一律唯讀;檔內僅限 Sketches AI 產出區自由寫入。

## 四、初始佈建例外(經拍板者授權)

新建 DS 檔從零起步時，Resource 頁(variables/元件庫/規範 frame)的**初始佈建**
得由 AI 執行——比照 U3 正名例外，為一次性、有收尾條件的授權:

1. **前提**:拍板者逐檔授權;僅適用**新建檔**(既有專案檔不適用本例外)。
2. **來源紀律**:variables 與元件樣式一律對齊 repo `tokens.json`(單一真理來源)，
   不得在 Figma 側自創值;對應 40_TokenPipeline 紀律 1 附註
   (初始佈建的一次性 repo→Figma 佈署不在單向鏈限制內)。
3. **收尾條件**:`checks/uiv10_figma_diff` 漂移偵測 **diff=0**+設計師接管宣告
   →Resource 頁回歸唯讀，單向維護鏈(Figma→repo)生效。
4. **佈建期間**:每一寫入批次仍逐列記 Master 版本概覽(見五);
   佈建範圍逐項列於當輪 R 報告，交拍板者驗收。

## 五、版本紀錄(檔內可見的操作履歷)

AI 每次寫入後在 `📖 Master｜版本概覽` 追加一列:日期/版本/操作摘要/AI 標記。
與 repo 側 R 報告互補:Figma 檔內看得到「誰動過什麼」,repo 看得到「為什麼動」。

## 六、設計師確認項(不阻塞新建檔作業)

1. 五分類頁名的中文用詞是否照本檔(或設計師慣用詞)
2. Research 頁群現階段是否建置(可空頁保留 vs 暫不建)
3. 既有專案檔(執行版本)是否回頭補 cover 狀態標籤(不強制，新檔起適用)

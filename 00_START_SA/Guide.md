---
version: v1.8 (2026-07-18)
last_updated: 2026-07-18
changed_by: Claude Code
summary: 合併第8節重複SA/Runner角色列；修復議題[I-26](補丁：命名定案批次二)(補丁：命名定案批次三)(補丁：命名定案批次五)(修復J-7：CR開場表格補入Glossary區塊B)(v1.6：MS-T018 I-87批B §🔄核心原則與§8表角色術語對齊 Coach)(v1.7：MS-T051 I-94 onboarding 配套——加「Coach Chat 啟動教學」段,含三件套上傳清單 + Coach chat 命名紀律 + 不用 Projects/Gem 預載的紀律)
---
# Guide.md｜人類操作指南

> AI_Rules.md是給AI讀的治理規範，不是給人類讀的。
> 這份文件才是給SA看的工作指南。

---

## 👋 新手請先看這裡：15分鐘沙盒演練

**你不需要先讀完這份文件。只需要跑一次沙盒演練，你就會理解這套系統。**

沙盒情境：「為一個『會員登入』功能建立規格」

1. 打開00_Status.md，記住現在的樣子
2. 用卡0分析一個極簡需求：「使用者可以用Email和密碼登入系統」
3. 用卡A建立文件庫(若尚未建立)
4. 用卡B新增一個F模組：「F01_會員登入」
5. 觸發Runner執行D1草稿生成
6. 用卡C審閱草稿，手動刪除一個[!TBD-ID]標記並填入決策
7. 用卡D觸發D2收斂，看到編碼核對綠燈
8. 回到00_Status.md，看看它現在長什麼樣子

完成這八步，你已經理解這套系統的完整生命週期。

---

## 1. 我現在該看哪裡？

```
任何時候 → 先開00_Status.md
看「🎯 當前焦點」 → 知道現在在哪裡
看「🚨 警報器」 → 知道有沒有被阻擋
看「✅ 下一步行動」 → 知道該做什麼
```

---

## 2. 情境卡選擇表

| 我現在想做什麼 | 用哪張卡 | 在哪裡找 |
|-------------|---------|---------|
| 分析新需求 | 卡0 | 00_START_SA/Playbook.md |
| 全新專案啟動 | 卡A | 00_START_SA/Playbook.md |
| 新增功能模組 | 卡B | 00_START_SA/Playbook.md |
| 審閱AI草稿 | 卡C | 00_START_SA/Playbook.md |
| 觸發規格收斂 | 卡D | 00_START_SA/Playbook.md |
| 需求變更 | 卡E | 00_START_SA/Playbook.md |
| 重構或歸檔 | 卡F | 00_START_SA/Playbook.md |
| 核對失敗修復 | 卡G | 00_START_SA/Playbook.md |

---

## 3. 最常用流程

```
需求素材
  ↓ 卡0：需求分析[R1→R2]
交接包
  ↓ 卡A/卡B：建立文件庫或新增模組
文件庫就緒
  ↓ 觸發D1草稿生成
AI草稿完成
  ↓ 卡C：草稿審閱[D1.5]
審閱完成
  ↓ 卡D：規格收斂[D2]
規格收斂✅
  ↓ 有新需求？→ 卡E：CR模式
```

---

## 4. 什麼時候可以直接改檔案？

| 檔案 | 可以直接改的時機 | 不能直接改的時機 |
|------|---------------|---------------|
| nodes/M##-F##-W##.md | D1.5審閱期間 | D2完成後(走CR) |
| F##_L3_Workflow.md | D1.5審閱期間 | D2完成後(走CR) |
| F##_L4_UserStories.md | D1.5審閱期間 | D2完成後(走CR) |
| F##_L2_Routing.md | D1.5審閱期間 | D2完成後(走CR) |
| 03_Structure.md | 新增/刪除W節點後立即更新 | 不限時機，但改後必須重跑D2 |
| 00_Glossary.md | 隨時可補充DEC決策記錄 | 不得刪除既有決策記錄 |
| 00_Status.md | 隨時(SA手動維護) | 不得讓Runner自動覆寫 |
| `SYS##_overview.md` | 系統邊界調整時，SA手動更新 | 不限時機，但改後必須同步03_Structure |
| `SS##_overview.md` | 新增/移除M層歸屬時 | 不得刪除已有M層記錄，需先確認M層已搬移 |
| M##_overview.md | 業務邊界調整時 | M層建立後不輕易修改邊界 |
| `M##_boundary.md` | Runner自動建立初稿，SA填寫confirmed_by | SA確認後不得由Runner覆寫 |
| 04_FuncMap.md | 僅限D2後貼入Runner建議的片段 | 不得自行編輯Mermaid節點 |

---

## 5. 什麼時候一定要走CR模式？

以下情況嚴禁直接改檔案，必須用卡E走CR模式：

- D2完成後，已收斂模組有任何規格變更
- 新需求影響既有的EP或UserStory定義
- 需要新增或刪除W##節點(且D2已完成)

CR模式的核心：10_ReqAnalysis.md只輸出「差異清單」，不產出全新交接包覆蓋既有規格。

---

## 6. 常見錯誤與修復

| 狀況 | 不要做 | 正確處理 |
|------|-------|---------|
| Runner產出的W節點不合理 | 不要全刪重跑 | 在節點單檔標記TBD，回卡0補交接包 |
| D2發現幽靈節點 | 不要跳過不理 | 執行卡G依編碼核對報告修復 |
| D2完成後需求變更 | 不要直接改nodes | 執行卡E走CR模式 |
| 重構後連結壞掉 | 不要人工猜路徑 | 執行卡F讓Runner掃描並修復 |
| Runner跑到一半方向錯 | 輸入!!STOP暫停 | 確認狀態後輸入←BACK退回重跑 |

---

## 7. 語法速查表(Cheatsheet)

### TBD標記語法

```markdown
> [!TBD-XXX] 一句話描述待確認內容
> 🔒 解鎖條件：[需要回答什麼問題才能繼續]
> 🌊 下游影響：[未解鎖前阻塞哪些節點]
> 💡 預設假設：[AI在此假設下繼續推進]
```

### 跨模組W99引用(目標模組尚未建立時)

```markdown
> 🔒 解鎖條件：等待[目標M##-F##]功能模組實體初始化後，
>              將本連結變更為目標物理路徑。
```

### 雙向導覽連結格式(節點單檔頂端)

```markdown
> 🔗 雙向導覽
> 向上對齊：[F##_L4_UserStories.md](../F##_L4_UserStories.md)
> 流程定位：[F##_L3_Workflow.md](../F##_L3_Workflow.md)
> 模組狀態：[04_FuncMap.md](../../04_FuncMap.md)
```

### 全域DEC決策引用

```markdown
> 參照決策：[DEC-XXX] [決策內容摘要](詳見00_Glossary.md)
```

---

## 8. 誰可以改哪個檔案

| 角色 | 可以改的檔案 | 不能改的檔案 |
|------|------------|------------|
| SA | `00_Status.md`、`M##_overview.md`、`SYS##_overview.md`（系統邊界調整時）、節點單檔(D1.5期間)、`00_Glossary.md` | `04_FuncMap.md`(只能貼Runner建議)、`03_Structure.md`(改後必須同步) |
| Runner | `nodes/*.md`(D1/D2期間)、`F##_Review.md`、`03_Structure.md`、`SS##_overview.md`(D1/D2期間，新增M層時同步更新) | `00_Status.md`(只能輸出diff建議)、`M##_overview.md`、`SYS##_overview.md`(只能輸出建議片段) |
| Coach | 產出交接包與差異清單(Chat：Claude/Gemini) | 所有實體檔案(不直接操作檔案系統) |

**M##_boundary.md說明**：
由Runner在21_AddModule.md的M層引導流程中自動建立初稿，
SA填寫confirmed_by後即為確認版本。
SA確認後Runner嚴禁覆寫此文件。
此文件只記錄M層首次建立時的SA確認記錄，
不作為M層目前有效邊界的SSOT（SSOT在M##_overview.md）。

---

## 附錄：完整狀態字典

### 專案層狀態
| 狀態碼 | 🔴🟡🟢 | 顯示名稱 | 說明 |
|--------|--------|---------|------|
| NEEDS_CLARIFICATION | 🔴 | 需求待釐清 | 素材尚在概念討論階段 |
| HANDOFF_READY | 🟡 | 交接包可用 | R2已產出，可進D1 |
| PROJECT_INITIALIZED | 🟢 | 文件庫就緒 | DesignSpecs已建立 |
| CHANGE_REQUIRED | 🔴 | 變更待處理 | 已定稿後有新需求 |

### F模組層狀態
| 狀態碼 | 🔴🟡🟢 | 顯示名稱 | 說明 |
|--------|--------|---------|------|
| NOT_STARTED | 🟢 | 尚未建立 | F結構尚未初始化 |
| STRUCTURE_READY | 🟢 | 架構就緒 | F目錄已建立，等待D1 |
| GENERATING | 🟡 | AI產出中 | D1進行中，禁止碰觸檔案 |
| DRAFT_REVIEW | 🟡 | 草稿待審[D1.5] | D1完成，等待SA審閱 |
| REVIEW_BLOCKED | 🔴 | TBD阻塞中 | 有阻塞性TBD未解鎖 |
| READY_SYNC | 🟡 | 可同步[D2] | 審閱完成，可觸發D2 |
| SYNC_ISSUE | 🔴 | 核對失敗 | 編碼核對發現異常 |
| SYNC_DONE | 🟢 | 規格已收斂 | D2完成，規格定稿 |
| REFACTORING | 🟡 | 重構中 | 90_Restructure執行中 |
| ARCHIVED | 🟢 | 已歸檔 | 模組已下架 |

---

## 🔄 跨工具銜接：Chat指引模式

### 什麼是Chat指引模式

R2交接包完成後，Coach(Chat端AI)會切換為「流程指引模式」，
扮演流程導航員角色，引導SA與Code(Runner)之間的協作。

**角色分工：**
| 角色 | 工具 | 職責 |
|------|------|------|
| SA | 人類 | 業務決策、確認指引、把關品質 |
| Coach | Chat(Claude/Gemini等) | 流程導航、產生執行指令、檢查DoD |
| Runner | Code(Claude Code等) | 讀寫實體檔案、執行設定檔、產出DoD |

**核心原則：Coach導航、SA決策、Runner落檔。**

### 開啟新對話時的開場格式

每次開新Chat對話繼續工作時，使用以下格式讓Coach快速掌握脈絡：

```
這是MetaSA流程指引模式。

目前狀態：
- 焦點模組：[M##_名稱 / F##_名稱]
- 目前階段：[HANDOFF_READY / STRUCTURE_READY / DRAFT_REVIEW / READY_SYNC]
- 已完成：[R2 / 卡A / 卡B / D1 / D1.5 / D2]
- 接下來想做：[目標]

附上：
1. handoff.md摘要或R2交接包
2. 00_Status目前狀態
3. 本步驟需要的設定檔（見下表）
4. Code(Runner)最近輸出的DoD報告（若有）
```

**按需提供的設定檔：**
| 下一步 | 需要提供的設定檔 |
|--------|---------------|
| 初始化文件庫(卡A) | 20_Setup.md |
| 新增F模組(卡B) | 21_AddModule.md |
| 草稿生成(D1) | 30_DraftSync.md |
| 規格收斂(D2) | 30_DraftSync.md + DoD報告 |
| 需求變更(CR) | 10_ReqAnalysis.md + 既有規格 + `DesignSpecs/00_Glossary.md` 區塊B |
| 重構歸檔(卡F) | 90_Restructure.md |

> 不需要每次都提供全部六個設定檔。只提供當前步驟需要的那一份。

### Code(Runner)執行後的回報方式

Code(Runner)每次執行完成後，把DoD報告貼回Chat對話，
Coach會：
1. 確認DoD是否完整
2. 判斷下一步是否可前進
3. 產生下一個Code(Runner)執行指令

---

## Coach Chat 啟動教學

### 第一次開 Coach Chat(新案 onboarding 後 / 接手新代 Coach)

1. **開新 Chat**(Claude / GPT / Gemini 任一 Chat 介面)
2. **上傳以下三檔**:
   - `.metasa/COACH/CoachHandbook.md`
   - `00_START_SA/00_Status.md`
   - `00_START_SA/Guide.md`(本檔)
3. **貼上啟動 prompt**:
   - 新案首次:`你是 SA Coach,請依這套方法論引導我`
   - 接手新代:上代 Coach 結尾交接 Part 2 完整啟動 prompt
4. **送出後 Chat 成立**,將 Chat 命名為:
   `[專案簡稱]-Coach-第 N 代`
   - 專案簡稱從 `00_Status.md` 「Coach 接手清單」取
   - 代數從 `00_Status.md` 「Coach 第 N 代」欄位取(新案首次為 1)
5. Coach 自動讀完三檔,主動輸出開場回應(報狀態 + 建議下一步 + 請 SA 提供今天日期)
6. SA 提供今天日期 + 本輪意圖,推進開始

### 每次新 Chat 都要重新上傳檔案

不使用 Claude Projects / Gemini Gem 預載——預載機制版本失控風險高,改用 Chat 上傳每次拉最新版,維持 SSOT 純度。

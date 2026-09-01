---
file: 00_START_SA/AGENT_TASK_範本目錄大小寫.md
role: upstream_defect_report
status: DRAFT_待SA拍板
version: v0.1 (2026-09-01)
last_updated: 2026-09-01
changed_by: Runner
summary: 上游套件缺陷回報單——MetaOS SA_DEPLOY 鋪設的 _templates/ 目錄名為大寫 _Template,與其自身 KIT 全篇 18 處小寫引用及 20_Setup.md DoD 第 3/4/7/8 條驗收路徑不一致。本專案已於 2026-09-01 本地修正,本單用於回報上游避免下次部署回歸。屬 SA 內部工具,非交付物(AI_Rules §5 條 12)。
---
# 上游套件缺陷回報:`_templates/` 目錄名大小寫

> **狀態:草稿,待 SA 拍板後轉交上游套件維護方。** 本專案端已於 2026-09-01 自行修正並驗證通過,本單的目的是**讓上游在源頭修掉,避免下次部署回歸**。
>
> 落點依 `AI_Rules.md` §5 條 12:屬 SA 內部追蹤工具,非交付物,不入 `DesignSpecs/`。

---

## 給 SA 的說明(轉交前先看這段)

**這不是本專案手滑,是部署包自己內部不一致。**

追 git 確認:三個大寫目錄與整套 KIT 由**同一個 commit `53b7d22`「初始基線: MetaOS 部署架」**一起進來。也就是同一個部署包,發的 KIT 說小寫、發的目錄是大寫。

**部署來源**:`metaos-v0.12.0/SA_DEPLOY@v1.2`(來源 `8af140c`)

**為什麼要回報而不是只修本地**:本地改完,下次部署包再鋪一次還是會被打回大寫。這種錯在 Windows 上靜默通過、只在 Linux / CI 上炸,回歸了不容易第一時間發現。

**本專案已做的處置**(2026-09-01,不需上游動作):

| 動作 | 內容 |
|---|---|
| 改 3 個目錄名為小寫 | `F00_Template/` → `F00_template/`、`M00_Template/` → `M00_template/`、`SYS00_Template/` → `SYS00_template/` |
| 不動 KIT 任何字面值 | 18 處小寫引用全部保留原樣 |
| 驗證 | `20_Setup.md` DoD 第 3 / 4 / 7 / 8 條路徑檢查逐條通過;全庫無殘留大寫引用 |

**為什麼是改目錄不是改 KIT**:`20_Setup.md` 第 410~418 行的 DoD 驗收檢查**逐條寫小寫路徑**。也就是套件用來驗收自己的那把尺就是小寫 —— repo 現況跑不過套件自己的驗收。錯的是目錄名,不是 KIT。

**同時附帶一個職責疑點**(請上游一併確認):`20_Setup.md` 第 133 / 168 / 199 / 236 / 321 / 356 行是**「建立」範本檔的指令**,但部署包又預先鋪好了同一批範本。到底範本應由部署包鋪、還是由 `20_Setup.md` 執行時建?兩邊都做,才會出現「鋪的和寫的不一致而沒人發現」這種狀況。這是本缺陷的**根因**,只改大小寫治標不治本。

---

## 缺陷事實

**現象**:部署包鋪設的範本目錄名為 `*_Template/`(大寫 T),而套件內所有引用皆為 `*_template/`(小寫 t)。Windows / macOS 預設檔案系統不分大小寫故靜默通過,**Linux / CI 會 fail**。

**受影響的引用共 18 處,散在 4 個檔:**

| 檔案 | 處數 | 行號 | 觸發時機 |
|---|---|---|---|
| `.metasa/SA_KIT/20_Setup.md` | 12 | 133, 168, 199, 236, 321, 356, 410, 412, 413, 416, 417, 418 | 初始化 + **其自身 DoD 驗收** |
| `.metasa/SA_KIT/21_AddModule.md` | 4 | 40, 89, 158, 223 | 新增模組(建實體結構) |
| `.metasa/SA_KIT/30_DraftSync.md` | 1 | 14 | **D1 草稿生成強制讀黃金範例** |
| `00_START_SA/Playbook.md` | 1 | 78 | 卡 B 手動建 `M##_overview.md` |

> ⚠️ 影響面比初判廣:不只擋「建實體結構」,`30_DraftSync.md` 第 14 行的**強制讀取**會讓 D1 草稿生成也踩到。

**部署包鋪設的 3 個目錄 / 8 個檔案:**

```
DesignSpecs/_templates/F00_Template/     (5 檔:L4 / L3 / L2 + nodes/W03 + nodes/W99)
DesignSpecs/_templates/M00_Template/     (1 檔:M00_overview.md)
DesignSpecs/_templates/SYS00_Template/   (2 檔:SYS00_overview.md / SS00_overview.md)
```

---

## 派工單(以下整段轉交上游)

````markdown
# AGENT_TASK:修正 SA_DEPLOY 範本目錄名大小寫

**議題編號**:待上游編號(本專案端無權發號)
**來源**:樹碳集專案 SA(`rossi7966-ai/treetreelook-sa`)回報
**部署來源**:`metaos-v0.12.0/SA_DEPLOY@v1.2`(來源 `8af140c`)
**模式**:AGENT_TASK 模式(修復方向已確認,純執行)

## 背景

SA_DEPLOY 鋪設的範本目錄名為 `*_Template/`(大寫 T),但套件內 18 處引用皆為 `*_template/`(小寫 t),其中包含 `20_Setup.md` 自身的 DoD 驗收檢查。Windows / macOS 靜默通過,Linux / CI 會 fail。

## 目標

讓部署包鋪設的目錄名與套件引用一致,方向為**改目錄名為小寫**。

**判準**:`20_Setup.md` 第 410~418 行的 DoD 驗收檢查逐條寫小寫路徑 —— 套件驗收自己的尺就是小寫,故目錄名為偏離方。**嚴禁反向修改 18 處引用。**

## 目標檔案(完整路徑)

部署包內對應 `DesignSpecs/_templates/` 的來源目錄,三個:

| 現況 | 應改為 |
|---|---|
| `SYS00_Template/` | `SYS00_template/` |
| `M00_Template/` | `M00_template/` |
| `F00_Template/` | `F00_template/` |

## 允許修改範圍

**僅限上述三個目錄的目錄名**。目錄內 8 個檔案的**檔名與內容一律不動**。

## 禁止修改範圍

- ❌ `20_Setup.md` / `21_AddModule.md` / `30_DraftSync.md` / `Playbook.md` 的任何字面值(18 處引用全部保留小寫)
- ❌ 三個目錄內任何檔案的檔名或內容
- ❌ 任何 frontmatter 版次(本次無 KIT 檔案異動,**不需升版、不需砍合併補丁標注**)

## 執行方式

檔案系統不分大小寫者(Windows / macOS)必須走**兩步改名**,單步會被檔案系統吃掉:

```bash
cd <部署包>/DesignSpecs/_templates
for d in F00 M00 SYS00; do
  git mv "${d}_Template" "${d}_tmpren" && git mv "${d}_tmpren" "${d}_template"
done
```

## 預設決策規則

- 若目錄**已是小寫**:該項標「無需處理」,繼續下一項,不報錯。
- 若目錄**不存在**:停止,於 LOG 標 ⚠️ 並回報實際目錄清單 —— 代表部署包結構已與本回報不符,需重新確認。
- 若 `git mv` 因未追蹤而失敗:改用 `mv` 兩步,並於 LOG 標明該目錄未納入版控。

## 驗證指令(逐條執行並貼出輸出)

```bash
# 1. 三個目錄應全為小寫
ls DesignSpecs/_templates/

# 2. 全庫應無殘留大寫引用(預期:無輸出)
grep -rn "F00_Template\|M00_Template\|SYS00_Template" . --exclude-dir=.git

# 3. 20_Setup.md DoD 第 3/4/7/8 條路徑應全部存在(預期:8 行皆存在)
ls DesignSpecs/_templates/M00_template/M00_overview.md \
   DesignSpecs/_templates/F00_template/F00_L4_UserStories.md \
   DesignSpecs/_templates/F00_template/F00_L3_Workflow.md \
   DesignSpecs/_templates/F00_template/F00_L2_Routing.md \
   DesignSpecs/_templates/F00_template/nodes/M00-F00-W99_OutOfScope.md \
   DesignSpecs/_templates/F00_template/nodes/M00-F00-W03_申請權限.md \
   DesignSpecs/_templates/SYS00_template/SYS00_overview.md \
   DesignSpecs/_templates/SYS00_template/SS00_overview.md

# 4. 確認為改名而非刪除重建(預期:8 個 R 開頭,無 D / A)
git status --short
```

## 範圍邊界稽核(LOG 審閱時對比)

| 項目 | 預期值 |
|---|---|
| 目錄改名 | 3 |
| 檔案移動 | 8(git 應識別為 rename,非 delete + add) |
| 內容 insertions | **0** |
| 內容 deletions | **0** |
| KIT 檔案異動 | **0** |
| frontmatter 升版 | **0** |

**任一項不符即為越界,停止並於 LOG 標 ⚠️。**

## 附帶請上游確認(不在本次執行範圍)

`20_Setup.md` 第 133 / 168 / 199 / 236 / 321 / 356 行是**「建立範本檔」的指令**,但部署包又預先鋪好同一批範本。範本應由部署包鋪、還是由 `20_Setup.md` 執行時建?

兩邊都做正是本缺陷的**根因** —— 鋪的和寫的不一致而沒有任何一方負責核對。只改大小寫是治標。請上游決定單一責任歸屬後另開議題。

## 輸出要求

完成後輸出 AGENT_LOG,**整段以四個反引號包覆**,內含:

1. 每條驗證指令的實際輸出
2. `git status --short` 的完整結果
3. `files changed, insertions, deletions` 數字
4. 任何 ⚠️ 區與其判讀
````

---

## 本專案端的回歸監測

在上游修好之前,**每次重新部署 SA_DEPLOY 後**須複跑:

```bash
ls DesignSpecs/_templates/
grep -rn "F00_Template\|M00_Template\|SYS00_Template" .metasa/ 00_START_SA/
```

第一條應為三個全小寫目錄,第二條應無輸出。此監測點已登記於 `00_START_SA/Roadmap.md` §5 R2。

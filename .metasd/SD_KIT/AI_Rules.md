---
file: .metasd/SD_KIT/AI_Rules.md
role: sd_ai_rules
info_level: Candidate
origin: PREP-SD 前置準備產出(PREP-SD-2)
version: v0.2
last_updated: 2026-08-14
summary: SD側AI(Coach/Runner)在專案repo的行為守則。邊界、規則優先序(三層,棕地慣例延續)、產製紀律、檢核紀律、決策紀律、停止條件。
---

# SD AI 行為守則

## 身份

你是專案repo內的SD側AI:Coach(Chat介面,引導拍板者)或Runner(Coding Session,讀寫實體檔案)。生成鏈(字典→DDL/ERD/OAS schemas→規格卡;OAS paths=行為源)是你的工作骨架,SOP見SD_KIT 10~90。

## 讀寫邊界

- **可寫**:`DesignContracts/`全目錄、`00_START_SD/00_Status.md`
- **唯讀**:`DesignSpecs/`一切(SA職權)、`ui/`與`UIFoundation/`(MetaUI職權)——發現上游問題走先修後報,不修上游檔
- **禁手改生成物**:DDL、規格卡、`.profile.md`、全域ERD、OAS的schemas生成段——由腳本/生成流程產出,手改即違規(freshness檢核會抓)

## 規則優先序(三層)

> 白話:在既有系統上工作,最好的規矩就是它自己的規矩。工具配合系統,不是系統配合工具。

| 層 | 內容 | 既有系統擴建(棕地) | 新系統(綠地) |
|----|------|-------------------|--------------|
| 風格層 | 命名、主鍵、時間欄、路徑、認證位置、錯誤與分頁形…(DbStyleRule/ApiStyleRule條文) | **延續既有系統慣例**,以`DesignContracts/00_ProjectConvention.md`(專案慣例檔)為準;既有系統沒有慣例的空白處,才用家規預設值補位 | 家規預設值 |
| 結構品質層 | 正規化、型別選擇、約束、多值拆表…(DesignDecisionRule決策卡) | 決策卡個案判;既有做法是證據,不自動勝出 | 決策卡 |
| 陷阱底線層 | 憑證字面入檔、代碼同碼不同義擴散、未經變更程序破壞已頒行契約 | **不延續**;要延續須決策卡顯性拍板 | 同左 |

- 開案第一張卡=DP-SD-001系統邊界判定(擴建或新系統),結果寫入專案慣例檔檔頭。
- 「延續」必須落檔:慣例檔每一格附依據(既有文件何處/DB實測),不憑印象;可由introspect對既有DB統計起草,人確認後定案。
- 慣例檔未填妥前,風格層檢核一律出needs-review不出fail(不在盤點完成前咬人)。

## 產製紀律

1. **字典先行**:欄位先入`00_DataDictionary/`才可入DDL/OAS;改欄位回字典改,再讓下游再生
2. **SSOT不重複**:同一事實只在權威載體拍板(對照B §1.2宣告表);UI綁定表欄位一律`$ref`回OAS,禁抄型別
3. **缺口有戶口**:「待補」「缺少API」字面禁用;一律登`90_GapRegister.md`(GAP-###+解鎖條件)
4. **override必登記**:上游缺陷本地先修者,登`HandoffManifest.md`LocalOverrides表;禁隱形修正
5. **sentinel不外洩**:特殊碼在`01_DataSemantics/`洗成null+quality_flag;禁入schema/OAS範例
6. **曆制**:存儲與API一律ISO;民國年僅顯示層
7. **擬真資料**:範例用貼近領域的擬真資料,不用lorem ipsum(對齊MetaUI慣例)

## 檢核紀律

- 產出後跑`python .metasd/scripts/<check>.py`(腳本就位前,依規則檔逐條人工核,結果仍分fail/needs-review兩列呈報)
- 報告貼**真實stdout原文**,不轉述不美化;fail不辯解:能修即修,不能修登GapRegister
- 檢核判定**零LLM**;語意疑義列needs-review留人判

## 決策紀律

- 遇多解決策先查`DesignDecisionRule.md`:有卡照卡走(預設解或觸發改道);偏離預設→登ADR(`.issues/I-SD-###/ADR-N.md`體例)
- 卡上升級條件命中→產「請示卡」給拍板者:附選項+各自後果,不丟開放題
- 無卡的新決策點→先提決策卡草案再執行

## 停止條件

- SSOT衝突(兩處各自宣稱同一事實)→停,先裁權威
- 規格輸入缺席(缺字典/缺SA節點)→以parse-error呈報,不硬猜
- 涉SA/UI檔修改需求→僅登錄轉介(先修後報),SA pass管道處理
- 決策卡升級條件命中而拍板者未回→該線暫停,轉做不依賴該決策的工作

---
feature_id: M07-F01
feature_name: 稽核紀錄
parent_module: M07_系統維運
status: S1_DRAFT
parent_system: SYS01
parent_subsystem: SS01
version: v1.1 (2026-09-15)
---
# F01 UserStory清單

> 🗺️ 流程定位:[查看L3 Workflow拓樸圖](./F01_L3_Workflow.md) ｜ 決策脈絡:`00_Glossary.md` DEC-013 / DEC-014 / DEC-015 ｜ 交接包:`06_HandoffPackage.md` §9

## Epic清單
### EP12_系統維運與稽核(M07-F01 稽核紀錄段)
- [M07-F01-US01] As a 系統管理員(Role 2), I want 系統自動記下每位使用者何時進入、切換、離開本組織, so that 發生權限或資料爭議時能確認當時是誰在組織內操作. *(P1)* → [M07-F01-W01](./nodes/M07-F01-W01_記錄進出組織事件.md)
- [M07-F01-US02] As a 系統管理員(Role 2), I want 系統自動記下各模組每一次新增、查詢、修改、刪除, so that 資料或權限被改動時能追到是誰、改了什麼、改之前是什麼. *(P1)* → [M07-F01-W02](./nodes/M07-F01-W02_記錄模組操作事件.md)
- [M07-F01-US03] As a 系統管理員(Role 2), I want 依日期、姓名、事件、系統端篩選本組織的進出紀錄, so that 能確認某段時間內誰進出過本組織. *(P1)* → [M07-F01-W03](./nodes/M07-F01-W03_查詢登入登出紀錄.md)
- [M07-F01-US04] As a 系統管理員(Role 2), I want 依模組頁籤、日期、動作、操作者、操作對象篩選本組織的操作紀錄, so that 能快速找到某筆資料或某個權限被誰改動. *(P1)* → [M07-F01-W04](./nodes/M07-F01-W04_查詢操作紀錄.md)
- [M07-F01-US05] As a 系統管理員(Role 2), I want 打開單筆紀錄看到完整時間、帳號、角色、IP、裝置與異動內容, so that 能判斷該操作是否合理並作為佐證. *(P1)* → [M07-F01-W05](./nodes/M07-F01-W05_檢視紀錄詳情.md)
- [M07-F01-US06] As a 系統管理員(Role 2), I want 將目前篩選結果匯出為檔案, so that 能提交給業主或主管機關作為稽核佐證. *(P1)* → [M07-F01-W06](./nodes/M07-F01-W06_匯出稽核紀錄.md)

## 範圍外(本 F 不處理)
- 帳號驗證層事件(登入成功 / 失敗、帳號不存在)的查看:歸 SYS02-SS03(DEC-014),見 [M07-F01-W99](./nodes/M07-F01-W99_OutOfScope.md)。
- 系統設定、自訂規則的變更紀錄呈現方式:待 M07-F02 / F03 展開時一併檢視。

---
table_name: TBL00_TEMPLATE
module_prefix: <!-- SYS_/AUTH_/CODE_/LOG_/[BIZ]_ -->
status: TEMPLATE_EMPTY
origin: <!-- authored | reverse_engineered | spreadsheet_import -->
derived: false
regen_rule: null   # derived=true時必填:來源表+聚合/投影邏輯
source_sheet: null # 試算表來源(sheet名/分頁),spreadsheet_import時必填
version: v0.1 (YYYY-MM-DD)
last_updated: YYYY-MM-DD
---
# <TABLE_NAME> 資料字典

> 一句話說明這張表是什麼。
> 機檢:欄名lower_snake(R-DB-N02)/保留字(R-DB-R01)/邏輯型別白名單(R-DB-T01)/FK目標存在/代碼表type存在。

## 欄位表

| 欄名 | 邏輯型別 | 長度精度 | nullable | default | PK | FK目標 | 代碼表type | 單位 | quality_flag | 白話說明 | source_column |
|------|---------|---------|----------|---------|----|--------|-----------|------|--------------|---------|---------------|
| sid | int | - | N | identity | Y | - | - | - | - | 主鍵 | - |
| <!-- 業務欄位… --> | | | | | | | | | | | |
| create_time | datetime | - | N | now() | - | - | - | - | - | 建立時間 | - |
| edit_time | datetime | - | Y | - | - | - | - | - | - | 異動時間 | - |
| create_user_id | int | - | N | - | - | SYS_USER_INFO | - | - | - | 建立者 | - |
| edit_user_id | int | - | Y | - | - | SYS_USER_INFO | - | - | - | 異動者 | - |

## 備註

<!-- 索引建議、關聯說明、derived再生規則細節 -->

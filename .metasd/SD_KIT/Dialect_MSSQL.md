---
file: .metasd/SD_KIT/Dialect_MSSQL.md
role: db_dialect_overlay_mssql
info_level: Candidate
origin: PREP-SD 前置準備產出(PREP-SD-2)
version: v0.2
last_updated: 2026-08-14
summary: MSSQL方言overlay——只載與DbStyleRule核心的差異:邏輯型別對映(含ascii窄型別分流)、語法差異、方言禁令。機檢:對映表必須覆蓋核心宣告的全部邏輯型別。
---

# Dialect_MSSQL(overlay,只載差異)

## 一、邏輯型別對映(必須完整覆蓋R-DB-T01白名單)

| 邏輯型別 | MSSQL實型 | 備註 |
|---------|-----------|------|
| text | nvarchar(max) | 中文一律n系列 |
| varchar(n) | nvarchar(n);字典標`ascii: true`者→varchar(n),固定長度代碼→char(n) | 純代碼/ASCII欄走窄型別(R-DB-T04) |
| int | int | |
| bigint | bigint | |
| decimal(p,s) | decimal(p,s) | |
| bool | bit | |
| datetime | datetime2 | 禁datetime(舊型別精度低) |
| date | date | |
| time | time | |
| uuid | uniqueidentifier | |
| json | nvarchar(max) + `CHECK(ISJSON(欄)=1)` | |

## 二、語法差異

| 語意 | MSSQL寫法 |
|------|-----------|
| identity主鍵 | `sid int IDENTITY(1,1) PRIMARY KEY` |
| now()預設 | `GETDATE()`(相容Guide既有);datetime2高精度場景可用`SYSDATETIME()` |
| uuid預設 | `NEWID()` |
| 分頁 | `OFFSET n ROWS FETCH NEXT m ROWS ONLY`(禁裸TOP做分頁) |
| 布林字面 | 1/0 |

## 三、方言注意與禁令

- **定序collation**:中文環境定序必須於EnvBaseline明文(如Chinese_Taiwan_Stroke_CI_AS);DDL生成引用之,禁隱含依賴伺服器預設。
- 禁舊型別:text/ntext/image/datetime/smalldatetime。
- 時區:datetime2不帶時區——儲存時區策略(UTC或UTC+8)必須於EnvBaseline明文,API層一律帶偏移量輸出(+08:00)。

---
file: .metasd/SD_KIT/Dialect_PostgreSQL.md
role: db_dialect_overlay_postgresql
info_level: Candidate
origin: PREP-SD 前置準備產出(PREP-SD-2)
version: v0.1
last_updated: 2026-07-07
summary: PostgreSQL方言overlay——只載差異:邏輯型別對映、語法差異、方言禁令。機檢:對映表必須覆蓋核心宣告的全部邏輯型別。
---

# Dialect_PostgreSQL(overlay,只載差異)

## 一、邏輯型別對映(必須完整覆蓋R-DB-T01白名單)

| 邏輯型別 | PostgreSQL實型 | 備註 |
|---------|----------------|------|
| text | text | |
| varchar(n) | varchar(n) | |
| int | integer | |
| bigint | bigint | |
| decimal(p,s) | numeric(p,s) | |
| bool | boolean | |
| datetime | timestamptz | 預設帶時區;若EnvBaseline宣告「無時區策略」改timestamp並明文理由 |
| date | date | |
| time | time | |
| uuid | uuid | |
| json | jsonb | 禁json型(查詢效率),一律jsonb |

## 二、語法差異

| 語意 | PostgreSQL寫法 |
|------|----------------|
| identity主鍵 | `sid int GENERATED ALWAYS AS IDENTITY PRIMARY KEY`(**禁serial**) |
| now()預設 | `now()` |
| uuid預設 | `gen_random_uuid()`(pgcrypto/內建13+) |
| 分頁 | `LIMIT m OFFSET n` |
| 布林字面 | true/false |

## 三、方言注意與禁令

- 識別字預設小寫:表名UPPER_SNAKE在PG中以雙引號建立保持大寫,或於EnvBaseline宣告「PG側表名折疊小寫」策略——**二擇一必須明文**(預設:雙引號保持,與MSSQL字面一致,利跨方言對齊檢核)。
- 時區:timestamptz儲存UTC、輸出依連線時區——與MSSQL策略的對齊由EnvBaseline統一宣告。
- 禁serial(改identity);禁money型(用numeric)。

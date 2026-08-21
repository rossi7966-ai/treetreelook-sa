---
file: .metasd/SD_KIT/DbApiConvRule.md
role: db_api_conversion_rule
info_level: Candidate
origin: PREP-SD 前置準備產出(PREP-SD-2)
version: v0.1
last_updated: 2026-07-07
summary: DB↔API確定性轉換規則——命名轉換演算法(round-trip恆等)、型別對映四欄表、曆制條款。零判斷、純查表,生成器與檢核腳本共用此檔為唯一依據。
---

# DbApiConvRule(確定性轉換)

> 白話:DB的名字跟型別怎麼「機械地」變成API的名字跟型別,反向亦然。本檔是查表,不是指引——查不到就是缺,補表,不現場發明。

## 一、命名轉換

### 演算法(lower_snake_case → camelCase)

1. 以`_`切段;首段全小寫;其後每段首字母大寫、餘字母小寫。
2. **縮寫詞不例外**:一律「僅首字母大寫」(station_id→stationId、api_url→apiUrl、ip_address→ipAddress)——保證可逆。
3. 反向(camelCase→snake):每個大寫字母前插`_`後轉小寫。

### 恆等條款

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-CONV-01 | round-trip恆等:snake→camel→snake必須還原;不可逆的欄名禁用(如連續數字緊鄰底線的歧義樣式`addr_2_line`) | hard | `check_naming.py`往返測試 |
| R-CONV-02 | 轉換例外(轉不動/歷史包袱)登記於下方例外表,生成器只認表 | hard | 例外表比對 |

### 例外登記表

| DB欄名 | API欄名 | 理由 | 登記日 |
|--------|---------|------|--------|
| (空——例外發生時登記) | | | |

## 二、型別對映(四欄表)

| 邏輯型別 | MSSQL | PostgreSQL | JSON/OAS |
|---------|-------|------------|----------|
| text | nvarchar(max) | text | string |
| varchar(n) | nvarchar(n) | varchar(n) | string, maxLength: n |
| int | int | integer | integer, format: int32 |
| bigint | bigint | bigint | integer, format: int64 |
| decimal(p,s) | decimal(p,s) | numeric(p,s) | number(文件標精度;金流場景的string承載議題見DP-API-005) |
| bool | bit | boolean | boolean |
| datetime | datetime2 | timestamptz | string, format: date-time(輸出一律帶+08:00偏移或Z,依EnvBaseline) |
| date | date | date | string, format: date |
| time | time | time | string, format: time |
| uuid | uniqueidentifier | uuid | string, format: uuid |
| json | nvarchar(max)+ISJSON | jsonb | object(schema於字典attribute宣告) |

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-CONV-03 | OAS schemas的型別**只准**由本表推導;手寫型別=違規(反例:農氣宣告與範例矛盾,C表§三) | hard | `check_alignment.py` |

## 三、曆制條款

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-CONV-04 | 存儲與API一律ISO(date/date-time);**民國年字面(YYY/MM/DD、1140501)禁入DB與API** | hard | 值樣式掃描 |
| R-CONV-05 | 民國年業務欄(roc_year int)須在字典標`calendar: roc`+換算式(西元=roc+1911);顯示層轉換歸UI | hard | 字典欄檢查 |

---
scenario: <!-- 應用情境名(業務語言),如:災害應變 -->
source_epics: []   # 輔助索引:EP##
entities: []       # 本情境引用的字典表清單
status: TEMPLATE_EMPTY
version: v0.1 (YYYY-MM-DD)
last_updated: YYYY-MM-DD
---
# 情境ER:<情境名>

> 鐵律:本圖只裁切、不添事實——圖中實體與關聯必存在於`00_DataDictionary/`與全域ERD(機檢=yes)。
> 讀者:SA/業主/PG溝通用;施工看全域ERD。

## 關聯強調(白話一段)

<!-- 本情境下哪幾張表如何協作、關鍵關聯是哪條 -->

## ER圖

```mermaid
erDiagram
  TABLE_A ||--o{ TABLE_B : "關聯語意"
```

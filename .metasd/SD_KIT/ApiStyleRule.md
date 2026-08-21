---
file: .metasd/SD_KIT/ApiStyleRule.md
role: api_style_rule
info_level: Candidate
origin: PREP-SD 前置準備產出(PREP-SD-2)
version: v0.2
last_updated: 2026-08-14
summary: API設計家規八節——資源命名、工作流端點、錯誤envelope、分頁、代碼表供應鏈、enum跨層、認證、長任務。條文值=綠地預設值,棕地以專案慣例檔本案值為準;同碼不同義屬底線不延續。
---

# ApiStyleRule

> 白話:API怎麼命名、怎麼回錯誤、怎麼分頁的家規。反例證據指向`_staging/prep_sd_1_out/C_MaterialMapping.md`。
>
> **本案值優先**:本檔各條文的值=綠地預設值。專案屬既有系統擴建時(DP-SD-001判定),風格類條文(命名/認證位置/錯誤形/分頁形等)以`DesignContracts/00_ProjectConvention.md`登記的本案值為準;本檔只在慣例檔空白處補位。注意:R-API-C01「同碼不同義」屬陷阱底線層,不隨慣例延續。

## 一、資源命名

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-API-N01 | 路徑全小寫;資源名複數;多字kebab-case(`/api/v1/station-records`) | hard | 路徑lint |
| R-API-N02 | 同一資源家族禁混用大小寫與單複數(反例:農氣StationList vs station/all;台電api/Codes vs codes vs Code) | hard | 路徑lint |
| R-API-N03 | 版次入路徑(`/api/v1/`) | hard | 路徑lint |
| R-API-N04 | 路徑書寫零容錯:禁雙斜線、禁缺前綴、禁相對路徑字面(台電GET//api、GETapi、./api全譜反例) | hard | 路徑lint |

## 二、工作流端點語意

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-API-W01 | 狀態動作統一`POST /{resources}/{id}/actions/{verb}`(submit/approve/reject/withdraw…);動詞清單掛代碼表。式樣替代案見DP-API-004 | soft(依卡) | OAS路徑樣式 |
| R-API-W02 | 審核鏈狀態機必落UI綁定表/行為書並與OAS動作一一對應(台電p141狀態機為正例結構) | soft | 對映存在性 |

## 三、錯誤envelope

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-API-E01 | 統一錯誤結構`{code(機器碼string), message(人讀), details[], traceId}`;400含欄位級details | hard | OAS共用schema引用 |
| R-API-E02 | HTTP狀態對映表:400參數/401未認證/403無權限/404不存在/409衝突/422語意錯/429限流/500系統(對齊農氣表1的401/403/429/400實務) | hard | OAS responses檢查 |
| R-API-E03 | 錯誤code值掛代碼表,禁自由字串 | soft | 代碼表ref |

## 四、分頁

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-API-P01 | 清單端點一律`limit/offset`參數+回應`meta{total,limit,offset}` | hard | OAS參數檢查 |
| R-API-P02 | limit預設值與上限必須宣告(預設20/上限100起手,專案可調) | soft | OAS檢查 |
| R-API-P03 | cursor分頁屬偏離,依DP-API-002 | 依卡 | — |

## 五、代碼表供應鏈

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-API-C01 | 一源三投影:DB `CODE_`表↔`GET /api/v1/codes/{type}`單一端點家族↔前端選單;禁各端點私定代碼(反例:農氣同碼異義1=風向/1=日最高溫) | hard | codes端點唯一性 |
| R-API-C02 | 代碼值=string(穩定識別);附name/sort/is_active;擴充屬性走attribute結構欄(吸收台電sys_code attribute JSON,schema登記於字典) | hard | 型別檢查 |
| R-API-C03 | 代碼異動走字典→CODE_表,禁API側hardcode | soft | — |

## 六、enum跨層策略

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-API-EN01 | **禁中文字面當enum值**(反例:dataSource="初始資料"、regions=["全台"]);API傳code,顯示名分離 | hard | enum值regex |
| R-API-EN02 | 每個enum必掛代碼表或OAS enum宣告,三層對映(DB碼/API碼/顯示名)登記於字典 | hard | 對映存在性 |
| R-API-EN03 | 禁一欄打包雙語值(反例:windDirection="東南,SE") | hard | 值樣式掃描 |

## 七、認證擺放

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-API-A01 | `Authorization: Bearer <token>` header;OAS securitySchemes統一宣告 | hard | OAS檢查 |
| R-API-A02 | **禁token入query string**(含文件範例)(反例:農氣全書`?token=`) | hard | `?token=`字面掃描 |
| R-API-A03 | 權限模型引用AUTH五表種子;禁magic number判權(反例:台電department=5451001) | soft | — |

## 八、長任務與大結果集

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-API-L01 | 處理時間長/結果大者採「受理+取件」模式:回`202`+取件連結+保留期限(吸收農氣Download/{id}正例);同步閾值見DP-API-003 | advisory(依卡) | — |
| R-API-L02 | 匯出類端點(`?format=xlsx`)回連結不回串流大檔 | advisory | — |

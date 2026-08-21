---
file: .metasd/SD_KIT/DbStyleRule.md
role: db_style_rule_core
info_level: Candidate
origin: PREP-SD 前置準備產出(PREP-SD-2)
version: v0.3
last_updated: 2026-08-14
summary: DB設計家規(方言無關核心)。條文=ID+enforcement(hard/soft/advisory)+機檢方式+理由指針;條文值=綠地預設值,棕地以專案慣例檔本案值為準。方言差異落Dialect overlay。
---

# DbStyleRule(S類方言無關核心)

> 白話:資料庫怎麼命名、怎麼開欄位的家規。hard=檢核腳本擋下;soft=警告放行;advisory=建議。「理由」欄指向`_staging/prep_sd_1_out/C_MaterialMapping.md`證據。
>
> **本案值優先**:本檔各條文的值=綠地預設值。專案屬既有系統擴建時(DP-SD-001判定),風格類條文以`DesignContracts/00_ProjectConvention.md`登記的本案值為準,檢核腳本讀該檔參數;本檔只在慣例檔空白處補位。三層劃分見AI_Rules「規則優先序」。

## 一、命名

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-DB-N01 | 表名=UPPER_SNAKE_CASE+模組前綴(`SYS_`/`AUTH_`/`CODE_`/`LOG_`/`VIEW_`/`[BIZ]_`3-4碼);附件表後綴`_FILES`;資料庫名稱全大寫 | hard | regex+前綴清單 |
| R-DB-N02 | 欄位名=lower_snake_case | hard | regex |
| R-DB-N03 | 布林欄位`is_`前綴被動語態(is_active/is_closed) | hard | regex |
| R-DB-N04 | 多語系採後綴法(name_zh/name_en/description_zh) | advisory | — |
| R-DB-N05 | 度量單位後綴於欄名(area_ha/weight_kg);民國年欄`roc_year`必標`calendar: roc`(見DbApiConvRule §三) | soft | 字典單位欄非空 |

## 二、保留字

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-DB-R01 | 表名與欄位名禁用雙方言保留字聯集(ORDER/CLASS/USER/GROUP/TYPE/KEY/INDEX/DESC/CHECK…完整清單維護於`check_naming.py`) | hard | 清單比對 |
| R-DB-R02 | 近保留字(name/path/status/value)允許但列needs-review提醒 | advisory | 清單比對 |

理由:Guide範本自身§5含`order`欄(收編改`sort_order`);csvToMSSQL實踩ORDER(C表§一/§二)。

## 三、主鍵與外鍵

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-DB-K01 | 主鍵統一`sid`(int identity;方言實作見overlay) | hard | 字典PK欄檢查 |
| R-DB-K02 | `uuid`欄僅主業務表且會外顯(URL/API查詢、外部連結、安全隔離)時加;代碼表/關聯表/日誌表/同步暫存表預設不建(全卡DP-DB-002) | soft | 字典uuid欄+表類別比對 |
| R-DB-K03 | FK命名=`<目標表名小寫>_id`(auth_group_id) | hard | regex+FK目標存在 |
| R-DB-K04 | 識別碼由server端生成;禁client端「取最大值+1」造號 | advisory | — (理由:台電p261) |

## 四、型別基準

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-DB-T01 | 字典只准邏輯型別:`text/varchar(n)/int/bigint/decimal(p,s)/bool/datetime/date/time/uuid/json`;方言實型由overlay對映 | hard | 型別白名單 |
| R-DB-T02 | 金額/面積等精密數值必用decimal(p,s),禁float | hard | 型別檢查 |
| R-DB-T03 | 日期時間存ISO語意;禁以字串欄存日期 | hard | 型別檢查 |
| R-DB-T04 | 純代碼/ASCII欄位(code/account/email/ip/url/token/hash/external_*_id等)於字典標`ascii: true`,由overlay對映窄字元型別;可能存中文才用寬字元 | soft | 欄名清單heuristic→needs-review |

## 五、預設值與稽核欄位

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-DB-D01 | 顯性預設:int=0(必填FK除外)/bool=0/decimal=0.00 | soft | 字典default欄 |
| R-DB-A01 | 全表標配稽核欄:create_time/edit_time(datetime,now()語意預設)+create_user_id/edit_user_id(FK→SYS_USER_INFO.sid) | hard | 欄位存在性 |
| R-DB-A02 | 軟刪除採`delete_time`(null=未刪) | soft | — |

## 六、狀態與代碼欄

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-DB-S01 | 狀態/分類欄一律掛代碼表(`CODE_`供應鏈,見ApiStyleRule §五);欄位型別與起值**依DP-DB-005決策卡**,本檔不硬拍 | 依卡 | 字典代碼表ref非空 |
| R-DB-S02 | 同語意狀態欄跨表同名(禁stage/statusType/condition異名同義並存) | soft | 字典正名比對(理由:台電C表§四) |

## 七、結構模式

| ID | 條文 | enforcement | 機檢 |
|----|------|-------------|------|
| R-DB-P01 | 附件表`[MODULE]_FILES`模式(sid/fk_id/type/name/path/sort_order+稽核欄);polymorphic fk_id的完整性代價**依DP-DB-004** | 依卡 | — |
| R-DB-P02 | 權限五表種子(AUTH_ROLE/AUTH_GROUP/AUTH_GROUP_USER/SYS_FUNCTION/AUTH_RIGHTS)為預設起點;衝突解決採聯集+最小權限(Guide §2.2) | advisory | — |
| R-DB-P03 | 反正規化寬表/彙總表=字典標`derived: true`+再生規則;禁直寫、禁成第二事實源(DP-DB-001) | hard | 字典derived欄+regen_rule必填 |
| R-DB-P04 | 多值禁以分隔符打包單欄;確需打包=登記為derived/multivalue例外 | soft | (理由:csvToMSSQL L236-244) |

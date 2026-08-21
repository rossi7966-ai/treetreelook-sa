---
dataset: DS00_Template
status: TEMPLATE_EMPTY
profile_ref: null  # 對應<資料集>.profile.md,特殊碼對照憑實測不憑印象
version: v0.1 (YYYY-MM-DD)
last_updated: YYYY-MM-DD
---
# <資料集名> 資料語意載體

## 一、來源
- 來源系統/介接方式:
- 供應頻率:
- 涵蓋範圍:

## 二、更新機制
<!-- 資料分級(如:初始/校正/最終)與各級更新節奏;吸收農氣三級資料源範式 -->

## 三、換算邏輯
<!-- 公式字面,如:風速=√(U²+V²)四捨五入至小數1位 -->

## 四、特殊碼對照表(sentinel→正規化)

| 原始碼 | 語意 | 處置 | quality_flag |
|--------|------|------|--------------|
| <!-- -999 --> | 缺值 | →null | missing |
| <!-- -9.8 --> | 雨跡(有語意觀測) | 保值 | trace |

> 旗標詞彙表(初版):missing / instrument_fault / accumulating / no_obs / trace / calm / indeterminate。
> 鐵律:sentinel字面不外洩至schema/OAS範例(check_semantics.py)。

## 五、有效位數與單位

| 欄位/參數 | 單位 | 有效位數 |
|-----------|------|---------|

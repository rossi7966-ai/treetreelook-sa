---
job_id: JOB00_Template
job_type: <!-- etl | batch | report | notify -->
status: TEMPLATE_EMPTY
version: v0.1 (YYYY-MM-DD)
last_updated: YYYY-MM-DD
---
# 作業規格:<作業名>

## 一、目的與範圍
<!-- 一句話:這支作業把什麼變成什麼 -->

## 二、輸入/輸出
- 輸入:<!-- 來源檔pattern或來源表;引用.profile.md與語意載體 -->
- 輸出:<!-- 目標表(引用字典)/檔案/通知 -->

## 三、觸發與依賴
- 觸發:<!-- cron字面 | 事件 | 手動 -->
- 上游依賴:<!-- 前置作業job_id -->
- 下游消費:<!-- 誰吃輸出 -->

## 四、冪等聲明
<!-- 重跑N次結果一致的機制:staging表+交易+merge鍵 -->

## 五、失敗處置
- 重試:<!-- N次/間隔 -->
- 告警:<!-- 通知對象與方式 -->

## 六、etl型五紀律checklist(job_type=etl必填)
- [ ] schema-first:啟動驗證目標表存在且結構=DDL,永不建表
- [ ] 冪等:staging+交易+merge
- [ ] 設定憑證分離(見.config.yaml,env變數名)
- [ ] 結構化日誌(JSONL:ts/level/step/rows_in/rows_out/error)
- [ ] 雙方言連線層(driver依config.dialect)

## 七、欄位對映
> rename map由字典`source_column`欄生成,禁手寫(R:csvToMSSQL病灶)。
<!-- 特殊轉換(代碼轉換/固定值/例外處置)列此,對齊台電遷移範式 -->

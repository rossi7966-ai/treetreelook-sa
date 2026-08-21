---
file: DesignContracts/08_EnvBaseline.md
role: environment_baseline
status: TEMPLATE_EMPTY
version: v0.1 (YYYY-MM-DD)
last_updated: YYYY-MM-DD
---
# 環境基線(EnvBaseline)

> 收「環境規格」、不收「部署執行」(CI/CD/容器/IaC歸PG,見FolderOwnership §三)。
> collation入DDL生成參數、base URL入OAS servers——引用一致性受檢核。

| 屬性 | dev | stage | prod |
|------|-----|-------|------|
| DB方言 | <!-- mssql/postgresql --> | | |
| DB版本 | | | |
| collation定序 | <!-- 如Chinese_Taiwan_Stroke_CI_AS --> | | |
| 時區策略 | <!-- 儲存UTC或UTC+8,全環境一致 --> | | |
| 編碼 | UTF-8 | | |
| database/schema分配 | | | |
| 連線樣式 | <!-- env變數名,禁字面憑證 --> | | |
| API base URL | | | |
| 憑證管理方式 | | | |

---
file: DesignSpecs/UIFoundation/90_IssueLedger.md
role: ui_issue_ledger
status: TEMPLATE_EMPTY
version: v0.1 (YYYY-MM-DD)
last_updated: YYYY-MM-DD
summary: 設計議題唯一現況帳。UIX-### 終身編號;狀態四態(識別/排序/處理/結案);與審查報告雙向同步(UIV-07 驗)。
---
# 設計議題帳

> 唯一可變狀態載體:「現在還有什麼沒修」只看這裡。報告是不可變存證,不回改。
> 結案不自證:需下一輪對應閘門 V 重跑通過或 R 覆核。

| UIX-### | 狀態 | 嚴重度 | 歸屬 | 來源報告 | 可攔截閘門 | 處理 commit | 備註 |
|---------|------|--------|------|---------|-----------|------------|------|
| UIX-001 | 識別 | 🔴 | ⟪F##/P##/全域⟫ | R01_G1 | G0 | - | ⟪⟫ |

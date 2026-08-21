---
file: DesignSpecs/04_FuncMap.md
role: global_funcmap
status: TEMPLATE_EMPTY
version: v0.1 (YYYY-MM-DD)
last_updated: YYYY-MM-DD
summary: 全域功能架構圖——畫到 F 功能模組層,W## 不入本圖。
---
# 全域功能架構圖

> 本圖由30_DraftSync.md Phase 2逐步累積生成，嚴禁跳過Phase 2直接編輯。
> 層級限制：本圖畫到F功能模組層，嚴禁將W##操作節點加入本圖。
> 結構順序：SYS## > SS##(選用) > M## > F##
> W##節點的拓樸由各F模組的F##_L3_Workflow.md承擔。
> SA從本圖點擊F模組連結，跳轉至對應的F##_L3_Workflow.md查看詳細流程。

## 拆分觸發條件
- 單一M層F模組數量 > 5→ ⚠️建議評估M層拆分
- 單一F模組Epic數量 > 3→ ⚠️建議評估F模組拆分
- 同一F模組含不同RBAC角色的業務閉環 → ⚠️強制觸發拆分評估
- 單一F模組W##節點數量 > 15→ ⚠️建議評估Epic細分

## 功能樹
```mermaid
flowchart TB
  SYS_ROOT["核心系統名"]
```

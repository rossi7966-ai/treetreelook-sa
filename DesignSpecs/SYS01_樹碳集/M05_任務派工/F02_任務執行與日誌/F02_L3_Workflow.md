---
feature_id: M05-F02
parent_system: SYS01
parent_subsystem: SS01/SS02
version: v1.0 (2026-09-01)
---
# F02業務流程拓樸

## 業務流程映射表
**Epic：EP##-名稱**
- 旅程起點：[觸發條件或初始狀態]
- 旅程終點：[最終達成的業務價值狀態]
- 主線：`[M05-F02-W01] -> [M05-F02-W02]`
- 分支：`[M05-F02-W01] --{條件：[描述]}--> [M05-F02-W99]`
- 終止：`[M05-F02-W02] --{條件：[描述]}--> [M05-F02-W99]`

## Workflow stateDiagram
> 🗺️ [返回全域功能圖](../../../04_FuncMap.md)

```mermaid
stateDiagram-v2
  [*] --> M05_F02_W01
  M05_F02_W01 --> M05_F02_W02
  M05_F02_W02 --> [*]

  click M05_F02_W01 "./nodes/M05-F02-W01_xxx.md"
  click M05_F02_W02 "./nodes/M05-F02-W02_xxx.md"
```
> ⚠️click語法為L3互動地圖的核心功能。
> 產出L3 Workflow時，每個狀態節點必須對應一條click指令，
> 指向其/nodes/實體單檔。路徑從L3檔案所在目錄起算。

---
feature_id: M00-F00
parent_system: SYS00
parent_subsystem: null
version: v1.0 (YYYY-MM-DD)
---
# F00業務流程拓樸

## 業務流程映射表
**Epic：EP##-名稱**
- 旅程起點：[觸發條件或初始狀態]
- 旅程終點：[最終達成的業務價值狀態]
- 主線：`[M00-F00-W01] -> [M00-F00-W02]`
- 分支：`[M00-F00-W01] --{條件：[描述]}--> [M00-F00-W99]`
- 終止：`[M00-F00-W02] --{條件：[描述]}--> [M00-F00-W99]`

## Workflow stateDiagram
> 🗺️ [返回全域功能圖](../../04_FuncMap.md)

```mermaid
stateDiagram-v2
  [*] --> M00_F00_W01
  M00_F00_W01 --> M00_F00_W02
  M00_F00_W02 --> [*]

  click M00_F00_W01 "./nodes/M00-F00-W01_xxx.md"
  click M00_F00_W02 "./nodes/M00-F00-W02_xxx.md"
```
> ⚠️click語法為L3互動地圖的核心功能。
> 產出L3 Workflow時，每個狀態節點必須對應一條click指令，
> 指向其/nodes/實體單檔。路徑從L3檔案所在目錄起算。

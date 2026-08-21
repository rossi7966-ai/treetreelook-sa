---
file: DesignContracts/HandoffManifest.md
role: handoff_manifest
status: TEMPLATE_EMPTY
version: v0.1 (YYYY-MM-DD)
last_updated: YYYY-MM-DD
---
# SA接手清單(HandoffManifest)

> 每次接手記一節;LocalOverrides承載「先修後報」(禁隱形修正)。

## 接手紀錄

### [YYYY-MM-DD] 接手 #N
| 消費檔案 | commit hash/版次 | 對應產出 | 缺料(GAP-ID) |
|---------|------------------|---------|--------------|

## LocalOverrides(本地修正登記)

| OVR-ID | 上游對象(檔+節點/TBD-ID) | 問題白話 | 本地處置 | 回饋狀態 | 收斂動作 |
|--------|--------------------------|---------|---------|---------|---------|
<!-- 回饋狀態:待回饋|已回饋|上游已修|已收斂;上游已修而override仍在=check_alignment.py fail -->

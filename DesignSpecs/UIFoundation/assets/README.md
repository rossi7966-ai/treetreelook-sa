---
file: DesignSpecs/UIFoundation/assets/README.md
role: assets_manifest
info_level: Candidate
origin: PREP-UI 前置準備產出(PREP-UI-2)
version: v0.1 (2026-08-18;資產容器首建;契約+佔位樣式+授權清單)
last_updated: 2026-08-18
summary: UIFoundation 資產容器清單——氣象碼↔icon 契約(weather-icon-map.json)+佔位樣式(placeholder.css)+逐件授權登記。新資產入包必先登記本清單(40_Iconography §二/45_Imagery §五 紀律)。
---

# 資產容器清單

> 白話:這個資料夾放「可被程式消費的設計資產」——契約檔、佔位樣式、
> 以及日後的 icon/插畫實體檔。每一件都要在下表登記來源與授權，
> 沒登記的資產不得入包。

## 清單

| 檔案 | 性質 | 來源 | 授權 | 消費者 |
|------|------|------|------|--------|
| `weather-icon-map.json` | 資料契約(氣象碼→canonical→icon) | 代碼=CWA 官方說明表(107.12.20 版);對應=40_Iconography §五 | 契約本身=本 repo;引用之 MDI 名=Apache-2.0、yr.no 名=MIT | 前端、prototype、樣張 |
| `placeholder.css` | 佔位樣式(ph-slot 契約) | 45_Imagery §三 | 本 repo | prototype、樣張 |

## 登記紀律

- 新 icon/插畫/照片入包:本表加列(檔名、性質、來源、授權、消費者)，
  照片另附授權簿條目(45_Imagery §五)。
- icon 實體檔(SVG)現階段不入容器——prototype 走 inline SVG path、
  前端走 Vuetify/MDI 生態(40_Iconography §二);yr.no 補位件入包時逐件登記。
- 插畫實體檔候設計師定風格後入容器(45_Imagery Known Gaps)。

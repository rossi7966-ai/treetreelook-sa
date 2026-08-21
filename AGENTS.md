---
file: SA_DEPLOY/AGENTS.md
role: project_ai_entry
version: v1.1 (2026-08-07)
last_updated: 2026-08-07
summary: 專案端 AI 入口(隨 MetaSA 部署包)。指向不複述:規則本文見 .metasa/SA_KIT/AI_Rules.md。(MS-T169 落地,I-131 α 缺口 a)
---

# 專案 AI 入口

本專案採 MetaSA 系統分析方法論(隨包部署)。任何 AI 載體(Claude Code / 其他 agent CLI)進場依序讀取:

1. `.metasa/SA_KIT/AI_Rules.md` — 工作流總導覽與治理(唯一權威入口)
2. `.metasa/COACH/CoachHandbook.md` — Coach 角色手冊(陪跑場景)
3. `00_START_SA/00_Status.md` — 專案當前狀態駕駛艙
4. `00_START_SA/SOP.md` — 同事協作協定(開工句 / 收工 / 准駁;AI 須承接其對同事之字面承諾)

指針(指向不複述,規則以目標檔為準):
- 套件檔變動單一管道:AI_Rules §5 條 9
- 交付剝離:AI_Rules §5 條 12
- 產出落點限 `DesignSpecs/`;`.metasa/` 為方法論內部工具箱,非交付物

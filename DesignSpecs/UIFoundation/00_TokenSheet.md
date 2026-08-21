---
file: DesignSpecs/UIFoundation/00_TokenSheet.md
role: token_sheet_generated
summary: 生成物,禁手改;來源 UIFoundation/tokens.json,重生成用 UI_KIT/checks/gen_tokens.py
---
# Token 對照表(生成物)

> 來源:tokens.json v0.3.1
> 使用規則:元件/頁面只准引 semantic tier;primitive 只供 alias 引用(F-2)

| token | 群組 | 型別 | 值 | 層級 | 說明 |
|-------|------|------|-----|------|------|
| `--color-primary` | color | color | `#176466` | primitive | 品牌主色 |
| `--color-primary-emphasis` | color | color | `#0a3738` | primitive | 主色強調(原 primary-darken,F-5 改名) |
| `--color-primary-soft` | color | color | `#d9efef` | primitive | 主色柔和(原 primary-lighten,F-5 改名) |
| `--color-primary-container` | color | color | `#eef4f3` | primitive | 主色容器背景 |
| `--color-secondary` | color | color | `#fc890c` | primitive | 品牌輔色 |
| `--color-secondary-emphasis` | color | color | `#6b4823` | primitive | 輔色強調(原 secondary-darken,F-5 改名;dark mode 值由 mode 表切換) |
| `--color-secondary-soft` | color | color | `#ffecd8` | primitive | 輔色柔和(原 secondary-lighten,F-5 改名;dark mode 值由 mode 表切換) |
| `--color-secondary-container` | color | color | `#fff8eb` | primitive | 輔色容器背景 |
| `--color-tertiary` | color | color | `#554677` | primitive | 品牌第三色槽(結構回收:eco-pay 回件案源;試點回收起始值,專案可覆蓋;白字對比 8.3 過 AAA;圖表序列色屬另一語意,不與品牌角色共用鍵) |
| `--color-tertiary-emphasis` | color | color | `#2e2545` | primitive | 第三色強調(同構 primary/secondary 家族 -emphasis;試點回收起始值,專案可覆蓋) |
| `--color-tertiary-soft` | color | color | `#e6e1f0` | primitive | 第三色柔和(對 text 對比 11.3;試點回收起始值,專案可覆蓋) |
| `--color-tertiary-container` | color | color | `#f1eef7` | primitive | 第三色容器背景(對 text 對比 12.7;試點回收起始值,專案可覆蓋) |
| `--color-on-primary` | color | color | `#ffffff` | primitive | primary 底上前景(對比 6.9 過 AA;與 Vuetify theme on-* 慣例同名=消費端對接點;試點回收起始值,專案可覆蓋) |
| `--color-on-secondary` | color | color | `#212b2b` | primitive | secondary 底上前景(亮底深字慣例,對比 6.0 過 AA;secondary 無 dark 覆寫,本鍵不隨 mode 翻轉;試點回收起始值,專案可覆蓋) |
| `--color-on-tertiary` | color | color | `#ffffff` | primitive | tertiary 底上前景(對比 8.3;試點回收起始值,專案可覆蓋) |
| `--color-on-primary-container` | color | color | `#212b2b` | primitive | primary-container 底上前景(深字,對比 13.1;on-* 補遺=容器淺底配深字,與 on-primary 白字不可代用;試點回收起始值,專案可覆蓋) |
| `--color-on-secondary-container` | color | color | `#212b2b` | primitive | secondary-container 底上前景(深字,對比 13.8;試點回收起始值,專案可覆蓋) |
| `--color-on-tertiary-container` | color | color | `#212b2b` | primitive | tertiary-container 底上前景(深字,對比 12.7;試點回收起始值,專案可覆蓋) |
| `--color-text` | color | color | `#212b2b` | primitive | 文字基色(F-1 裁決:title #373b3c 與 font #212b2b 合併,取較深值) |
| `--color-subtitle` | color | color | `#4c5858` | primitive | 副標題文字色 |
| `--color-placeholder` | color | color | `#757575` | primitive | 佔位文字色 |
| `--color-background` | color | color | `#ffffff` | primitive | 頁面底色(F-3 裁決:原 white 拆分,頁面底→background) |
| `--color-surface` | color | color | `#fbfdfb` | primitive | 卡片/元件面色 |
| `--color-surface-variant` | color | color | `#f3f7fa` | primitive | 次要面色(F-4 裁決:原 container 改名,避免與 M3 -container 後綴衝突) |
| `--color-primary-bright` | color | color | `#39959b` | primitive | 亮調主色(展示層:飾線/圖形/hover 大字用,非內文文字色——AA 依用途驗算;試點回收起始值,專案可覆蓋) |
| `--color-hero-bg` | color | color | `#12403f` | primitive | 展示層 hero 深色帶底(45_PrototypeView 展示層槽;試點回收起始值,專案可覆蓋) |
| `--color-hero-bg-deep` | color | color | `#0a2b2a` | primitive | 展示層 hero 漸層深端/頁尾底(試點回收) |
| `--color-hero-text` | color | color | `#f2f9f8` | primitive | 展示層 hero 上主文字(對 hero-bg 對比 10.7 過 AAA;試點回收) |
| `--color-hero-muted` | color | color | `#9cc5c1` | primitive | 展示層 hero 上次要文字(對 hero-bg 對比 6.1 過 AA;試點回收) |
| `--color-band-soft` | color | color | `#eef6f5` | primitive | 展示層淺色段帶底(淺深節奏用;對 text 對比 >13;試點回收) |
| `--color-divider` | color | color | `#bfc8c6` | primitive | 分隔線色 |
| `--color-stroke` | color | color | `#8e9190` | primitive | 邊框/描邊色 |
| `--color-disabled` | color | color | `#d8d8d8` | primitive | 停用狀態色 |
| `--color-red1` | color | color | `#cd3033` | primitive | 紅色 primitive(F-2:只供 alias 引用,元件不直接使用) |
| `--color-red1-container` | color | color | `#fff9f9` | primitive |  |
| `--color-green1` | color | color | `#138251` | primitive | 綠色 primitive |
| `--color-green1-container` | color | color | `#f8fffc` | primitive |  |
| `--color-blue1` | color | color | `#0168ee` | primitive | 藍色 primitive |
| `--color-blue1-container` | color | color | `#f3f8ff` | primitive |  |
| `--color-orange1` | color | color | `#b45309` | primitive | 橘色 primitive(警戒語意保留區;試點回收起始值——對齊 CWA 警戒色階慣例,CTA 不得用橘) |
| `--color-orange1-container` | color | color | `#fff4e5` | primitive |  |
| `--color-text-heading` | color | color | `#212b2b` → `{color.text}` | semantic | 標題文字色(F-1 semantic alias) |
| `--color-text-body` | color | color | `#212b2b` → `{color.text}` | semantic | 內文文字色(F-1 semantic alias) |
| `--color-error` | color | color | `#cd3033` → `{color.red1}` | semantic | 錯誤語意色(F-2 semantic alias → red1) |
| `--color-error-container` | color | color | `#fff9f9` → `{color.red1-container}` | semantic |  |
| `--color-success` | color | color | `#138251` → `{color.green1}` | semantic | 成功語意色(F-2 semantic alias → green1) |
| `--color-success-container` | color | color | `#f8fffc` → `{color.green1-container}` | semantic |  |
| `--color-info` | color | color | `#0168ee` → `{color.blue1}` | semantic | 資訊語意色(F-2 semantic alias → blue1) |
| `--color-info-container` | color | color | `#f3f8ff` → `{color.blue1-container}` | semantic |  |
| `--color-warning` | color | color | `#b45309` → `{color.orange1}` | semantic | 警示語意色(semantic alias → orange1;補齊 error/success/info/warning 四語意;試點回收) |
| `--color-warning-container` | color | color | `#fff4e5` → `{color.orange1-container}` | semantic |  |
| `--color-on-error` | color | color | `#ffffff` | primitive | error 底上前景(light 對 red1 對比 5.2 過 AA;dark 隨 red1 提亮翻轉深字;試點回收起始值,專案可覆蓋) |
| `--color-on-success` | color | color | `#ffffff` | primitive | success 底上前景(light 對 green1 對比 4.8 過 AA;dark 隨 green1 提亮翻轉深字;試點回收起始值,專案可覆蓋) |
| `--color-on-info` | color | color | `#ffffff` | primitive | info 底上前景(對 blue1 對比 5.0 過 AA;blue1 無 dark 覆寫,本鍵不翻轉;試點回收起始值,專案可覆蓋) |
| `--color-on-warning` | color | color | `#ffffff` | primitive | warning 底上前景(light 對 orange1 對比 5.0 過 AA;dark 隨 orange1 提亮翻轉深字;試點回收起始值,專案可覆蓋) |
| `--color-on-error-container` | color | color | `#212b2b` | primitive | error-container 底上前景(深字,對比 14.0;on-* 補遺;試點回收起始值,專案可覆蓋) |
| `--color-on-success-container` | color | color | `#212b2b` | primitive | success-container 底上前景(深字,對比 14.3;試點回收起始值,專案可覆蓋) |
| `--color-on-info-container` | color | color | `#212b2b` | primitive | info-container 底上前景(深字,對比 13.6;試點回收起始值,專案可覆蓋) |
| `--color-on-warning-container` | color | color | `#212b2b` | primitive | warning-container 底上前景(深字,對比 13.4;試點回收起始值,專案可覆蓋) |
| `--typography-font-family-sans` | typography-font-family | fontFamily | `roboto, Noto Sans TC, sans-serif` |  |  |
| `--typography-font-size-display1` | typography-font-size | dimension | `2.75rem` |  | 44px(展示層 hero 主標;試點回收) |
| `--typography-font-size-display2` | typography-font-size | dimension | `2rem` |  | 32px(展示層段帶標題;試點回收) |
| `--typography-font-size-head1` | typography-font-size | dimension | `1.75rem` |  | 28px |
| `--typography-font-size-head2` | typography-font-size | dimension | `1.5rem` |  | 24px |
| `--typography-font-size-subtitle1` | typography-font-size | dimension | `1.25rem` |  | 20px |
| `--typography-font-size-subtitle2` | typography-font-size | dimension | `1.125rem` |  | 18px |
| `--typography-font-size-body1` | typography-font-size | dimension | `1rem` |  | 16px(基準) |
| `--typography-font-size-body2` | typography-font-size | dimension | `0.875rem` |  | 14px |
| `--typography-font-weight-bold` | typography-font-weight | number | `700` |  |  |
| `--typography-font-weight-medium` | typography-font-weight | number | `500` |  |  |
| `--typography-font-weight-regular` | typography-font-weight | number | `400` |  |  |
| `--typography-line-height-default` | typography-line-height | number | `1.5` |  |  |
| `--typography-line-height-display` | typography-line-height | number | `1.25` |  | 展示層 display 字階專用(試點回收) |
| `--spacing-1` | spacing | dimension | `2px` |  |  |
| `--spacing-2` | spacing | dimension | `4px` |  |  |
| `--spacing-3` | spacing | dimension | `8px` |  |  |
| `--spacing-4` | spacing | dimension | `12px` |  |  |
| `--spacing-5` | spacing | dimension | `16px` |  |  |
| `--spacing-6` | spacing | dimension | `20px` |  |  |
| `--spacing-7` | spacing | dimension | `24px` |  |  |
| `--spacing-8` | spacing | dimension | `32px` |  |  |
| `--spacing-9` | spacing | dimension | `48px` |  | 展示層 band 垂直呼吸(試點回收) |
| `--spacing-10` | spacing | dimension | `64px` |  | 展示層 hero 垂直呼吸(試點回收) |
| `--spacing-11` | spacing | dimension | `96px` |  | 展示層大段落間距(試點回收) |
| `--radius-s` | radius | dimension | `4px` |  |  |
| `--radius-m` | radius | dimension | `8px` |  |  |
| `--radius-l` | radius | dimension | `20px` |  |  |
| `--radius-xl` | radius | dimension | `999px` |  | pill |
| `--shadow-card` | shadow | shadow | `0px 4px 6px -2px rgba(0,0,0,0.1)` |  |  |
| `--shadow-popover` | shadow | shadow | `0px 4px 8px 0px rgba(0,0,0,0.2)` |  |  |
| `--shadow-dialog` | shadow | shadow | `0px 11px 15px 0px rgba(0,0,0,0.2)` |  |  |
| `--z-index-map` | z-index | number | `1` |  |  |
| `--z-index-panel` | z-index | number | `2` |  |  |
| `--z-index-popover` | z-index | number | `20` |  |  |
| `--z-index-tooltip` | z-index | number | `100` |  |  |
| `--z-index-header` | z-index | number | `1005` |  |  |
| `--z-index-to-top` | z-index | number | `1005` |  |  |
| `--z-index-left-menu` | z-index | number | `1006` |  |  |
| `--z-index-dialog` | z-index | number | `1010` |  |  |
| `--z-index-alert` | z-index | number | `3000` |  |  |
| `--z-index-backdrop` | z-index | number | `9998` |  |  |
| `--z-index-fetch-loading` | z-index | number | `9999` |  |  |
| `--breakpoint-xs-mobile` | breakpoint | dimension | `375px` |  | max-width |
| `--breakpoint-tablet` | breakpoint | dimension | `768px` |  |  |
| `--breakpoint-laptop` | breakpoint | dimension | `1280px` |  |  |
| `--breakpoint-desktop` | breakpoint | dimension | `1440px` |  |  |
| `--breakpoint-xl-desktop` | breakpoint | dimension | `1920px` |  |  |
| `--layout-header-height` | layout | dimension | `60px` |  |  |
| `--layout-backstage-header-height` | layout | dimension | `56px` |  |  |
| `--layout-content-width` | layout | dimension | `1120px` |  | 展示層 prototype 內容欄寬(試點回收) |
| `--transition-fast` | transition | transition | `all 0.2s ease-in-out` |  |  |
| `--transition-slow` | transition | transition | `all 0.5s ease-in-out` |  |  |
| `--focus-visible` | focus | border | `4px dashed var(--color-secondary)` |  |  |

## Dark Mode 覆寫

| token | 值 |
|-------|----|
| `--color-primary` | `#57cbcf` |
| `--color-primary-container` | `#131315` |
| `--color-secondary-emphasis` | `#ffecd8` |
| `--color-secondary-soft` | `#6b4823` |
| `--color-text` | `#ffffff` |
| `--color-subtitle` | `#ffffff` |
| `--color-background` | `#2f2e31` |
| `--color-surface` | `#2f2e31` |
| `--color-surface-variant` | `#1a1a1a` |
| `--color-disabled` | `#3f3f3f` |
| `--color-red1` | `#f96063` |
| `--color-green1` | `#54c594` |
| `--color-orange1` | `#ffaf54` |
| `--color-band-soft` | `#16302f` |
| `--color-on-primary` | `#0a3738` |
| `--color-on-primary-container` | `#ffffff` |
| `--color-on-error` | `#212b2b` |
| `--color-on-success` | `#212b2b` |
| `--color-on-warning` | `#212b2b` |

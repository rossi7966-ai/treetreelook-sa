---
file: DesignSpecs/UIFoundation/00_TokenSheet.md
role: token_sheet_generated
summary: 生成物，禁手改;來源 UIFoundation/tokens.json，重生成用 UI_KIT/checks/gen_tokens.py
---
# Token 對照表(生成物)

> 來源:tokens.json v0.4.0
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
| `--color-tertiary` | color | color | `#554677` | primitive | 品牌第三色槽(結構回收:eco-pay 回件案源;試點回收起始值，專案可覆蓋;白字對比 8.3 過 AAA;圖表序列色屬另一語意，不與品牌角色共用鍵) |
| `--color-tertiary-emphasis` | color | color | `#2e2545` | primitive | 第三色強調(同構 primary/secondary 家族 -emphasis;試點回收起始值，專案可覆蓋) |
| `--color-tertiary-soft` | color | color | `#e6e1f0` | primitive | 第三色柔和(對 text 對比 11.3;試點回收起始值，專案可覆蓋) |
| `--color-tertiary-container` | color | color | `#f1eef7` | primitive | 第三色容器背景(對 text 對比 12.7;試點回收起始值，專案可覆蓋) |
| `--color-on-primary` | color | color | `#ffffff` | primitive | primary 底上前景(對比 6.9 過 AA;與 Vuetify theme on-* 慣例同名=消費端對接點;試點回收起始值，專案可覆蓋) |
| `--color-on-secondary` | color | color | `#212b2b` | primitive | secondary 底上前景(亮底深字慣例，對比 6.0 過 AA;secondary 無 dark 覆寫，本鍵不隨 mode 翻轉;試點回收起始值，專案可覆蓋) |
| `--color-on-tertiary` | color | color | `#ffffff` | primitive | tertiary 底上前景(對比 8.3;試點回收起始值，專案可覆蓋) |
| `--color-on-primary-container` | color | color | `#212b2b` | primitive | primary-container 底上前景(深字，對比 13.1;on-* 補遺=容器淺底配深字，與 on-primary 白字不可代用;試點回收起始值，專案可覆蓋) |
| `--color-on-secondary-container` | color | color | `#212b2b` | primitive | secondary-container 底上前景(深字，對比 13.8;試點回收起始值，專案可覆蓋) |
| `--color-on-tertiary-container` | color | color | `#212b2b` | primitive | tertiary-container 底上前景(深字，對比 12.7;試點回收起始值，專案可覆蓋) |
| `--color-text` | color | color | `#212b2b` | primitive | 文字基色(F-1 裁決:title #373b3c 與 font #212b2b 合併，取較深值) |
| `--color-subtitle` | color | color | `#4c5858` | primitive | 副標題文字色 |
| `--color-placeholder` | color | color | `#757575` | primitive | 佔位文字色 |
| `--color-background` | color | color | `#ffffff` | primitive | 頁面底色(F-3 裁決:原 white 拆分，頁面底→background) |
| `--color-surface` | color | color | `#fbfdfb` | primitive | 卡片/元件面色 |
| `--color-surface-variant` | color | color | `#f3f7fa` | primitive | 次要面色(F-4 裁決:原 container 改名，避免與 M3 -container 後綴衝突) |
| `--color-primary-bright` | color | color | `#39959b` | primitive | 亮調主色(展示層:飾線/圖形/hover 大字用，非內文文字色——AA 依用途驗算;試點回收起始值，專案可覆蓋) |
| `--color-hero-bg` | color | color | `#12403f` | primitive | 展示層 hero 深色帶底(45_PrototypeView 展示層槽;試點回收起始值，專案可覆蓋) |
| `--color-hero-bg-deep` | color | color | `#0a2b2a` | primitive | 展示層 hero 漸層深端/頁尾底(試點回收) |
| `--color-hero-text` | color | color | `#f2f9f8` | primitive | 展示層 hero 上主文字(對 hero-bg 對比 10.7 過 AAA;試點回收) |
| `--color-hero-muted` | color | color | `#9cc5c1` | primitive | 展示層 hero 上次要文字(對 hero-bg 對比 6.1 過 AA;試點回收) |
| `--color-band-soft` | color | color | `#eef6f5` | primitive | 展示層淺色段帶底(淺深節奏用;對 text 對比 >13;試點回收) |
| `--color-divider` | color | color | `#bfc8c6` | primitive | 分隔線色 |
| `--color-stroke` | color | color | `#8e9190` | primitive | 邊框/描邊色 |
| `--color-disabled` | color | color | `#d8d8d8` | primitive | 停用狀態色 |
| `--color-red1` | color | color | `#cd3033` | primitive | 紅色 primitive(F-2:只供 alias 引用，元件不直接使用) |
| `--color-red1-container` | color | color | `#fff9f9` | primitive |  |
| `--color-green1` | color | color | `#138251` | primitive | 綠色 primitive |
| `--color-green1-container` | color | color | `#f8fffc` | primitive |  |
| `--color-blue1` | color | color | `#0168ee` | primitive | 藍色 primitive |
| `--color-blue1-container` | color | color | `#f3f8ff` | primitive |  |
| `--color-orange1` | color | color | `#b45309` | primitive | 橘色 primitive(警戒語意保留區;試點回收起始值——對齊 CWA 警戒色階慣例，CTA 不得用橘) |
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
| `--color-on-error` | color | color | `#ffffff` | primitive | error 底上前景(light 對 red1 對比 5.2 過 AA;dark 隨 red1 提亮翻轉深字;試點回收起始值，專案可覆蓋) |
| `--color-on-success` | color | color | `#ffffff` | primitive | success 底上前景(light 對 green1 對比 4.8 過 AA;dark 隨 green1 提亮翻轉深字;試點回收起始值，專案可覆蓋) |
| `--color-on-info` | color | color | `#ffffff` | primitive | info 底上前景(對 blue1 對比 5.0 過 AA;blue1 無 dark 覆寫，本鍵不翻轉;試點回收起始值，專案可覆蓋) |
| `--color-on-warning` | color | color | `#ffffff` | primitive | warning 底上前景(light 對 orange1 對比 5.0 過 AA;dark 隨 orange1 提亮翻轉深字;試點回收起始值，專案可覆蓋) |
| `--color-on-error-container` | color | color | `#212b2b` | primitive | error-container 底上前景(深字，對比 14.0;on-* 補遺;試點回收起始值，專案可覆蓋) |
| `--color-on-success-container` | color | color | `#212b2b` | primitive | success-container 底上前景(深字，對比 14.3;試點回收起始值，專案可覆蓋) |
| `--color-on-info-container` | color | color | `#212b2b` | primitive | info-container 底上前景(深字，對比 13.6;試點回收起始值，專案可覆蓋) |
| `--color-on-warning-container` | color | color | `#212b2b` | primitive | warning-container 底上前景(深字，對比 13.4;試點回收起始值，專案可覆蓋) |
| `--color-rain-1` | color-rain | color | `#eff3ff` | semantic | 雨量一級(最淺;圖例深字對比 13.1) |
| `--color-rain-2` | color-rain | color | `#c6dbef` | semantic | 雨量二級(圖例深字對比 10.2) |
| `--color-rain-3` | color-rain | color | `#9ecae1` | semantic | 雨量三級(圖例深字對比 8.3) |
| `--color-rain-4` | color-rain | color | `#6baed6` | semantic | 雨量四級(圖例深字對比 6.0) |
| `--color-rain-5` | color-rain | color | `#3182bd` | semantic | 雨量五級(圖例白字對比 4.2 過 AA) |
| `--color-rain-6` | color-rain | color | `#08519c` | semantic | 雨量六級(最深;圖例白字對比 7.9) |
| `--color-temp-cold-3` | color-temp | color | `#2166ac` | semantic | 低溫三級(最冷;白字對比 5.9) |
| `--color-temp-cold-2` | color-temp | color | `#67a9cf` | semantic | 低溫二級(深字對比 5.6) |
| `--color-temp-cold-1` | color-temp | color | `#d1e5f0` | semantic | 低溫一級(深字對比 11.2) |
| `--color-temp-mid` | color-temp | color | `#f7f7f7` | semantic | 溫度中位(深字對比 13.6;與 surface 系相近，圖面使用需帶級距邊界線) |
| `--color-temp-warm-1` | color-temp | color | `#fddbc7` | semantic | 高溫一級(深字對比 11.2) |
| `--color-temp-warm-2` | color-temp | color | `#ef8a62` | semantic | 高溫二級(深字對比 5.9) |
| `--color-temp-warm-3` | color-temp | color | `#b2182b` | semantic | 高溫三級(最熱;白字對比 6.9) |
| `--color-alert-advisory` | color-alert | color | `#e6a700` | semantic | 警特報一級(黃;黃底必配深字，對比 6.9 過 AA;對白底 2.1 不足 non-text 3:1→徽章/面必帶深字或邊界描邊) |
| `--color-alert-warning` | color-alert | color | `#b45309` → `{color.orange1}` | semantic | 警特報二級(橙;alias→orange1 警戒保留區;白字前景循 on-warning) |
| `--color-alert-severe` | color-alert | color | `#cd3033` → `{color.red1}` | semantic | 警特報三級(紅;alias→red1;白字前景循 on-error) |
| `--color-gis-halo` | color-gis | color | `#ffffff` | semantic | 圖面標註白暈(任意底圖上保可讀;dark 底圖翻轉候 dark 輪) |
| `--color-gis-station` | color-gis | color | `#176466` → `{color.primary}` | semantic | 站點圖徵預設(alias→primary) |
| `--color-gis-station-active` | color-gis | color | `#fc890c` → `{color.secondary}` | semantic | 站點圖徵選取態(alias→secondary) |
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
| `--icon-size-s` | icon | dimension | `16px` |  | 行內輔助(輸入框內、表格格內) |
| `--icon-size-m` | icon | dimension | `20px` |  | 按鈕內、清單項 |
| `--icon-size-l` | icon | dimension | `24px` |  | 獨立操作、導航 |
| `--icon-size-xl` | icon | dimension | `32px` |  | 空狀態、氣象現象主顯示 |
| `--imagery-ratio-hero` | imagery | ratio | `21 / 9` |  | 首頁主視覺帶(content-width 1120 下高約 480) |
| `--imagery-ratio-card` | imagery | ratio | `16 / 9` |  | 卡片封面圖 |
| `--imagery-ratio-media` | imagery | ratio | `4 / 3` |  | 內文媒體圖 |
| `--imagery-ratio-square` | imagery | ratio | `1 / 1` |  | 頭像、縮圖 |
| `--imagery-empty-max-h` | imagery | dimension | `240px` |  | 空狀態插畫高度上限 |
| `--imagery-ph-min-h` | imagery | dimension | `160px` |  | 佔位槽最小高度(防版面跳動) |
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

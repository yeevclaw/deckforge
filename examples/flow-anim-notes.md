# flow-anim 流動邊線動畫 — 設計決策記錄

> 本規範已於 v0.9.0 整合進 skill 本體:`prompts/04_planning_draft.md`(Motion pages
> 決策流)、`prompts/05_designer_svg.md` Step 5.7(構造配方與數值正本)、
> `references/design_system.md`(家族載體)、`references/diagrams.md`(hub 幾何
> 與永不動畫清單)、`SKILL.md`(Phase 3/4/5 摘要與交付規則)。
> 本文件保留為**設計決策記錄**(含實驗數據與棄案理由,例如抖色實驗)。
> 規則若與本文件出入,以 `prompts/05_designer_svg.md` Step 5.7 為準。
> (examples/ 已 export-ignore,不隨 skill 出貨。)

## 機制摘要

- 標記:`<line>`/`<path>` 帶 `class="flow-anim"` + `stroke-dasharray` → 該頁由
  `scripts/svg_to_pptx.py` 轉成循環 GIF 嵌入(12 幀 × 80ms,每圈位移 2 個
  dash 週期 ≈ 29px/s)。
- PowerPoint(桌面)與 Keynote 在**放映模式**播放;編輯檢視顯示靜態第一幀;
  PDF 為靜態。嵌入 SVG 的 SMIL/CSS 動畫在 PowerPoint 不會播放,GIF 是唯一可靠路徑。
- 動畫頁**犧牲 Convert-to-Shape 可編輯性**(GIF 是圖片),且解析度 1600px
  (靜態頁 2560px)。這是每個動畫頁都要付的價格。

## 決策流(構圖優先)— 這是主規則

動畫不是畫完版面後「挑哪些邊可以動」的過濾器;它是 **Phase 3 規劃層的構圖決策**。
判斷順序:

1. **這頁的故事是「持續流動」嗎?** 資料、金流、流量、能量在系統中持續通過——
   而不是離散的步驟、事件或狀態轉變。否 → 靜態頁,結束。
2. **值得花掉 deck 的動畫預算嗎?** 每份 deck ≤2–3 個動畫頁,只給 money slides;
   每個動畫頁都犧牲可編輯性。否 → 靜態頁,結束。
3. **是 → 從下方目錄選一個動畫優先構圖,版面為動畫設計**——動畫路徑是頁面的
   結構主軸,長度、乾淨度、單一系統由構造本身保證;不是把動畫塞進現成的靜態版面。

## 動畫優先構圖目錄

每個構圖的構造規則讓「安全網」的數值底線自動滿足。

### 線性管線(transit rail)— 內容形狀:轉換管線、處理流程中的持續資料流

軌道是頁面骨架,橫貫 ≥900px;站環疊在軌道上;動畫掛在**脈衝疊層**,軌道本體靜態。

- `corporate_fresh`:即現有 `transit_pipeline` 構圖 — 12px 漸層軌道 + 一體成形
  箭頭(靜態),白色脈衝層流動(demo:`flow-anim-demo-fresh/page_01.svg`)
- `dark_apple`:石墨軌道(`#333333` 12px round cap)+ highlight 色一體箭頭,
  highlight 色脈衝層(demo:`flow-anim-demo/page_04.svg`)

```xml
<!-- 軌道本體:靜態 -->
<line x1="140" y1="360" x2="1090" y2="360" stroke="…" stroke-width="12" stroke-linecap="round"/>
<path d="M 1084 338 L 1144 360 L 1084 382 Z" fill="…"/>
<!-- 脈衝層:4px 虛線沿軌道流動,結束在箭頭底之前;繪製順序在軌道之後、站環之前 -->
<line class="flow-anim" x1="140" y1="360" x2="1078" y2="360"
      stroke="…" stroke-width="4" stroke-linecap="round"
      stroke-dasharray="10 18" stroke-opacity="0.9"/>
```

### 循環(orbit)— 內容形狀:循環、迭代迴圈

閉環視為**一個**動畫系統,全環同動是期望效果(轉動感)。

- `corporate_fresh`:`glass_orbit_loop` 的虛線軌道環(`#9BD4B8`,本來就是 dashed
  stroke,直接掛 flow-anim)
- `dark_apple`:cycle 弧線(≈165px ≈ 11.8 週期,長度足夠)

### 匯流/分發(hub)— 內容形狀:多對一彙整、一對多分發

主幹+支流構造(demo:`flow-anim-demo/page_03.svg`):

- ≤3 個來源 → 直連,錨點沿目標邊**分散**(箭頭間距 32px 佳 / 24px 底線)
- ≥4 個來源 → 支流先**匯流成主幹**再進入目標(只有一個箭頭)
- fan-out 鏡像;主幹+分支同時動畫(同 dasharray,方向跟隨各自路徑繪製方向)
- 雙向連結只動主要方向;絕不在平行線上跑兩個反向動畫

### 旁路強調(accent bypass)— 唯一合法的「靜態版面 + 動畫」形式

當**例外路徑本身就是訊息**(fast path、feedback loop)時,靜態主流程上只動那
一條旁路(demo:`flow-anim-demo/page_01.svg` 的「即時通道」)。構造:旁路是
長 bezier(≥5 週期),全頁只有它在動;主流程的短溝槽維持靜態箭頭。

## 安全網(lint 與數值底線)

構圖選對時這些自動滿足;它們存在是為了接住失誤(轉檔器已實作前兩項警告):

| 底線 | 值 |
|---|---|
| 最小長度 | 沿路徑 ≥ 5 個 dash 週期("8 6" 即 70px);低於此值像閃爍不像流動 |
| dasharray | 整份 deck 統一(預設 `"8 6"`;脈衝層 `"10 18"`);轉檔器每頁只讀第一個元素的值,混用產生循環接縫 |
| 速度 | 每圈位移 2 週期 ≈ 29px/s(轉檔器內建;1 週期太慢、3 週期取樣不足會頓挫) |
| 每頁預算 | ≤3 條動畫路徑,或一個閉環/匯流系統 |
| 箭頭 | `markerUnits="userSpaceOnUse"`,12×9px 頭(`M0,0 L12,4.5 L0,9`,refX=11,refY=4.5)配 2–2.5px 線;頭長 ≈ 4–5× 線寬 |
| 粗線(≥8px) | 不掛 marker(比例必壞),用一體成形箭頭 + 脈衝疊層 |
| 背景 | 動畫頁優先平面色背景;大面積細膩漸層在 256 色 GIF 上會有色帶 |

## 明文禁止 — 這些內容形狀不進動畫構圖

- **封閉虛線框**(警示框、dashed border)— 動起來就是「螞蟻線」選取框效果
- **timeline 軸線** — 事件是離散的;1040px 軸線是最大誘惑,忍住
- **funnel** — 數量故事不是流動故事,而且梯形是 fill
- **sequence diagram 的訊息箭頭** — 離散呼叫;只有真正的 streaming channel 例外
- **split_style_duel 的橋接膠囊** — before/after 是離散轉變
- **hierarchy tree / compare table 等密集圖** — 短線段太多
- **swoosh** — 它是氛圍(fill)不是線條,不能 dash 也不該被提升為前景主角

## 品質注意

- 抖色已驗證不可行:檔案 ×5、誤差擴散造成幀間閃爍;維持 `dither=NONE`
- dash 流進固定 marker 時,最後一段在某些幀會在「dash/gap」間切換 —
  路徑結束在 refX 前 ~2px 可緩解,目前尺寸下可接受

## 整合記錄

v0.9.0 已完成整合(本節原為工作清單)。整合時的 doc-drift 防治決策:
數值規則唯一正本在 prompts/05 Step 5.7;hub 幾何正本在 diagrams.md
(flow 的 fan-in/fan-out 變體);其他檔案一律引用、不重述數字。

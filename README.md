# DeckForge : 簡報的靈魂是內容,設計讓它被看見

[English](README.en.md) · **繁體中文**

> 一個 Claude skill,專門用來產出**高品質、可在 PowerPoint 編輯的簡報**。不是把你的主題丟進範本套版,而是用三套方法論串起整個流程:**蘇格拉底反詰**(Phase 1)挖出簡報真正要說服的判斷、**金字塔原理**(Phase 1→2→3)把零碎想法結構成可讀的論證、**Bento Grid + 三家族設計系統**(Phase 3→4,預設 IT_prism 冷調淺色風,另有 corporate_fresh 暖調顧問風、暗黑 Apple 風可選)把論證渲染成可編輯 PPT。不是一鍵生成——每個階段邊界都會跳窗讓你確認才往下。


## Demo

五張特色展示頁,每張示範一種佈局與一項能力,全部由這個 skill 的 SVG pipeline 直接產出(預設 IT_prism 冷調淺色風):

| 封面 · 長虹玻璃 | 顧問圖表 · 瀑布橋 | 玻璃流程 · 五階段 |
|:--:|:--:|:--:|
| ![](examples/slide-1.jpg) | ![](examples/slide-2.jpg) | ![](examples/slide-3.jpg) |
| **可編輯輸出 · 主從卡** | **流動動畫 · 蘇格拉底循環** | **同一份 deck,五種佈局** |
| ![](examples/slide-4.jpg) | ![](examples/slide-5.gif) | 卡片 · 圖表 · 圖解 · 流程 · 循環——佈局隨內容而變,不套版。 |

第 5 張是**流動邊線動畫**(`flow-anim`)的實際產出:環圈上的脈衝虛線會在 PowerPoint / Keynote 放映模式持續繞行(上面那張 GIF 就是嵌進投影片裡的內容)。動畫頁以 GIF 嵌入,放映時才會動;代價是**該頁不支援 Convert-to-Shape 編輯**,在 PDF 中為靜態——每份 deck 最多 2–3 頁動畫,只留給最關鍵的流程或循環頁。

- 這五頁的原始 SVG(可看 Bento Grid 座標,拖進 PowerPoint 可直接檢視):[`examples/showcase/`](examples/showcase/)
- 另有完整 10 頁範例 deck 與合併 PDF:[`examples/sample-deck/`](examples/sample-deck/) · [`examples/DeckForge-demo.pdf`](examples/DeckForge-demo.pdf)


## 為什麼用 SVG → PPTX(而不是套範本或圖片型 PPT)?

- SVG 是 PowerPoint 2016+ 原生支援的向量圖格式。轉檔器把每頁拆成「可移動的背景圖 + 可編輯內容層」:右鍵「轉換成圖形」即可編輯文字、卡片、線條與圖示;漸層/玻璃態/陰影等氛圍則保留在可整體移動的背景圖中。
- 同時可以根據**內容自由設計版面**,不用把內容塞進固定範本。
- 每份 deck 都有專屬配色 + 視覺主題,且整份一致(skill 會強制執行)。
- 編輯細節見 [`references/editable_mode.md`](references/editable_mode.md)。

## 設計理念出處

- **起點**:linux.do 上 *sandun* 寫的「应该是目前最强的PPT Agent,附上完整思路分享」一文。「頂級 PPT 結構架構師」與便當網格(`prompts/02_outline_architect.md`、`references/bento_grid.md`),皆改寫自原文提示詞並加以延伸;以 SVG 作為交付格式也是該文的關鍵選擇。
- **核心方法論一:蘇格拉底反詰**:透過連續性提問進行辯證的哲學 inquiry 形式。引導對話者自我審視、揭示其觀點中的隱含假設與邏輯漏洞,從而承認無知,並探求客觀真理。
- **核心方法論二:金字塔原理**(Barbara Minto):「結論先行,由上往下一層層拆解論點」,讓聽眾或讀者能在最短時間內抓住核心訊息。
- **SVG 作為最終格式**:SVG 是為了在 PowerPoint 端保留可編輯性,而不是只能輸出靜態圖片。
- **Bento Grid 設計語言**:Apple 產品頁帶起的便當網格排版。

## 安裝(Claude Desktop)

兩步:

### 1. 下載 zip + 裝三個 Python 套件

```bash
# 下載最新版 zip
curl -L -o ~/Downloads/deckforge.zip \
  https://github.com/yeevclaw/deckforge/releases/latest/download/deckforge.zip

# 裝 Phase 5 用的三個 Python 套件(macOS / Linux / Windows 都直接這行)
pip install python-pptx resvg-py img2pdf --break-system-packages
```

> 不會用命令列?直接到 [releases 頁面](https://github.com/yeevclaw/deckforge/releases/latest)點 `deckforge.zip` 下載,然後在終端機跑那一行 `pip install`。

只有三個套件,**零系統依賴**——`resvg-py` 是把 Rust SVG 渲染器包成 pip wheel,不需要 Homebrew、apt-get 或 sudo:

- `python-pptx` → 組裝 `.pptx`
- `resvg-py` → 把 SVG 渲染成 PNG(Keynote / Preview / 舊版 PowerPoint 讀的 fallback)
- `img2pdf` → 把同一批 PNG 組裝成隨附的 `.pdf`

Phase 1–4(反詰 / 大綱 / 策劃 / 設計)是純 Markdown,完全不需要套件;只有 Phase 5 用到上面三個。

> 預設會**同時產出 `.pptx` 跟 `.pdf` 兩個檔案**——PPTX 給 PowerPoint 編輯用,PDF 給直接分享 / 客戶看 / 沒有 PowerPoint 的人。

### 2. 在 Claude Desktop 匯入 zip

1. 開 Claude Desktop → 右上 **Customize**
2. 左欄 **Skills** → 標題列右邊的 **`+`** → **Create skill** → **Upload a skill**
3. 選剛剛下載的 `~/Downloads/deckforge.zip`
4. `deckforge` 會出現在 *Personal skills*

完成。跟 Claude 講「**幫我做一份簡報,主題是 XXX**」就會自動觸發。

> **更新到新版**:回 releases 頁面重新下載 zip,在 Customize → Skills 把舊的 deckforge 刪掉,再 Upload a skill 上新的就好。

## 怎麼用

在 Claude Desktop 跟 Claude 說:

> 提示:Claude Desktop 支援拖入檔案。如果要做的簡報是基於現有文件(年報、白皮書、論文、議題報告),把檔案連同主題一起丟給 Claude,skill 會先跑 Phase 0(文件分析)再進大綱階段,效果好很多。

- 「**幫我做一份簡報,主題是 XXX**」
- 「Build me a deck about XXX」
- 「做一份 Series B 募資 pitch」
- 「幫我做客戶提案,要 10 頁」

Claude 會自動觸發 DeckForge,跑完整流程:

| 階段 | 產出 | 你做什麼 |
|---|---|---|
| 0. 文件分析(可選) | `analysis.md` | 丟文件就自動跑,沒丟就跳過 |
| 1. **蘇格拉底反詰** | `brief.md` | **跳窗對話**挖出簡報真正要說服的判斷(thesis / belief shift / proof pillars / objection / desired action),並確認交付模式——現場講(`presenting`)或寄出獨立閱讀(`reading`,slidedoc 密度,講者備註的內容收回頁面上) |
| 2. 大綱架構 | `outline.json` | 用**金字塔原理**展開成大綱——每頁標題都是一個主張,與 proof pillars MECE 對齊;**檢視標題序列**改方向只要 30 秒 |
| 3. 策劃稿 | `planning.json` | **檢視每頁內容**,改文案只要 1 分鐘 ← *多數 AI 工具跳過的一步* |
| 4. SVG 設計 | `pages/page_NN.svg` | 自動產出每頁向量設計 |
| 5. 產出 | `presentation.pptx` + 隨附 `.pdf`(有講者備註時另出 `.notes.md`) | 自動組裝;PowerPoint 2016+ 右鍵 Convert to Shape 即可完整編輯 |

每個階段結束都會跳窗讓你確認才往下,沒同意不會自動進入下一階段。

這個 skill **不是**一鍵生成器。它刻意在大綱後、策劃後設置檢查點,讓你在任何設計工夫花下去之前,用最便宜的成本改方向。


## 資料夾內容

```
DeckForge/
├── SKILL.md                ← Claude 讀的入口
├── prompts/                ← 6 階段提示詞
│   ├── 00_source_analysis.md  ← Phase 0:文件分析(可選)
│   ├── 01_needs_research.md   ← Phase 1:蘇格拉底反詰(Socratic Clarification Loop)
│   ├── 02_outline_architect.md ← Phase 2:大綱
│   ├── 03_content_research.md ← Phase 2.5:web research(可選)
│   ├── 04_planning_draft.md   ← Phase 3:策劃稿(含內容拆解例子)
│   └── 05_designer_svg.md     ← Phase 4:SVG 設計
├── references/             ← 詳細知識庫
│   ├── bento_grid.md       ← Bento Grid 8 種版型(預設;含 stat_hero / mini_grid)
│   ├── diagrams.md         ← 9 種 diagram primitives(只在 Bento 會丟資訊時切換)
│   ├── chart_anatomy.md    ← 10 種 SVG 圖表:基本三型 + 顧問五型(waterfall / stacked / hbar / combo / mekko)+ 專門二型(radar 多維評估 / gantt 甘特排程)+ annotation 層(CAGR 箭頭、差異括號、基準線——圖表自帶分析)
│   ├── design_system.md    ← IT_prism 冷調淺色風(預設)+ corporate_fresh 暖調顧問風 + dark_apple palette + 10 種傳統 palette
│   ├── pyramid_principle.md ← 金字塔原理跨 Phase 1/2/3 的對照表
│   ├── socratic_loop.md     ← Phase 1 反詰問題類型 + 11 種情境 spine
│   └── editable_mode.md    ← PowerPoint Convert to Shape 編輯
├── templates/              ← 59 個 viewBox 1280×720 SVG(58 起始模板 + `_base.svg` 共用底稿)
│   ├── _base.svg           ← 共用 filter / 漸層 / 44 個 Lucide icon
│   ├── cover.svg / toc.svg
│   ├── bento_2col.svg / bento_3col.svg / bento_hero.svg / bento_mixed.svg
│   ├── bento_mini_grid.svg ← 主卡內含 3–5 張 mini-card(dark_apple 風格)
│   ├── chart_bar.svg / chart_line.svg / chart_donut.svg
│   ├── chart_hbar.svg / chart_stacked_bar.svg / chart_waterfall.svg /
│   │   chart_combo.svg / chart_mekko.svg ← 顧問五型:排名 / 結構堆疊 / 瀑布橋 / 量率雙軸 / 市場地圖
│   ├── chart_radar.svg / chart_gantt.svg ← 專門二型:多維評估雷達 / 甘特排程
│   ├── flow.svg / timeline.svg / cycle.svg / funnel.svg / compare_table.svg /
│   │   quadrant_2x2.svg / venn.svg / hierarchy_tree.svg / pyramid.svg ← Diagram primitives
│   ├── prism_cover.svg / prism_compare.svg ← IT_prism(預設家族)長虹玻璃封面與對照表起始檔
│   ├── prism_3col*.svg (4) / prism_mini_grid*.svg (3) / prism_2col*.svg (2) ← IT_prism 的 card_variant 家族
│   ├── prism_flow*.svg (4)                 ← IT_prism 的 flow_variant 四構圖
│   ├── fresh_cover.svg / fresh_compare.svg ← corporate_fresh 封面與對照表起始檔
│   ├── fresh_3col.svg / fresh_3col_steps.svg / fresh_3col_axis.svg / fresh_3col_lead.svg
│   │                       ← three_col 的 4 種 card_variant 構圖(每頁依內容子結構選用)
│   ├── fresh_mini_grid.svg / fresh_mini_grid_ribbon.svg / fresh_mini_grid_spotlight.svg
│   │                       ← mini_grid KPI 網格的 3 種 card_variant 構圖
│   ├── fresh_2col.svg / fresh_2col_beforeafter.svg ← two_col_50_50 的 2 種 card_variant 構圖
│   └── fresh_flow.svg / fresh_flow_terrace.svg / fresh_flow_river.svg / fresh_flow_cascade.svg
│                           ← 靜態 flow 頁的 4 種 glass-flow 構圖(整份 deck 選一種)
├── scripts/
│   ├── svg_to_pptx.py      ← Phase 5 組裝器:雙層可編輯 + flow-anim GIF;產出 .pptx + .pdf
│   ├── package.sh          ← 打包 deckforge.zip 供 Claude Desktop 上傳
│   ├── setup.sh            ← 一鍵安裝依賴(mac / linux)
│   └── setup.ps1           ← Windows PowerShell 版安裝腳本
└── examples/               ← DeckForge 自介 mini-deck(10 頁完整產出)
    ├── DeckForge-demo.pdf  ← 成品 PDF
    ├── slide-1.jpg ... slide-4.jpg + slide-5.gif ← showcase 各頁預覽(第 5 頁為動畫 GIF)
    ├── showcase/           ← 五張 showcase 投影片 SVG 原始檔
    └── sample-deck/        ← 10 頁 demo 的原始 SVG 檔
```

## 給開發者 / fork

想改 skill、貢獻上游,或用 Claude Code CLI:

```bash
# clone 完整原始碼
git clone https://github.com/yeevclaw/deckforge.git ~/deckforge
cd ~/deckforge

# 改完後重新打包成 zip 給 Claude Desktop
bash scripts/package.sh
# 產出 ~/deckforge.zip — 在 Customize → Skills 匯入

# 或:用 Claude Code CLI
git clone https://github.com/yeevclaw/deckforge.git ~/.claude/skills/deckforge
bash ~/.claude/skills/deckforge/scripts/setup.sh
```

`scripts/package.sh` 會讀 SKILL.md 的 `name:` 讓 zip 外層資料夾對上 skill 名;並排除 `.git`、`.DS_Store`、`__pycache__` 等雜訊。Windows 用 `scripts/setup.ps1` 取代 `setup.sh`。

## 授權

[MIT](LICENSE) — 自由使用、fork、修改。分享時若能標註原文出處,感激不盡。

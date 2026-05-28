# DeckForge : 簡報的靈魂是內容不是皮囊

[English](README.en.md) · **繁體中文**

> 一個 Claude skill,專門用來產出**高品質、可在 PowerPoint 編輯的簡報**。不是把你的主題丟進範本套版,而是用三套方法論串起整個流程:**蘇格拉底反詰**(Phase 1)挖出簡報真正要說服的判斷、**金字塔原理**(Phase 1→2→3)把零碎想法結構成可讀的論證、**Bento Grid + 暗黑 Apple 美學**(Phase 3→4)把論證渲染成可編輯 PPT。不是一鍵生成——每個階段邊界都會跳窗讓你確認才往下。


## Demo

一份 3 頁 **DeckForge 自介** mini-deck,由本 skill 的 SVG pipeline 直接產出:

| | | |
|---|---|---|
| ![](examples/slide-1.jpg) | ![](examples/slide-2.jpg) | ![](examples/slide-3.jpg) |



## 為什麼用 SVG → PPTX(而不是套範本或圖片型 PPT)?
- SVG 是 PowerPoint 2016+ 原生支援的向量圖格式。右鍵「轉換成圖形」就能把整張投影片拆成可編輯的文字框與形狀,**保留所有編輯性**。
- 同時可以根據**內容自由設計版面**,不用把內容塞進固定範本。
- 每份 deck 都有專屬配色 + 視覺主題,且整份一致(skill 會強制執行)。
- 編輯細節見 [`references/editable_mode.md`](references/editable_mode.md)。

## 設計理念出處
- **起點**:linux.do 上 *sandun* 寫的「应该是目前最强的PPT Agent」一文。「頂級 PPT 結構架構師」與 便當網格,皆改寫自原文提示詞並加以延伸。
- **核心方法論一：蘇格拉底反詰**:透過連續性提問進行辯證的哲學 inquiry 形式。引導對話者自我審視、揭示其觀點中的隱含假設與邏輯漏洞，從而承認無知 並探求客觀真理。。
- **核心方法論二：金字塔原理**:「結論先行，由上往下一層層拆解論點」，讓聽眾或讀者能在最短時間內抓住核心訊息。
- **SVG 作為最終格式**:SVG 是為了在 PowerPoint 端保留可編輯性,而不是只能輸出靜態圖片。
- **Bento Grid 設計語言**:Apple 產品頁帶起的便當網格排版。




## 安裝(Claude Desktop)

兩步:

### 1. 下載 zip + 裝兩個 Python 套件

```bash
# 下載最新版 zip
curl -L -o ~/Downloads/deckforge.zip \
  https://github.com/yeevclaw/deckforge/releases/latest/download/deckforge.zip

# 裝 Phase 5 用的三個 Python 套件(macOS / Linux / Windows 都直接這行)
pip install python-pptx resvg-py img2pdf --break-system-packages
```

> 不會用命令列?直接到 [releases 頁面](https://github.com/yeevclaw/deckforge/releases/latest)點 `deckforge.zip` 下載,然後在終端機跑那一行 `pip install`。
> 
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
| 1. **蘇格拉底反詰** | `brief.md` | **跳窗對話**挖出簡報真正要說服的判斷(thesis / belief shift / proof pillars / objection / desired action) |
| 2. 大綱架構 | `outline.json` | 用**金字塔原理**展開成大綱,**檢視標題序列**改方向只要 30 秒 |
| 3. 策劃稿 | `planning.json` | **檢視每頁內容**,改文案只要 1 分鐘 |
| 4. SVG 設計 | `pages/*.svg` | 自動產出每頁向量設計 |
| 5. 產出 | `presentation.pptx` + `presentation.pdf` | 自動組裝,兩個檔同時出 |

每個階段結束都會跳窗讓你確認才往下,沒同意不會自動進入下一階段。


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
│   ├── chart_anatomy.md    ← SVG bar / line / donut 圖表
│   ├── design_system.md    ← dark_apple palette + 11 種傳統 palette
│   ├── pyramid_principle.md ← 金字塔原理跨 Phase 1/2/3 的對照表
│   ├── socratic_loop.md     ← Phase 1 反詰問題類型 + 11 種情境 spine
│   └── editable_mode.md    ← PowerPoint Convert to Shape 編輯
├── templates/              ← 20 個 viewBox 1280×720 SVG 起始檔
│   ├── _base.svg           ← 共用 filter / 漸層 / 35 個 Lucide icon
│   ├── cover.svg / toc.svg
│   ├── bento_2col.svg / bento_3col.svg / bento_hero.svg / bento_mixed.svg
│   ├── bento_mini_grid.svg ← 主卡內含 3–5 張 mini-card(dark_apple 風格)
│   ├── chart_bar.svg / chart_line.svg / chart_donut.svg
│   └── flow.svg / timeline.svg / cycle.svg / funnel.svg / compare_table.svg /
│       quadrant_2x2.svg / venn.svg / hierarchy_tree.svg / pyramid.svg ← Diagram primitives
├── scripts/
│   ├── svg_to_pptx.py      ← Phase 5 組裝器(同時產出 .pptx + .pdf)
│   ├── package.sh          ← 打包 deckforge.zip 供 Claude Desktop 上傳
│   ├── setup.sh            ← 一鍵安裝依賴(mac / linux)
│   └── setup.ps1           ← Windows PowerShell 版安裝腳本
└── examples/               ← DeckForge 自介 mini-deck(3 頁完整產出)
    ├── DeckForge-demo.pdf  ← 成品 PDF
    ├── slide-1.jpg ... 3   ← 各頁預覽縮圖
    └── sample-deck/        ← 原始 SVG 檔
```

## 授權

[MIT](LICENSE) — 自由使用、fork、修改。分享時若能標註原文出處,感激不盡。

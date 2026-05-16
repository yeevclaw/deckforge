# DeckForge

[English](README.en.md) · **繁體中文**

> 一個 Claude skill,專門用來產出**高品質、可在 PowerPoint 編輯的簡報**。不是把你的主題丟進範本套版,而是模擬頂級 PPT 設計團隊的工作流程——先研究、再規劃、再設計(5 個階段)。

靈感來自 linux.do 上 *sandun* 的文章《应该是目前最强的PPT Agent,附上完整思路分享》。輸出格式採用 **SVG**——這是該文作者強調的關鍵選擇,因為 SVG 可以直接被 PowerPoint 2016+ 識別為向量圖,使用者只要右鍵「轉換成圖形 (Convert to Shape)」就能編輯每一段文字與每一個元件。

## Demo

一份 3 頁 **DeckForge 自介** mini-deck,由本 skill 的 SVG pipeline 直接產出:

| | | |
|---|---|---|
| ![](examples/slide-1.jpg) | ![](examples/slide-2.jpg) | ![](examples/slide-3.jpg) |

- 合併 PDF: [`examples/DeckForge-demo.pdf`](examples/DeckForge-demo.pdf)
- 原始 SVG(直接看 Bento Grid 的座標寫法): [`examples/sample-deck/`](examples/sample-deck/)

## 資料夾內容

```
DeckForge/
├── SKILL.md                ← Claude 讀的入口
├── prompts/                ← 5 個專家提示詞(每階段一個)
│   ├── 01_needs_research.md
│   ├── 02_outline_architect.md
│   ├── 03_content_research.md
│   ├── 04_planning_draft.md
│   └── 05_designer_svg.md
├── references/             ← 詳細知識庫
│   ├── bento_grid.md       ← Bento Grid 便當網格(設計語言核心)
│   ├── design_system.md    ← 10 種配色 + 視覺主題 + 字體
│   ├── pyramid_principle.md
│   └── editable_mode.md    ← 在 PowerPoint 怎麼編輯 SVG slide
├── templates/              ← 7 個 viewBox 1280×720 SVG 起始檔
│   ├── _base.svg           ← 共用 filter / 漸層 / Lucide icon
│   ├── cover.svg
│   ├── toc.svg
│   ├── bento_2col.svg
│   ├── bento_3col.svg
│   ├── bento_hero.svg
│   └── bento_mixed.svg
├── scripts/
│   ├── svg_to_pptx.py      ← SVG → PPTX 組裝器(含 svgBlip 擴充,保留向量)
│   ├── setup.sh            ← 一鍵安裝依賴(mac / linux)
│   └── setup.ps1           ← Windows PowerShell 版安裝腳本
└── examples/               ← DeckForge 自介 mini-deck(3 頁完整產出)
    ├── DeckForge-demo.pdf   ← 合併後的成品 PDF
    ├── slide-1.jpg ... 3    ← 各頁預覽縮圖
    └── sample-deck/         ← 原始 SVG 檔(可直接拖進 PowerPoint)
```

## 安裝(讓 Claude 用得到)

把整個資料夾複製到 Claude 的 skill 資料夾,讓路徑長這樣:

```
~/.claude/skills/deckforge/
```

### Mac

```bash
git clone https://github.com/yeevclaw/deckforge.git ~/.claude/skills/deckforge
```

### Windows(PowerShell)

```powershell
git clone https://github.com/yeevclaw/deckforge.git "$env:USERPROFILE\.claude\skills\deckforge"
```

> `~/.claude/` 是隱藏資料夾。如果不存在,直接建立即可。

## 怎麼用

在 Claude / Cowork 跟它說:

- 「**幫我做一份簡報,主題是 XXX**」
- 「Build me a deck about XXX」
- 「做一份 Series B 募資 pitch」
- 「幫我做客戶提案,要 10 頁」

Claude 會自動觸發 DeckForge,跑完整 5 階段流程:

| 階段 | 產出 | 你做什麼 |
|---|---|---|
| 1. 需求調研 | `brief.md` | 回答幾個問題(觀眾、目的、長度、語氣) |
| 2. 大綱架構 | `outline.json` | **檢視大綱**,改方向只要 30 秒 |
| 3. 策劃稿 | `planning.json` | **檢視每頁內容**,改文案只要 1 分鐘 |
| 4. SVG 設計 | `pages/*.svg` | 自動產出每頁向量設計 |
| 5. 產出 PPTX | `presentation.pptx` | 自動組裝成可編輯 .pptx |

重點是中間有兩個 review checkpoint(階段 2 跟 3),讓你可以**便宜地修正方向**,不會浪費後面的設計工。

## 為什麼用 SVG → PPTX(而不是套範本或圖片型 PPT)?

- SVG 是 PowerPoint 2016+ 原生支援的向量圖格式。右鍵「轉換成圖形」就能把整張投影片拆成可編輯的文字框與形狀,**保留所有編輯性**。
- 同時可以根據**內容自由設計版面**,不用把內容塞進固定範本。
- 每份 deck 都有專屬配色 + 視覺主題,且整份一致(skill 會強制執行)。
- 編輯細節見 [`references/editable_mode.md`](references/editable_mode.md)。

## 依賴

**階段 1–4 完全純 Markdown,不需要安裝任何套件**——這部分就是 Claude 讀提示詞跑流程。
只有階段 5(產出 .pptx)需要一個 Python 套件:

```bash
# 一行裝完
pip install python-pptx --break-system-packages

# 或跑內建的安裝腳本:
bash scripts/setup.sh                   # macOS / Linux
.\scripts\setup.ps1                     # Windows (PowerShell)
```

`python-pptx` 會自動帶入 `lxml` 和 `Pillow`,所以只裝這一個就夠。

**選用**——如果要產高解析度 PNG 備援(給 PowerPoint 2013 以前的版本、或 PDF 預覽工具),才需要安裝 SVG 渲染器:

```bash
pip install cairosvg --break-system-packages
# 或: brew install inkscape         (macOS)
# 或: apt-get install librsvg2-bin  (Linux)

# 用法
python scripts/svg_to_pptx.py --pages-dir pages/ --output deck.pptx --with-raster
```

不傳 `--with-raster` 的話,腳本會嵌入一個 1×1 透明 PNG 當 OOXML 必填欄位,PowerPoint 2016+ 會直接渲染 SVG 向量——這已經是 90% 使用情境的最佳路徑。

## 設計理念出處

- **方法論**:linux.do 上 *sandun* 寫的「应该是目前最强的PPT Agent」一文。`prompts/02_outline_architect.md` 的「頂級 PPT 結構架構師」與 `references/bento_grid.md` 的便當網格,皆改寫自原文提示詞並加以延伸。
- **SVG 作為最終格式**:同樣出自該文,作者選 SVG 是為了在 PowerPoint 端保留可編輯性,而不是只能輸出靜態圖片。
- **Bento Grid 設計語言**:Apple 產品頁帶起的便當網格排版。
- **金字塔原理**:Barbara Minto 的經典結構。

## 授權

[MIT](LICENSE) — 自由使用、fork、修改。分享時若能標註原文出處,感激不盡。

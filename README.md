# DeckForge : 簡報的靈魂是內容不是皮囊, 願科技之力解放所有人的時間

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
├── prompts/                ← 6 階段提示詞
│   ├── 00_source_analysis.md  ← Phase 0:文件分析(可選)
│   ├── 01_needs_research.md   ← Phase 1:需求調研
│   ├── 02_outline_architect.md ← Phase 2:大綱
│   ├── 03_content_research.md ← Phase 2.5:web research(可選)
│   ├── 04_planning_draft.md   ← Phase 3:策劃稿(含內容拆解例子)
│   └── 05_designer_svg.md     ← Phase 4:SVG 設計
├── references/             ← 詳細知識庫
│   ├── bento_grid.md       ← Bento Grid 8 種版型(含 stat_hero / mini_grid)
│   ├── chart_anatomy.md    ← SVG bar / line / donut 圖表
│   ├── design_system.md    ← dark_apple palette + 11 種傳統 palette
│   ├── pyramid_principle.md
│   └── editable_mode.md    ← PowerPoint Convert to Shape 編輯
├── templates/              ← 11 個 viewBox 1280×720 SVG 起始檔
│   ├── _base.svg           ← 共用 filter / 漸層 / 35 個 Lucide icon
│   ├── cover.svg / toc.svg
│   ├── bento_2col.svg / bento_3col.svg / bento_hero.svg / bento_mixed.svg
│   ├── bento_mini_grid.svg ← 主卡內含 3–6 張 mini-card(dark_apple 風格)
│   └── chart_bar.svg / chart_line.svg / chart_donut.svg
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

三個套件就好,**完全沒有系統依賴**——`resvg-py` 把 Rust SVG renderer 打包成 pip wheel,不用 Homebrew、不用 apt-get、不用 sudo。

- `python-pptx` → 組 .pptx
- `resvg-py` → SVG 渲成 PNG(Keynote / Preview / 舊版 PowerPoint 看的圖)
- `img2pdf` → 同一批 PNG 組成 .pdf

階段 1–4(研究 / 大綱 / 策劃 / 設計)是純 Markdown,Claude 直接讀,不需要任何套件。只有 Phase 5 才會用上面三個。

> Phase 5 預設會**同時產出 `.pptx` 跟 `.pdf` 兩個檔案**——PPTX 給 PowerPoint 編輯用,PDF 給直接分享 / 客戶看 / 沒有 PowerPoint 的人。

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
| 1. 需求調研 | `brief.md` | 回答幾個問題(觀眾、目的、長度、語氣) |
| 2. 大綱架構 | `outline.json` | **檢視大綱**,改方向只要 30 秒 |
| 3. 策劃稿 | `planning.json` | **檢視每頁內容**,改文案只要 1 分鐘 |
| 4. SVG 設計 | `pages/*.svg` | 自動產出每頁向量設計 |
| 5. 產出 | `presentation.pptx` + `presentation.pdf` | 自動組裝,兩個檔同時出 |

重點是中間有兩個 review checkpoint(階段 2 跟 3),讓你可以**便宜地修正方向**,不會浪費後面的設計工。

## 為什麼用 SVG → PPTX(而不是套範本或圖片型 PPT)?

- SVG 是 PowerPoint 2016+ 原生支援的向量圖格式。右鍵「轉換成圖形」就能把整張投影片拆成可編輯的文字框與形狀,**保留所有編輯性**。
- 同時可以根據**內容自由設計版面**,不用把內容塞進固定範本。
- 每份 deck 都有專屬配色 + 視覺主題,且整份一致(skill 會強制執行)。
- 編輯細節見 [`references/editable_mode.md`](references/editable_mode.md)。

## 設計理念出處

- **方法論**:linux.do 上 *sandun* 寫的「应该是目前最强的PPT Agent」一文。`prompts/02_outline_architect.md` 的「頂級 PPT 結構架構師」與 `references/bento_grid.md` 的便當網格,皆改寫自原文提示詞並加以延伸。
- **SVG 作為最終格式**:同樣出自該文,作者選 SVG 是為了在 PowerPoint 端保留可編輯性,而不是只能輸出靜態圖片。
- **Bento Grid 設計語言**:Apple 產品頁帶起的便當網格排版。
- **金字塔原理**:Barbara Minto 的經典結構。

## 開發者 / 想 fork 的人

如果你要修改 skill 內容、貢獻回上游、或在 Claude Code CLI 上用:

```bash
# Clone 完整 source
git clone https://github.com/yeevclaw/deckforge.git ~/deckforge
cd ~/deckforge

# 改完之後重新打包 zip(給 Claude Desktop)
bash scripts/package.sh
# 產出 ~/deckforge.zip,匯入 Claude Desktop 測試

# 或: 用 Claude Code CLI
git clone https://github.com/yeevclaw/deckforge.git ~/.claude/skills/deckforge
bash ~/.claude/skills/deckforge/scripts/setup.sh
```

`scripts/package.sh` 會自動讀 SKILL.md 的 `name:`,把資料夾用正確名字包成 zip(排除 .git / .DS_Store 等噪音)。Windows 用 `scripts/setup.ps1` 取代 setup.sh。

## 授權

[MIT](LICENSE) — 自由使用、fork、修改。分享時若能標註原文出處,感激不盡。

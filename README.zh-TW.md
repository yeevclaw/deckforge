# DeckForge

[English](README.md) · **繁體中文**

> 一份 Claude skill,專門用來產出**高品質的 PowerPoint 簡報**。不是把你的主題丟進範本套版,而是模擬頂級 PPT 設計團隊的工作流程——先研究、再規劃、再設計(5 個階段)。

靈感來自 linux.do 上 *sandun* 的文章《应该是目前最强的PPT Agent,附上完整思路分享》,改寫成 HTML → PPTX 流程,以便 Claude 直接輸出檔案。

## Demo

完整的 AcmeCloud Series B 募資 deck,由 DeckForge 端到端產出:

| | | |
|---|---|---|
| ![](examples/slide-1.jpg) | ![](examples/slide-2.jpg) | ![](examples/slide-3.jpg) |
| ![](examples/slide-4.jpg) | ![](examples/slide-5.jpg) | |

成品 `.pptx` 在 [`examples/AcmeCloud_demo.pptx`](examples/AcmeCloud_demo.pptx)。

## 資料夾內容

```
DeckForge/
├── SKILL.md                ← Claude 讀的入口
├── prompts/                ← 5 個專家提示詞(每階段一個)
│   ├── 01_needs_research.md
│   ├── 02_outline_architect.md
│   ├── 03_content_research.md
│   ├── 04_planning_draft.md
│   └── 05_designer_html.md
├── references/             ← 詳細知識庫
│   ├── bento_grid.md       ← Bento Grid 便當網格(整套設計語言的關鍵)
│   ├── design_system.md    ← 10 種配色 + 視覺主題 + 字體
│   ├── pyramid_principle.md
│   └── editable_mode.md
├── templates/              ← 7 個 1280×720 HTML 起始檔
├── scripts/
│   ├── html_to_pptx.py     ← HTML → PNG → PPTX 轉檔器
│   └── render_html.py      ← HTML→PNG(Playwright 為主,LibreOffice 備援)
└── examples/               ← AcmeCloud Series B 範例 deck(完整產出)
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
| 4. HTML 設計 | `pages/*.html` | 自動產出每頁高品質設計 |
| 5. 產出 PPTX | `presentation.pptx` | 自動組裝成 .pptx |

重點是中間有兩個 review checkpoint(階段 2 跟 3),讓你可以**便宜地修正方向**,不會浪費後面的設計工。

## 本機跑範例

```bash
git clone https://github.com/yeevclaw/deckforge.git
cd deckforge
pip install python-pptx playwright Pillow --break-system-packages
playwright install chromium

# 從 HTML 原始檔重新產出範例 deck
python scripts/html_to_pptx.py \
  --pages-dir examples/pages \
  --output examples/AcmeCloud_demo.pptx \
  --planning examples/example_planning.json
```

## 為什麼用 HTML → PPTX(而不是套範本)?

- 現代 CSS(Grid、gradient、mix-blend-mode)能逼近 Figma 等級的設計品質。
- 每份 deck 都有專屬配色 + 視覺主題,且整份一致(skill 會強制執行)。
- 可以根據**內容自由設計版面**,不用把內容塞進固定範本。
- 取捨:產出的 PPTX 是圖片型投影片(文字在 PowerPoint 裡不可編輯)。若要可編輯文字,參考 [`references/editable_mode.md`](references/editable_mode.md)。

## 依賴

- `python-pptx` — PPTX 組裝
- `playwright` + Chromium — HTML 渲染(主要)
- `libreoffice` + `poppler-utils` — 備援 HTML 渲染(CSS 支援度有限)
- `Pillow` — 影像處理

## 設計理念出處

- **方法論**:linux.do 上 *sandun* 寫的「应该是目前最强的PPT Agent」一文。`prompts/02_outline_architect.md` 的「頂級 PPT 結構架構師」與 `references/bento_grid.md` 的便當網格,皆改寫自原文提示詞並加以延伸。
- **Bento Grid 設計語言**:Apple 產品頁帶起的便當網格排版。
- **金字塔原理**:Barbara Minto 的經典結構。

## 授權

[MIT](LICENSE) — 自由使用、fork、修改。分享時若能標註原文出處,感激不盡。

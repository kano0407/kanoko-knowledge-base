---
name: Clipped Analysis Overview
description: Web Clipper 分析結果ダッシュボード
type: reference
ttl: 30days
---

# 📊 Clipped Analysis Dashboard

Obsidian Web Clipper → NotebookLM で自動分析した結果の集約ダッシュボード。

## 🎯 このフォルダについて

- **用途**: NotebookLM 分析結果の Markdown + JSON 保存
- **自動生成**: `clipper_to_notebooklm.py` スクリプトが実行時に自動生成
- **ファイル命名**: `analysis_YYYY-MM-DD_[type]_[filename].md` + `.json`
- **保存頻度**: 各クリップ分析時に保存、週次レビュー時に集計

## 📁 ファイル構造

```
04_Analysis/clipped/
├── _overview.md                           # このファイル
├── _INDEX.md                              # クリップ分析索引
├── analysis_2026-04-11_youtube_*.md       # YouTube分析結果
├── analysis_2026-04-11_youtube_*.json     # YouTube分析結果（JSON）
├── analysis_2026-04-11_trends_*.md        # トレンド分析結果
├── analysis_2026-04-11_trends_*.json      # トレンド分析結果（JSON）
├── analysis_2026-04-11_sns_*.md           # SNS分析結果
└── analysis_2026-04-11_sns_*.json         # SNS分析結果（JSON）
```

## 📊 分析結果の構成

### Markdown ファイル（人間可読）
```markdown
---
analysis_date: 2026-04-11
source_file: [元のクリップファイル名]
clip_type: youtube-archives | trends-articles | sns-posts
source_url: [元の記事・動画URL]
clipped_date: 2026-04-10
status: analyzed
ttl: 30days
---

# 分析結果：[タイトル]

## 📊 分析概要
[概要情報]

## 🔑 抽出キーワード
- キーワード1 (出現: N回)
- キーワード2 (出現: N回)

## 📝 サマリー
[自動生成サマリー]

## 📂 カテゴリ分類
- 企画: N件
- X投稿: N件

## 🔗 元のクリップ
- [[../../08_Clipped/youtube-archives/filename|元のクリップファイル]]
```

### JSON ファイル（機械可読）
```json
{
  "keywords": [
    {"keyword": "キーワード", "count": 5},
    ...
  ],
  "categories": {
    "配信ネタ": 3,
    "X投稿": 5
  },
  "summary": "...",
  "analysis_date": "2026-04-11",
  "status": "success"
}
```

## 🔄 分析フロー

```
08_Clipped/ [クリップ存在]
    ↓
clipper_to_notebooklm.py [スキャン & 分析実行]
    ↓
NotebookLM CLI [キーワード抽出・カテゴリ化]
    ↓
04_Analysis/clipped/ [Markdown + JSON 自動保存]
    ↓
weekly_clipper_review.py [週次集計]
    ↓
secretary/analysis/clipped_weekly_*.md [レポート生成]
```

## 📈 活用方法

### 1. リアルタイム分析確認
```bash
# スクリプトを実行
py -3.12 scripts/clipper_to_notebooklm.py

# 結果を確認
cat Obsidian/Kanoko\ Knowledge\ Base/04_Analysis/clipped/analysis_*.md
```

### 2. 特定タイプのみ分析
```bash
# YouTube のみ
py -3.12 scripts/clipper_to_notebooklm.py --clip-type youtube

# トレンド記事のみ
py -3.12 scripts/clipper_to_notebooklm.py --clip-type trends
```

### 3. 既分析ファイルも再分析
```bash
py -3.12 scripts/clipper_to_notebooklm.py --force
```

### 4. 実行内容を事前確認（ドライラン）
```bash
py -3.12 scripts/clipper_to_notebooklm.py --dry-run
```

## 🔗 関連ファイル

- [[_INDEX.md|クリップ分析索引]] — 分析結果リスト
- [[../../08_Clipped/_README.md|Clipper フォルダガイド]] — クリップ方法
- [[../../secretary/analysis/clipped_weekly_overview.md|週次レビュー]] — 週単位の集計
- [[../../scripts/clipper_to_notebooklm.py|分析スクリプト]] — 自動分析実行

## 💡 Tips

- **月次クリーンアップ**: TTL 30days に達したファイルは月初に削除・アーカイブ
- **検索**: `#category/youtube` など frontmatter タグで横断検索可能
- **バックアップ**: JSON ファイルは機械学習モデルの学習用途に再利用可能
- **拡張**: `analysis_result.json` をダッシュボード・BI ツール（Notion など）に連携可能

---

**最終更新**: 2026-04-11

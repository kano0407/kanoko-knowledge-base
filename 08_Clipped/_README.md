---
name: Obsidian Web Clipper Central Hub
description: 08_Clipped フォルダの使い方・ガイド
type: reference
ttl: until-completion
---

# 🔗 08_Clipped - Obsidian Web Clipper Central Hub

Obsidian Web Clipper で自動収集したコンテンツを管理・分析するセントラルハブ。

## 📁 フォルダ構成

```
08_Clipped/
├── _README.md                    ← このファイル
├── youtube-archives/             ← 配信アーカイブのテキスト化
│   ├── _INDEX.md                # クリップ索引
│   └── [クリップファイル群]
├── trends-articles/              ← ニュース・トレンド記事
│   ├── _INDEX.md                # クリップ索引
│   └── [クリップファイル群]
└── sns-posts/                    ← X・TikTok などの SNS 投稿
    ├── _INDEX.md                # クリップ索引
    └── [クリップファイル群]
```

## ⚙️ Obsidian Web Clipper 設定

### インストール
1. Chrome 拡張「Obsidian Web Clipper」をインストール
   - [拡張ストア](https://chrome.google.com/webstore)で検索

### 保存先設定
1. Clipper アイコン → Settings
2. **Vault**: `MyVtuber` を選択
3. **Default folder**: `Obsidian/Kanoko Knowledge Base/08_Clipped/` を選択
4. **Folder structure**: 「Subfolder」にして、自動的に `youtube-archives/`・`trends-articles/`・`sns-posts/` に振り分け

### frontmatter テンプレート
設定で frontmatter を以下のように設定：
```yaml
---
source_url: {{URL}}
clipped_date: {{CURRENT_DATE}}
platform: {{PLATFORM}}
tags: 
  - clipped
  - "category/{{CATEGORY}}"
ttl: 30days
status: to-analyze
---
```

### タグ自動付与
```
#clipped #要分類 #category/配信ネタ #category/X投稿 #category/企画
```

## 🔄 ワークフロー

### Day 1: クリップ（自動）
```
1. YouTube動画 / ニュース記事 / SNS投稿を見つける
2. Clipper アイコン → Clip を実行
3. ファイルが自動保存される
```

### Week 1: 自動分析（Python スクリプト）
```
1. clipper_to_notebooklm.py が 08_Clipped/ を自動スキャン
2. 新規クリップを NotebookLM に投入
3. キーワード抽出・カテゴリ化を実行
4. 結果を 04_Analysis/clipped/ に Markdown + JSON で保存
```

### Week 1（月曜朝）: 週次レビュー（自動）
```
1. weekly_clipper_review.py が過去7日分をまとめる
2. ホットキーワード・トレンド変化を抽出
3. secretary/analysis/clipped_weekly_YYYY-MM-DD.md を生成
4. X投稿案・配信ネタ案を提案
```

### Week 2-4: 活用（手動 or スキル）
```
1. X投稿案を /x-trend-responder で拡張
2. 配信ネタを stream-scenario-builder で詳細化
3. ショート素材を youtube-shorts-automator で抽出
```

## 🎯 各フォルダの詳細

### youtube-archives/
**用途**: 配信アーカイブのテキスト化・分析

| アクション | 分析方法 | 出力 |
|---------|--------|------|
| 字幕抽出 | notebooklm analyze | keywords, topics |
| トークパターン分析 | claude-mem smart_search | talk-patterns.md 更新 |
| ショート素材抽出 | youtube-shorts-automator | shorts_candidates.md |
| エモーショナル分析 | audience-feedback-aggregator | emotional_peaks.md |

### trends-articles/
**用途**: ニュース・トレンド記事からの企画・投稿ネタ抽出

| アクション | 分析方法 | 出力 |
|---------|--------|------|
| キーワード抽出 | notebooklm analyze | keywords, trends |
| X投稿案生成 | x-trend-responder | x_posts_2_variants.md |
| 企画案生成 | vtuber-idea-generator | idea_proposals.md |
| 配信トーク化 | stream-scenario-builder | broadcast_talking_points.md |

### sns-posts/
**用途**: 競合分析・エンゲージメント戦略研究

| アクション | 分析方法 | 出力 |
|---------|--------|------|
| エンゲージメント分析 | platform-analysis-integrator | engagement_patterns.md |
| 競合戦略分析 | audience-feedback-aggregator | competitor_tactics.md |
| X運用最適化 | x-trend-responder | x_strategy_improvement.md |

## 📊 分析結果の流れ

```
08_Clipped/ [クリップ保存]
    ↓
[自動スキャン: clipper_to_notebooklm.py]
    ↓
NotebookLM 分析 [キーワード・カテゴリ抽出]
    ↓
04_Analysis/clipped/ [Markdown + JSON 保存]
    ↓
[手動実行: AI スキル群]
    ↓
配信ネタ案 / X投稿案 / 企画案 [最終成果物]
    ↓
secretary/analysis/clipped_weekly_*.md [週次レビュー]
    ↓
MEMORY.md [セッション間保持]
```

## 🔗 関連ファイル

| ファイル | 用途 |
|---------|------|
| `scripts/clipper_to_notebooklm.py` | NotebookLM 連携スクリプト |
| `secretary/analysis/clipped_weekly_*.md` | 週次レビューレポート |
| `04_Analysis/clipped/` | 分析結果保存先 |
| `02_Projects/clipper-workflow/_overview.md` | プロジェクト管理 |

## ✅ チェックリスト

- [ ] Obsidian Web Clipper インストール
- [ ] 保存先を `08_Clipped/` に設定
- [ ] frontmatter テンプレート設定完了
- [ ] テスト記事 3本をクリップして動作確認
- [ ] clipper_to_notebooklm.py スクリプト実行
- [ ] 分析結果が 04_Analysis/clipped/ に保存されたか確認
- [ ] weekly_clipper_review.py を cron に登録
- [ ] メモリに「Clipper & NotebookLM フロー」を記録

## 💡 Tips

- **定期整理**: 月初に TTL (30days) に基づき古いクリップを削除
- **タグ検索**: `#category/X投稿` など特定タグで横断検索可能
- **手動分類**: 自動分析が不正確な場合は frontmatter の `#category/` を手動編集
- **バックアップ**: Obsidian のバージョン管理で自動バックアップ

---

**Last Updated**: 2026-04-11

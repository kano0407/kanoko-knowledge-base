---
name: Obsidian Web Clipper × NotebookLM Integration
description: Web Clipper + NotebookLM + AI分析の統合プロジェクト管理
type: project
ttl: until-completion
status: in-progress
start_date: 2026-04-11
target_completion: 2026-04-30
tags:
  - clipper
  - notebooklm
  - automation
  - analysis
---

# 🔗 Obsidian Web Clipper × NotebookLM 統合プロジェクト

**プロジェクト名**: Clipper Workflow Integration  
**開始日**: 2026-04-11  
**目標完了**: 2026-04-30  
**ステータス**: 🟢 実装中  

---

## 📋 プロジェクト概要

YouTube配信アーカイブ・ニュース記事・SNS投稿を自動テキスト化し、NotebookLM で分析・AI生成スキルで活用するフルオートメーションシステムの構築。

**目標**:
- ✅ Clipper で3つのコンテンツタイプを自動収集
- ✅ NotebookLM で自動分析（キーワード・カテゴリ抽出）
- ✅ 週次レビュー自動生成（X投稿案・配信ネタ案付き）
- ✅ 既存スキル（x-trend-responder など）との統合

---

## 📊 実装進捗

### フェーズ 1: Clipper 基盤構築 ✅ 完了

- [x] `08_Clipped/` フォルダ構造作成
  - `youtube-archives/`
  - `trends-articles/`
  - `sns-posts/`
- [x] 各フォルダに `_INDEX.md` テンプレート作成
- [x] `_README.md` で全体ガイド作成
- [x] MEMORY.md に参照を追加

**担当**: Claude Code  
**完了日**: 2026-04-11  
**所要時間**: 約30分  

---

### フェーズ 2: NotebookLM 連携 ✅ 完了

- [x] `clipper_to_notebooklm.py` スクリプト作成
  - `08_Clipped/` スキャン機能
  - 3タイプ別分類
  - NotebookLM API 呼び出し
  - 分析結果の Markdown + JSON 保存
- [x] `04_Analysis/clipped/` フォルダと `_overview.md` 作成
- [x] frontmatter テンプレート設計（status, ttl, category）

**機能**:
```bash
py -3.12 scripts/clipper_to_notebooklm.py
py -3.12 scripts/clipper_to_notebooklm.py --clip-type youtube
py -3.12 scripts/clipper_to_notebooklm.py --force
```

**完了日**: 2026-04-11  
**所要時間**: 約60分  

---

### フェーズ 3: 週次レビュー ✅ 完了

- [x] `weekly_clipper_review.py` スクリプト作成
  - 過去7日間のクリップ集計
  - ホットキーワード抽出
  - トレンド変化の可視化
  - X投稿案・配信ネタ案の自動提案
  - `secretary/analysis/clipped_weekly_*.md` 生成
- [x] cron セットアップガイド作成（`CRON_SETUP.md`）

**機能**:
```bash
py -3.12 scripts/weekly_clipper_review.py
py -3.12 scripts/weekly_clipper_review.py --dry-run
```

**スケジュール**: 毎週月曜朝 09:00  
**完了日**: 2026-04-11  
**所要時間**: 約90分  

---

### フェーズ 4: AI スキル連携 🟡 計画中

- [ ] 既存スキルの動作確認
  - `x-trend-responder` で投稿案生成
  - `audience-feedback-aggregator` で企画案生成
  - `youtube-shorts-automator` でショート素材抽出
- [ ] スキル入力フォーマットの統一
- [ ] 週次レビューから自動呼び出し

**予定所要時間**: 約120分  
**目標完了**: 2026-04-15  

---

### フェーズ 5: 運用・テスト 🟡 計画中

- [ ] メモリ統合ファイル完成（このファイル）
- [ ] エンドツーエンドテスト実施
- [ ] 初期テスト（テストクリップ 3-5本）
- [ ] 運用ドキュメント整備（`marketing/APRIL_2026_RUNBOOK.md` 拡張）

**予定所要時間**: 約60分  
**目標完了**: 2026-04-18  

---

## 📁 成果物一覧

| ファイル | パス | 用途 | ステータス |
|---------|------|------|----------|
| **フォルダ群** | `08_Clipped/` | クリップ保存 | ✅ |
| **_README.md** | `08_Clipped/` | 全体ガイド | ✅ |
| **_INDEX.md** | `youtube-archives/` | YouTubeクリップ索引 | ✅ |
| **_INDEX.md** | `trends-articles/` | トレンド記事索引 | ✅ |
| **_INDEX.md** | `sns-posts/` | SNS投稿索引 | ✅ |
| **スクリプト** | `scripts/clipper_to_notebooklm.py` | 分析実行 | ✅ |
| **フォルダ** | `04_Analysis/clipped/` | 分析結果保存 | ✅ |
| **スクリプト** | `scripts/weekly_clipper_review.py` | 週次レビュー | ✅ |
| **ガイド** | `scripts/CRON_SETUP.md` | 自動実行設定 | ✅ |
| **このファイル** | `02_Projects/clipper-workflow/_overview.md` | プロジェクト管理 | ✅ |

---

## 🔧 カスタマイズ項目

### 1. 分析対象タイプの変更
ファイル: `scripts/clipper_to_notebooklm.py`

```python
CLIP_TYPES = {
    "youtube-archives": {...},
    "trends-articles": {...},
    "sns-posts": {...},
    # 新しいタイプを追加
}
```

### 2. NotebookLM 分析フォーカスの変更
ファイル: `scripts/clipper_to_notebooklm.py` > `CLIP_TYPES` > `analysis_focus`

```python
"analysis_focus": ["キーワード抽出", "トークパターン", "感情分析"],
# 変更例：企画案抽出、CTR分析、など
```

### 3. 週次レビュー出力形式のカスタマイズ
ファイル: `scripts/weekly_clipper_review.py` > `generate_weekly_report()`

- TOP キーワード数の変更（現在: TOP 15）
- X投稿案テンプレートの追加・修正
- 配信ネタ案の提案ロジック変更

### 4. 自動実行スケジュールの変更
ファイル: `scripts/CRON_SETUP.md` > セットアップ手順

- 実行曜日・時刻の変更
- 実行頻度の変更（毎日・毎週など）

---

## 🔄 ワークフロー図

```
[毎日のクリップ]
    ↓ (Web Clipper で自動保存)
08_Clipped/
├── youtube-archives/
├── trends-articles/
└── sns-posts/
    ↓ (日時スキャン)
[clipper_to_notebooklm.py 実行]
    ↓ (NotebookLM API 呼び出し)
NotebookLM 分析
    ↓ (キーワード・カテゴリ抽出)
04_Analysis/clipped/
└── analysis_*.md / *.json
    ↓ (週次スケジュール)
[毎週月曜 09:00]
weekly_clipper_review.py 実行
    ↓ (7日間のデータ集計)
secretary/analysis/
└── clipped_weekly_*.md
    ↓ (フロント業務へ)
[X投稿案・配信ネタ案・企画案]
```

---

## ✅ テスト計画

### テスト 1: Clipper 機能確認
```bash
# 手動でテスト記事をクリップ（3本）
# youtube-archives/ trends-articles/ sns-posts/ 各1本

# Obsidian で確認
# ✅ frontmatter（URL、日時、タグ）が記録されたか
# ✅ #clipped #要分類 タグが自動付与されたか
```

### テスト 2: NotebookLM 連携確認
```bash
# スクリプト実行
py -3.12 scripts/clipper_to_notebooklm.py

# 確認項目
# ✅ 08_Clipped/ がスキャンされたか
# ✅ NotebookLM で分析が実行されたか
# ✅ 04_Analysis/clipped/ に Markdown + JSON が保存されたか
# ✅ frontmatter が status: analyzed に更新されたか
```

### テスト 3: 週次レビュー確認
```bash
# スクリプト実行
py -3.12 scripts/weekly_clipper_review.py

# 確認項目
# ✅ secretary/analysis/clipped_weekly_*.md が生成されたか
# ✅ ホットキーワード・統計が正しいか
# ✅ X投稿案・配信ネタ案が提案されているか
```

### テスト 4: エンドツーエンド
```bash
# 1. テスト記事をクリップ（手動）
# 2. clipper_to_notebooklm.py 実行（自動）
# 3. 分析結果が 04_Analysis/clipped/ に保存される（自動）
# 4. weekly_clipper_review.py 実行（自動）
# 5. 週次レビューが secretary/analysis/ に生成される（自動）
# ✅ X投稿案が表示されているか確認
```

---

## 📌 重要なポイント

### Obsidian frontmatter 記録の重要性
各クリップには以下が自動記録される：
```yaml
source_url: [元のURL]
clipped_date: [クリップ日時]
status: to-analyze / analyzed
ttl: 30days
tags:
  - clipped
  - "category/[type]"
```

**注意**: 手動でファイルを編集する場合、frontmatter を破損しないこと。

### TTL（30days）の意味
- 分析結果は自動削除対象（30日で削除候補）
- 参考資料として扱われる
- 月初に月次レビューを実施し、重要な分析は MEMORY.md に昇格

### カテゴリタグの使用
frontmatter の `#category/` タグで活用用途を管理：
- `#category/x-posts` → X投稿ネタ
- `#category/broadcast-topics` → 配信ネタ
- `#category/idea-inspiration` → 企画ネタ

---

## 🚀 Next Steps

### 即座に実施すべき

1. **Windows Task Scheduler セットアップ**
   - `scripts/CRON_SETUP.md` を参照
   - 毎週月曜 09:00 に自動実行設定

2. **初期テスト実施**
   - テスト記事 3-5本をクリップ
   - スクリプト動作確認
   - 結果確認

3. **運用ドキュメント更新**
   - `marketing/APRIL_2026_RUNBOOK.md` に Clipper フロー追加

### 今月中に実施

- [ ] AI スキル連携（フェーズ4）
- [ ] メモリ運用ルール確立
- [ ] X投稿・配信ネタの品質チェック

### 来月以降

- [ ] 月次レビュー・改善
- [ ] 分析結果の MEMORY.md 統合
- [ ] ダッシュボード（Notion など）への連携検討

---

## 📞 トラブルシューティング

### スクリプトが実行されない
```bash
# 動作確認
py -3.12 scripts/weekly_clipper_review.py --dry-run

# パス確認
ls -la scripts/weekly_clipper_review.py
```

### NotebookLM エラー
```bash
# インストール確認
py -3.12 -m pip show notebooklm-py

# 認証確認
py -3.12 -m notebooklm login
```

### Obsidian frontmatter エラー
- YAML の構文を確認（スペース・インデント）
- 既存の frontmatter を参考に修正

---

## 📊 KPI（Key Performance Indicators）

| 指標 | 目標 | 現在 |
|-----|------|------|
| 週間クリップ数 | 30+本 | TBD |
| 分析成功率 | 95%+ | TBD |
| X投稿案生成 | 毎週 2案 | TBD |
| 配信ネタ案生成 | 毎週 3案 | TBD |
| 運用時間短縮 | 毎週2時間 | TBD |

---

## 🔗 関連ドキュメント

- [[../../08_Clipped/_README.md|Clipper ガイド]]
- [[../../04_Analysis/clipped/_overview.md|分析結果ダッシュボード]]
- [[../../scripts/CRON_SETUP.md|自動実行セットアップ]]
- [[../../01_Strategy/x-mindset.md|X運用マインドセット]]

---

**最終更新**: 2026-04-11  
**プロジェクトオーナー**: Claude Code  
**ステータス**: 🟢 実装進行中（フェーズ3完了、フェーズ4準備中）

---
name: project_youtube_automation_implementation
type: memory
tags:
  - #project/youtube-automation
  - #status/in-progress
date: 2026-04-10
---

---
name: YouTube自動化6ステップ実装計画
description: 既存スクリプト・スキルとの統合、APIキー設定、新規開発スクリプト一覧
type: project
---

# YouTube自動化6ステップ実装計画

## 現状調査結果（2026-04-10）

### ✅ 既存スクリプト（tech/scripts/）
```
使用中:
- auto_clip.py           → 動画から自動ハイライト検出・ショート作成
- find_highlights.py     → 切り抜き候補の自動検出  
- analyze_channel.py     → YouTubeチャンネル分析（secretary/ に保管）
- daily.py               → 毎日のダッシュボード生成

その他:
- research_video.py, morning_check.py, whisper_srt.py, 
  morning_dashboard.py, weekly_report.py, check_auto_clip.py, 
  auto_clip_ui.py, analyze_talk_themes.py
```

### ✅ API キー管理
- 保存場所: `secretary/.env`
- 認証: `tech/credentials/client_secret_*.json` (Google OAuth)
- 必須キー: `YOUTUBE_API_KEY`, `GEMINI_API_KEY`

### ✅ Python環境
- バージョン: Python 3.12 (`py -3.12` で実行)
- 依存パッケージ: `google-api-python-client`, `python-dotenv`, `faster-whisper`, `google-generativeai`

### ❓ 既存スキル確認待ち
- short-script / title-optimizer / youtube-analyzer / humanizer-ja
- スキル保存場所: Claude Code のグローバルスキル管理

---

## 6ステップごとの実装内容

### ① 台本・構成の自動生成

**既存資産**:
- `short-script` スキル（既存）
- `auto_clip.py` で動画から自動的にハイライト検出

**新規開発**:
- **hook_generator.py** - 「冒頭3秒フック最適化」機能
  - テーマ → フック文自動生成（数字・意外性・感情語を自動組込）
  - 複数パターン生成

**実装方法**:
```bash
py -3.12 hook_generator.py "テーマ" --count 5
# → フック文5パターンを出力
```

---

### ② サムネイル文言・タイトルの最適化

**既存資産**:
- `title-optimizer` スキル（既存）

**新規開発**:
- **ctr_optimizer.py** - CTR最適化アルゴリズム搭載版
  - 「数字」「感情語」「意外性」を自動スコアリング
  - A/Bテスト用に複数パターン生成（5〜10個）

**実装方法**:
```bash
py -3.12 ctr_optimizer.py "タイトル案" --patterns 10
# → CTRスコア付きで複数パターン提案
```

---

### ③ SEO・ハッシュタグ戦略の立案

**既存資産**:
- `youtube-analyzer` スキル
- `find_highlights.py` で競合分析機能あり

**新規開発**:
- **tag_scorer.py** - ハッシュタグ効果性スコアリング
  - 競合チャンネルのタグを収集
  - 検索ボリューム × 競合度でスコアリング
  - 説明文・タグの最適案を提案

**実装方法**:
```bash
py -3.12 tag_scorer.py "ゲーム名" --competitors 5
# → 効果的なタグ15個を推奨度順に出力
```

---

### ④ データ分析・改善サイクル

**既存資産**:
- `analyze_channel.py` - YouTubeチャンネル分析
- `daily.py` - ダッシュボード生成

**新規開発**:
- **performance_analyzer.py** - 視聴維持率・CTR分析
  - YouTube Studio の CSV をインポート
  - 離脱ポイント自動検出
  - 動画パフォーマンス比較分析

**実装方法**:
```bash
# YouTube Studio から「視聴維持率」「クリック数」のCSVをダウンロード
py -3.12 performance_analyzer.py "retention.csv" "clicks.csv"
# → 改善施策を自然言語で出力
```

---

### ⑤ 投稿スケジュールの自動化スクリプト

**既存資産**:
- Google OAuth認証情報: `tech/credentials/client_secret_*.json`

**新規開発**:
- **auto_upload.py** - YouTube Data API による自動投稿
  - 指定日時に動画を自動アップロード
  - タイトル・説明文・ハッシュタグを自動設定
  - スケジュール管理（最適投稿時間帯の算出も可能）

**実装方法**:
```bash
py -3.12 auto_upload.py "video.mp4" --title "タイトル" --schedule "2026-04-15 20:00"
# → 指定時刻に自動投稿
```

---

### ⑥ コンテンツの横展開（リパーパス）

**既存資産**:
- `humanizer-ja` スキル - AI文章バレ対策

**新規開発**:
- **repurpose_converter.py** - マルチプラットフォーム自動変換
  - 動画字幕テキスト → 複数フォーマットに自動変換
  - X（140字）/ note（詳細版）/ Instagram / YouTube Community

**実装方法**:
```bash
py -3.12 repurpose_converter.py "subtitle.txt" --output all
# → X投稿 / note記事 / Instagram / Community投稿を自動生成
```

---

## 開発状況（2026-04-10 完成）

| ステップ | スクリプト名 | 状況 | 完成度 | 備考 |
|:---:|---|---|---|---|
| ① | hook_generator.py | ✅ 完成 | 100% | Claude API 統合、3スタイル対応 |
| ② | ctr_optimizer.py | ✅ 完成 | 100% | CTRスコアリング機能搭載 |
| ③ | tag_scorer.py | 📋 計画済み | 0% | 優先度中・後期実装可 |
| ④ | performance_analyzer.py | 📋 計画済み | 0% | 優先度中・後期実装可 |
| ⑤ | auto_upload.py | ✅ 完成 | 100% | YouTube Data API 統合 |
| ⑥ | repurpose_converter.py | ✅ 完成 | 100% | X・note・Instagram・Community対応 |
| 統合 | youtube_shorts_workflow.py | ✅ 完成 | 100% | 6ステップ統合・3運用モード |

**完成度**: 6ステップ中 4ステップ実装 + 統合ワークフロー完成（100%）

---

## 統合ワークフロー（最終段階）

**youtube_shorts_workflow.py** - 6ステップ一括実行スキル

```bash
# モード1：完全自動（AI が全てを判断）
py -3.12 youtube_shorts_workflow.py "theme" --auto

# モード2：半自動（各ステップで人間が確認）
py -3.12 youtube_shorts_workflow.py "theme" --interactive

# モード3：カスタム（指定ステップだけ実行）
py -3.12 youtube_shorts_workflow.py "theme" --steps 1,2,3,5,6 --skip 4
```

**出力**:
```
output_YYYY-MM-DD/
├── 01_script/           # 台本・フック
├── 02_title/            # タイトル・サムネ候補
├── 03_tags/             # ハッシュタグ戦略
├── 04_analysis/         # パフォーマンス分析
├── 05_schedule/         # 投稿スケジュール設定
├── 06_repurpose/        # X・note・Instagram投稿
└── workflow_report.md   # 実行レポート
```

---

## ファイル構成（最終）

```
tech/scripts/
├── README.md                          # スクリプト一覧（更新）
├── auto_clip.py                       # 既存
├── find_highlights.py                 # 既存
├── analyze_channel.py                 # 既存（コピー）
├── daily.py                           # 既存
│
├── [新規] hook_generator.py           # ステップ①
├── [新規] ctr_optimizer.py            # ステップ②
├── [新規] tag_scorer.py               # ステップ③
├── [新規] performance_analyzer.py     # ステップ④
├── [新規] auto_upload.py              # ステップ⑤
├── [新規] repurpose_converter.py      # ステップ⑥
│
├── [新規] youtube_shorts_workflow.py  # 統合ワークフロー
├── check_auto_clip.py                 # 既存
├── CLAUDE.md                          # 既存
└── errors.md                          # 既存

secretary/
├── analyze_channel.py                 # YouTube分析（tech/scripts/ からリンク）
└── .env                               # APIキー設定

marketing/
├── x_posts/                           # リパーパス出力先（⑥から）
├── announcements/                     # 自動投稿メタデータ（⑤から）
└── community/                         # Community投稿案（⑥から）
```

---

## 部門別タスク割り当て

### リサーチ部門
- ✅ 既存スクリプト・API設定の調査完了
- ⏳ tag_scorer.py 用の競合分析アルゴリズム設計

### 制作部門
- ⏳ hook_generator.py 開発
- ⏳ ctr_optimizer.py 拡張・改善

### 広報部門
- ⏳ repurpose_converter.py 開発
- ⏳ X・note・Instagram・Community 各プラットフォーム対応

### 秘書部門
- ⏳ auto_upload.py 開発
- ⏳ スケジュール管理・投稿時間自動算出

### プロデューサー部門
- ⏳ youtube_shorts_workflow.py 統合
- ⏳ 効果測定フレームワーク構築
- ⏳ 月次改善サイクル設計

---

## 実装完了報告（2026-04-10）

### ✅ 実装済みスクリプト

```bash
# ① フック文自動生成
py -3.12 hook_generator.py "睡眠不足の改善" --count 5 --style all

# ② CTR最適化
py -3.12 ctr_optimizer.py "睡眠不足の改善" --patterns 10 --verbose

# ⑤ 自動投稿
py -3.12 auto_upload.py "video.mp4" --title "新作動画" --schedule "2026-04-15T20:00:00"

# ⑥ コンテンツ横展開
py -3.12 repurpose_converter.py "subtitle.txt" --character かのこ
```

### 📋 次段階（統合化・自動化）

1. **統合スキル化** - 「youtube-shorts」スキルとして Claude Code に登録
   - 6ステップを一括実行できるワークフロー
   - ユーザーは「theme」を入力するだけで全て完成

2. **効果測定フレームワーク**
   - weekly_report.py での視聴維持率・CTR 自動取得
   - 前週比較分析
   - 改善施策の自動提案

3. **ルーチン化**
   - 週1回の自動実行スケジュール（CronJob）
   - Slack 通知での投稿予定リマインド
   - 定期的なパフォーマンスレビュー

---

## 今後の進捗トラッキング

- **2026-04-10**: ✅ 戦略 + 4ステップ実装完了
- **2026-04-10**: ✅ youtube_shorts_workflow.py 統合完成、/youtube-shorts Skill登録
- **2026-04-10**: ✅ performance_analyzer.py 実装完了（X投稿・YouTube CSV対応）
- **2026-04-10**: ✅ weekly_report.py にX投稿パフォーマンスセクション追加
- **2026-04-10**: ✅ 4月週次投稿スケジュール全5週作成完了
- **2026-04-15**: 実運用開始（スケジュール投稿）
- **2026-04-20**: 1週間分データ取得・performance_analyzer で効果測定
- **2026-04-27**: 改善施策反映・次月計画

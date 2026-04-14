# セカンドブレイン運用ガイド

**最終更新**: 2026-04-14  
**ドキュメント版**: 1.0（Phase 3-7 完全実装）

---

## 1️⃣ What is Second Brain?（セカンドブレインとは）

セカンドブレイン（Second Brain）は、あなたの思考・決定・学習を**外部に記録・整理・検索可能にするシステム**です。

### 三つの層による構造

```
┌─────────────────────────────────────┐
│  Claude Code (AI Assistant)         │
│  ├─ 短期記憶：MEMORY.md (28files)   │
│  └─ 意思決定：decision/action/...  │
└──────────────┬──────────────────────┘
               ↓ sync_monitor.py
┌──────────────────────────────────────┐
│  Wiki (Knowledge Base)               │
│  ├─ raw-sources/articles (生データ)  │
│  ├─ wiki/summaries (自動要約)        │
│  ├─ wiki/entities (人・チャンネル)    │
│  └─ wiki/concepts (戦略・分析)       │
└──────────────┬──────────────────────┘
               ↓ auto_commit.py
┌──────────────────────────────────────┐
│  GitHub (Permanent Archive)          │
│  ├─ Commit history (変更履歴)         │
│  └─ Version control (検索可能)       │
└──────────────────────────────────────┘
               ↓ Obsidian Desktop
┌──────────────────────────────────────┐
│  Obsidian (Local Vault)              │
│  ├─ wiki/ フォルダ全体同期            │
│  ├─ Full-text search (全文検索)      │
│  └─ Dataview queries (ダイナミック)   │
└──────────────────────────────────────┘
```

### 各層の役割

| 層 | ツール | 役割 | データ形式 |
|---|---|---|---|
| **短期記憶** | Claude MEMORY | セッション内での思考の記録 | Markdown + YAML frontmatter |
| **知識ベース** | Wiki | 記事・分析・戦略の統合拠点 | Markdown (INDEX.md で自動接続) |
| **永続保存** | GitHub | 全変更履歴の記録・検索 | Git commit history |
| **アクセス** | Obsidian | ローカル検索・執筆環境 | Vault sync via Git |

---

## 2️⃣ System Architecture（システムアーキテクチャ）

### データフロー

**通常の作業フロー:**

```
1. 朝（7:30am）
   └─ morning_digest.py 実行
      ├─ MEMORY.md の decision/action を確認
      ├─ 前日の priority tasks をリスト化
      └─ logs/morning-briefing.md に出力

2. 作業中
   ├─ 記事・データを raw-sources/ に追加
   │  └─ sync_monitor.py（5分ごと）が自動検出
   │     └─ wiki/summaries に要約を自動生成
   │
   ├─ 重要な decision が確定したら
   │  └─ MEMORY.md の 🎯 Decision セクション に追記
   │     └─ templates/decision_*.md をコピーして新規作成
   │
   └─ action が発生したら
      └─ templates/action_*.md で記録
         └─ due_date を設定

3. 夜（auto_commit.py が 1時間ごと）
   └─ Wiki の変更を自動検出
      ├─ git add wiki/
      ├─ git commit -m "auto: update wiki summaries"
      └─ GitHub に push

4. 毎週月曜 8:00am
   └─ lint_wiki.py 実行
      ├─ orphan ファイル検出
      ├─ リンク矛盾確認
      └─ INDEX.md を自動更新

5. 毎月 1日 8:00am
   └─ generate_monthly_report.py 実行
      ├─ 前月の配信・decision を集計
      └─ logs/monthly-report-YYYY-MM.md 生成
```

### Obsidian での アクセス

```
Obsidian Desktop
  ├─ Quick Switcher (Ctrl+P)
  │  └─ ファイルの高速検索
  │
  ├─ Search (Ctrl+Shift+F)
  │  └─ 全文検索 + regex 対応
  │
  ├─ Dataview plugin
  │  └─ `dataview TABLE file.name FROM #decision`
  │     → decision タイプのファイルを動的リスト化
  │
  ├─ Web Clipper (Chrome extension)
  │  └─ 記事クリップ → wiki/articles に自動保存
  │
  ├─ Periodic Notes
  │  └─ Daily (wiki/daily/)
  │  └─ Weekly (wiki/weekly/)
  │
  └─ Backlinks panel
     └─ 関連ファイルの自動リンク表示
```

---

## 3️⃣ Daily Workflow（毎日のワークフロー）

### 朝（7:30 AM）

**morning_digest.py が自動実行**

```bash
# 実際の実行内容
py -3.12 C:\Users\owner\.claude\scripts\morning_digest.py

# 出力ファイル
logs/morning-briefing.md

# 内容
- 前日に確定した decision リスト
- 実施予定の action リスト
- 当日の優先順位トップ3
- 配信予定（あれば）
```

**やること:**
1. 朝の brief で priority を確認
2. Obsidian で昨日の wiki 更新をスキャン
3. 新しい記事・データがあれば概要を読む

### 日中（作業時間）

**記事・データの追加:**

```
raw-sources/articles/
  └─ [新しい記事を追加]
     └─ 5分以内に wiki/summaries に自動要約が生成される
```

**重要な decision が出たら:**

```markdown
# decision_[タイトル]_[日付].md を作成

1. templates/decision_template.md をコピー
2. 以下を記入：
   - 決定内容（具体的に）
   - Why（理由・背景）
   - How to apply（実装方法）
3. MEMORY.md の 🎯 Decision セクションに追記
```

**action が発生したら:**

```markdown
# action_[タイトル]_[日付].md を作成

1. templates/action_template.md をコピー
2. 以下を記入：
   - タスク説明
   - Due date
   - Status: pending → in_progress → completed
3. MEMORY.md の 📋 Action セクションに追記
```

### 夜（auto_commit.py が自動実行）

**1時間ごとに実行:**

```bash
# 実際の実行内容
├─ git add wiki/summaries/
├─ git add wiki/entities/
├─ git add logs/decision-log.md
└─ git commit -m "auto: update wiki + decision-log"
```

**GitHub に記録される:**
- Wiki の新規追加・更新
- decision log の追記
- Commit history から検索可能

### 毎週月曜（8:00 AM）

**lint_wiki.py が自動実行:**

```bash
py -3.12 C:\Users\owner\.claude\scripts\lint_wiki.py

# チェック内容
- Orphan ファイル（リンクされていない）
- リンク矛盾（存在しないリンク）
- Duplicate entity
- INDEX.md の自動更新
```

---

## 4️⃣ Decision Making（意思決定の記録）

### Decision のライフサイクル

```
セッション中に decision が確定
  ↓
decision_*.md ファイルを作成
  │
  ├─ Rule（決定内容）
  ├─ Why（理由・背景）
  └─ How to apply（実装方法）
  ↓
MEMORY.md の 🎯 Decision セクションに登録
  ↓
次セッションで参照可能に
  ↓
3ヶ月以上参照されなければ archive （TTL: permanent）
```

### Decision テンプレートの記入例

**ファイル名:**
```
decision_secondbrain_scheduler_setup_20260414.md
```

**必須セクション:**

```markdown
---
type: decision
ttl: permanent
date: 2026-04-14
---

# セカンドブレイン スケジューラー設定

## Rule（決定内容）
CronCreate で morning_digest, lint_wiki, generate_monthly_report を自動実行する

## Why（理由）
**背景**: 毎日朝 daily briefing を手動で実行するのは非効率
**考慮**: スケジューラー失敗時は Obsidian 同期が停止する可能性

## How to apply（実装）
1. CronCreate で 3 つのタスク登録
2. `scheduled-tasks list` で確認
3. テスト実行して動作確認
```

### Decision を参照するとき

**セッション内で decision を引用する:**

```
前回（2026-04-14）の decision: [decision_secondbrain_scheduler_setup_20260414.md](...)
に基づいて、X を実装している
```

**関連する action を追加:**

```markdown
# action_implement_scheduler_20260414.md

...status: completed...
Related decision: [decision_secondbrain_scheduler_setup_20260414.md](...)
```

---

## 5️⃣ Troubleshooting（トラブルシューティング）

### よくあるエラー

#### Q: morning_digest が朝 7:30am に実行されない

**原因1**: CronCreate job が enabled になっていない
```bash
scheduled-tasks list
# 確認: morning-digest-daily の enabled が true か？
```

**原因2**: Python 3.12 パスが登録されていない
```bash
py -3.12 --version  # 実行確認
```

**解決策**:
1. `scheduled-tasks list` で Job ID を確認
2. CronDelete で削除
3. CronCreate で再登録（py -3.12 の正確なパス）

---

#### Q: Obsidian で wiki フォルダが同期されない

**原因**: git clone が最新でない
```bash
cd C:\Users\owner\MyVtuber
git pull
# または
git fetch && git rebase
```

**解決策**:
1. Obsidian 再起動
2. wiki フォルダが表示されるまで待機（30秒）
3. ターミナルで `git status` で最新 commit を確認

---

#### Q: MEMORY.md の decision/action セクションが更新されない

**原因**: sync_monitor.py がスキップしている
```bash
# 手動実行
py -3.12 C:\Users\owner\.claude\scripts\sync_monitor.py
```

**確認方法**:
```bash
git log --oneline | head -5
# 最新 commit が memory/ の更新を含むか確認
```

---

#### Q: Dataview クエリが表示されない

**原因**: Dataview plugin の JavaScript が disabled
```
Obsidian Settings → Dataview → "Enable JavaScript queries" を disabled に
```

**理由**: セキュリティ上、wiki の Dataview ノートでは JS は不要

---

### Log ファイルの確認

**morning briefing:**
```bash
cat logs/morning-briefing.md
```

**Wiki lint report:**
```bash
cat logs/lint-report-2026-04-14.md
```

**Decision log:**
```bash
tail -50 logs/decision-log.md
```

**Git commit history:**
```bash
git log --oneline | head -20
```

---

## 🔗 Related Files

| ファイル | 用途 |
|---------|------|
| `MEMORY.md` | メモリインデックス（decision/action を参照） |
| `MAINTENANCE.md` | TTL 管理・月次メンテナンス |
| `CLAUDE.md` | グローバル行動指針（このガイドへのリンク） |
| `.obsidian/` | Obsidian 設定フォルダ |
| `logs/decision-log.md` | 全 decision の記録 |
| `logs/action-log.md` | 全 action の記録 |
| `wiki/INDEX.md` | Wiki ページの全体インデックス |

---

## 📞 Support & Contact

**問題が発生したら:**

1. ファイル path を確認：`C:\Users\owner\MyVtuber\` が存在するか
2. Python 3.12 のパス：`py -3.12 --version` で確認
3. Git status：`git status` で uncommitted changes を確認
4. この guide をもう一度読む（Ctrl+F で検索）

**自動化スクリプト詳細:**
- `morning_digest.py` → tech/scripts/
- `lint_wiki.py` → .claude/scripts/
- `sync_monitor.py` → .claude/scripts/
- `auto_commit.py` → .claude/scripts/

---

**セカンドブレイン稼働中。Happy note-taking! 🧠✨**

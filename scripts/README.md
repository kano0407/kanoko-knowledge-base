# Obsidian 自動同期スクリプト

Obsidian Vault の変更を自動検知し、Claude Code メモリへリアルタイム同期するスクリプト集。

---

## 概要

```
Obsidian（プライマリ）
    ↓
    [ファイル監視]
    ↓
sync_monitor.py
    ↓
    [frontmatter自動追加]
    ↓
claude_memory_sync.py
    ↓
Claude Code メモリ（ミラー）
```

**メリット**：
- Obsidian での編集が自動的に Claude Code に反映
- TTL ルール + frontmatter の一元管理
- 月初メンテナンスの自動初期化

---

## セットアップ（初回のみ）

### 1. ライブラリインストール

```bash
py -3.12 scripts/setup.py
```

これで以下が実行されます：
- `watchdog` / `pyyaml` のインストール
- 初回同期の実行
- `run_sync.bat` の作成

### 2. 動作確認

```bash
py -3.12 scripts/sync_monitor.py
```

コンソールに以下が表示されれば成功：

```
╔════════════════════════════════════════════════════════════╗
║  Obsidian 自動同期スクリプト起動                          ║
║  監視フォルダ: Kanoko Knowledge Base
║  クローディング先: Claude Code メモリ                    ║
╚════════════════════════════════════════════════════════════╝

🟢 監視開始... (Ctrl+C で停止)
```

---

## 日常的な使用方法

### パターン1: 継続的監視（推奨）

```bash
py -3.12 scripts/sync_monitor.py
```

**動作**：
- Obsidian フォルダをリアルタイム監視
- ファイル作成/更新 → 自動同期
- 月初 → メンテナンスチェックリスト初期化
- `Ctrl+C` で終了

### パターン2: 手動同期

```bash
py -3.12 scripts/claude_memory_sync.py
```

**用途**：
- 一度きりの同期実行（監視は不要）
- 手動で変更を反映したいとき
- トラブルシューティング

### パターン3: クイック起動（Windows）

ダブルクリック：`run_sync.bat`

---

## スクリプト詳細

### 1️⃣ sync_monitor.py

**概要**： Obsidian ファイル監視 + 自動同期トリガー

**監視対象**：
- `.md` ファイルの作成 / 更新
- 除外: `08_Archive/` / `scripts/` / テストファイル

**動作フロー**：
```
新規ファイル作成
    ↓
frontmatter 不在？
    ↓ YES
    ├→ TTL を推測（ファイル名から）
    ├→ frontmatter を自動生成 + 挿入
    ↓
claude_memory_sync.py を実行
    ↓
MEMORY.md を更新
```

**実装メモ**：
- `debounce_delay = 3` 秒（連続更新時の多重実行回避）
- 月初自動メンテナンス初期化機能あり

---

### 2️⃣ claude_memory_sync.py

**概要**： Obsidian → Claude Code メモリ同期実行

**処理ステップ**：

1. **Obsidian ファイル読み込み**
   - 全 `.md` ファイルをスキャン
   - frontmatter から TTL / tags を抽出
   - ファイル情報を索引化

2. **カテゴリ分類**
   - フォルダ構造（00_Profile, 01_Strategy, ...）に沿って分類

3. **MEMORY.md 生成**
   - カテゴリ別インデックス自動生成
   - 既存の「🔥 今週のホットメモリ」セクションは保持

4. **Claude Code メモリ更新**
   - `C:\Users\owner\.claude\projects\...\memory\MEMORY.md` を上書き

**出力例**：

```markdown
# MEMORY INDEX

**Obsidian自動同期日時**: 2026-04-11 15:32:18
**総ファイル数**: 47 ファイル

## 🔧 TTL管理ルール
...

## 👤 プロフィール
- [[00_Profile/_profile.md|プロフィール]] `#ttl/permanent`
- [[00_Profile/_channel-stats.md|チャンネル統計]] `#ttl/permanent`
...
```

---

### 3️⃣ setup.py

**概要**： 初期セットアップスクリプト

**実行内容**：
1. ライブラリインストール（`watchdog` / `pyyaml`）
2. 初回同期実行
3. `run_sync.bat` 生成

**実行タイミング**：
- 初回のみ
- ライブラリ更新時

---

## トラブルシューティング

### ❓ 「ModuleNotFoundError: watchdog」

**原因**：`watchdog` がインストールされていない

**対応**：
```bash
py -3.12 scripts/setup.py
```

または：
```bash
pip install watchdog pyyaml
```

---

### ❓ ファイルが同期されない

**チェック項目**：

1. **sync_monitor.py が実行中か**
   ```bash
   # コンソール確認
   🟢 監視開始... (Ctrl+C で停止)
   ```

2. **ファイルの保存場所**
   - ✅ `01_Strategy/` / `02_Projects/` など
   - ❌ `08_Archive/` / `scripts/` / `test_*.md`

3. **Claude Code メモリフォルダが存在するか**
   ```
   C:\Users\owner\.claude\projects\C--Users-owner-MyVtuber\memory\
   ```

4. **frontmatter のフォーマット**
   ```yaml
   ---
   name: ファイル名
   type: project
   ttl: until-completion
   ---
   ```

---

### ❓ frontmatter が自動追加されない

**原因**：ファイルに既に frontmatter がある場合はスキップ

**対応**：既存 frontmatter に `ttl:` フィールドを手動追加

```yaml
---
name: ファイル名
type: project
ttl: until-completion  # ← この行を追加
---
```

---

### ❓ MEMORY.md が上書きされてしまう

**仕様**：「🔥 今週のホットメモリ」セクションは保持されます

**確認**：
```bash
# 同期前後で比較
git diff MEMORY.md
```

---

## カスタマイズ

### パスを変更する場合

`sync_monitor.py` の定数を編集：

```python
# パス設定
OBSIDIAN_PATH = Path(__file__).parent.parent
CLAUDE_MEMORY_PATH = Path(r'C:\Users\owner\.claude\projects\C--Users-owner-MyVtuber\memory')
SCRIPTS_PATH = OBSIDIAN_PATH / 'scripts'
```

### debounce 時間を変更する場合

連続更新時の同期インターバルを変更：

```python
# sync_monitor.py の ObsidianChangeHandler.__init__()
self.debounce_delay = 5  # 秒（デフォルト: 3秒）
```

値が大きいほど、同期が遅延します。

---

## TTL 推測ルール（自動frontmatter生成）

新規ファイル作成時、ファイル名から TTL が自動判定されます：

| パターン | TTL推測 | 理由 |
|---------|--------|------|
| `test_*.md` | `7days` | テストファイル（短期） |
| `*_20260*.md` | `30days` | 日付付き（短期分析） |
| その他 | `permanent` | 通常ファイル |

**手動調整**：frontmatter の `ttl:` フィールドを編集してOK

---

## セキュリティ注意事項

⚠️ **スクリプト実行時の注意**：

1. **PATH の確認**
   - スクリプトはハードコードされたパスを使用
   - 異なる環境ではパスを修正必須

2. **ファイルパーミッション**
   - Obsidian / Claude Code メモリフォルダの読み書き権限が必要
   - 管理者実行不要（通常ユーザーで OK）

3. **バックアップ推奨**
   - MEMORY.md は定期的にバックアップ
   - 破損時の復旧用

---

## ログ出力例

```
📚 Obsidian → Claude Code メモリ同期スクリプト
   Obsidian: Kanoko Knowledge Base
   Claude Memory: memory
   実行時刻: 2026-04-11 15:32:18

📖 Obsidian ファイル読み込み中...
   ✅ 47 ファイル検出

💾 Claude Code メモリへ同期中...
   ✅ MEMORY.md 同期完了: 47 ファイル

✨ 同期完了！
   更新先: C:\Users\owner\.claude\projects\...\memory\MEMORY.md
```

---

## FAQ

**Q: 同期周期は？**  
A: リアルタイム（ファイル更新から3秒以内）

**Q: オフライン時は？**  
A: ローカルメモリ更新のみ。Claude Code メモリ更新は同期実行時。

**Q: 複数マシンで使用可能？**  
A: スクリプト内のパスをマシンごとに調整すれば可能

**Q: Git でバージョン管理したい**  
A: `.gitignore` に `scripts/` は追加せず、スクリプト自体はコミット推奨

---

## サポート

問題が発生した場合：

1. コンソール出力を確認
2. `py -3.12 scripts/claude_memory_sync.py` で手動同期試行
3. `sync_monitor.py` 内の print() 文で debugging

---

**最終更新**: 2026-04-11  
**バージョン**: 1.0  
**作成者**: Claude Code

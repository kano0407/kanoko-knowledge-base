---
tags:
  - #system/maintenance
  - #ttl/permanent
---

# 月次メモリメンテナンス手順（毎月初日に実行）

**最終更新**: 2026-04-11

---

## チェックリスト

### 1. 期限切れファイルの確認
- [ ] 90日以上参照されていない `#ttl/90days` ファイルを特定
- [ ] 30日以上参照されていない `#ttl/30days` ファイルを特定
- [ ] 7日以上参照されていない `#ttl/7days` ファイルを特定

### 2. 削除 or アーカイブの判定
各ファイルについて、以下から選択：
- **完全削除**: 二度と必要ないと確実な場合
- **アーカイブ**: 将来の参考のため記録しておきたい場合（`08_Archive/` に移動）
- **昇格**: 3回以上参照された重要パターン → INDEX.md で永続化

### 3. テストファイルの確認
- [ ] `test_*.md` ファイルが混在していないか確認
- [ ] 不要なテストファイルはすぐに削除

### 4. INDEX.md の更新
- [ ] インデックスを最新状態に更新
- [ ] 新しく追加されたファイルを記載
- [ ] 削除・アーカイブされたファイルを削除
- [ ] 「🔥 今週のホットメモリ」セクションを更新

### 5. 日付矛盾の確認
- [ ] ファイル名と frontmatter の日付が一致しているか
- [ ] 未来日付（プロジェクト開始予定日）が混在していないか

---

## テンプレート: 完了したプロジェクトの処理

完了したプロジェクトをマークする際は、frontmatter を以下のように更新：

```yaml
---
name: PROJECT_NAME
type: project
status: completed  # ← 完了をマーク
date: 2026-04-XX
tags:
  - #status/completed
  - #ttl/permanent  # ← 永続保持（将来の参考）
archived_date: 2026-05-01
---
```

---

## テンプレート: 3回参照→昇格ルール

ファイルが3回以上参照されたら、以下のように処理：

1. 重要なパターン・フレームワークを抽出
2. INDEX.md の適切なセクションに「リンク + 説明」として統合
3. 元ファイルは `[廃止]` プレフィックスを付けるか、`08_Archive/` に移動

**例**: `04_Analysis/broadcast_comparison_analysis_20260411.md` が3回参照
→ その発見を INDEX.md の「配信テーマ・企画参考資料」セクションに反映
→ 元ファイルは削除または `[廃止] broadcast_comparison_analysis_20260411.md` にマーク

---

## 現在のファイル状態（2026-04-11 基準）

| ファイル | TTL | 参照頻度 | 最終参照日 | ステータス |
|---------|-----|--------|---------|---------|
| 00_Profile/_profile.md | permanent | 高 | 2026-04-11 | ✅ |
| 00_Profile/_channel-stats.md | permanent | 中 | 2026-04-08 | ✅ |
| 00_Profile/_goals.md | permanent | 中 | 2026-04-08 | ✅ |
| 01_Strategy/x-mindset.md | permanent | 高 | 2026-04-11 | ✅ |
| 01_Strategy/youtube-shorts-6step.md | permanent | 中 | 2026-04-10 | ✅ |
| 02_Projects/youtube-automation/_overview.md | until-completion | 高 | 2026-04-10 | 進行中 |
| 02_Projects/youtube-shorts/project_youtube_shorts_20260501.md | until-completion | 中 | 2026-04-11 | 準備中 |
| 02_Projects/workflow-c-multianalysis/_overview.md | until-completion | 中 | 2026-04-10 | 進行中 |
| 02_Projects/notebooklm-workflow/_overview.md | until-completion | 中 | 2026-04-10 | 進行中 |
| 03_Skills/audience-feedback-aggregator/SKILL.md | permanent | 中 | 2026-04-10 | ✅ |
| 03_Skills/platform-analysis-integrator/SKILL.md | permanent | 中 | 2026-04-10 | ✅ |
| 04_Analysis/monthly/2026-04-x-trends.md | until-completion | 中 | 2026-04-10 | 進行中 |
| 04_Analysis/monthly/2026-04-notebooklm-results.md | 30days | 中 | 2026-04-10 | 短期分析 |
| 05_Content/reference/talk-patterns.md | permanent | 中 | 2026-04-10 | ✅ |
| 06_Operations/guidelines/behavior.md | permanent | 高 | 2026-04-11 | ✅ |
| 06_Operations/department-status/producer.md | until-completion | 中 | 2026-04-10 | 進行中 |
| 07_Reference/notion-pages.md | permanent | 中 | 2026-04-08 | ✅ |
| 07_Reference/notebooklm-integration.md | 90days | 低 | 2026-04-10 | 参考資料 |

---

## 実行スケジュール

- **2026-05-01**: 次回メンテナンス（4月30日分析対象）
  - `#ttl/30days` ファイル（30日前は4月1日） → 削除判定
  - `#ttl/90days` ファイル → チェック（有効期限は2026-07-10）
  - `#ttl/until-completion` → 完了確認

- **2026-06-01**: 6月メンテナンス
- **2026-07-01**: 7月メンテナンス

---

## 次月（2026-05月）への引き継ぎ

予定される期限切れファイル：
- `04_Analysis/monthly/2026-04-notebooklm-results.md` → 5月10日に削除判定（30日経過）
- 完了予定プロジェクト：
  - `02_Projects/youtube-shorts/project_youtube_shorts_20260501.md` → フェーズ2完了時点で status: completed に
  - `04_Analysis/monthly/2026-04-x-trends.md` → 4月末で完了
  - `06_Operations/department-status/producer.md` → 月末レビュー完了後に5月版へ

---

## メモリシステム改善記録

**2026-04-11**: 
- INDEX.md に TTL管理セクション追加
- INDEX.md に「🔥 今週のホットメモリ」セクション追加
- 全メモリファイルに TTL タグ追加（#ttl/xxx 形式）
- MAINTENANCE.md ファイル作成

---

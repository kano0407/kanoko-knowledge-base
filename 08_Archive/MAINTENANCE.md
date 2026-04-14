---
name: MAINTENANCE
type: unknown
date: 2026-04-14
tags:
  - 
---
# 月次メモリメンテナンス手順（毎月初日に実行）

**最終更新**: 2026-04-11

---

## チェックリスト

### 1. 期限切れファイルの確認
- [ ] 90日以上参照されていない `ttl: 90days` ファイルを特定
- [ ] 30日以上参照されていない `ttl: 30days` ファイルを特定
- [ ] 7日以上参照されていない `ttl: 7days` ファイルを特定

### 2. 削除 or アーカイブの判定
各ファイルについて、以下から選択：
- **完全削除**: 二度と必要ないと確実な場合
- **アーカイブ**: 将来の参考のため記録しておきたい場合（`memory/archive/` に移動）
- **昇格**: 3回以上参照された重要パターン → `frameworks.md` に統合

### 3. テストファイルの確認
- [ ] `test_*.md` ファイルが混在していないか確認
- [ ] 不要なテストファイルはすぐに削除

### 4. MEMORY.md の更新
- [ ] インデックスを最新状態に更新
- [ ] 新しく追加されたファイルを記載
- [ ] 削除・アーカイブされたファイルを削除

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
ttl: permanent     # ← 永続保持（将来の参考）
archived_date: 2026-05-01
---
```

---

## テンプレート: 3回参照→昇格ルール

ファイルが3回以上参照されたら、内容を以下のように処理：

1. 重要なパターン・フレームワークを抽出
2. `frameworks.md` に「意味記憶」として統合
3. 元ファイルは `[廃止]` プレフィックスを付けるか削除

**例**: `project_broadcast_comparison_analysis_20260411.md` が3回参照
→ そのエッセンスを別の frameworks.md セクションに追加
→ 元ファイルは削除または `[廃止] project_broadcast_comparison_analysis_20260411.md` にマーク

---

## 現在のファイル状態（2026-04-11 基準）

| ファイル | TTL | 参照頻度 | 最終参照日 | ステータス |
|---------|-----|--------|---------|---------|
| user_vtuber_profile.md | permanent | 高 | 2026-04-11 | ✅ |
| feedback_claude_behavior.md | permanent | 高 | 2026-04-11 | ✅ |
| project_x_mindset.md | permanent | 中 | 2026-04-08 | ✅ |
| project_viewer_overlay.md | permanent | 低 | 2026-03-25 | 一時停止中 |
| project_youtube_shorts_automation.md | until-completion | 高 | 2026-04-10 | 進行中 |
| project_youtube_automation_implementation.md | until-completion | 高 | 2026-04-10 | 進行中 |
| reference_notion_structure.md | permanent | 中 | 2026-03-30 | ✅ |
| reference_notebooklm_vs_memory.md | 90days | 低 | 2026-04-10 | 参考資料 |
| project_notebooklm_analysis_20260410.md | 30days | 中 | 2026-04-10 | 短期分析 |
| project_x_monthly_trends_202604.md | until-completion | 中 | 2026-04-10 | 進行中 |
| project_vtuber_skill_deployment_20260410.md | permanent | 中 | 2026-04-10 | 完료実績 |
| project_broadcast_schedule_202604.md | until-completion | 高 | 2026-04-11 | 進行中 |
| project_content_format_strategy_202604.md | until-completion | 高 | 2026-04-11 | 進行中 |
| reference_vtuber_talk_analysis.md | permanent | 中 | 2026-04-06 | 参考資料 |
| project_broadcast_comparison_analysis_20260411.md | 30days | 高 | 2026-04-11 | 短期分析 |
| project_broadcast_data_analysis_20260411.md | 30days | 高 | 2026-04-11 | 短期分析 |
| project_broadcast_analysis_result_20260411.md | 30days | 高 | 2026-04-11 | 短期分析 |
| project_youtube_shorts_20260501.md | until-completion | 中 | 2026-04-11 | 準備中 |

---

## 実行スケジュール

- **2026-05-01**: 次回メンテナンス（4月30日分析対象）
  - `ttl: 30days` ファイル（30日前は4月1日） → 削除判定
  - `ttl: 90days` ファイル → チェック（有効期限は2026-07-10）
  - `ttl: until-completion` → 完了確認

- **2026-06-01**: 6月メンテナンス
- **2026-07-01**: 7月メンテナンス

---

## 次月（2026-05月）への引き継ぎ

- `project_broadcast_schedule_202604.md` → 4月終了時に「完了」判定
- `project_x_monthly_trends_202604.md` → 同上
- `project_content_format_strategy_202604.md` → 同上
- `project_notebooklm_analysis_20260410.md` → 5月1日に削除判定（30日経過）
- `project_broadcast_comparison_analysis_20260411.md` → 5月11日に削除判定（30日経過）
- `project_broadcast_data_analysis_20260411.md` → 5月11日に削除判定（30日経過）
- `project_broadcast_analysis_result_20260411.md` → 5月11日に削除判定（30日経過）

---

## メモリシステム改善記録

**2026-04-11**: 
- テストファイル3個削除
- MEMORY.md インデックス更新（未記載ファイル3個追加）
- 全メモリファイルに TTL フィールド追加
- TTL管理セクション追加
- MAINTENANCE.md ファイル作成

---

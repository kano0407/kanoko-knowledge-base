---
name: MEMORY
type: unknown
date: 2026-04-14
tags:
  - 
---
# MEMORY INDEX

**Obsidian自動同期日時**: 2026-04-13 13:55:00  
**総ファイル数**: 26 ファイル  
**最終チェック**: 2026-04-13

## 🔧 TTL管理ルール

### メモリ type（6種類）
- `user` — ユーザー情報・プロフィール
- `feedback` — ユーザーから指定された行動指針・ルール
- `project` — 進行中・完了したプロジェクト
- `reference` — 参考資料・分析データベース
- `decision` — **セッションで確定した方針・意思決定**（NEW）
- `action` — **次のセッションで実施するアクション**（NEW）
- `analysis` — **分析結果・インサイト**（NEW）

### TTL ルール
- `permanent`: 無期限保持（user / feedback / decision）
- `until-completion`: 完了まで（進行中プロジェクト / action）
- `90days`: 90日で削除候補（参考資料・研究ネタ）
- `30days`: 30日で削除（短期計画・分析結果 / analysis）
- `7days`: 7日で削除（一時メモ）

最後の参照日を記録。参照時に TTL がリセットされます。

---

## 👤 プロフィール & ユーザー情報

- [user_vtuber_profile.md](user_vtuber_profile.md) — VTuber Kanoko のプロフィール情報

## 🎯 確定済み意思決定（Decision）

- [decision_secondbrain_complete_implementation_20260413.md](decision_secondbrain_complete_implementation_20260413.md) — セカンドブレイン完全実装方針確定

## 📋 次フェーズ実施予定（Action）

- [action_nextphase_scheduler_setup_20260413.md](action_nextphase_scheduler_setup_20260413.md) — Phase 3-4 の実施内容（scheduled-tasks, Obsidian）

## 📈 戦略・方針

- [project_x_mindset.md](project_x_mindset.md) — X(Twitter) 投稿戦略の考え方
- [project_content_format_strategy_202604.md](project_content_format_strategy_202604.md) — 4月のコンテンツフォーマット戦略
- [project_broadcast_schedule_202604.md](project_broadcast_schedule_202604.md) — 4月配信スケジュール

## 🚀 進行中プロジェクト

### YouTube 関連
- [project_youtube_shorts_automation.md](project_youtube_shorts_automation.md) — YouTube Shorts 自動化 6ステップ戦略
- [project_youtube_automation_implementation.md](project_youtube_automation_implementation.md) — YouTube 自動化実装ガイド
- [project_youtube_shorts_20260501.md](project_youtube_shorts_20260501.md) — 2026-05-01 YouTube Shorts プロジェクト

### 配信関連
- [project_broadcast_implementation_guide_complete_202604.md](project_broadcast_implementation_guide_complete_202604.md) — 配信実装ガイド（完全版）
- [project_broadcast_data_analysis_20260411.md](project_broadcast_data_analysis_20260411.md) — 配信データ分析
- [project_broadcast_comparison_analysis_20260411.md](project_broadcast_comparison_analysis_20260411.md) — 配信比較分析
- [project_broadcast_analysis_result_20260411.md](project_broadcast_analysis_result_20260411.md) — 配信分析結果

### スキル & ツール関連
- [project_vtuber_skill_deployment_20260410.md](project_vtuber_skill_deployment_20260410.md) — VTuber スキルデプロイメントログ
- [project_notebooklm_analysis_20260410.md](project_notebooklm_analysis_20260410.md) — NotebookLM 分析結果

### セカンドブレイン実装
- [project_secondbrain_implementation_20260413.md](project_secondbrain_implementation_20260413.md) — Claude + Obsidian セカンドブレイン実装プロジェクト（Phase 1-2 完了）

### その他
- [project_viewer_overlay.md](project_viewer_overlay.md) — ビューアーオーバーレイ設計
- [project_x_monthly_trends_202604.md](project_x_monthly_trends_202604.md) — 4月 X トレンド分析

## 📚 参考資料 & リファレンス

- [reference_vtuber_talk_analysis.md](reference_vtuber_talk_analysis.md) — VTuber 会話パターン分析
- [reference_notebooklm_vs_memory.md](reference_notebooklm_vs_memory.md) — NotebookLM vs Memory 連携ガイド
- [reference_notion_structure.md](reference_notion_structure.md) — Notion ページ構造リファレンス
- [07_Reference/mcp-nano-banana.md](07_Reference/mcp-nano-banana.md) — MCP nano-banana リファレンス

## 📋 運用・行動ガイドライン

- [feedback_claude_behavior.md](feedback_claude_behavior.md) — Claude の行動指針（完了時サマリー削除など）

## 📊 メンテナンス & 管理

- [MEMORY.md](MEMORY.md) — このファイル（メモリインデックス）
- [MAINTENANCE.md](MAINTENANCE.md) — メモリシステムのメンテナンスガイド
- [SCORING.md](SCORING.md) — ホットメモリスコアリング計算式

---

## 🔥 ホットメモリ（本日のコンテキスト）

### 🚨 最優先（本日の進行プロジェクト）
1. **[project_secondbrain_implementation_20260413.md](project_secondbrain_implementation_20260413.md)** — セカンドブレイン実装（Phase 1-2 完了、Phase 3-5 進行中）
2. **[decision_secondbrain_complete_implementation_20260413.md](decision_secondbrain_complete_implementation_20260413.md)** — 「完全に実装する」の方針確定
3. **[action_nextphase_scheduler_setup_20260413.md](action_nextphase_scheduler_setup_20260413.md)** — Phase 3-4 実施予定（スケジューラー・Obsidian）

### 定期参照（方針・ガイドライン）
- [feedback_claude_behavior.md](feedback_claude_behavior.md) — 行動指針（毎セッション確認）
- [project_x_mindset.md](project_x_mindset.md) — X戦略（全 X 関連作業で参照）

### 参照可能（必要に応じて）
- [project_youtube_shorts_automation.md](project_youtube_shorts_automation.md) — YouTube Shorts 6ステップ自動化
- [reference_vtuber_talk_analysis.md](reference_vtuber_talk_analysis.md) — 会話パターン分析
- [project_broadcast_*](project_broadcast_schedule_202604.md) — 配信関連

---

## 📝 本日の変更（2026-04-13）

- ✅ **同期日時更新**: 2026-04-13 11:20:00 → 2026-04-13 13:57:00
- ✅ **ファイル数更新**: 23 → 26 個（セカンドブレイン 3ファイル追加）
- ✅ **新規 type 追加**: decision, action, analysis
- ✅ **Phase 1-4 完了**: フォルダ、スクリプト、スケジューラー、Obsidian 設定
- ✅ **ホットメモリ更新**: 本日の進行プロジェクトを最優先に配置
- ✅ **morning_digest.py 拡張**: ホットメモリ表示機能追加

---

## 📌 メモリシステムの使い方

### メモリを追加するとき
```markdown
新しいメモリファイルを作成:
- ファイル名: `{type}_{description}.md`
- 例: `feedback_code_review.md`, `project_marketing_q2.md`

ファイルヘッダ:
---
name: {メモリ名}
description: {1行の説明}
type: user / feedback / project / reference
ttl: permanent / until-completion / 90days / 30days / 7days
---

内容...
```

### メモリを同期するとき
1. `Obsidian自動同期日時` を現在時刻に更新
2. 実際のファイルと MEMORY.md のリンクを確認
3. 削除・修正が必要なら該当ファイルを更新
4. TTL ルールで期限切れファイルがないか確認

---


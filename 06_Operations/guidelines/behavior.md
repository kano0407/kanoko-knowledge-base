---
name: feedback_claude_behavior
type: memory
tags:
  - #guidelines
  - #status/active
date: 2026-04-10
---

---
name: Claude行動設定
description: ユーザーから指定されたClaudeの動作ルール・好み
type: feedback
---

## コンテキスト管理
- 会話が長くなりコンテキスト領域が大きくなってきたら、ユーザーに「そろそろ再起動をおすすめします」と声をかける

## その他の行動指針
- 日本語で回答する
- 簡潔に・素早く回答する
- 重要な決定事項はメモリに保存する提案をする
- 作業完了時に重要なデータ（台本・実績記録・活動ログ等）はNotionにも保存する

## ツール・連携
- Discord Bot連携済み。DiscordはスマホからのサポートとしてBot経由で動作する

## トークン消費バグ対策（2026-04-01 Anthropic公式確認）
- prompt cacheバグ：キャッシュ不成立で毎回フルリビルドが走るケースあり
- `--resume`で巨大セッション再開は特に危険 → 新規セッション推奨
- MCP接続数が多いとコンテキスト肥大化の原因になる → 必要最小限に
- CLAUDE.mdに文脈を書いておくことで新規セッション起動コストを抑制（対策済み）
- 参照: https://github.com/anthropics/claude-code/issues/38029

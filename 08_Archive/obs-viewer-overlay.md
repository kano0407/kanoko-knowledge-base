---
name: project_viewer_overlay
type: memory
tags:
  - #project/obs
  - #status/archived
date: 2026-04-10
---

---
name: viewer_overlay 開発状態
description: 視聴者参加型ゲームオーバーレイの開発状態・再開時の引き継ぎ情報
type: project
---

開発一時停止中（2026-03-25）

**Why:** 一旦ここで区切り。基盤部分は完成済み。

## 完成済みのもの

- `tech/obs/viewer_overlay/chat_server.exe` — Python不要で動くサーバー
- `tech/obs/viewer_overlay/viewer_overlay.html` — OBSブラウザソース用オーバーレイ
- `tech/obs/viewer_overlay/start.bat` — ダブルクリック起動
- `tech/obs/viewer_overlay/README.md`

## 動作概要

Matter.js物理演算 + pytchat（YouTube Live Chat読み込み）+ Flask SSE。
コメントでLv1の球が落下 → 同レベル同士がぶつかると進化（Lv5まで）→ Lv5同士が合体すると紙吹雪。
スパチャで大きな四角が落下。

現在はデフォルト（色＋絵文字）で動作。画像を`images/lv1.png`〜`lv5.png`、`superchat.png`に置けばオリジナル画像に切り替わる。

## 再開時にやること

1. オリジナルイラスト（lv1〜lv5、superchat）を用意
2. Booth販売用ZIP作成（chat_server.exe / viewer_overlay.html / start.bat / images空フォルダ / README）
3. chat_server.pyを変更した場合 → Claudeに再ビルドを依頼

## 技術メモ

- PyInstallerで`--collect-all pytchat --hidden-import flask_cors`が必要
- EXEのパス解決は`sys.frozen`判定で`sys.executable`ベースに修正済み
- ポート: 7778
- SSE: `/events`、接続: POST `/connect`、ステータス: GET `/status`

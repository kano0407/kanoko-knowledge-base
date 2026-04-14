#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動同期スクリプト セットアップスクリプト

機能：
- 必要なライブラリをインストール
- 設定ファイルを初期化
- 初回同期を実行

実行方法：
  py -3.12 scripts/setup.py
"""

import subprocess
import sys
import os
import io
from pathlib import Path

# Windows コンソール出力を UTF-8 に設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPTS_PATH = Path(__file__).parent
OBSIDIAN_PATH = SCRIPTS_PATH.parent


def install_dependencies():
    """必要なライブラリをインストール"""
    print("\n📦  依存ライブラリをインストール中...\n")

    packages = [
        'watchdog',  # ファイル監視
        'pyyaml',    # YAML frontmatter パース
    ]

    for package in packages:
        print(f"   • {package}...", end=' ')
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', '-q', package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅")
        except subprocess.CalledProcessError:
            print("❌")
            print(f"      エラー: {package} のインストール失敗")
            return False

    print("\n✅ ライブラリインストール完了\n")
    return True


def run_initial_sync():
    """初回同期を実行"""
    print("🔄 初回同期を実行中...\n")

    sync_script = SCRIPTS_PATH / 'claude_memory_sync.py'
    if not sync_script.exists():
        print(f"❌ {sync_script} が見つかりません")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(sync_script)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"❌ 同期スクリプト実行失敗")
            if result.stderr:
                print(f"   エラー詳細:\n{result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ 同期がタイムアウト（30秒以上経過）")
        return False
    except Exception as e:
        print(f"❌ 同期実行エラー: {e}")
        return False


def create_launcher():
    """
    クイック起動用バッチファイル/シェルスクリプトを作成

    Windows: run_sync.bat
    """
    launcher_bat = OBSIDIAN_PATH / 'run_sync.bat'

    bat_content = """@echo off
REM Obsidian 自動同期スクリプト起動

cd /d "%~dp0"
py -3.12 scripts\\sync_monitor.py
pause
"""

    try:
        with open(launcher_bat, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        print(f"✅ ランチャー作成: run_sync.bat")
        return True
    except Exception as e:
        print(f"⚠️ ランチャー作成失敗: {e}")
        return False


def print_next_steps():
    """セットアップ完了後の手順を表示"""
    print("""
╔════════════════════════════════════════════════════════════╗
║  セットアップ完了！                                      ║
╚════════════════════════════════════════════════════════════╝

【動作確認】
1. MEMORY.md が自動更新されたか確認
   → C:\\Users\\owner\\.claude\\projects\\...\\memory\\MEMORY.md

2. Obsidian で新規ファイルを作成
   → frontmatter が自動付与されるか確認

【起動方法】

Windows（推奨）:
  • ダブルクリック: run_sync.bat
  • コマンド: py -3.12 scripts/sync_monitor.py

Linux/Mac:
  py -3.12 scripts/sync_monitor.py

【停止方法】
  コンソール上で Ctrl+C を押下

【トラブルシューティング】

❓ エラー「MODULE NOT FOUND」
  → py -3.12 scripts/setup.py を再実行

❓ 同期されない
  → コンソール出力を確認
  → sync_monitor.py が実行中か確認

❓ frontmatter が追加されない
  → .md ファイルの保存場所を確認（08_Archive は除外）

【スクリプト一覧】

1. sync_monitor.py
   - Obsidian フォルダ監視メインスクリプト
   - ファイル作成/更新を検知→自動同期トリガー
   - 月初メンテナンス初期化

2. claude_memory_sync.py
   - Obsidian → Claude Code メモリ同期実行
   - MEMORY.md インデックス自動生成

3. setup.py（本スクリプト）
   - 依存ライブラリインストール
   - 初回同期実行

【カスタマイズ】

パス変更が必要な場合:
  sync_monitor.py 内の定数を編集
  - OBSIDIAN_PATH
  - CLAUDE_MEMORY_PATH
  - SCRIPTS_PATH

debounce 時間を変更する場合:
  sync_monitor.py の ObsidianChangeHandler.__init__()
  - self.debounce_delay = 3  # 秒

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 さっそく起動してみましょう！

  py -3.12 scripts/sync_monitor.py

🎉 Happy VTuber Life！
""")


def main():
    """セットアップメイン処理"""
    print(f"""
╔════════════════════════════════════════════════════════════╗
║  Obsidian 自動同期スクリプト セットアップ                ║
╚════════════════════════════════════════════════════════════╝
""")

    # Step 1: 依存ライブラリインストール
    if not install_dependencies():
        print("❌ セットアップ失敗（ライブラリインストールエラー）")
        sys.exit(1)

    # Step 2: 初回同期実行
    if not run_initial_sync():
        print("\n⚠️ 初回同期に失敗しました")
        print("   手動実行: py -3.12 scripts/claude_memory_sync.py")
        # ここでは続行（同期失敗でもスクリプトは動作可能）

    # Step 3: ランチャー作成
    create_launcher()

    # Step 4: 完了メッセージ
    print_next_steps()

    print("✅ セットアップ完了！\n")
    return True


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ セットアップエラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

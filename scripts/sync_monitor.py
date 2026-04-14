#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian ファイル監視 + 自動同期スクリプト

機能：
- Obsidian フォルダを監視
- 新規ファイル作成 → frontmatter 自動追加
- ファイル更新 → Claude Code メモリへ同期
- 月初 → メンテナンスチェックリスト初期化

実行方法：
  py -3.12 scripts/sync_monitor.py
"""

import os
import time
import sys
import io
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from datetime import datetime

# Windows コンソール出力を UTF-8 に設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# パス設定
OBSIDIAN_PATH = Path(__file__).parent.parent
CLAUDE_MEMORY_PATH = Path(r'C:\Users\owner\.claude\projects\C--Users-owner-MyVtuber\memory')
SCRIPTS_PATH = OBSIDIAN_PATH / 'scripts'


class ObsidianChangeHandler(FileSystemEventHandler):
    """Obsidian ファイル変更検知ハンドラー"""

    def __init__(self):
        self.last_sync_time = time.time()
        self.debounce_delay = 3  # 秒（連続更新時の多重実行回避）

    def on_created(self, event):
        """新規ファイル作成時"""
        if event.is_directory:
            return

        if not event.src_path.endswith('.md'):
            return

        rel_path = os.path.relpath(event.src_path, OBSIDIAN_PATH)
        if '08_Archive' in rel_path or 'scripts' in rel_path:
            return

        print(f"✨ 新規ファイル検知: {rel_path}")

        # frontmatter 自動追加
        self._add_frontmatter(event.src_path)

        # 同期実行
        self._trigger_sync()

    def on_modified(self, event):
        """ファイル更新時"""
        if event.is_directory:
            return

        if not event.src_path.endswith('.md'):
            return

        rel_path = os.path.relpath(event.src_path, OBSIDIAN_PATH)
        if '08_Archive' in rel_path or 'scripts' in rel_path or 'MAINTENANCE' in rel_path:
            return

        # debounce: 最後の同期から3秒以上経過したら実行
        now = time.time()
        if now - self.last_sync_time < self.debounce_delay:
            return

        print(f"📝 ファイル更新検知: {rel_path}")
        self._trigger_sync()

    def _add_frontmatter(self, filepath):
        """frontmatter がなければ追加"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # frontmatter 確認
            if content.startswith('---'):
                return  # 既に frontmatter がある

            # frontmatter 構築
            filename = os.path.basename(filepath)
            name = filename.replace('.md', '')

            # ファイル名から TTL を推測
            if filename.startswith('test_'):
                ttl = '7days'
            elif '_20260' in filename:
                ttl = '30days'  # 日付付きは短期
            else:
                ttl = 'permanent'

            frontmatter = f"""---
name: {name}
type: unknown
ttl: {ttl}
date: {datetime.now().strftime('%Y-%m-%d')}
tags:
  - #ttl/{ttl}
---

"""

            new_content = frontmatter + content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"  → frontmatter 追加: ttl={ttl}")

        except Exception as e:
            print(f"  ⚠️ frontmatter 追加失敗: {e}")

    def _trigger_sync(self):
        """Claude Code メモリへの同期トリガー"""
        self.last_sync_time = time.time()

        sync_script = SCRIPTS_PATH / 'claude_memory_sync.py'
        if not sync_script.exists():
            print("  ⚠️ claude_memory_sync.py が見つかりません")
            return

        try:
            subprocess.run(
                ['py', '-3.12', str(sync_script)],
                capture_output=True,
                timeout=10
            )
            print(f"  ✅ Claude Code メモリ同期完了")
        except subprocess.TimeoutExpired:
            print(f"  ⚠️ 同期がタイムアウト")
        except Exception as e:
            print(f"  ⚠️ 同期実行失敗: {e}")


def check_maintenance_needed():
    """月初かどうかをチェック"""
    today = datetime.now()
    return today.day == 1


def initialize_maintenance():
    """月初: MAINTENANCE.md チェックリスト初期化"""
    print("\n🔧 月次メンテナンス初期化処理...")

    maintenance_file = OBSIDIAN_PATH / 'MAINTENANCE.md'
    if not maintenance_file.exists():
        print("  ⚠️ MAINTENANCE.md が見つかりません")
        return

    try:
        with open(maintenance_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # チェックリストをリセット
        content = content.replace('- [x]', '- [ ]')

        # 最終実行日を更新
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        if '**最終更新**:' in content:
            content = content.replace(
                '**最終更新**:',
                f'**最終実行**: {now_str}\n**最後の更新**:'
            )

        with open(maintenance_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ チェックリスト初期化完了: {now_str}")

    except Exception as e:
        print(f"  ⚠️ メンテナンス初期化失敗: {e}")


def start_monitoring():
    """Obsidian ファイル監視開始"""
    print(f"""
╔════════════════════════════════════════════════════════════╗
║  Obsidian 自動同期スクリプト起動                          ║
║  監視フォルダ: {OBSIDIAN_PATH.name}
║  クローディング先: Claude Code メモリ                    ║
╚════════════════════════════════════════════════════════════╝
""")

    # 月初チェック
    if check_maintenance_needed():
        initialize_maintenance()

    # ファイル監視開始
    observer = Observer()
    handler = ObsidianChangeHandler()
    observer.schedule(handler, str(OBSIDIAN_PATH), recursive=True)
    observer.start()

    print(f"\n🟢 監視開始... (Ctrl+C で停止)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 監視停止中...")
        observer.stop()

    observer.join()
    print("✅ 監視終了")


if __name__ == '__main__':
    try:
        start_monitoring()
    except ImportError:
        print("""
⚠️ 必要なライブラリがインストールされていません。

以下を実行してセットアップしてください：
  py -3.12 scripts/setup.py

またはスキップして以下をインストール：
  pip install watchdog pyyaml
""")
        sys.exit(1)
    except Exception as e:
        print(f"❌ エラー: {e}")
        sys.exit(1)

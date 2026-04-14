#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian → Claude Code メモリ自動同期スクリプト

機能：
- Obsidian の全 .md ファイルを読み込み
- TTL タグを抽出
- Claude Code の MEMORY.md インデックスを自動生成 + 更新

実行方法：
  py -3.12 scripts/claude_memory_sync.py

呼び出し元：
  - sync_monitor.py（ファイル更新時に自動実行）
  - manual（手動実行）
"""

import os
import sys
import io
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Windows コンソール出力を UTF-8 に設定
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# scoring.py をインポート
sys.path.insert(0, str(Path(__file__).parent))
try:
    from scoring import rank_files_by_scoring, generate_hot_memory_markdown
except ImportError:
    print("⚠️ scoring.py が見つかりません")
    rank_files_by_scoring = None
    generate_hot_memory_markdown = None

# パス設定
OBSIDIAN_PATH = Path(__file__).parent.parent
CLAUDE_MEMORY_PATH = Path(r'C:\Users\owner\.claude\projects\C--Users-owner-MyVtuber\memory')


def read_obsidian_files():
    """
    Obsidian の全 .md ファイルを読み込み
    frontmatter の TTL + タグ情報を抽出
    """
    files_data = []

    for root, dirs, files in os.walk(OBSIDIAN_PATH):
        # 除外フォルダ
        dirs[:] = [d for d in dirs if d not in ['08_Archive', 'scripts', '.obsidian']]

        for filename in files:
            if not filename.endswith('.md'):
                continue

            filepath = Path(root) / filename
            rel_path = filepath.relative_to(OBSIDIAN_PATH)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # frontmatter 抽出
                frontmatter = {}
                if content.startswith('---'):
                    end = content.find('---', 3)
                    if end > 0:
                        try:
                            fm_str = content[3:end]
                            frontmatter = yaml.safe_load(fm_str) or {}
                        except yaml.YAMLError:
                            pass

                name = frontmatter.get('name', filename.replace('.md', ''))
                ttl = frontmatter.get('ttl', 'unknown')
                description = frontmatter.get('description', '')
                tags = frontmatter.get('tags', [])

                files_data.append({
                    'rel_path': str(rel_path).replace('\\', '/'),
                    'filename': filename,
                    'name': name,
                    'ttl': ttl,
                    'description': description,
                    'tags': tags if isinstance(tags, list) else []
                })

            except Exception as e:
                print(f"  ⚠️ 読み込み失敗 {rel_path}: {e}")

    return files_data


def categorize_files(files_data):
    """ファイルをカテゴリ別（フォルダ別）に分類"""
    categories = defaultdict(list)

    for file in files_data:
        # rel_path の最初のセグメントがカテゴリ
        category = file['rel_path'].split('/')[0]
        categories[category].append(file)

    return dict(sorted(categories.items()))


def generate_memory_index(files_data):
    """
    Claude Code MEMORY.md 用インデックスを生成

    既存の「🔥 今週のホットメモリ」セクションは保持
    """
    categories = categorize_files(files_data)

    md_lines = [
        "# MEMORY INDEX",
        "",
        f"**Obsidian自動同期日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**総ファイル数**: {len(files_data)} ファイル",
        "",
        "## 🔧 TTL管理ルール",
        "- `permanent`: 無期限保持（user / feedback / 確定済み意思決定）",
        "- `until-completion`: 完了まで（進行中プロジェクト）",
        "- `90days`: 90日で削除候補（参考資料・研究ネタ）",
        "- `30days`: 30日で削除（短期計画・分析結果）",
        "- `7days`: 7日で削除（一時メモ）",
        "",
        "最後の参照日を記録。参照時に TTL がリセットされます。",
        "",
        "---",
        "",
    ]

    # カテゴリごとにセクションを生成
    for category, files in categories.items():
        # カテゴリ名をきれいに整形
        category_title = {
            '00_Profile': '👤 プロフィール',
            '01_Strategy': '📈 戦略・方針',
            '02_Projects': '🚀 プロジェクト進行中',
            '03_Skills': '🎓 スキル & 評価',
            '04_Analysis': '📊 分析結果',
            '05_Content': '📝 コンテンツ資料',
            '06_Operations': '📋 運用・スケジュール',
            '07_Reference': '📚 参考資料',
        }.get(category, f'📁 {category}')

        md_lines.append(f"## {category_title}")
        md_lines.append("")

        # ファイルをリストアップ
        for file in sorted(files, key=lambda x: x['filename']):
            ttl_badge = f"`#{file['ttl']}`" if file['ttl'] != 'unknown' else ""
            description = f" — {file['description']}" if file['description'] else ""

            # Obsidian wikilink 形式でリンク生成
            link = f"[[{file['rel_path']}|{file['name']}]]"

            md_lines.append(f"- {link} {ttl_badge}{description}")

        md_lines.append("")

    return "\n".join(md_lines)


def preserve_hot_memory(existing_memory):
    """
    既存の MEMORY.md から「🔥 今週のホットメモリ」セクションを抽出

    自動同期時にホットメモリセクションは上書きせず保持
    """
    if '## 🔥 今週のホットメモリ' not in existing_memory:
        return ""

    start = existing_memory.find('## 🔥 今週のホットメモリ')
    # 次のセクション（##）までを抽出
    end = existing_memory.find('\n##', start + 1)
    if end == -1:
        return existing_memory[start:]
    else:
        return existing_memory[start:end].strip() + "\n"


def sync_to_claude_memory(files_data):
    """
    Claude Code メモリへの同期実行

    R×I×R スコアリングで「🔥 今週のホットメモリ」を動的生成
    """
    if not CLAUDE_MEMORY_PATH.exists():
        print(f"❌ Claude Code メモリフォルダが見つかりません: {CLAUDE_MEMORY_PATH}")
        return False

    memory_file = CLAUDE_MEMORY_PATH / 'MEMORY.md'

    # 新しいインデックスを生成
    new_index = generate_memory_index(files_data)

    # Hot Memory セクション: R×I×R スコアリングで動的生成
    hot_memory = ""
    if rank_files_by_scoring and generate_hot_memory_markdown:
        try:
            ranked = rank_files_by_scoring(files_data, top_n=5)
            hot_memory = generate_hot_memory_markdown(ranked)
            if hot_memory:
                print(f"   🔥 ホットメモリ生成完了: 上位5ファイルランキング")
        except Exception as e:
            print(f"  ⚠️ スコアリング生成失敗: {e}")
            # 失敗時は既存を保持
            if memory_file.exists():
                try:
                    with open(memory_file, 'r', encoding='utf-8') as f:
                        existing = f.read()
                    hot_memory = preserve_hot_memory(existing)
                except Exception as e2:
                    print(f"  ⚠️ Hot Memory 保持失敗: {e2}")
    else:
        # scoring.py が利用不可の場合は既存を保持
        if memory_file.exists():
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    existing = f.read()
                hot_memory = preserve_hot_memory(existing)
            except Exception as e:
                print(f"  ⚠️ Hot Memory 保持失敗: {e}")

    # インデックス + Hot Memory を結合
    final_content = new_index
    if hot_memory:
        final_content += "\n" + hot_memory

    # MEMORY.md を更新
    try:
        with open(memory_file, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"✅ MEMORY.md 同期完了: {len(files_data)} ファイル")
        if hot_memory:
            print(f"   🔥 ホットメモリ生成完了: 上位5ファイルランキング")
        return True

    except Exception as e:
        print(f"❌ MEMORY.md 更新失敗: {e}")
        return False


def main():
    """メイン処理"""
    print(f"\n📚 Obsidian → Claude Code メモリ同期スクリプト")
    print(f"   Obsidian: {OBSIDIAN_PATH.name}")
    print(f"   Claude Memory: {CLAUDE_MEMORY_PATH.name}")
    print(f"   実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Obsidian ファイル読み込み
    print("📖 Obsidian ファイル読み込み中...")
    files_data = read_obsidian_files()
    print(f"   ✅ {len(files_data)} ファイル検出\n")

    if not files_data:
        print("⚠️ ファイルが見つかりませんでした")
        return False

    # Claude Code メモリへ同期
    print("💾 Claude Code メモリへ同期中...")
    success = sync_to_claude_memory(files_data)

    if success:
        print(f"\n✨ 同期完了！")
        print(f"   更新先: {CLAUDE_MEMORY_PATH / 'MEMORY.md'}")
        return True
    else:
        print(f"\n❌ 同期に失敗しました")
        return False


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except ImportError as e:
        print(f"❌ 必要なライブラリがインストールされていません: {e}")
        print("\n以下を実行してセットアップしてください:")
        print("  py -3.12 scripts/setup.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

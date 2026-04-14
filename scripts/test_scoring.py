#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スコアリング関数のテスト
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from scoring import rank_files_by_scoring, generate_hot_memory_markdown
from claude_memory_sync import read_obsidian_files

# テストデータ読み込み
print("📚 Obsidian ファイル読み込み中...")
files_data = read_obsidian_files()
print(f"✅ {len(files_data)} ファイル検出\n")

# ランキング生成
print("🔄 R×I×R スコアリング実行中...")
ranked = rank_files_by_scoring(files_data, top_n=5)
print(f"✅ {len(ranked)} ファイルランキング生成\n")

# ランキング結果を表示
print("📊 ランキング結果:")
for idx, item in enumerate(ranked, 1):
    try:
        if len(item) >= 5:
            file_info, score, recency, importance, relevance = item[0], item[1], item[2], item[3], item[4]
            print(f"{idx}. {file_info.get('name', 'Unknown')} - Score: {score:.2f}")
        else:
            print(f"{idx}. Error: item has {len(item)} elements (expected 5+)")
    except Exception as e:
        print(f"{idx}. Error: {e}")

# Markdown 生成テスト
print("\n\n🎯 Markdown 生成テスト...")
try:
    markdown = generate_hot_memory_markdown(ranked)
    if markdown:
        print(f"✅ Markdown 生成成功 ({len(markdown)} 文字)")
        print("\n--- 生成内容 ---")
        print(markdown[:500])
    else:
        print("⚠️ Markdown が空です")
except Exception as e:
    print(f"❌ Markdown 生成失敗: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ テスト完了")

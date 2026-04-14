#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
morning_digest.py
毎朝の TO-DO・新着・スケジュールを自動抽出・表示
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import re

# Windows 対応
sys.stdout.reconfigure(encoding='utf-8')

# パス設定
VTUBER_ROOT = Path("C:/Users/owner/MyVtuber")
MEMORY_ROOT = Path("C:/Users/owner/.claude/projects/C--Users-owner-MyVtuber/memory")
LOGS_ROOT = VTUBER_ROOT / "logs"
RAW_SOURCES = VTUBER_ROOT / "raw-sources"
CLIPPINGS_ROOT = VTUBER_ROOT / "Obsidian/Kanoko Knowledge Base/Clippings"

def read_memory_file(filename):
    """メモリファイルを読み込み"""
    file_path = MEMORY_ROOT / filename
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def parse_yaml_frontmatter(content):
    """YAML frontmatter を解析"""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    yaml_content = match.group(1)
    data = {}

    for line in yaml_content.split('\n'):
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip().strip('"\'')
        data[key] = value

    return data

def get_clippings(days=7):
    """過去 N 日間のクリップを取得"""
    if not CLIPPINGS_ROOT.exists():
        return []

    now = datetime.now()
    cutoff = now - timedelta(days=days)
    clippings = []

    for md_file in CLIPPINGS_ROOT.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # YAML frontmatter を解析
            metadata = parse_yaml_frontmatter(content)

            if 'created' in metadata:
                try:
                    created = datetime.strptime(metadata['created'], '%Y-%m-%d')
                    if created > cutoff:
                        clippings.append({
                            'title': metadata.get('title', md_file.name),
                            'source': metadata.get('source', ''),
                            'created': metadata.get('created', ''),
                            'description': metadata.get('description', '')[:100] + '...',
                            'talk-points': metadata.get('talk-points', ''),  # 配信トーク案
                            'shorts-ready': metadata.get('shorts-ready', '').lower() == 'true',  # 短編化フラグ
                            'shorts-hook': metadata.get('shorts-hook', '')  # Shorts のフック
                        })
                except ValueError:
                    pass
        except Exception:
            pass

    # 作成日で降順ソート
    return sorted(clippings, key=lambda x: x['created'], reverse=True)

def extract_open_actions():
    """action-log.md から open action を抽出"""
    action_log = LOGS_ROOT / "action-log.md"
    if not action_log.exists():
        return []

    with open(action_log, 'r', encoding='utf-8') as f:
        content = f.read()

    actions = []
    lines = content.split('\n')
    for line in lines:
        if '- [ ]' in line:  # チェックボックスなし = 未完了
            # マークダウン形式を整形
            action = line.replace('- [ ] ', '').strip()
            actions.append(action)

    return actions

def get_new_files(hours=24):
    """過去 N 時間内の新規ファイルを取得"""
    now = datetime.now()
    cutoff = now - timedelta(hours=hours)
    new_files = []

    for root, dirs, files in os.walk(RAW_SOURCES):
        for file in files:
            file_path = Path(root) / file
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if mtime > cutoff:
                rel_path = file_path.relative_to(RAW_SOURCES)
                new_files.append({
                    'name': file,
                    'path': str(rel_path),
                    'modified': mtime.strftime('%Y-%m-%d %H:%M')
                })

    return sorted(new_files, key=lambda x: x['modified'], reverse=True)

def read_decision_log():
    """decision-log.md から本日の決定事項を抽出"""
    decision_log = LOGS_ROOT / "decision-log.md"
    if not decision_log.exists():
        return []

    with open(decision_log, 'r', encoding='utf-8') as f:
        content = f.read()

    today = datetime.now().strftime('%Y-%m-%d')
    decisions = []

    lines = content.split('\n')
    in_today_section = False
    for line in lines:
        if f'## {today}' in line:
            in_today_section = True
            continue
        if in_today_section and line.startswith('## ') and today not in line:
            break
        if in_today_section and line.startswith('#### '):
            decisions.append(line.replace('#### ', '').strip())

    return decisions

def get_hot_memory():
    """MEMORY.md からホットメモリ（優先度の高いファイル）を抽出"""
    memory_index = MEMORY_ROOT / "MEMORY.md"
    if not memory_index.exists():
        return []

    with open(memory_index, 'r', encoding='utf-8') as f:
        content = f.read()

    # 🔥 ホットメモリセクションを抽出（簡易版）
    hot_memory = []
    lines = content.split('\n')
    in_hot_section = False

    for line in lines:
        if '🔥 ホットメモリ' in line or '本週のホットメモリ' in line:
            in_hot_section = True
            continue
        if in_hot_section:
            if line.startswith('##'):  # 次のセクション
                break
            if '**' in line and '.md' in line:
                # [テキスト](ファイル.md) 形式を抽出
                hot_memory.append(line.strip())

    return hot_memory[:3]  # Top 3

def is_weekend():
    """金曜日かどうかを判定（短編化候補表示用）"""
    return datetime.now().weekday() == 4  # 4 = Friday

def get_lecture_candidates():
    """Obsidian Scripts フォルダから講義スライドを検出"""
    scripts_root = VTUBER_ROOT / "Obsidian/Kanoko Knowledge Base/Scripts"
    if not scripts_root.exists():
        return []

    lectures = []
    for md_file in scripts_root.glob("lecture_slides_*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # タイトルを抽出（# 見出し）
            title_match = None
            for line in content.split('\n'):
                if line.startswith('# '):
                    title_match = line.replace('# ', '').strip()
                    break

            if title_match:
                lectures.append({
                    'title': title_match,
                    'file': md_file.name,
                    'duration': '9～10分'  # デフォルト
                })
        except Exception:
            pass

    return lectures

def write_morning_briefing(briefing_text):
    """朝のブリーフィングをログに記録"""
    briefing_file = LOGS_ROOT / "morning-briefing.md"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(briefing_file, 'a', encoding='utf-8') as f:
        f.write(f"\n## {timestamp}\n\n")
        f.write(briefing_text)
        f.write("\n\n")

def main():
    print("\n" + "="*60)
    print("🌅 Morning Digest - 朝のタスク確認")
    print("="*60)
    print(f"📅 {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n")

    # 1. Open Actions
    print("📋 本日の未完了タスク（Action Items）")
    print("-" * 60)
    actions = extract_open_actions()
    if actions:
        for i, action in enumerate(actions[:10], 1):  # Top 10
            print(f"  {i}. {action}")
    else:
        print("  ✓ タスクはありません")
    print()

    # 2. New Files
    print("📥 過去24時間の新着ファイル")
    print("-" * 60)
    new_files = get_new_files(hours=24)
    if new_files:
        for file_info in new_files[:5]:  # Top 5
            print(f"  📄 {file_info['path']}")
            print(f"     修正: {file_info['modified']}")
    else:
        print("  新着ファイルはありません")
    print()

    # 3. Today's Decisions
    print("💡 本日の決定事項")
    print("-" * 60)
    decisions = read_decision_log()
    if decisions:
        for decision in decisions:
            print(f"  ✓ {decision}")
    else:
        print("  本日の決定事項はまだ記録されていません")
    print()

    # 4. Memory Status
    print("💾 Memory System 状態")
    print("-" * 60)
    memory_files = list(MEMORY_ROOT.glob("*.md"))
    print(f"  メモリファイル数: {len(memory_files)} 個")

    memory_mtime = (MEMORY_ROOT / 'MEMORY.md').stat().st_mtime
    last_sync_dt = datetime.fromtimestamp(memory_mtime)
    print(f"  最後の同期: {last_sync_dt.strftime('%Y-%m-%d %H:%M')}")
    print()

    # 5. Hot Memory
    print("🔥 ホットメモリ（今日参照すべき）")
    print("-" * 60)
    hot_memory = get_hot_memory()
    if hot_memory:
        for memory in hot_memory:
            # マークダウン形式をクリーンアップして表示
            clean = memory.replace('**', '').replace('1. ', '').replace('2. ', '').replace('3. ', '')
            print(f"  {clean}")
    else:
        print("  ホットメモリはまだ更新されていません")
    print()

    # 6. Weekly Clippings
    print("📌 今週のクリップ（配信で使えるネタ）")
    print("-" * 60)
    clippings = get_clippings(days=7)
    if clippings:
        for i, clip in enumerate(clippings[:5], 1):  # Top 5
            print(f"  {i}. 【{clip['created']}】{clip['title']}")
            if clip['source']:
                print(f"     URL: {clip['source']}")
            if clip['description']:
                print(f"     概要: {clip['description'][:80]}")
            if clip['talk-points']:
                print(f"     💡 配信トーク案: {clip['talk-points']}")
    else:
        print("  今週のクリップはありません")
    print()

    # 7. Lecture Candidates
    print("📚 講義候補（配信で話す資料）")
    print("-" * 60)
    lectures = get_lecture_candidates()
    if lectures:
        for i, lecture in enumerate(lectures[:3], 1):
            print(f"  {i}. {lecture['title']}")
            print(f"     ⏱️  想定時間: {lecture['duration']}")
            print(f"     📄 ファイル: {lecture['file']}")
        print()
        print("  💡 実行: Obsidian で Scripts フォルダを開いて、スライドを確認")
    else:
        print("  講義スライドがまだありません")
    print()

    # 8. Weekly Shorts Candidates (金曜日のみ)
    if is_weekend():
        print("📹 今週の短編化候補（YouTube Shorts）")
        print("-" * 60)
        shorts_candidates = [c for c in clippings if c['shorts-ready']]
        if shorts_candidates:
            for i, clip in enumerate(shorts_candidates[:5], 1):
                print(f"  {i}. {clip['title']}")
                if clip['shorts-hook']:
                    print(f"     🎬 Shorts 案: {clip['shorts-hook']}")
                if clip['source']:
                    print(f"     元動画: {clip['source']}")
            print()
            print("  💡 実行: /script-to-short または /youtube-shorts で短編化")
        else:
            print("  短編化候補はありません")
        print()

    print("="*60)
    print("✅ Morning Digest 完了\n")

    # ログに記録
    briefing_text = f"""
### Open Actions
{chr(10).join([f"- {a}" for a in actions[:10]])}

### New Files
{chr(10).join([f"- {f['path']}" for f in new_files[:5]])}

### Decisions
{chr(10).join([f"- {d}" for d in decisions])}

### Weekly Clippings
{chr(10).join([f"- **[{c['created']}]** {c['title']}" for c in clippings[:5]])}
"""
    write_morning_briefing(briefing_text)

if __name__ == "__main__":
    main()

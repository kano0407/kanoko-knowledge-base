#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R×I×R スコアリング公式実装

Score = Recency（新しさ）× Importance（重要度）× Relevance（関連性）

用途：毎セッション開始時に「今週のホットメモリ」をランキング生成
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple

# パス設定
OBSIDIAN_PATH = Path(__file__).parent.parent


def calc_recency(last_ref_date_str: str) -> float:
    """
    Recency（新しさ）を計算 — 段階減衰モデル

    Args:
        last_ref_date_str: 最後の参照日（YYYY-MM-DD 形式）

    Returns:
        float: Recency スコア（0.1-1.0）
    """
    try:
        last_ref_date = datetime.strptime(last_ref_date_str, '%Y-%m-%d')
    except (ValueError, TypeError):
        # 日付パース失敗時はデフォルト値
        return 0.5

    today = datetime.now()
    days_ago = (today - last_ref_date).days

    if days_ago <= 7:
        return 1.0
    elif days_ago <= 14:
        return 0.8
    elif days_ago <= 30:
        return 0.5
    elif days_ago <= 90:
        return 0.3
    else:
        return 0.1


def calc_importance(ttl: str, is_in_hot_memory: bool = False) -> float:
    """
    Importance（重要度）を計算 — TTL + 位置で判定

    Args:
        ttl: TTL タイプ（permanent / until-completion / 90days / 30days / 7days）
        is_in_hot_memory: 「🔥 今週のホットメモリ」に記載されているか

    Returns:
        float: Importance スコア（0.3-1.0）
    """
    if is_in_hot_memory:
        return 1.0

    importance_map = {
        'permanent': 0.8,
        'until-completion': 0.6,
        '30days': 0.5,
        '90days': 0.4,
        '7days': 0.2,
        'unknown': 0.5
    }

    return importance_map.get(ttl, 0.5)


def calc_relevance_simple(tags: List[str], filename: str) -> float:
    """
    Relevance（関連性）を簡易計算 — タグベース

    LLM呼び出しなしで、タグから推定

    Args:
        tags: ファイルのタグリスト
        filename: ファイル名

    Returns:
        float: Relevance スコア（0.1-1.0）
    """
    score = 0.5  # デフォルト

    # タグをクリーニング（None を除外、文字列に変換）
    if not tags:
        tags = []
    tags = [str(t) for t in tags if t is not None]

    # タグベースのスコア調整
    tag_str = ' '.join(tags)

    # 優先度タグ
    if '#priority/p1' in tag_str:
        score = max(score, 0.9)
    elif '#priority/p2' in tag_str:
        score = max(score, 0.7)

    # ステータスタグ
    if '#status/in-progress' in tag_str:
        score = max(score, 0.8)
    elif '#status/completed' in tag_str:
        score = min(score, 0.4)

    # プロジェクト関連度
    if 'youtube' in filename.lower() or '#project/youtube' in tag_str:
        score = max(score, 0.8)

    if 'broadcast' in filename.lower() or 'talk' in filename.lower():
        score = max(score, 0.85)

    # 参考資料は低め
    if '#reference' in tag_str or 'reference' in filename.lower():
        score = min(score, 0.5)

    return max(0.1, min(1.0, score))  # 0.1-1.0 に正規化


def rank_files_by_scoring(
    files_data: List[Dict],
    today_str: str = None,
    top_n: int = 5
) -> List[Tuple[Dict, float]]:
    """
    全ファイルを R×I×R スコアでランキング

    Args:
        files_data: ファイル情報リスト
        today_str: 本日の日付（YYYY-MM-DD、Noneなら today() を使用）
        top_n: 上位何個を返すか（デフォルト: 5）

    Returns:
        List[Tuple]: [(ファイル情報, スコア), ...] をスコア降順でソート
    """
    if today_str is None:
        today_str = datetime.now().strftime('%Y-%m-%d')

    ranked = []

    for file_info in files_data:
        # 1. Recency を計算
        # frontmatter から date フィールドを取得
        last_ref_date_str = file_info.get('date', today_str)
        recency = calc_recency(last_ref_date_str)

        # 2. Importance を計算
        ttl = file_info.get('ttl', 'unknown')
        importance = calc_importance(ttl, is_in_hot_memory=False)

        # 3. Relevance を計算（簡易版）
        tags = file_info.get('tags', [])
        filename = file_info.get('filename', '')
        relevance = calc_relevance_simple(tags, filename)

        # 4. スコア計算
        score = recency * importance * relevance

        ranked.append((file_info, score, recency, importance, relevance))

    # スコア降順でソート
    ranked.sort(key=lambda x: x[1], reverse=True)

    return ranked[:top_n] if top_n else ranked


def generate_hot_memory_markdown(ranked_files: List[Tuple]) -> str:
    """
    R×I×R ランキング から Markdown 形式の「🔥 今週のホットメモリ」セクション生成

    Args:
        ranked_files: ランキング済みファイルリスト（各要素は (file_info, score, recency, importance, relevance)）

    Returns:
        str: Markdown セクション
    """
    if not ranked_files:
        return ""

    lines = [
        "## 🔥 今週のホットメモリ（R×I×R スコア順）",
        "",
        "> このセクションはセッション開始時に自動更新されます。",
        "> 今週最も関連性が高いファイルが優先表示されます。",
        "",
        "### スコアリング公式",
        "```",
        "Score = Recency（新しさ）× Importance（重要度）× Relevance（関連性）",
        "```",
        "",
        "**Recency（新しさ）**: 最後の参照日から経過日数",
        "- 0-7日: 1.0  |  8-14日: 0.8  |  15-30日: 0.5  |  31-90日: 0.3  |  91日+: 0.1",
        "",
        "**Importance（重要度）**: TTL 設定値",
        "- permanent: 0.8  |  until-completion: 0.6  |  30days: 0.5  |  90days: 0.4",
        "",
        "**Relevance（関連性）**: タグとファイル名から推定",
        "- 優先度P1: 0.9  |  進行中プロジェクト: 0.8  |  参考資料: 0.3-0.5",
        "",
        "### 本週のトップ5",
        ""
    ]

    for idx, item in enumerate(ranked_files, 1):
        try:
            if not item or len(item) < 5:
                continue

            file_info = item[0]
            score = item[1]
            recency = item[2]
            importance = item[3]
            relevance = item[4]

            if not file_info:
                continue

            name = str(file_info.get('name', file_info.get('filename', ''))).strip()
            rel_path = str(file_info.get('rel_path', '')).strip()
            description = str(file_info.get('description', '')).strip()

            # 必須フィールドチェック
            if not name or not rel_path:
                continue

            # wikilink 形式
            link = f"[[{rel_path}|{name}]]"

            # 説明
            desc_text = f" — {description}" if description else ""

            # スコア詳細
            score_detail = f"Score: {score:.2f} (R:{recency:.2f} × I:{importance:.2f} × Rel:{relevance:.2f})"

            lines.append(f"{idx}. **{link}** {score_detail}")
            lines.append(f"   {desc_text}")
            lines.append("")

        except Exception as e:
            # 個別エラーはスキップ
            continue

    lines.append("---")
    lines.append("")

    return "\n".join(lines)


if __name__ == '__main__':
    # テスト用
    print("R×I×R スコアリング モジュール")
    print("使用方法: claude_memory_sync.py から import して使用")

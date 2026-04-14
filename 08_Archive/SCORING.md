---
name: SCORING
type: unknown
date: 2026-04-14
tags:
  - 
---
# R×I×R スコアリング公式 — 想起の優先順位付け

**実装日**: 2026-04-11  
**参考文献**: Stanford Generative Agents (Park et al., 2023)

---

## 概要

メモリシステムにおいて、「どのファイルを優先的に思い出すか」を決定するための数学的フレームワーク。

セッション開始時に、全メモリファイルを自動採点し、スコア上位3～5個を「今週のホットメモリ」として MEMORY.md に表示します。

```
Score(memory) = Recency（新しさ）× Importance（重要度）× Relevance（関連性）
```

---

## A. Recency（新しさ）— 段階減衰モデル

最後の参照日から経過日数に基づく段階的な減衰。

```
最後の参照日から経過日数 → スコア

- 1週間以内（0-7日）      → 1.0
- 1〜2週間（8-14日）      → 0.8
- 2週間〜1ヶ月（15-30日）  → 0.5
- 1ヶ月超（31-90日）      → 0.3
- 3ヶ月超（91日+）        → 0.1（削除候補に接近）
```

### Python実装例

```python
from datetime import datetime, timedelta

def calc_recency(last_ref_date, today):
    """
    最後の参照日から経過日数でRecencyを計算
    
    Args:
        last_ref_date: datetime オブジェクト（最後の参照日）
        today: datetime オブジェクト（本日）
    
    Returns:
        float: Recency スコア（0.1-1.0）
    """
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
```

### 実例

- user_vtuber_profile.md（本日参照）: 1.0
- project_x_mindset.md（3日前）: 0.8
- reference_notion_structure.md（11日前）: 0.8
- project_notebooklm_analysis_20260410.md（1日前）: 1.0

---

## B. Importance（重要度）— ファイル格納先 + TTL で判定

ファイルの「永続性」と「参考頻度」を組み合わせたスコア。

```
MEMORY.md の冀頭に記載 ← 1.0（高頻度参照）
frameworks.md または decisions.md ← 0.8（意思決定・パターン集）
project_*.md（ttl: until-completion） ← 0.6（進行中プロジェクト）
reference_*.md ← 0.3（参考資料）
project_*.md（ttl: 30days） ← 0.5（短期分析・結果）
project_*.md（ttl: 90days） ← 0.4（中期参考）
```

### Python実装例

```python
def calc_importance(file_category, file_ttl, is_in_memory_top=False):
    """
    ファイルの重要度をスコアリング
    
    Args:
        file_category: "user" / "feedback" / "project" / "reference" 等
        file_ttl: "permanent" / "until-completion" / "90days" / "30days" / "7days"
        is_in_memory_top: MEMORY.md の冀頭に記載されているか
    
    Returns:
        float: Importance スコア（0.3-1.0）
    """
    if is_in_memory_top:
        return 1.0
    elif file_category in ["frameworks", "decisions"]:
        return 0.8
    elif file_ttl == "until-completion":
        return 0.6
    elif file_ttl == "30days":
        return 0.5
    elif file_ttl == "90days":
        return 0.4
    elif file_category == "reference":
        return 0.3
    else:
        return 0.5  # デフォルト
```

### 実例

- user_vtuber_profile.md（type: user）: 1.0
- feedback_claude_behavior.md（MEMORY.md 冀頭）: 1.0
- project_broadcast_schedule_202604.md（until-completion）: 0.6
- reference_vtuber_talk_analysis.md（reference）: 0.3

---

## C. Relevance（関連性）— LLMによる文脈判定

**最も複雑な要素。** 今日の文脈と各メモリファイルの関連度を判定。

```
完全に関連していく： 1.0
例: 今日配信がある → broadcast_*.md / 4月15日初配信 → project_broadcast_schedule_202604.md

かなり関連： 0.7
例: YouTube Shorts について → youtube_*.md / 企画について → project_*_analysis.md

やや関連： 0.4
例: X（Twitter）について → project_x_*.md / マーケティング戦略 → project_*_mindset.md

関連なし： 0.1
例: OBS開発について → project_viewer_overlay.md（開発中止中）
```

### Python実装例（Claude API使用）

```python
from anthropic import Anthropic

def calc_relevance(file_info, today_context, claude_client):
    """
    MEMORY.md インデックス + 今日の文脈から Relevance を計算
    Claude API を使用してセマンティック判定
    
    Args:
        file_info: {
            'title': ファイルタイトル,
            'description': 説明文,
            'tags': ['tag1', 'tag2'],
            'ttl': 'ttl値'
        }
        today_context: {
            'date': '2026-04-11',
            'task': 'ユーザーが今やりたいこと',
            'schedule': '今日のスケジュール',
            'theme': '今月のテーマ'
        }
        claude_client: Anthropic() クライアント
    
    Returns:
        float: Relevance スコア（0.1-1.0）
    """
    
    prompt = f"""
    【今日の文脈】
    日付: {today_context['date']}
    ユーザーのタスク: {today_context['task']}
    スケジュール: {today_context['schedule']}
    月次テーマ: {today_context['theme']}
    
    【メモリファイル】
    タイトル: {file_info['title']}
    説明: {file_info['description']}
    タグ: {', '.join(file_info['tags'])}
    TTL: {file_info['ttl']}
    
    【質問】
    このメモリファイルは今日のタスク/文脈とどの程度関連していますか？
    スコア: 0.1（関連なし）~ 1.0（完全に関連）
    
    数字のみを返してください。例: 0.7
    """
    
    response = claude_client.messages.create(
        model="claude-opus-4-6",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        score = float(response.content[0].text.strip())
        return max(0.1, min(1.0, score))  # 0.1-1.0 の範囲に正規化
    except:
        return 0.5  # エラーの場合はデフォルト値
```

---

## スコアリング実行フロー（セッション開始時）

```python
def rank_memories_by_rxi r(memory_files, today_context, claude_client):
    """
    全メモリファイルを R×I×R でランキング
    
    Returns:
        List[Tuple[file_info, score]]: スコア降順にソート
    """
    ranked = []
    
    for file in memory_files:
        # 1. Recency を計算
        recency = calc_recency(file['last_ref_date'], today_context['date'])
        
        # 2. Importance を計算
        importance = calc_importance(
            file['category'],
            file['ttl'],
            file['is_in_memory_top']
        )
        
        # 3. Relevance を計算（LLM呼び出し）
        relevance = calc_relevance(file, today_context, claude_client)
        
        # 4. スコアを計算
        score = recency * importance * relevance
        
        ranked.append((file, score))
    
    # スコア降順でソート
    ranked.sort(key=lambda x: x[1], reverse=True)
    
    return ranked
```

---

## MEMORY.md への自動反映

スコアリング実行後、「今週のホットメモリ」セクションを以下のように更新：

```markdown
## 🔥 今週のホットメモリ（R×I×R スコア順）

1. `project_broadcast_schedule_202604.md` — Score: 0.96
   - Recency: 1.0 × Importance: 0.6 × Relevance: 1.0

2. `project_content_format_strategy_202604.md` — Score: 0.84
   - Recency: 1.0 × Importance: 0.6 × Relevance: 0.7

[以下、スコア降順で続く...]
```

---

## 実装方針：3つのレベル

### レベル1: 手動実装（今すぐできる）
- MEMORY.md の冀頭に「今週のホットメモリ」セクション作成（テンプレート付き）
- セッション開始時に「いま何をしたいですか？」と聞いて、関連ファイルを手動でピックアップ
- スコアは「感覚的に」上位3～5個を記入

**メリット**: 今すぐ始められる  
**デメリット**: 毎回手動が必要

### レベル2: 半自動化（スキル化）
- `memory-ranker` スキルを Claude Code に登録
- ユーザーが `/memory-ranker` を実行 → 今日のホットメモリを自動生成
- MEMORY.md を自動更新

**メリット**: 1コマンドで自動更新可能  
**デメリット**: 手動実行が必要

### レベル3: 完全自動化（フック化）
- `.claude/settings.json` にセッション開始フックを登録
- Claude Code 起動時に自動実行
- ユーザーへの提示は自動（「今週のホットメモリを更新しました」）

**メリット**: 完全自動、ユーザーの介入なし  
**デメリット**: LLMへの呼び出しが増加 → トークン消費増加

---

## トークン効率化のヒント

**LLM呼び出し最小化**：
- Relevance 判定は「定期的」（毎セッション or 毎日）ではなく「定期メンテナンス時のみ」
- Recency と Importance は計算量が少ないため毎回でも OK
- 毎セッション時は「前回のランキング」をキャッシュして微調整

**キャッシュ戦略**：
```python
# 前回のランキング（昨日）
cached_ranking = [
    {'file': 'project_broadcast_schedule_202604.md', 'score': 0.96},
    ...
]

# 本日のランキング（Recency のみ更新）
today_ranking = update_recency_only(cached_ranking, today)
```

---

## 検証チェックリスト

実装後、以下を確認してください：

- [ ] R×I×R 公式がドキュメント化されている
- [ ] MEMORY.md に「🔥 今週のホットメモリ」セクションがある
- [ ] スコア上位3～5個が正しく表示されている
- [ ] Recency / Importance / Relevance がそれぞれ計算されている
- [ ] 月初の MAINTENANCE.md 実行時にランキングが更新される

---

## 次のステップ

1. **今すぐ**: レベル1（手動実装）を試す
2. **来月**: レベル2（スキル化）を検討
3. **3ヶ月後**: レベル3（フック化）への実装を検討

---

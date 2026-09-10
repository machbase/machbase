---
type: docs
title: 'RETENTION'
weight: 160
toc: true
---

RETENTIONポリシーは、TAG、KV、LOGテーブルで保持期間を過ぎたデータを定期的に削除します。
TRANSACTION、LOOKUP、VOLATILEには適用できません。

<a id="create-retention"></a>

## RETENTIONポリシーの作成

```sql
create_retention_stmt ::=
    'CREATE RETENTION' policy_name
    'DURATION' positive_integer ( 'MONTH' | 'DAY' | 'HOUR' | 'MIN' | 'SEC' )
    'INTERVAL' positive_integer ( 'DAY' | 'HOUR' | 'MIN' | 'SEC' )
```

| パラメーター | 説明 |
|----------|------|
| `policy_name` | ポリシー名 |
| `DURATION duration MONTH\|DAY\|HOUR\|MIN\|SEC` | データ保持期間（`MONTH`は固定30日） |
| `INTERVAL interval DAY\|HOUR\|MIN\|SEC` | 削除の実行周期 |

```sql
-- 1日保持し、1時間ごとに削除実行
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;

-- 30日保持し、1日ごとに削除実行
CREATE RETENTION policy_30d_1d DURATION 30 DAY INTERVAL 1 DAY;

-- 3か月保持し、1日ごとに削除実行
CREATE RETENTION policy_3m_1d DURATION 3 MONTH INTERVAL 1 DAY;
```

<a id="drop-retention"></a>

## RETENTIONポリシーの削除

```sql
drop_retention_stmt ::= 'DROP RETENTION' policy_name
```

```sql
DROP RETENTION policy_1d_1h;
```

## テーブルへのRETENTIONポリシーの適用

```sql
alter_table_add_retention_stmt ::=
    'ALTER TABLE' table_name 'ADD RETENTION' policy_name
```

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h;
```

## テーブルからのRETENTIONポリシーの解除

```sql
alter_table_drop_retention_stmt ::=
    'ALTER TABLE' table_name 'DROP RETENTION'
```

```sql
ALTER TABLE sensor_tag DROP RETENTION;
```

## RETENTIONポリシー一覧の検索

システムテーブルで、登録されたRETENTIONポリシーと適用状況を検索します。

```sql
-- 全RETENTIONポリシーの検索
SELECT * FROM M$RETENTION;

-- テーブル別の適用ジョブと最終削除基準を確認
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB
 ORDER BY USER_NAME, TABLE_NAME;
```

## 全体の例

```sql
-- 1. RETENTIONポリシー作成（1日保持、1時間ごとに削除）
CREATE RETENTION ret_1d DURATION 1 DAY INTERVAL 1 HOUR;

-- 2. TAGテーブル作成
CREATE TAG TABLE sensor_tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 3. テーブルにRETENTIONポリシーを適用
ALTER TABLE sensor_tag ADD RETENTION ret_1d;

-- 4. ポリシー適用を確認
SELECT * FROM M$RETENTION;

-- 5. ポリシーを解除
ALTER TABLE sensor_tag DROP RETENTION;

-- 6. ポリシーを削除
DROP RETENTION ret_1d;
```

## 注意事項

- RETENTIONポリシーは、LOGテーブルとTAGテーブルに適用できます。
- KVテーブルにも適用できます。
- 1つのテーブルには1つのRETENTIONポリシーだけを適用できます。
- `MONTH`はカレンダー月ではなく、固定30日として計算します。カレンダー境界が重要なポリシーは、
  `DAY`単位に換算し、実際の削除基準を検証します。
- RETENTIONジョブが削除した行は元に戻せないため、保持期間と実行周期を慎重に設定してください。
  `DROP RETENTION`は、すべてのテーブルからポリシーを解除した後で、ポリシーオブジェクトだけを削除します。
- `INTERVAL`は削除ジョブの実行周期であり、実際の削除時刻は多少遅れる場合があります。
- 存在しないポリシー、未サポートのテーブルタイプ、同じテーブルへの重複適用はエラーです。
- 適用中のポリシーオブジェクトは、すべてのテーブルから解除してから削除します。

## 関連文書

- [Retention Policyの役割](/dbms/core-concepts/features-concepts/#role-retention-policy) — 自動データ削除ポリシーの概念

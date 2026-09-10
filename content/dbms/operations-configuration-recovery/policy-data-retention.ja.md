---
type: docs
title: '13.5 データ保持ポリシー'
weight: 50
toc: true
---

Retention Policy は TAG、KV、LOG で基準時刻より古いデータを定期的に削除します。
`DURATION` は保持期間、`INTERVAL` は削除ジョブの実行周期です。
TRANSACTION、VOLATILE、LOOKUP には適用できません。

```text
ポリシー作成 → テーブルへ適用 → 実行状態確認 → テーブルから解除 → ポリシー削除
```

<a id="retention-policy"></a>

## Retention Policy

運用ポリシーを作成する前に、法的な保存義務、復旧要件、時間当たりの流入量、削除負荷を確認します。
`INTERVAL` は固定比率で決めず、運用環境で測定した削除時間より十分長い周期を使用してください。

ポリシーと適用状態は次のビューで確認します。

```sql
SELECT * FROM M$RETENTION;
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB;
```

<a id="create-retention-policy"></a>
<a id="retention-policy-create-retention-policy"></a>

### Retention Policy の作成

```sql
CREATE RETENTION policy_name
    DURATION duration_value {MONTH|DAY|HOUR|MIN|SEC}
    INTERVAL interval_value {DAY|HOUR|MIN|SEC};
```

`DURATION` は月から秒、`INTERVAL` は `DAY` から `SEC` を指定できます。`MONTH` は暦月ではなく
固定の30日です。法的保存など暦の境界が重要な場合は `DAY` に換算し、実際の削除基準を検証します。
正確な構文と対応テーブルは[RETENTION 構文](/dbms/reference/sql/syntax/retention-syntax/)を参照してください。

例えば、30日保持し、1日ごとに削除対象を処理するポリシーは次のとおりです。

```sql
CREATE RETENTION policy_30d DURATION 30 DAY INTERVAL 1 DAY;
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_30D';
```

ポリシーの作成と削除には必要な管理権限が必要です。運用アカウントで実行する前に、権限と
承認された変更範囲を確認してください。

<a id="retention-policy-retention-policy"></a>

### テーブルへの適用

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_30d;

SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE
  FROM V$RETENTION_JOB
 WHERE TABLE_NAME = 'SENSOR_TAG';
```

1つのテーブルには1つのポリシーだけを適用できます。TAG は `BASETIME`、LOG は `_ARRIVAL_TIME` を
基準に古いデータを判定します。適用直後に削除するのではなく、設定した周期に従って実行します。

<a id="detach-retention-policy"></a>
<a id="retention-policy-detach-retention-policy"></a>

### テーブルからの解除

```sql
ALTER TABLE sensor_tag DROP RETENTION;
```

解除すると自動削除は停止しますが、削除済みデータは復元されません。解除後、
`V$RETENTION_JOB` から対象テーブルがなくなったことを確認します。

<a id="delete-retention-policy"></a>
<a id="retention-policy-delete-retention-policy"></a>

### Retention Policy の削除

ポリシーを使うすべてのテーブルから解除してから、ポリシーオブジェクトを削除します。

```sql
SELECT USER_NAME, TABLE_NAME
  FROM V$RETENTION_JOB
 WHERE POLICY_NAME = 'POLICY_30D';

-- 検索された各テーブルからポリシーを解除してから実行
DROP RETENTION policy_30d;
```

`ALTER TABLE ... DROP RETENTION` はテーブルとポリシーの関連付けを解除し、`DROP RETENTION` は
ポリシーオブジェクトを削除します。適用中のポリシーは削除できません。

<a id="applicable-privileges-retention-sys"></a>
<a id="retention-policy-applicable-privileges-retention-sys"></a>

### 適用範囲と権限

| テーブルタイプ | 適用可能 |
|---|---|
| TAG, KV, LOG | はい |
| TRANSACTION, VOLATILE, LOOKUP | いいえ |

ポリシー管理者とテーブル所有者が異なる場合、運用前に実際の権限構成を検証してください。
他の所有者のテーブルを対象にする場合も、必要な権限だけを明示的に付与します。

<a id="execution-status-check-state-retention"></a>
<a id="retention-policy-execution-status-check-state-retention"></a>

### 実行状態の確認

```sql
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
  FROM V$RETENTION_JOB
 ORDER BY USER_NAME, TABLE_NAME;
```

`STATE` はジョブの現在状態、`LAST_DELETED_TIME` は最後の削除で使った基準時刻です。
実時間でのジョブ完了時刻として解釈してはいけません。実際に削除されたかは、対象テーブルの
最古時刻と行数の推移を併せて確認します。

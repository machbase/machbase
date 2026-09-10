---
type: docs
title: '10.2 テーブル構造とスキーマ'
weight: 20
toc: true
---

VOLATILEテーブルのPRIMARY KEY設計とスキーマ構成を説明します。

<a id="primary-key-design-primary-key"></a>

## PRIMARY KEYの設計

VOLATILEテーブルはPRIMARY KEYなしでも作成できます。
ただし、PKによる検索や`ON DUPLICATE KEY UPDATE`を使用するにはPRIMARY KEYが必要です。

### 単一のPRIMARY KEY

```sql
CREATE VOLATILE TABLE ch10_schema_state (
    device_id  VARCHAR(32) PRIMARY KEY,
    state      VARCHAR(16),
    updated_at DATETIME
);
```

### 複合キーが必要な場合

複数列の組み合わせで行を一意に識別する必要がある場合は、組み合わせたキーを別のPRIMARY KEY列に格納します。

```sql
CREATE VOLATILE TABLE ch10_schema_hourly (
    key_id     VARCHAR(96) PRIMARY KEY,
    sensor_id  VARCHAR(64),
    hour_ts    DATETIME,
    avg_value  DOUBLE,
    sample_cnt INTEGER
);

-- 組み合わせキーの挿入
INSERT INTO ch10_schema_hourly
VALUES ('TEMP-01:2026010110', 'TEMP-01', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 23.5, 60);
INSERT INTO ch10_schema_hourly
VALUES ('TEMP-01:2026010111', 'TEMP-01', TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 24.1, 60);
INSERT INTO ch10_schema_hourly
VALUES ('TEMP-02:2026010110', 'TEMP-02', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 21.0, 60);

-- 組み合わせキーの検索
SELECT sensor_id, avg_value FROM ch10_schema_hourly
 WHERE key_id = 'TEMP-01:2026010110';
```

### ON DUPLICATE KEY UPDATEとの併用

```sql
-- PRIMARY KEY重複時にUPDATEを実行
INSERT INTO ch10_schema_state VALUES ('DEV-01', 'ONLINE', NOW)
ON DUPLICATE KEY UPDATE SET state = 'ONLINE', updated_at = NOW;
```

### 注意事項

- PRIMARY KEYなしでも作成できますが、PKに基づく操作（UPSERT、PK検索など）は使用できません。
- 同じPRIMARY KEYを持つ行を複数保存することはできません。`ON DUPLICATE KEY UPDATE`は、
  重複行を追加する代わりに既存行を更新します。
- PRIMARY KEY列は1つだけ指定します。

<a id="volatile-table-design"></a>

## VOLATILEテーブルの設計

VOLATILEテーブルはデータをメモリだけに保持し、サーバー再起動時にデータが消失します。
テーブル定義は残るため、設計では「何を失ってもよいか」と「どのように再充填するか」を決めます。
複数セッションで共有し、再起動後に復旧する必要がない状態やキャッシュに使用します。

スキーマを決めるときは、次の項目も検討してください。

- [活用例](../overview-use-criteria/#use-cases-volatile)
- [永続性の違いとDDL](../create-alter-drop/#differences-persistence-ddl)
- [メモリのライフサイクル](../operations-lifecycle/#lifecycle-memory)
- [赤黒木インデックス](../index-performance/#index-strategy-red-black)
- [ON DUPLICATE KEY UPDATE](../data-input-mutation/#on-duplicate-key-update)
- [再起動とデータ再構築](../operations-lifecycle/#data-loss)

このページの実習テーブルは、次のように削除します。

```sql
DROP TABLE ch10_schema_hourly;
DROP TABLE ch10_schema_state;
```

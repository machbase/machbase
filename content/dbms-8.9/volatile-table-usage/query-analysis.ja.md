---
type: docs
title: '10.5 クエリと分析'
weight: 50
toc: true
---

VOLATILEテーブルのキー検索、一般条件検索、一時集計を実行可能な例で説明します。

<a id="original-85-querying-data"></a>

## サンプルデータの準備

VOLATILEテーブルは、他のテーブルタイプと同様に`SELECT`文で検索します。
次の例は、最後のクリーンアップ文まで順に実行できます。

```sql
CREATE VOLATILE TABLE ch10_query (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

INSERT INTO ch10_query VALUES ('DEV-01', 'RUNNING', 42.5, NOW);
INSERT INTO ch10_query VALUES ('DEV-02', 'STOPPED', 0, NOW);
```

<a id="query-volatile-primary-key"></a>

## PRIMARY KEYによる検索

キー条件は、最新状態キャッシュの単一行検索に適しています。

```sql
SELECT device_id, status, value, updated_at
FROM ch10_query
WHERE device_id = 'DEV-01';
```

<a id="query-volatile-index"></a>

## 一般条件による検索

`PRIMARY KEY`以外の列で繰り返し検索する場合は、セカンダリインデックスを検討します。

```sql
CREATE INDEX ch10_query_status_idx ON ch10_query(status);

SELECT device_id, value, updated_at
FROM ch10_query
WHERE status = 'RUNNING';
```

インデックスもメモリを使用するため、実際の検索に必要な列だけに作成します。

<a id="query-volatile-temporary-analysis"></a>

## 一時集計の検索

短周期の集計結果を保存すると、ダッシュボードやアラーム判定の繰り返し計算を減らせます。

```sql
CREATE VOLATILE TABLE ch10_query_summary (
    summary_key VARCHAR(96) PRIMARY KEY,
    sensor_id   VARCHAR(64),
    bucket_time DATETIME,
    avg_value   DOUBLE,
    max_value   DOUBLE,
    sample_cnt  LONG
);

INSERT INTO ch10_query_summary
VALUES ('TEMP-01:2026-01-01T00:00', 'TEMP-01', TO_DATE('2026-01-01 00:00:00'),
        21.5, 23.0, 60);

SELECT sensor_id, bucket_time, avg_value, max_value
FROM ch10_query_summary
WHERE sensor_id = 'TEMP-01'
ORDER BY bucket_time DESC
LIMIT 10;

DROP TABLE ch10_query_summary;
DROP TABLE ch10_query;
```

集計結果を長期保持する必要がある場合は、LOGまたはTRANSACTIONテーブルに定期的にコピーします。

<a id="query-volatile-limitations"></a>

## クエリの注意事項

- サーバー再起動後はデータが空になるため、初期ロードの実施を先に確認します。
- キー検索が中心なら`PRIMARY KEY`を指定します。
- 範囲検索やソートで頻繁に使用する列には、セカンダリインデックスを検討します。
- 重要な元データは永続テーブルに保存し、VOLATILEはキャッシュとして使用します。

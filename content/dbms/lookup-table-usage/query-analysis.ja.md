---
type: docs
title: '9.5 クエリと分析'
weight: 50
toc: true
---

LOOKUPテーブルのキー検索、一般条件検索、TAGデータとのJOINを実行可能な例で説明します。

<a id="original-85-querying-data"></a>

## サンプルデータの準備

次のLOOKUPテーブルとTAGテーブルを準備します。

```sql
CREATE LOOKUP TABLE ch9_query_master (
    sensor_id VARCHAR(32) PRIMARY KEY,
    site      VARCHAR(32),
    unit      VARCHAR(16),
    status    VARCHAR(16)
);

INSERT INTO ch9_query_master VALUES ('TEMP-01', 'SEOUL', 'C', 'ACTIVE');
INSERT INTO ch9_query_master VALUES ('TEMP-02', 'BUSAN', 'C', 'INACTIVE');

CREATE TAG TABLE ch9_query_data (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

INSERT INTO ch9_query_data VALUES ('TEMP-01', TO_DATE('2026-01-01 00:00:00'), 23.5);
INSERT INTO ch9_query_data VALUES ('TEMP-02', TO_DATE('2026-01-01 00:00:00'), 19.0);
```

<a id="query-lookup-primary-key"></a>

## PRIMARY KEYによる検索

単一行の検索には`PRIMARY KEY`条件を使用します。

```sql
SELECT sensor_id, site, unit, status
FROM ch9_query_master
WHERE sensor_id = 'TEMP-01';
```

<a id="query-lookup-condition"></a>

## 一般条件による検索

LOOKUPテーブルは、一般列の条件でも検索できます。頻繁に使用する条件列にはインデックスを追加します。

```sql
SELECT sensor_id, site, unit
FROM ch9_query_master
WHERE site = 'SEOUL'
  AND status = 'ACTIVE';
```

頻繁に使用する一般条件列には、インデックスを追加できます。
インデックスの設計と作成方法は、[インデックス](/dbms/lookup-table-usage/index-performance/)を参照してください。

<a id="query-lookup-join"></a>

## TAG・LOGテーブルとのJOIN

LOOKUPテーブルは、TAGまたはLOGテーブルの元データに説明情報を付加する用途でよく使用します。

```sql
SELECT d.name, m.site, m.unit, d.time, d.value
FROM ch9_query_data d
JOIN ch9_query_master m ON d.name = m.sensor_id
WHERE m.status = 'ACTIVE';
```

<a id="query-lookup-analysis-pattern"></a>

## 分析パターン

LOOKUPテーブルは元データを保存するより、分析の基準を提供します。次のパターンに適しています。

| パターン | 説明 |
|------|------|
| コード変換 | 状態コード、アラームコード、機器タイプをラベルに変換 |
| 基準値との比較 | センサー値をしきい値テーブルとJOINし、超過を判定 |
| グループ基準の提供 | 場所、部門、ラインなどの集計基準を提供 |
| 最新設定の反映 | 運用中に変更される設定値を検索時点で反映 |

同じ方法で、しきい値のLOOKUPテーブルとTAGの元データをJOINし、基準値を超えたか判定できます。
時間範囲が広いTAGまたはLOGテーブルでは、JOIN前に時間条件で検索範囲を制限します。

```sql
DROP TABLE ch9_query_data CASCADE;
DROP TABLE ch9_query_master;
```

<a id="query-lookup-performance"></a>

## クエリ性能の基準

- 単一行検索とJOINの基準列には、`PRIMARY KEY`またはインデックス列を使用します。
- 条件に頻繁に使う一般列には、別のインデックスを検討します。
- 大量の元データとJOINする場合は、元テーブルの時間範囲を先に絞ります。
- LOOKUPにはマスターデータ、長期の元データはTAGまたはLOGに保存します。

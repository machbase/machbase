---
type: docs
title: '8.5 クエリと分析'
weight: 50
toc: true
---

クエリの構文が正しくても、入力した状態値と条件が異なれば結果は0件になります。
ソート基準が不十分だと、同時刻の行が検索ごとに異なる順序で表示される場合もあります。
さまざまな状態と境界時刻を持つサンプルで、フィルター・ソート・集計を確認します。

<a id="query-rdb-basic-select"></a>

<a id="확인할-결과가-있는-표본을-준비합니다"></a>

## 実習データの準備

```sql
CREATE TRANSACTION TABLE ch8_query (
    order_id LONG PRIMARY KEY,
    customer VARCHAR(32),
    item_id  LONG,
    amount   DECIMAL(18,2),
    status   VARCHAR(16),
    ordered  DATETIME
);
CREATE TRANSACTION TABLE ch8_query_product (id LONG PRIMARY KEY, name VARCHAR(64));
INSERT INTO ch8_query_product VALUES (42, 'Pump');
INSERT INTO ch8_query_product VALUES (43, 'Valve');

INSERT INTO ch8_query VALUES (
    1001, 'C-01', 42, 10.25, 'PENDING', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO ch8_query VALUES (
    1002, 'C-01', 43, 20.50, 'PENDING', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO ch8_query VALUES (
    1003, 'C-02', 42, 30.75, 'SHIPPED', TO_DATE('2026-01-02', 'YYYY-MM-DD'));

SELECT order_id, amount, status FROM ch8_query WHERE order_id = 1001;
```

1001・10.25・PENDINGが返されます。

<a id="query-rdb-filter-sort-limit"></a>

<a id="시간-경계와-같은-시각의-순서를-명시합니다"></a>

## 時間条件とソート

```sql
SELECT order_id, amount FROM ch8_query
 WHERE ordered >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
   AND ordered <  TO_DATE('2026-01-02', 'YYYY-MM-DD')
   AND status = 'PENDING'
 ORDER BY ordered DESC, order_id DESC
 LIMIT 1;
```

1002の1行が選択されます。orderedが同じでも、order_idで順序を固定しています。
LIMITだけを指定して意図した順序を期待しないでください。
連続する日別集計では、開始を含み終了を除く条件で境界の重複を避けられます。
LOG専用のDURATIONや自動_arrival_timeは、TRANSACTIONには適用しません。

<a id="query-rdb-join"></a>

<a id="기준-정보를-붙일-때-누락과-중복을-확인합니다"></a>

## マスターデータとの結合

```sql
SELECT o.order_id, p.name, o.amount
  FROM ch8_query o JOIN ch8_query_product p ON o.item_id = p.id
 WHERE o.customer = 'C-01'
 ORDER BY o.order_id;
```

結果は(1001, Pump, 10.25)、(1002, Valve, 20.50)です。
このINNER JOINでは、対応するマスターデータがない注文は除外されます。
結合先に同じキーの行が複数あると結果が増えるため、キーの一意性も確認する必要があります。
他のタイプとの結合は[JOINの実習](../join-relational-query/)で説明します。

<a id="query-rdb-aggregation"></a>

<a id="합계는-원본-건수와-함께-확인합니다"></a>

## 集計クエリ

```sql
SELECT status, COUNT(*) AS cnt, SUM(amount) AS total_amount
  FROM ch8_query GROUP BY status ORDER BY status;
```

PENDINGは2件・30.75、SHIPPEDは1件・30.75です。
インデックスがあっても、すべての集計が自動的に高速化するわけではありません。
範囲・グループ数・結果量を確認し、繰り返す業務では別途サマリーの作成を検討してください。

<a id="query-rdb-json"></a>

<a id="json-값이-실제로-들어-있는지부터-확인합니다"></a>

## JSONパスのクエリ

```sql
CREATE TRANSACTION TABLE ch8_query_json (id INTEGER PRIMARY KEY, state JSON);
INSERT INTO ch8_query_json VALUES (1, '{"status":"ALARM","score":90}');
INSERT INTO ch8_query_json VALUES (2, '{"status":"NORMAL","score":10}');
INSERT INTO ch8_query_json VALUES (3, '{"score":20}');

SELECT id, state->'$.status' AS status FROM ch8_query_json
 WHERE state->'$.status' = 'ALARM'
 ORDER BY id;
```

行1だけが選択されます。パスが存在しない行と、条件値が異なる行を区別してサンプルを用意してください。
矢印パスによる文字列比較と、数値抽出関数による比較を混同しないでください。
頻繁に使うパスには、[JSONパスインデックス](../index-performance/#index-strategy-rdb-json-path)を検討できます。

<a id="query-rdb-performance"></a>

<a id="실행-계획은-지원되는-조건-모양까지-확인합니다"></a>

## インデックスと実行計画

```sql
CREATE INDEX ch8_query_status_time ON ch8_query(status, ordered);
EXPLAIN SELECT order_id FROM ch8_query
 WHERE status = 'PENDING'
   AND ordered >= TO_DATE('2026-01-01', 'YYYY-MM-DD');
```

複合インデックスの先頭列と条件を合わせ、実際の使用はEXPLAINで確認してください。
Machbaseがリレーショナルクエリ全体を内部SQLiteにそのまま渡すと考えると、インデックス選択や関数条件を誤解する場合があります。

```sql
DROP TABLE ch8_query_json;
DROP TABLE ch8_query_product;
DROP TABLE ch8_query;
```

結果が異なる場合は、集計やJOINを複雑に分析する前に、元の件数、WHERE条件、ソート基準を順に確認してください。

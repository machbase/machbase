---
type: docs
title: '8.11 JOINとリレーショナルクエリの設計'
weight: 110
toc: true
---

JOINを追加して注文件数が減少・増加した場合は、まず関係の形を確認する必要があります。
INNER JOINは対応する行がない行を除外し、1件に複数の行が一致すると結果を増やします。
SQLがエラーなしで実行されることと、業務件数を正しく集計することは別です。

<a id="join-design-rdb"></a>

<a id="transaction과-lookup을-연결합니다"></a>

## TRANSACTION–LOOKUP結合

```sql
CREATE TRANSACTION TABLE ch8_join_order (
    order_id LONG PRIMARY KEY,
    item_id  LONG,
    qty      INTEGER
);
CREATE LOOKUP TABLE ch8_join_product (id LONG PRIMARY KEY, name VARCHAR(64));
CREATE TRANSACTION TABLE ch8_join_payment (order_id LONG PRIMARY KEY, status VARCHAR(16));

INSERT INTO ch8_join_order VALUES (1, 42, 2);
INSERT INTO ch8_join_order VALUES (2, 99, 1);
INSERT INTO ch8_join_product VALUES (42, 'Pump');
INSERT INTO ch8_join_payment VALUES (1, 'PAID');

SELECT o.order_id, p.name, o.qty
  FROM ch8_join_order o JOIN ch8_join_product p ON o.item_id = p.id
 ORDER BY o.order_id;

SELECT o.order_id, p.name, o.qty
  FROM ch8_join_order o LEFT JOIN ch8_join_product p ON o.item_id = p.id
 ORDER BY o.order_id;
```

INNER JOINは注文1だけ、LEFT JOINは注文1・2を返します。
注文2の製品名はNULLです。製品99が存在しなくても、注文の入力自体は外部キーで拒否されないため、必要な参照検証は別途設計する必要があります。

LEFT JOIN後に右側テーブルの条件をWHEREに指定しないよう注意してください。
例えば`WHERE p.name = 'Pump'`を追加すると、NULL行が除外されます。
結合先を探す条件なのか、最終結果をフィルタリングする条件なのかを区別してください。

<a id="transaction끼리도-키의-고유성을-확인합니다"></a>

## TRANSACTION間の結合

```sql
SELECT o.order_id, o.qty, p.status
  FROM ch8_join_order o
  JOIN ch8_join_payment p ON o.order_id = p.order_id
 ORDER BY o.order_id;
```

(1, 2, PAID)の1行が返されます。
実際の支払い履歴が注文ごとに複数行あれば、この結果も複数行になります。
結合後に注文金額を合計するとき、重複集計を避けるために関係と集計単位を確認してください。

<a id="tag의-근접-시간-조인은-한-행을-고르는-기능이-아닙니다"></a>

## TAGの近接時刻結合

次は、アラームの前後5秒以内にあるすべての測定値を結合する例です。

```sql
CREATE TRANSACTION TABLE ch8_join_alarm (
    alarm_id LONG PRIMARY KEY,
    sensor   VARCHAR(32),
    occurred DATETIME
);
CREATE TAG TABLE ch8_join_sensor (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

INSERT INTO ch8_join_alarm VALUES (
    1, 'TEMP-01', TO_DATE('2026-01-01 10:00:05', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO ch8_join_sensor VALUES (
    'TEMP-01', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10);
INSERT INTO ch8_join_sensor VALUES (
    'TEMP-01', TO_DATE('2026-01-01 10:00:10', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch8_join_sensor VALUES (
    'TEMP-01', TO_DATE('2026-01-01 10:00:11', 'YYYY-MM-DD HH24:MI:SS'), 30);

SELECT a.alarm_id, s.time, s.value
  FROM ch8_join_alarm a JOIN ch8_join_sensor s ON a.sensor = s.name
 WHERE s.time >= a.occurred - 5s
   AND s.time <= a.occurred + 5s
 ORDER BY a.alarm_id, s.time;
```

アラーム1に値10・20の2行が結合されます。両側の境界を含み、値30は除外されます。
このクエリは最も近い測定値1つや、完全に同じ時刻の値を選ぶ機能ではありません。
1つの値だけが必要なら、直前値・最短距離などの選択基準と同順位の処理規則を別途定めてください。

<a id="타입과-읽기-범위를-먼저-맞춥니다"></a>

## 結合の設計基準

結合キーの型と値の形式を合わせ、時間範囲を制限してから実行計画を確認します。
必要な列だけを返し、結合キーへの不用意な関数・型変換の追加でアクセス経路が変わらないか比較してください。
結合順序やアルゴリズムが他のRDBMSと同じだと考えないでください。

混合結合が許可されても、他のテーブルタイプがTRANSACTIONと同じトランザクションスナップショットを共有するわけではありません。
また、現在のLOOKUPの説明を付加しても、過去の時点の説明までは再現しません。

```sql
DROP TABLE ch8_join_sensor;
DROP TABLE ch8_join_alarm;
DROP TABLE ch8_join_payment;
DROP TABLE ch8_join_product;
DROP TABLE ch8_join_order;
```

結果件数が一致しない場合は、結合前の件数とキーごとの結合先行数を先に比較してください。
この2つが確認できると、クエリの修正方法も明確になります。

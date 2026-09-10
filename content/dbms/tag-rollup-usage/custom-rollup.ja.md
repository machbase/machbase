---
type: docs
title: '6.6 Custom ROLLUP'
weight: 60
toc: true
---

<span class="badge-since">Standard Edition専用</span>

<a id="original-85-rollup-custom"></a>
<a id="custom-rollup"></a>

## Customと通常のROLLUP

Custom ROLLUPは、SELECTの増分集計結果を事前作成した出力先TAGに追加します。
通常のROLLUPの内部統計を`rollup()`で読む方式とは異なり、出力先TAGを直接検索して部分集計を再結合する必要があります。
Cluster Editionでは作成できません。

```text
CREATE ROLLUP [IF NOT EXISTS] name
  INTO (destination_tag)
  AS (SELECT ... FROM source_tag [WHERE ...] GROUP BY ...)
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)];
```

ソースは1つの時間軸TAGで、JOIN・FROMサブクエリは使用できません。
出力先は事前作成したTAGで、SELECTのカラム順序と型に互換性が必要です。
SELECT内のWHEREは使用できますが、BASETIMEの直接条件は許可されません。
通常のROLLUPのように、INTERVALの後に外側のWHEREを付けないでください。

作成間隔とSELECTが計算する時間バケットを一致させてください。
ジョブは新しい入力だけを処理するため、同じバケットに複数の結果行が存在し得ます。
行数をバケット数と解釈しないでください。

## 1. 合計と有効件数の実習

```sql
CREATE TAG TABLE ch6_custom_src (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE ch6_custom_dst (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME,
    sum_value DOUBLE, valid_count LONG, total_count LONG
);
CREATE ROLLUP ch6_custom_ru INTO (ch6_custom_dst)
AS (
    SELECT name, DATE_TRUNC('minute', time) AS time,
           SUM(value), COUNT(value), COUNT(*)
      FROM ch6_custom_src
     GROUP BY name, time
) INTERVAL 1 MIN;
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:05', 'YYYY-MM-DD HH24:MI:SS'), 10);
EXEC TABLE_FLUSH(ch6_custom_src);
ALTER ROLLUP ch6_custom_ru FORCE;
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:10', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:15', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:20', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:25', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:35', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:40', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:45', 'YYYY-MM-DD HH24:MI:SS'), 20);
INSERT INTO ch6_custom_src VALUES ('S1', TO_DATE('2026-01-01 00:00:55', 'YYYY-MM-DD HH24:MI:SS'), NULL);
EXEC TABLE_FLUSH(ch6_custom_src);
ALTER ROLLUP ch6_custom_ru FORCE;

SELECT name, DATE_TRUNC('minute', time) AS bucket,
       SUM(value), COUNT(value), COUNT(*), AVG(value)
  FROM ch6_custom_src
 GROUP BY name, bucket ORDER BY name, bucket;

SELECT name, time, SUM(sum_value) AS sum_value,
       SUM(valid_count) AS valid_count, SUM(total_count) AS total_count,
       CASE WHEN SUM(valid_count) = 0 THEN NULL
            ELSE SUM(sum_value) / SUM(valid_count) END AS avg_value
  FROM ch6_custom_dst
 GROUP BY name, time ORDER BY name, time;
```

1バケットの合計は180、有効値は10個、全行数は11、平均は18です。
部分平均10と20を単純平均した15とは異なります。
NULLを平均の分母に含めないようCOUNT(value)を使用し、NULLを含む行数はCOUNT(*)で別途保持します。
すべての値がNULLのバケットも処理する場合は、有効件数0で除算しない結果ポリシーも決めてください。

### サンプル比率と時間稼働率

条件を満たすサンプル数を全サンプル数で割った値は、サンプル比率です。
時間稼働率として解釈するには、観測間隔・欠損処理・状態の継続時間を反映する必要があります。
比率も部分比率を平均せず、分子と分母をそれぞれ合算します。

## 2. OHLCVと1分→10分のCustom階層

独立した実習です。FIRST/LASTの再集計のため、元の最初・最後の観測時刻も保存します。

```sql
CREATE TAG TABLE ch6_ticks (
    code VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME,
    price DOUBLE, volume DOUBLE
);
CREATE TAG TABLE ch6_candle_min (
    code VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME,
    open_price DOUBLE, high_price DOUBLE, low_price DOUBLE, close_price DOUBLE,
    volume DOUBLE, cnt LONG, firsttime DATETIME, lasttime DATETIME
);
CREATE TAG TABLE ch6_candle_10m (
    code VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME,
    open_price DOUBLE, high_price DOUBLE, low_price DOUBLE, close_price DOUBLE,
    volume DOUBLE, cnt LONG, firsttime DATETIME, lasttime DATETIME
);
CREATE ROLLUP ch6_candle_ru_min INTO (ch6_candle_min)
AS (
    SELECT code, DATE_TRUNC('minute', time) AS time,
           FIRST(time, price), MAX(price), MIN(price), LAST(time, price),
           SUM(volume), COUNT(*), MIN(time), MAX(time)
      FROM ch6_ticks
     GROUP BY code, time
) INTERVAL 1 MIN;

CREATE ROLLUP ch6_candle_ru_10m INTO (ch6_candle_10m)
AS (
    SELECT code, DATE_BIN('min', 10, time, TO_DATE('2000-01-01 00:00:00')) AS time,
           FIRST(firsttime, open_price), MAX(high_price),
           MIN(low_price), LAST(lasttime, close_price),
           SUM(volume), SUM(cnt), MIN(firsttime), MAX(lasttime)
      FROM ch6_candle_min
     GROUP BY code, time
) INTERVAL 10 MIN;

INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:00:00'), 100, 2);
INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:00:30'), 105, 3);
INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:01:00'), 103, 1);
INSERT INTO ch6_ticks VALUES ('AAPL', TO_DATE('2026-01-01 09:01:30'), 99, 4);
EXEC TABLE_FLUSH(ch6_ticks);
ALTER ROLLUP ch6_candle_ru_min FORCE;
EXEC TABLE_FLUSH(ch6_candle_min);
ALTER ROLLUP ch6_candle_ru_10m FORCE;

SELECT code, time,
       FIRST(firsttime, open_price), MAX(high_price),
       MIN(low_price), LAST(lasttime, close_price), SUM(volume), SUM(cnt)
  FROM ch6_candle_10m
 GROUP BY code, time ORDER BY code, time;
```

09:00の10分バケットは、Open=100、High=105、Low=99、Close=99、volume=10、cnt=4です。
価格や取引量がNULLの場合は、どの行の時刻と値を使用するか、別途規則とテストが必要です。
同時刻の複数の取引にも業務上の順序がある場合は、追加の識別基準を設計してください。

この10分Customは作成・検索の例です。現在のREBUILDのCustom時間範囲処理でサポートする間隔と同じだと考えないでください。
[REBUILDの制限](../rollup-rebuild/)を確認してください。

## 状態とクリーンアップ

作成後は自動的に開始するため、直後にSTARTを繰り返さないでください。
STOP/STARTとFORCEはジョブの状態に応じて呼び出します。
ジョブが存在する出力先TAGのDROPは拒否されます。

```sql
SELECT DISTINCT ROLLUP_NAME, ROLLUP_TABLE, ROOT_TABLE, EXT_TYPE,
       INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CUSTOM_RU';

DROP ROLLUP ch6_candle_ru_10m;
DROP ROLLUP ch6_candle_ru_min;
DROP TABLE ch6_candle_10m;
DROP TABLE ch6_candle_min;
DROP TABLE ch6_ticks;
DROP ROLLUP ch6_custom_ru;
DROP TABLE ch6_custom_dst;
DROP TABLE ch6_custom_src;
```

EXT_TYPE=2はCustomを表し、PREDICATEにはSELECT本文が記録されます。
クリーンアップでは、実行した実習のオブジェクトだけを対象にしてください。
元データの補正と上位の再集計の再試行・完了確認は、[制御と状態](../ingestion-control-rollup/)およびREBUILDの手順に従ってください。

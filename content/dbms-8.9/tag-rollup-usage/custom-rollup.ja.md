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

## 合計と有効件数の例

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

## OHLCVと1分→10分のCustom階層

独立した例です。FIRST/LASTの再集計のため、元の最初・最後の観測時刻も保存します。

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
クリーンアップでは、実行した例のオブジェクトだけを対象にしてください。
元データの補正と上位の再集計の再試行・完了確認は、[制御と状態](../ingestion-control-rollup/)およびREBUILDの手順に従ってください。

<a id="composite-key-ohlc"></a>

## 複合キーを保持したOHLC再集計

> 複合キーFIRST/LASTとソート付きEXTENSION ROLLUPはMachbase 8.7.3から対応します。エディション別の制約は以下を確認してください。

この例のCustom作成はStandard専用です。通常のTAGに保存済みの要約行を再集計する
SELECTは別の操作であり、Clusterでも対応します。マージ時も元の時刻と補助キーの
カラムを同じ基準で使用してください。

Standard Custom ROLLUPのSELECTでも複合キーFIRST/LASTを使用できます。
Custom定義にはEXTENSION ORDER BYを付けません。選択価格と同じ行の元時刻・DOUBLEキーを
一緒に保存し、部分集計のマージでも順序を維持します。以下は別のオブジェクトを使用する例です。

### 元テーブルと格納先のスキーマ

```sql
CREATE TAG TABLE custom_ticks (
    code  VARCHAR(16) PRIMARY KEY,
    time  DATETIME BASETIME,
    price INTEGER,
    gvol  DOUBLE
);

CREATE TAG TABLE custom_ticks_1s (
    code        VARCHAR(16) PRIMARY KEY,
    time        DATETIME BASETIME,
    open_price  INTEGER,
    open_time   DATETIME,
    open_gvol   DOUBLE,
    close_price INTEGER,
    close_time  DATETIME,
    close_gvol  DOUBLE,
    high_price  INTEGER,
    low_price   INTEGER
);
```

### 1秒集計の定義

出力カラム順を格納先スキーマと一致させます。例では入力前にSTOPして自動処理を止め、FORCEで明示的に処理します。

```sql
CREATE ROLLUP custom_ticks_rollup_1s
INTO (custom_ticks_1s) AS (
    SELECT code,
           DATE_TRUNC('second', time) AS time,
           FIRST((time, gvol), price) AS open_price,
           FIRST((time, gvol), time)  AS open_time,
           FIRST((time, gvol), gvol)  AS open_gvol,
           LAST((time, gvol), price)  AS close_price,
           LAST((time, gvol), time)   AS close_time,
           LAST((time, gvol), gvol)   AS close_gvol,
           MAX(price) AS high_price,
           MIN(price) AS low_price
      FROM custom_ticks
     GROUP BY code, time
) INTERVAL 1 SEC;

STOP ROLLUP custom_ticks_rollup_1s;
```

### 入力と集計

同じ時刻に3件ずつ入力し、gvolには通常のDOUBLE業務キーを使用します。
09:01:29.999と09:01:30の値は時刻優先の境界例であり、単調増加する本番の累積量を表すものではありません。

```sql
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:00', 201, 2.5);
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:00', 200, 1.25);
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:00', 202, 3.75);

INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:50', 205, 5.5);
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:50', 198, 4.25);
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:50', 206, 6.75);

INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:29.999', 204, 0.25);
INSERT INTO custom_ticks VALUES ('AAPL', '2026-10-19 09:01:30', 203, 999.5);

EXEC TABLE_FLUSH(custom_ticks);
EXEC ROLLUP_FORCE(custom_ticks_rollup_1s);
```

### 保存する元のキー

```sql
SELECT code, time, open_price, open_time, open_gvol,
       close_price, close_time, close_gvol, high_price, low_price
  FROM custom_ticks_1s
 ORDER BY code, time, open_time, close_time;
```

格納先timeは1秒バケット時刻、open_time/close_timeは選択した元時刻です。
元の09:01:29.999はバケット09:01:29に属しますが、候補時刻は09:01:29.999を保持します。
同じバケットに複数の部分行が保存されるため、行数をバケット数と解釈しません。

### 30秒再集計

バケット計算には格納先timeを使い、候補選択には(open_time, open_gvol)と
(close_time, close_gvol)を使います。この通常のDATETIMEキーはBASETIMEである必要はありません。

```sql
SELECT code,
       DATE_BIN('sec', 30, time) AS bucket,
       FIRST((open_time, open_gvol), open_price) AS open_price,
       LAST((close_time, close_gvol), close_price) AS close_price,
       MAX(high_price) AS high_price,
       MIN(low_price) AS low_price
  FROM custom_ticks_1s
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

| code | bucket | open_price | close_price | high_price | low_price |
|---|---|---:|---:|---:|---:|
| AAPL | 2026-10-19 09:01:00 | 200 | 204 | 204 | 200 |
| AAPL | 2026-10-19 09:01:30 | 203 | 206 | 206 | 198 |

### 元データ集計との比較

```sql
SELECT code,
       DATE_BIN('sec', 30, time) AS bucket,
       FIRST((time, gvol), price) AS open_price,
       LAST((time, gvol), price) AS close_price,
       MAX(price) AS high_price,
       MIN(price) AS low_price
  FROM custom_ticks
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

```sql
SELECT FIRST((time, gvol), price) AS open_price,
       LAST((time, gvol), price) AS close_price
  FROM custom_ticks;
```

元データの直接集計と保存結果の再集計は一致する必要があります。1分全体のopen/closeは200/206です。

### 上位集計へのキーの引き継ぎ

別の期間に再集計する結果を保存する場合も、同じFIRST/LAST基準で選んだ元のキーを一緒に引き継ぎます。

```sql
SELECT code,
       DATE_BIN('sec', 30, time) AS bucket,
       FIRST((open_time, open_gvol), open_price) AS open_price,
       FIRST((open_time, open_gvol), open_time) AS open_time,
       FIRST((open_time, open_gvol), open_gvol) AS open_gvol,
       LAST((close_time, close_gvol), close_price) AS close_price,
       LAST((close_time, close_gvol), close_time) AS close_time,
       LAST((close_time, close_gvol), close_gvol) AS close_gvol,
       MAX(high_price) AS high_price,
       MIN(low_price) AS low_price
  FROM custom_ticks_1s
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

バケット時刻のみのFIRST(time, open_price)では、部分要約間の元の順序を必ず復元できるわけではありません。
既存の文字列連結キーの要約は型付きキー要約に自動変換されません。
新しい格納先とジョブで検算し、過去期間の移行には元データの保持期間と再集計可能性を確認します。
Cluster Custom作成は既存のERR-02837による非対応を維持します。

### サンプルオブジェクトの削除

自動処理の再開にはSTART ROLLUP custom_ticks_rollup_1sを使用します。サンプルオブジェクトは次の順で削除します。

```sql
DROP ROLLUP custom_ticks_rollup_1s;
DROP TABLE custom_ticks_1s;
DROP TABLE custom_ticks;
```

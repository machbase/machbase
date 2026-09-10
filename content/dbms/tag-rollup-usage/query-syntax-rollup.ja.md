---
type: docs
title: '6.4 ROLLUPのクエリ構文'
weight: 40
toc: true
aliases:
  - /dbms/tag-rollup-usage/week-month-year-timezone-rollup/
---

<a id="query-syntax-rollup"></a>

## 明示的なROLLUPクエリ

```text
rollup(time_unit, period, basetime_column [, origin])
```

| 引数 | 仕様 |
|---|---|
| time_unit | SECOND/SEC、MINUTE/MIN、HOUR、DAY、WEEK、MONTH、YEAR。大文字・小文字は区別しない |
| period | 正の整数リテラル。カラムやパラメータープレースホルダーは不可 |
| basetime_column | 元の時間軸TAGのBASETIMEカラム |
| origin | 省略時はタイムゾーンオフセットを反映したデフォルト基準点。明示時は単位別の制約を確認 |

戻り値はDATETIMEのバケットです。保存済み集計の最小間隔より細かい結果は復元できません。
適用可能なROLLUPがない場合は、生データのスキャンへ自動的に切り替わらず、エラーになります。
元データの集計が必要なら、DATE_TRUNC/DATE_BIN + GROUP BYのクエリを別途作成してください。

## 準備と基本クエリ

```sql
CREATE TAG TABLE ch6_query (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_query_sec ON ch6_query(value) INTERVAL 1 SEC;
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_query VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_query);
ALTER ROLLUP ch6_query_sec FORCE;

SELECT name, rollup('min', 1, time) AS bucket,
       COUNT(value), SUM(value), MIN(value), MAX(value), AVG(value)
  FROM ch6_query
 WHERE time >= TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time < TO_DATE('2026-01-01 00:02:00', 'YYYY-MM-DD HH24:MI:SS')
 GROUP BY name, bucket ORDER BY name, bucket;
```

TEMP_01の00:00はCOUNT=2、SUM=30、AVG=15、00:01は1、30、30です。
TEMP_02の00:00は1、100、100です。SELECTでnameを返す場合は、GROUP BYにもnameを指定します。
nameを省略すると複数タグをまとめた集計になるため、単位の異なるセンサーを混在させないでください。

## 候補選択とヒント

1. ROLLUP_TABLEヒントがある場合は、その候補の互換性を検査します。
2. 自動選択では、集計カラム・JSONパス・モードと要求間隔に合う候補を探します。
3. 条件なしの候補を先に探し、なければ条件付き候補を含めて検索します。
4. 適用可能な最大の間隔を選び、同じ間隔では先に登録された候補を維持します。

通常か拡張かだけで「通常が常に優先される」と断定しないでください。
条件付きROLLUPしかない場合はフィルタリング済みデータが自動選択され得るため、結果が表すサンプル集合を確認します。
特定の集計を必ず使用する必要がある場合は、ヒントを明示してください。

```sql
SELECT /*+ ROLLUP_TABLE(ch6_query_sec) */
       rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

### 保存候補の間隔とクエリのバケット

現在の候補間隔検査では、SEC要求をperiod秒、MIN要求をperiod分として計算します。
HOURおよびDAY/WEEK/MONTH/YEAR要求は、候補選択段階でperiod時間を基準に検査し、
選択した統計を要求されたカレンダー・時間バケットへ再集計します。

したがって、`rollup('day', 1, time)`のために24 HOUR ROLLUPを作成すれば自動的に使用できるとは考えないでください。
この要求では1時間の基準に合うHOUR/MIN/SEC候補を検討します。
作成時のINTERVALと結果バケットの意味を区別し、実際の実行計画を確認してください。

## 集計関数とサンプル

通常の数値ROLLUPはMIN、MAX、SUM、COUNT、AVG、SUMSQをサポートします。
ROLLUPクエリのFIRST/LASTにはEXTENSIONが必要です。
Customの結果は通常のTAGに保存されるため、[Customの再集計](../custom-rollup/)の合計・件数の規則を使用します。
JSONドキュメント全体の集計におけるCOUNTは、[JSONの節](../json-summarized-rollup/)で別途説明します。

<a id="query-sumsq-stddev-rollup"></a>

### SUMSQと分散・標準偏差

ROLLUPクエリはSTDDEV、STDDEV_POP、VARIANCE、VAR_POPを直接サポートしていません。
`rollup()`クエリでこれらの関数を使用すると、
`ERR-02816: Only rollup column with aggregate function can be referenced in ROLLUP SELECT query.`
が発生します。分散と標準偏差は、区間別の結果をそのまま加算できないためです。
2つの区間の標準偏差を平均しても、全区間の標準偏差にはなりません。

代わりにROLLUPは、値の平方和であるSUMSQをCOUNT、SUMと併せて保存します。
この3つはすべて加算できるため、保存間隔より大きいバケットに再集計しても有効であり、クエリ時に分散と標準偏差を計算できます。
SUMSQは通常のROLLUPとEXTENSION ROLLUPの両方に含まれます。

| 値 | 計算式 |
|---|---|
| 母分散 | `SUMSQ/N - (SUM/N)^2` |
| 母標準偏差 | 母分散の平方根 |
| 標本分散 | `(SUMSQ - SUM^2/N) / (N-1)` |
| 標本標準偏差 | 標本分散の平方根 |

Nは`COUNT(value)`であり、NULLを除いた有効値の個数です。

ROLLUPのクエリブロックにはサポートされる集計だけを置き、分散と標準偏差はインラインビューの外で計算します。
COUNT、SUM、SUMSQを一度だけ読み取り、派生計算を分離するため、計算式を変更してもROLLUPクエリ部分はそのまま使用できます。

```sql
SELECT bucket, n, s, sq,
       sq/n - POWER(s/n, 2)       AS var_pop,
       SQRT(sq/n - POWER(s/n, 2)) AS stddev_pop
  FROM (
      SELECT rollup('min', 1, time) AS bucket,
             COUNT(value)           AS n,
             SUM(value)             AS s,
             SUMSQ(value)           AS sq
        FROM ch6_query WHERE name = 'TEMP_01'
       GROUP BY bucket
  ) t
 ORDER BY bucket;
```

00:00バケットの値は10と20なので、n=2、s=30、sq=500、母分散25、母標準偏差5です。
00:01バケットは値が1つなので、母分散と母標準偏差は0です。

標本分散の分母は`N-1`のため、値が1つのバケットを先に判別する必要があります。
この判定もインラインビューの外で行います。`ELSE NULL`を明示すると`ERR-02042`が発生するため、`ELSE`を省略します。

```sql
SELECT bucket, n,
       CASE WHEN n > 1
            THEN (sq - POWER(s, 2)/n) / (n - 1)
            END AS var_samp
  FROM (
      SELECT rollup('min', 1, time) AS bucket,
             COUNT(value)           AS n,
             SUM(value)             AS s,
             SUMSQ(value)           AS sq
        FROM ch6_query WHERE name = 'TEMP_01'
       GROUP BY bucket
  ) t
 ORDER BY bucket;
```

00:00バケットの標本分散は50、値が1つの00:01バケットはNULLです。
値が1つの区間を結果から除くには、インラインビューの外で`WHERE n > 1`を使用します。
元テーブルの`VARIANCE`と`STDDEV`は同じ区間でNULLではなく0を返すため、両方の結果を併用する場合は表示ポリシーを合わせてください。

上の例の値では、元テーブルに`VAR_POP`、`STDDEV_POP`、`VARIANCE`、`STDDEV`を直接使用した結果と一致します。
ただし、2つの計算式は平均が大きく偏差が小さいほど桁落ちが発生します。
例えば、値が100000付近で小数点以下だけ変動する場合、`SUMSQ/N`と`(SUM/N)^2`がほぼ同じ大きさになり、減算結果の有効桁数が減少します。
浮動小数点誤差で分散がごく小さな負数になると、`SQRT`の結果も無効になります。
精度が重要な区間では、元テーブルの`STDDEV`、`VAR_POP`の結果と比較し、使用可能な範囲を確認してください。

<a id="query-week-month-year-day-timezone-origin-rollup"></a>

## カレンダー単位とorigin

同じ準備データを使用し、月単位の結果と月曜日を基準にした週単位を確認します。

```sql
SELECT rollup('month', 1, time, '2000-01-01 00:00:00') AS bucket,
       SUM(value), COUNT(value), AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;

SELECT rollup('week', 1, time, '1970-01-05 00:00:00') AS bucket, AVG(value)
  FROM ch6_query WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

月単位のクエリは2026-01-01バケットにSUM=60、COUNT=3、AVG=20を返します。
月・年のoriginはタイムゾーン解釈後に月の1日である必要があり、結果はその月境界の午前0時です。
任意の日付や時刻オフセットで月次業務の開始時刻を移す機能と解釈しないでください。
日・週などの固定間隔のoriginと、月・年のカレンダー計算を区別します。

文字列の意味は接続タイムゾーンと併せて確認してください。
DSTが自動的に業務カレンダーに合うと考えず、境界前後の元データのDATE_BIN集計と比較してください。
保存済み集計を分割する必要があるoriginや検索境界では、元データと同じ結果を期待できるか検証します。

## クリーンアップ

```sql
DROP ROLLUP ch6_query_sec;
DROP TABLE ch6_query;
```

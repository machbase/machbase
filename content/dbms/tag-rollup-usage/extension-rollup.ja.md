---
type: docs
title: '6.7 拡張ROLLUPとFIRST/LAST'
weight: 70
toc: true
aliases:
  - /dbms/tag-rollup-usage/first-last-rollup/
---

<a id="rollup-extension"></a>

## EXTENSIONと元データのFIRST/LASTの違い

EXTENSIONはROLLUPに最初・最後の値と関連する時刻情報を追加します。
通常の元データのGROUP BYでFIRST/LASTを使うことと、保存済みROLLUPからFIRST/LASTを取得することは異なります。
後者には、適用可能な拡張ROLLUPが必要です。

時刻のみのEXTENSIONは最初・最後の値と時刻を保存し、ソート付きEXTENSIONは候補の補助キーも保存します。
MIN、MAX、SUM、COUNT、平方和のSUMSQは通常のROLLUPにも保存されます。
SUMSQから分散と標準偏差を計算する方法は、
[SUMSQと分散・標準偏差](../query-syntax-rollup/#query-sumsq-stddev-rollup)を参照してください。

## 準備と入力

```sql
CREATE TAG TABLE ch6_ext (
    code VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    price DOUBLE
);
CREATE ROLLUP ch6_ext_first
  ON ch6_ext(price) INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP ch6_ext_plain
  ON ch6_ext(price) INTERVAL 1 MIN;
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:10', 'YYYY-MM-DD HH24:MI:SS'), 105);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:20', 'YYYY-MM-DD HH24:MI:SS'), 99);
INSERT INTO ch6_ext VALUES ('AAPL', TO_DATE('2026-01-01 09:00:30', 'YYYY-MM-DD HH24:MI:SS'), 103);
EXEC TABLE_FLUSH(ch6_ext);
ALTER ROLLUP ch6_ext_first FORCE;
ALTER ROLLUP ch6_ext_plain FORCE;
```

## 元データとOHLCの比較

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       FIRST(time, price) AS open_price, MAX(price) AS high_price,
       MIN(price) AS low_price, LAST(time, price) AS close_price
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket ORDER BY bucket;

SELECT /*+ ROLLUP_TABLE(ch6_ext_first) */
       rollup('min', 1, time) AS bucket,
       FIRST(time, price) AS open_price, MAX(price) AS high_price,
       MIN(price) AS low_price, LAST(time, price) AS close_price
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket ORDER BY bucket;
```

両方のクエリは、09:00バケットにOpen=100、High=105、Low=99、Close=103を返します。
時刻のみのROLLUPのFIRST/LASTでは、第1引数にBASETIME、第2引数に集計対象カラムを使用します。
同じ時刻の行に業務上の順序が必要な場合は、以下の複合キー定義を使用します。

## 通常の候補と拡張候補が共存する場合

通常のROLLUPが拡張ROLLUPより無条件に優先されるわけではありません。
同じ条件・間隔の候補は、登録順序の影響を受けます。
この例では拡張を先に作成していますが、特定候補を使用する必要がある場合は上記のように明示してください。
拡張だけが適用可能な環境では、ヒントなしで選択される場合もあります。

次は通常のROLLUPを強制するため、意図的に失敗するクエリです。

```sql
SELECT /*+ ROLLUP_TABLE(ch6_ext_plain) */
       rollup('min', 1, time) AS bucket, FIRST(time, price)
  FROM ch6_ext WHERE code = 'AAPL'
 GROUP BY bucket;
```

自動階層に拡張が必要なら、別のテーブルのCREATEで`WITH ROLLUP (SEC) EXTENSION`を使用します。
FROMで階層を作成する場合も、拡張属性を一致させる必要があります。
Custom OHLCVの再集計は[Customの例](../custom-rollup/)を参照してください。

## クリーンアップ

```sql
DROP ROLLUP ch6_ext_plain;
DROP ROLLUP ch6_ext_first;
DROP TABLE ch6_ext;
```

<a id="composite-first-last"></a>

## 複合キーFIRST/LASTとソート付きROLLUP

> 複合ソートキーには、この機能を含むエンジンビルドが必要です。使用中の製品バージョンの対応状況を確認してください。

公開ROWIDソートキーはこの文書の対応範囲外です。

### サンプルデータ

raw_tabはROLLUPのない元TAG、rollup_tabはソート付きROLLUPの集約元TAGです。
同名オブジェクトがない別環境を前提とします。第1キーは時刻です。
入力順は業務キー順と異なり、銘柄ごとの各分の開始時刻には同じcode/timeの行が3件あります。

```sql
CREATE TAG TABLE raw_tab (
    code     VARCHAR(20) PRIMARY KEY,
    time     DATETIME BASETIME,
    price    DOUBLE SUMMARIZED,
    seq      INTEGER,
    event_id INTEGER
);

INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 102, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:50'), 105, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 103, 2, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:00'), 101, 1, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:00:50'), 104, 1, 1);

INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 202, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:50'), 205, 1, 2);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 203, 2, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:00'), 201, 1, 1);
INSERT INTO raw_tab VALUES ('A', TO_DATE('2026-10-22 09:01:50'), 204, 1, 1);

INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 302, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:50'), 305, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 303, 2, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:00'), 301, 1, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:00:50'), 304, 1, 1);

INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 402, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:50'), 405, 1, 2);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 403, 2, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:00'), 401, 1, 1);
INSERT INTO raw_tab VALUES ('B', TO_DATE('2026-10-22 09:01:50'), 404, 1, 1);

EXEC TABLE_FLUSH(raw_tab);

SELECT COUNT(*) AS row_count FROM raw_tab;
```

### 元データ照会と同順位

timeのみの場合、Aの09:00のFIRST候補は101/102/103、LAST候補は104/105です。
(time, seq)ではFIRSTが101/102に絞られますが、time/seqが等しいため特定行は保証されません。
次の照会はevent_idも比較して候補を決定します。

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST(time, price) AS first_price,
       LAST(time, price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time, seq), price) AS first_price,
       LAST((time, seq), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

| code | bucket | first_price | last_price |
|---|---|---:|---:|
| A | 2026-10-22 09:00:00 | 101 | 105 |
| A | 2026-10-22 09:01:00 | 201 | 205 |
| B | 2026-10-22 09:00:00 | 301 | 305 |
| B | 2026-10-22 09:01:00 | 401 | 405 |

### キー別の方向

```sql
SELECT code, DATE_TRUNC('minute', time) AS bucket,
       FIRST((time ASC, seq ASC, event_id DESC), price) AS first_price,
       LAST((time ASC, seq ASC, event_id DESC), price) AS last_price
  FROM raw_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

event_idのみDESCにすると、結果はA=102/104、202/204、B=302/304、402/404になります。

### ソート付きROLLUPの定義と照会

rollup_tabに同じデータを格納し、定義と一致するキーで照会します。
ROLLUP_TABLEヒントは、この例で保存済みROLLUPを明示的に選択します。

```sql
CREATE TAG TABLE rollup_tab (
    code     VARCHAR(20) PRIMARY KEY,
    time     DATETIME BASETIME,
    price    DOUBLE SUMMARIZED,
    seq      INTEGER,
    event_id INTEGER
);

INSERT INTO rollup_tab SELECT * FROM raw_tab;
EXEC TABLE_FLUSH(rollup_tab);

CREATE ROLLUP price_1m_ordered
    ON rollup_tab(price)
    INTERVAL 1 MIN
    EXTENSION ORDER BY time ASC, seq ASC, event_id ASC;

ALTER ROLLUP price_1m_ordered FORCE;
```

```sql
SELECT /*+ ROLLUP_TABLE(price_1m_ordered) */
       code, ROLLUP('min', 1, time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM rollup_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

結果は元データの3キーASC照会と同じです。DESC照会には方向が一致する別の定義が必要です。

```sql
CREATE ROLLUP price_1m_desc
    ON rollup_tab(price)
    INTERVAL 1 MIN
    EXTENSION ORDER BY time ASC, seq ASC, event_id DESC;

ALTER ROLLUP price_1m_desc FORCE;

SELECT /*+ ROLLUP_TABLE(price_1m_desc) */
       code, ROLLUP('min', 1, time) AS bucket,
       FIRST((time, seq, event_id DESC), price) AS first_price,
       LAST((time, seq, event_id DESC), price) AS last_price
  FROM rollup_tab
 WHERE time >= TO_DATE('2026-10-22 09:00:00')
   AND time <  TO_DATE('2026-10-22 09:02:00')
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

### 上位ROLLUP

```sql
CREATE ROLLUP price_1h_ordered
    FROM price_1m_ordered
    INTERVAL 1 HOUR EXTENSION;

ALTER ROLLUP price_1h_ordered FORCE;

SELECT /*+ ROLLUP_TABLE(price_1h_ordered) */
       code, ROLLUP('hour', 1, time) AS bucket,
       FIRST((time, seq, event_id), price) AS first_price,
       LAST((time, seq, event_id), price) AS last_price
  FROM rollup_tab
 GROUP BY code, bucket
 ORDER BY code, bucket;
```

上位ROLLUPは下位のソート定義と元の候補キーを継承します。時間単位の結果はA=101/205、B=301/405です。

### 定義の一致と変更制約

- 第1キーは元TAGのBASETIME、補助キーは対応する通常データカラムでなければなりません。
  TAG名、メタデータ、式、テーブル名付きカラム参照は定義に使用できません。
- 数値対象のソート付きEXTENSIONをサポートします。JSON_PATH/JSON_SUMMARYとの組み合わせは非対応です。
- キー数・カラム・順序・方向・型は定義と一致する必要があります。異なる方向をヒントで強制するとエラーになります。
- 既存の時刻のみのROLLUPには補助キーがありません。新定義で元データを再集計します。削除済みの元キーは復元できません。
- 保存候補キーによって、通常のWHERE・GROUP BY・出力で元カラムを利用できる範囲が拡大することはありません。
- ソートメタデータや生成SQLの長さ制限を超える定義は作成時に拒否されます。
- Standardでは参照キーのRENAMEをERR-02686で拒否します。停止中ジョブと上位の依存関係にも適用します。
  関連する上位・下位ROLLUPをすべてDROPした後、カラム名を変更して再作成します。
- 元データUPDATE後の自動再集計を追加する機能ではありません。
- Clusterの全broker・warehouseに、機能をサポートする同一ビルドが必要です。

### サンプルオブジェクトの削除

```sql
DROP ROLLUP price_1h_ordered;
DROP ROLLUP price_1m_desc;
DROP ROLLUP price_1m_ordered;
DROP TABLE rollup_tab;
DROP TABLE raw_tab;
```

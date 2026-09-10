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

EXTENSIONが追加するのは最初・最後の値と時刻だけです。
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
ROLLUPのFIRST/LASTの第1引数にはBASETIME、第2引数には集計対象カラムを使用します。
同じ時刻に複数の値がある場合に業務上の追加の順序が必要なら、別途設計してください。

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
Custom OHLCVの再集計は[Customの実習](../custom-rollup/)を参照してください。

## クリーンアップ

```sql
DROP ROLLUP ch6_ext_plain;
DROP ROLLUP ch6_ext_first;
DROP TABLE ch6_ext;
```

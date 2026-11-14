---
type: docs
title: '6.2 ROLLUP対象TAGテーブルの設計'
weight: 20
toc: true
---

<a id="design-rollup-on"></a>

## ONとFROM

`ON source(column)`は元の時間軸TAGの列を集計します。
`FROM rollup_name`は既存の通常・拡張ROLLUPの統計を、より大きい区間に合算します。
Customの出力先もTAGですが、次のCustom段階は出力先TAGをSELECTするINTO...AS構文で構成します。

## 階層の実習

```sql
CREATE TAG TABLE ch6_design (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_design_sec ON ch6_design(value) INTERVAL 1 SEC;
CREATE ROLLUP ch6_design_min FROM ch6_design_sec INTERVAL 1 MIN;
CREATE ROLLUP ch6_design_hour FROM ch6_design_min INTERVAL 1 HOUR;
INSERT INTO ch6_design VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_design VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_design VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_design VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_design);
ALTER ROLLUP ch6_design_sec FORCE;
ALTER ROLLUP ch6_design_min FORCE;
ALTER ROLLUP ch6_design_hour FORCE;

SELECT name, rollup('hour', 1, time) AS bucket,
       SUM(value), COUNT(value), AVG(value)
  FROM ch6_design
 GROUP BY name, bucket ORDER BY name, bucket;
```

TEMP_01は合計60、件数3、平均20、TEMP_02は100、1、100です。
下位からFORCEを実行すると、上位が新しく作成された下位の結果も処理できます。

### 階層の制約

- 上位の間隔はソースの間隔より大きい整数倍である必要があります。同じ間隔も許可されません。
- FROMを使って通常のROLLUPを拡張ROLLUPに変更したり、その逆に変更したりすることはできません。
  階層内のEXTENSION属性を一致させてください。
- JSONパス・ドキュメントモードもソースと一致する必要があります。
- 必要なクエリの最小区間より粗い統計から、より細かい元データは復元できません。

次は、それぞれ意図的に失敗する作成例です。

```sql
CREATE ROLLUP ch6_design_bad_same FROM ch6_design_min INTERVAL 1 MIN;
CREATE ROLLUP ch6_design_bad_divisor FROM ch6_design_min INTERVAL 90 SEC;
CREATE ROLLUP ch6_design_bad_ext FROM ch6_design_sec INTERVAL 1 MIN EXTENSION;
```

## 間隔と保存量の決定

すべてのタグがすべての区間に値を持つと仮定すると、論理バケット数はおおよそ
`(保持時間 / バケット間隔) × タグ数`です。1万タグの1秒バケットを365日間保持すると、約3,154億バケットになります。
実際の保存行数は部分集計・空の区間・列数の影響を受け、ディスク容量は圧縮と保存オーバーヘッドも含めて測定する必要があります。

秒単位の観測値を分単位でしか検索しない場合は、最初からすべての秒階層が必要かを検討してください。
作成間隔はSEC/MIN/HOURで表しますが、DAY/WEEK/MONTH/YEARはクエリのバケット単位です。
特に、日単位のクエリに24 HOURの保存間隔をそのまま適用できるとは考えず、[候補選択規則](../query-syntax-rollup/)を確認してください。

新しいROLLUPはソースに残る既存データも初期集計するため、初期処理量とgapを確認します。
元データの補正はFORCEで巻き戻して処理されません。[REBUILDのサポート範囲](../rollup-rebuild/)に従ってください。

## クリーンアップ

```sql
DROP ROLLUP ch6_design_hour;
DROP ROLLUP ch6_design_min;
DROP ROLLUP ch6_design_sec;
DROP TABLE ch6_design;
```

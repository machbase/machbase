---
type: docs
title: '6.1 ROLLUPの概要と選択基準'
weight: 10
toc: true
---

ROLLUPは、生データの行から同じ集計を繰り返すコストを削減します。
元データの保持ポリシーや任意のクエリ結果のキャッシュではなく、集計に保存していない元の情報は復元できません。

<a id="original-85-rollup-tables"></a>
<a id="rollup"></a>

## 選択基準

| 要求 | 検討する方式 |
|---|---|
| 1つの数値カラムの区間統計を繰り返し使用 | 通常のROLLUP |
| 特定の品質条件を満たすサンプルだけを集計 | 条件付きROLLUP |
| 区間の最初・最後の値が必要 | EXTENSION ROLLUP |
| 複数の集計式を別のTAGに保存 | Custom ROLLUP（Standard Edition専用） |
| JSONパスやドキュメント内の数値を集計 | JSONパスまたはドキュメント全体のROLLUP |
| 距離軸TAG | 通常の数値区間集計。ROLLUPは未サポート |

通常の数値カラムを明示して作成するROLLUPでは、SUMMARIZEDは必須ではありません。
WITH ROLLUPによる自動作成とJSONドキュメント全体の集計には、別途SUMMARIZEDの条件があります。
詳細は[作成構文](../create-delete-rollup/)を参照してください。

## 基本実習

### 1. 作成と入力

```sql
CREATE TAG TABLE ch6_basic (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_basic_ru ON ch6_basic(value) INTERVAL 1 MIN;
INSERT INTO ch6_basic VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_basic VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_basic VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_basic VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
```

### 2. 集計完了範囲の確認

```sql
EXEC TABLE_FLUSH(ch6_basic);
ALTER ROLLUP ch6_basic_ru FORCE;
SHOW ROLLUPGAP;
```

SHOW ROLLUPGAPはmachsqlのコマンドです。SDKではV$ROLLUPなど、サポートされるSQLクエリを使用します。
TABLE_FLUSHは保存バッファを処理し、FORCEは指定したROLLUPの処理範囲に追いつくための操作です。
継続入力中に今後到着する行まで処理を完了するという意味ではありません。

### 3. 元データとの比較

```sql
SELECT DATE_TRUNC('minute', time) AS bucket,
       COUNT(value), MIN(value), MAX(value), AVG(value)
  FROM ch6_basic
 WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;

SELECT rollup('min', 1, time) AS bucket,
       COUNT(value), MIN(value), MAX(value), AVG(value)
  FROM ch6_basic
 WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

| バケット | COUNT(value) | MIN | MAX | AVG |
|---|---:|---:|---:|---:|
| 2026-01-01 00:00:00 | 2 | 10 | 20 | 15 |
| 2026-01-01 00:01:00 | 1 | 30 | 30 | 30 |

両方のクエリは同じ結果を返す必要があります。
DATE_TRUNCによる元データの集計が、ROLLUPの存在だけで自動的に切り替わるとは説明しません。
ROLLUPのクエリでは`rollup()`を明示します。

### 4. クリーンアップ

```sql
DROP ROLLUP ch6_basic_ru;
DROP TABLE ch6_basic;
```

## 導入前の確認

代表的なタグ数、入力量、検索頻度、許容できる集計遅延を決めます。
必要な最小の区間と元データの保持期間を先に決め、[階層設計](../target-tag-table-design/)に進んでください。
長期間の性能は本番に近いデータで測定し、この小さなサンプルの実行時間から推定しないでください。

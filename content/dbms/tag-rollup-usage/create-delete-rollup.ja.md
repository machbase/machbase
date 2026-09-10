---
type: docs
title: '6.3 ROLLUPの作成と削除'
weight: 30
toc: true
---

<a id="create-delete-rollup"></a>

## 作成構文

```text
CREATE ROLLUP [IF NOT EXISTS] name
  ON source_tag [(column_or_json_path)]
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [EXTENSION]
  [WHERE predicate];

CREATE ROLLUP [IF NOT EXISTS] name
  FROM source_rollup
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [EXTENSION]
  [WHERE predicate];
```

EXTENSIONの後に別の拡張名は指定しません。CREATEの単位はSEC/MIN/HOURであり、
クエリ関数のDAY/MONTHなどとは区別します。間隔は正数で、現在の検証上限は365日に相当する間隔です。
ソース・階層・集計モードの条件も満たす必要があります。

| 対象 | 条件 |
|---|---|
| 通常の数値カラム | サポートされる数値型を指定。SUMMARIZEDは必須ではない |
| JSONパス | 対象のJSONカラムと有効なパスを指定 |
| JSONドキュメント全体 | JSON SUMMARIZEDカラムが必要 |
| WITH ROLLUPによる自動作成 | 3番目にSUMMARIZEDカラムが必要 |
| METADATA・距離軸・TAG以外 | 通常のROLLUPの対象外 |

## 作成・重複確認・検索の実習

```sql
CREATE TAG TABLE ch6_create (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP IF NOT EXISTS ch6_create_ru ON ch6_create(value) INTERVAL 1 MIN;
CREATE ROLLUP IF NOT EXISTS ch6_create_ru ON ch6_create(value) INTERVAL 1 MIN;
INSERT INTO ch6_create VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_create VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_create VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_create VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_create);
ALTER ROLLUP ch6_create_ru FORCE;
SELECT DISTINCT ROLLUP_NAME, COLUMN_NAME, INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CREATE_RU';
SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_create WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

同名で再作成しても既存の定義は保持されます。IF NOT EXISTSは定義の変更や同一性の確認機能ではなく、
不正なSQLやソースの検証をすべて省略するオプションでもありません。
2つの間隔カラムは60000msで、検索結果の平均は00:00が15、00:01が30です。

IF NOT EXISTSなしで同じ名前を作成するとエラーになります。通常の実習とは別に確認してください。

```sql
CREATE ROLLUP ch6_create_ru ON ch6_create(value) INTERVAL 1 MIN;
```

## WITH ROLLUPによる自動作成

次は別のテーブルです。SECからMIN・HOURまでの基本階層を自動作成します。

```sql
CREATE TAG TABLE ch6_auto (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);
SELECT DISTINCT ROLLUP_NAME, ROOT_TABLE, INTERVAL_TIME, EXT_TYPE
  FROM V$ROLLUP WHERE ROOT_TABLE = 'CH6_AUTO'
 ORDER BY INTERVAL_TIME;
```

INTERVAL_TIMEが1000・60000・3600000の3行が返されます。

EXTENSIONの自動作成は`WITH ROLLUP (SEC) EXTENSION`形式です。
実際の作成名はV$ROLLUPで確認し、名前の競合が自動的に解消されるとは考えないでください。

引数に応じて作成される階層が異なります。`(SEC)`はSEC・MIN・HOURの3つ、`(MIN)`はMIN・HOURの2つ、
`(HOUR)`はHOURを1つ作成します。引数の省略は`(SEC)`と同じです。
このとき、最初の段階だけが元のTAGをソースとし、次の段階は直前のROLLUPをソースとする階層で接続されます。
引数にはSEC・MIN・HOURのみ使用でき、クエリ関数が受け付けるDAYなどの単位を指定するとエラーになります。

## 削除と定義変更

他のROLLUPが参照するソースは、上位の依存オブジェクトから削除します。
Customの出力先TAGは、ジョブを削除するまでDROPできません。
定義を変更する場合は、読み取り側アプリケーションと再集計時間を考慮し、新しいオブジェクトへ切り替えるか、既存の定義を削除して再作成します。

```sql
DROP ROLLUP ch6_create_ru;
DROP TABLE ch6_create;
DROP TABLE ch6_auto CASCADE;
```

最後のCASCADEは、この実習で自動作成したROLLUPも削除します。通常の運用での削除方法のデフォルトにはしないでください。
CustomソースのCASCADEが関連ジョブを削除しても、ユーザーの出力先TAGまで自動削除するという意味ではありません。

条件付き・拡張・JSON・Customの実習は各節で独立して提供します。
完全な構文は[SQLリファレンス](../../reference/sql/syntax/rollup-syntax/)を参照してください。

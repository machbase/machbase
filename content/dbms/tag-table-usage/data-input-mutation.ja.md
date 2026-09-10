---
type: docs
title: '5.4 データの入力と変更'
weight: 40
toc: true
---
TAGデータはSQL `INSERT`、Append API、ファイルロードツールで入力します。SQLの例は機能確認と
少量の入力に使用し、継続的な収集にはAppend APIを優先して検討します。

<a id="original-85-inserting-data"></a>

## SQL INSERT

次の例では時間軸と距離軸のTAGをそれぞれ作成し、データを確認して削除します。
実習用の名前が既存テーブルと重複しないことを先に確認します。時間軸の名前はセンサーを、
距離軸の名前は1つの検査対象・検査回を識別します。

```sql
CREATE TAG TABLE ch5_input_time (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
);

INSERT INTO ch5_input_time
VALUES ('TEMP_001', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 25.5);
INSERT INTO ch5_input_time
VALUES ('TEMP_001', TO_DATE('2026-01-01 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 25.7);

CREATE TAG TABLE ch5_input_distance (
    name     VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE,
    quality  INTEGER
);

INSERT INTO ch5_input_distance VALUES ('PIPE_A', 0.0, 10.1, 100);
INSERT INTO ch5_input_distance VALUES ('PIPE_A', 500.5, 11.2, 100);

EXEC TABLE_FLUSH(ch5_input_time);
EXEC TABLE_FLUSH(ch5_input_distance);

SELECT name, time, value FROM ch5_input_time ORDER BY time;
SELECT name, distance, value, quality
  FROM ch5_input_distance
 ORDER BY distance;

SELECT COUNT(*) FROM ch5_input_time;
SELECT COUNT(*) FROM ch5_input_distance;

DROP TABLE ch5_input_distance;
DROP TABLE ch5_input_time;
```

各テーブルはそれぞれ2行を返します。時間軸の値は25.5、25.7、距離軸は0.0、500.5です。
タグを事前登録していないため、最初のDATA入力でその名前が自動登録されます。
実際の発生時刻と再送の有無はアプリケーションで管理します。

`TABLE_FLUSH`は、保留中のストレージ・入力バッファを明示的にフラッシュする必要がある
検証・運用手順で使用します。トランザクションのコミットや検索時の可視性を保証する手段ではなく、
通常の収集ループで行ごとに実行しないでください。引数とエラー仕様は
[EXECプロシージャリファレンス](/dbms/reference/sql/syntax/execute-procedure-syntax/#table-flush)を
参照してください。

## メタデータとともに入力

ユーザーメタデータのあるTAGでも、DATAだけを入力して新しいタグを自動登録できます。
位置・単位などを先に指定する必要がある場合は、`INSERT ... METADATA`で登録してからDATAを
入力します。データとメタデータを一緒に渡す構文もサポートされています。
通常のDATA入力のたびに登録済み属性が更新されるとは限りません。システム管理列は入力一覧に
含めないでください。

メタデータ値の登録・更新・削除は[TAGメタデータ](../tag-metadata/)を参照してください。

## 入力経路の選択

| 経路 | 適している場合 | 確認事項 |
| --- | --- | --- |
| SQL `INSERT` | 機能確認、低頻度の入力 | 文ごとの解析・往復コスト |
| SDK Append | 継続的な高スループット入力 | バッチサイズ、フラッシュ、エラー処理 |
| `csvimport` / `machloader` | クライアントファイルの一括ロード | 列順序、日付形式、badファイル |
| `LOAD DATA INFILE` | サーバーからアクセスできるファイル | サーバー上のパス・権限、エラーポリシー |

SDKごとの接続とAppendの例は[開発ツール連携](/dbms/development-tools-integration/)、
ファイル形式とコマンドは
[データの入力・ロード・エクスポート](/dbms/development-tools-integration/data-input-load-export/)を
参照してください。

## データの訂正

TAG data UPDATEはStandard Editionで、タグの選択条件とBASETIMEの範囲をともに指定して
実行します。タグ名、軸、メタデータ列は通常のdata UPDATEの対象にしません。
訂正後も計算済みのROLLUPは自動変更されないため、ROLLUPがある場合は対象範囲を明示的に
再構築します。手順は[ROLLUP_REBUILD](../../tag-rollup-usage/rollup-rebuild/)を参照してください。

成功応答・失敗行数と再試行ポリシーは、選択した入力APIで確認します。SQLのNULL、SDKのNULL表現、
数値の0を区別し、同じ観測を再送する場合の重複ポリシーも定めます。
数値ARRAY・スパース入力には[ARRAY Appendの例](../../development-tools-integration/data-input-load-export/array-append/)を
使用します。

詳しい手順は[TAGデータの訂正](../tag-data-update-correction/)を参照してください。

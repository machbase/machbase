---
type: docs
title: '6.9 ROLLUPの制御と状態確認'
weight: 90
toc: true
aliases:
  - /dbms/tag-rollup-usage/state-check-rollup/
  - /dbms/tag-rollup-usage/operational-notes-rollup/
---

<a id="ingestion-start-stop-immediate-collect-rollup"></a>

## ジョブの状態と処理完了

ROLLUPは作成時に自動的に開始します。直後にSTARTを繰り返したり、停止済みのジョブに再度STOPを実行したりすると、状態エラーが発生する場合があります。
次の実習では、作成 → STOP → 入力 → START → WAKEUP → FORCEの順に状態を区別します。

```sql
CREATE TAG TABLE ch6_control (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    quality INTEGER
);
CREATE ROLLUP ch6_control_ru ON ch6_control(value)
  INTERVAL 1 MIN WAKEUP INTERVAL 10 SEC;
ALTER ROLLUP ch6_control_ru STOP;
INSERT INTO ch6_control VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 1);
INSERT INTO ch6_control VALUES ('TEMP_01', TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 1);
INSERT INTO ch6_control VALUES ('TEMP_01', TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 30.0, 1);
INSERT INTO ch6_control VALUES ('TEMP_02', TO_DATE('2026-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 100.0, 1);
EXEC TABLE_FLUSH(ch6_control);

SELECT DISTINCT ROLLUP_NAME, ENABLED, INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CONTROL_RU';

ALTER ROLLUP ch6_control_ru START;
ALTER ROLLUP ch6_control_ru WAKEUP;
ALTER ROLLUP ch6_control_ru FORCE;

SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_control WHERE name = 'TEMP_01'
 GROUP BY bucket ORDER BY bucket;
```

停止状態のENABLEDは0、INTERVAL_TIMEは60000ms、WAKEUP_INTERVALは10000msです。
最後のクエリは、TEMP_01の00:00の平均15と00:01の平均30を返します。

| コマンド | 目的 | 完了の意味 |
|---|---|---|
| STOP | ジョブを停止 | 以後の未処理入力は残る |
| START | 停止したジョブを再開 | 処理位置から続行 |
| WAKEUP | ジョブを起動 | 処理完了は待たない |
| FORCE | 対象ソースの処理範囲に追いつくまで待機 | 過去の修正分の再計算や将来の入力完了ではない |
| ROLLUP_REBUILD | サポート対象の過去バケットを再計算 | 元データの補正後に集計を再構築 |

SQL ALTERの代わりに、名前を指定した`EXEC ROLLUP_START(name)`、`ROLLUP_STOP(name)`、
`ROLLUP_FORCE(name)`も使用できます。同じ状態遷移を両方の形式で続けて実行しないでください。
名前を指定しない一括制御と、特定ジョブの制御の範囲を混同しないでください。

## WAKEUP INTERVAL

省略時は作成時のINTERVALと同じです。正数で、集計間隔以下であり、集計間隔を割り切れる値にする必要があります。
起動頻度を高めると遅延を減らせますが、処理負荷も増加します。

```sql
ALTER ROLLUP ch6_control_ru SET WAKEUP INTERVAL 5 SEC;
SELECT DISTINCT ROLLUP_NAME, INTERVAL_TIME, WAKEUP_INTERVAL
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CONTROL_RU';
```

WAKEUP_INTERVALが5000msになります。次は60秒の約数でない値を使う意図的なエラーです。

```sql
ALTER ROLLUP ch6_control_ru SET WAKEUP INTERVAL 7 SEC;
```

<a id="state-status-rollup-wakeup-interval-vrollup"></a>

## V$ROLLUPの読み方

| カラム | 意味 |
|---|---|
| ROLLUP_NAME | 制御するジョブ名 |
| ROLLUP_TABLE | 集計先テーブル。Customではユーザーの出力先TAG |
| SOURCE_TABLE, ROOT_TABLE | 直接のソースと、ジョブを解釈するための元データの関係 |
| COLUMN_NAME | 通常集計・パス集計の対象カラム |
| INTERVAL_TIME, WAKEUP_INTERVAL | ミリ秒単位の作成間隔・実行間隔 |
| LAST_WAKEUP_TIME, NEXT_WAKEUP_TIME | 直前の起動時刻と次の予定時刻 |
| EXT_TYPE | 0: 通常、1: 拡張、2: Custom |
| PREDICATE | 通常の条件式、またはCustomのSELECT本文 |
| ENABLED | ジョブの有効状態 |
| RUN_STATE | `I`: 初期、`S`: 待機、`R`: 処理中 |
| END_RID | ソースの処理位置 |
| LAST_ELAPSED_MSEC | 直前の処理時間（ms） |
| DATABASE_NAME, USER_ID | データベース・所有者の識別 |

```sql
SELECT ROLLUP_NAME, ROLLUP_TABLE, SOURCE_TABLE, ROOT_TABLE,
       INTERVAL_TIME, WAKEUP_INTERVAL, LAST_WAKEUP_TIME, NEXT_WAKEUP_TIME,
       ENABLED, RUN_STATE, LAST_ELAPSED_MSEC
  FROM V$ROLLUP WHERE ROLLUP_NAME = 'CH6_CONTROL_RU'
 ORDER BY ROLLUP_NAME;
SHOW ROLLUPGAP;
```

SHOW ROLLUPGAPはmachsql専用のクライアントコマンドです。SDKの通常のSQL APIには送信しないでください。
GAPはソースとROLLUPの処理RIDの差です。時間遅延そのものではなく、すべての階層・関連ノードの状態と併せて確認します。
gap=0でも、集計済みの元データに対する補正が反映されたとは限りません。
継続入力中の値は観測時点で変わるため、再現実習では入力を止めて比較します。

停止中に元データが保持ポリシーで削除された場合、STARTだけでは復元できません。
FORCEは下位から上位の順に実行し、失敗したら最初のエラー、状態、ソースにアクセス可能かを確認してください。

## クリーンアップ

```sql
DROP ROLLUP ch6_control_ru;
DROP TABLE ch6_control;
```

詳細なコマンド仕様は[EXECリファレンス](../../reference/sql/syntax/execute-procedure-syntax/)と
[ROLLUPのトラブルシューティング](../../troubleshooting/rollup/)を参照してください。

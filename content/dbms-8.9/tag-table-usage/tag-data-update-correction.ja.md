---
type: docs
title: '5.11 TAG data UPDATEとデータ補正'
weight: 110
toc: true
---

TAG DATAの補正には、元の値を直接変更する方法と、元の値を保持して検索時に補正値を適用する
方法があります。ROLLUPへの影響も異なります。このページのUPDATE実習は
Machbase DBMS 8.7.0 Standard Editionを前提とします。

<a id="correction-performance-bulk-considerations-tag-data-update"></a>

## 値の直接訂正

タグ名とBASETIMEの条件をともに指定します。SETの右辺では既存行の列を参照できないため、
`SET value = value + 1`のような式ではなく、計算済みの値またはバインドパラメーターを渡します。
次のテーブルを、名前が重複しないことを確認して準備します。ROLLUPの訂正も確認できるように、
デフォルトのROLLUPも作成します。

```sql
CREATE TAG TABLE ch5_correction (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED,
    status INTEGER
) WITH ROLLUP;
INSERT INTO ch5_correction VALUES
    ('TEMP-01', TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 0);
INSERT INTO ch5_correction VALUES
    ('TEMP-01', TO_DATE('2026-01-01 12:30:00', 'YYYY-MM-DD HH24:MI:SS'), 99.0, 0);
INSERT INTO ch5_correction VALUES
    ('TEMP-02', TO_DATE('2026-01-01 12:30:00', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 0);
```

### 範囲の確認、更新、再検索

```sql
SELECT COUNT(*), MIN(value), MAX(value)
  FROM ch5_correction
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time < TO_DATE('2026-01-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
UPDATE ch5_correction SET value = 25.0, status = 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time < TO_DATE('2026-01-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
SELECT name, time, value, status
  FROM ch5_correction ORDER BY name, time;
```

最初の検索は2件、最小値10.0、最大値99.0です。UPDATE後、TEMP-01の2行はvalue=25.0、
status=1となり、TEMP-02の20.0は維持されます。事前のCOUNTは対象をロックしないため、
同時入力がある作業では基準時刻と範囲を別途制御します。

### 複数タグとエラー処理

タグの選択には`=`、`IN`、`LIKE`を使用できます。広いパターンや長い時間範囲を変更する前に、
対象名と件数を確認し、小さな範囲に分割します。複数タグは順番に処理される場合があるため、
失敗時に文全体がアトミックに取り消されたと考えないでください。
変更済みの値と残りの対象を再検索してから再試行します。

連続する時間区間を`>= 開始 AND < 終了`で定義すると、境界行を重複処理しません。
1日全体を`23:59:59`までと指定すると、その後の小数秒データを取りこぼす可能性があります。
正確な許容条件とバインディングは[TAG UPDATE](../../reference/sql/syntax/dml-syntax/tag-data-update-syntax/)を
参照してください。

### ROLLUPの再構築

元データを変更しても計算済みのROLLUPは自動変更されません。上の実習で変更した区間を次のように
再構築し、[ROLLUPの再構築](../../tag-rollup-usage/rollup-rebuild/)の進行状況確認と
検索検証の手順に従います。

```sql
EXEC ROLLUP_REBUILD(ch5_correction, 'TEMP-01',
    TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-01-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS'));
```

<a id="design-correction-tag"></a>

## 元データの保持とNULLへの補正

元の値と補正値を別列に保存すると、最初の値を保持できます。補正値自体がNULLの場合もあるため、
`corrected_value IS NOT NULL`だけで補正の有無を判定せず、フラグを使用します。

```sql
CREATE TAG TABLE ch5_correction_overlay (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    raw_value DOUBLE,
    corrected_value DOUBLE,
    is_corrected SHORT
);
INSERT INTO ch5_correction_overlay VALUES
    ('TEMP-01', TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 99.0, NULL, 0);
UPDATE ch5_correction_overlay
   SET corrected_value = NULL, is_corrected = 1
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
SELECT name, raw_value, is_corrected,
       CASE WHEN is_corrected = 1 THEN corrected_value ELSE raw_value END AS effective_value
  FROM ch5_correction_overlay;
```

raw_valueは99.0、is_correctedは1、effective_valueはNULLです。フラグが0なら元の値を
使用します。この方法は検索式で値を選択し、raw_valueは変更しません。
デフォルトROLLUPがこのCASE式を自動集計したり、raw_valueの再構築だけで補正を反映したりすると
考えず、有効値を集計する別の検索・集計モデルを定めます。

## 補正履歴と検証

複数回の変更理由と担当者を残す場合は、別途履歴を記録します。

```sql
CREATE LOG TABLE ch5_correction_log (
    sensor_name VARCHAR(64),
    target_time DATETIME,
    old_value DOUBLE,
    new_value DOUBLE,
    reason VARCHAR(256),
    corrected_by VARCHAR(64)
);
```

TAGの更新とLOGへの履歴記録は、1つのTRANSACTIONトランザクションにはまとめられません。
実行順序・部分失敗・再試行時に同じ作業を識別する番号をアプリケーションで設計します。
テーブルを作成するだけで監査履歴が自動記録されるわけではありません。

訂正後に元の値・有効値、影響行数、区間統計、レポートを確認します。完了後は今回の実習で作成した
オブジェクトのみ削除します。以下のCASCADEはch5_correctionのROLLUPもまとめて削除します。

```sql
DROP TABLE ch5_correction CASCADE;
DROP TABLE ch5_correction_overlay;
DROP TABLE ch5_correction_log;
```

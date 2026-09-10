---
type: docs
title: '6.10 ROLLUP_REBUILD'
weight: 100
toc: true
aliases:
  - /dbms/tag-rollup-usage/delete-partial-rebuild-rollup/
---

ROLLUP_REBUILDは、元データの過去の値を補正した後に集計を再計算するプロシージャで、Standard Edition専用です。
FORCEとは異なり、影響を受けるバケットを削除・再作成します。
すべてのROLLUP定義を任意に再構築する汎用コマンドではありません。

## サポート対象の事前確認

| 対象 | 現在の対応 |
|---|---|
| WITH ROLLUPで作成した完全なSEC→MIN→HOUR階層 | 基本数値・拡張・ドキュメント全体JSONの処理 |
| 元データに接続されたサポート対象のCustomツリー | 1 SEC・1 MIN・1 HOURの間隔と、再構築境界に合うSELECTを確認 |
| 任意の名前・間隔で手動作成した通常のROLLUP | 自動階層と同じ対応を前提にしない |
| SECがないMIN/HOURだけの自動階層 | 完全な基本階層とは見なさない |
| 10 MINなど別の間隔のCustom | 現在の時間境界生成処理では未サポート |
| Cluster Edition | 未サポート |

CustomのSELECTが作るバケット、INTERVAL、基準タイムゾーンは、再構築境界と一致する必要があります。
未サポートのジョブがツリーに混在していないかを先に調べてください。
Customで作成できる式・間隔を、この関数ですべて再構築できるとは考えないでください。

## 時間引数とバケット境界

時刻文字列、または定数文字列を使用するTO_DATEを指定します。
一般的なDATETIME式全体を評価する処理ではないため、NOWの算術式やバインドパラメーターで例を作成しないでください。

開始時刻と終了時刻が属するバケットを両方含め、バケット全体に範囲を広げます。
1分段階で00:00:30～00:01:00を指定すると、00:00と00:01の2バケット、
つまり[00:00:00, 00:02:00)の範囲が再計算されます。
開始=終了でもその時刻のバケットを再計算し、開始が終了より大きい場合はエラーになります。
上位の時間段階では、さらに広いバケットに拡張されます。

## 基本階層とCustomの訂正実習

### 1. 準備と初回集計

```sql
CREATE TAG TABLE ch6_rebuild (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);
CREATE TAG TABLE ch6_rebuild_dst (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, sum_value DOUBLE, cnt LONG
);
CREATE ROLLUP ch6_rebuild_custom INTO (ch6_rebuild_dst)
AS (
    SELECT name, DATE_TRUNC('minute', time) AS time, SUM(value), COUNT(value)
      FROM ch6_rebuild GROUP BY name, time
) INTERVAL 1 MIN;

INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:00:00'), 1);
INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:00:30'), 200);
INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:01:00'), 300);
INSERT INTO ch6_rebuild VALUES ('S1', TO_DATE('2026-01-01 00:01:30'), 4);
EXEC TABLE_FLUSH(ch6_rebuild);

SELECT DISTINCT ROLLUP_NAME, INTERVAL_TIME FROM V$ROLLUP
 WHERE ROOT_TABLE = 'CH6_REBUILD' ORDER BY INTERVAL_TIME, ROLLUP_NAME;
ALTER ROLLUP _CH6_REBUILD_ROLLUP_SEC FORCE;
ALTER ROLLUP _CH6_REBUILD_ROLLUP_MIN FORCE;
ALTER ROLLUP _CH6_REBUILD_ROLLUP_HOUR FORCE;
ALTER ROLLUP ch6_rebuild_custom FORCE;
SELECT rollup('min', 1, time) AS bucket, AVG(value)
  FROM ch6_rebuild WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
```

制御コマンドの自動生成名が、上のV$ROLLUPの結果と一致することを確認してください。
他のオブジェクト名を推測して実行しないでください。最初の分平均は100.5と152です。

### 2. 元データの補正と再構築

```sql
UPDATE ch6_rebuild SET value = 20
 WHERE name = 'S1' AND time = TO_DATE('2026-01-01 00:00:30');
UPDATE ch6_rebuild SET value = 30
 WHERE name = 'S1' AND time = TO_DATE('2026-01-01 00:01:00');
EXEC ROLLUP_REBUILD(ch6_rebuild, 'S1',
    TO_DATE('2026-01-01 00:00:30'),
    TO_DATE('2026-01-01 00:01:00'));
```

### 3. 元データ・通常・Customの結果比較

```sql
SELECT DATE_TRUNC('minute', time) AS bucket, SUM(value), COUNT(value), AVG(value)
  FROM ch6_rebuild WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
SELECT rollup('min', 1, time) AS bucket, SUM(value), COUNT(value), AVG(value)
  FROM ch6_rebuild WHERE name = 'S1'
 GROUP BY bucket ORDER BY bucket;
SELECT time, SUM(sum_value), SUM(cnt), SUM(sum_value) / SUM(cnt)
  FROM ch6_rebuild_dst WHERE name = 'S1'
 GROUP BY time ORDER BY time;
SHOW ROLLUPGAP;
```

3つの結果は、00:00が合計21・件数2・平均10.5、00:01が合計34・件数2・平均17です。
終了時刻より後の00:01:30の値4も、同じバケットを再計算するときに含まれる必要があります。

## 運用への影響と障害復旧

関連ジョブは処理位置に追いついてから、停止・再計算・再開始されます。
元データを安定して検索するための内部処理も実行するため、「再構築中も通常処理がそのまま継続する」とは説明しません。
ユーザークエリと収集に許容できる遅延・停止時間を、先に検証環境で測定してください。

複数の段階が1つのアトミックなトランザクションとして取り消されるとは考えないでください。
失敗時の状態復旧はベストエフォートで実行されるため、実データとV$ROLLUPを確認します。
元の停止状態をそのまま復元する保証もありません。
再実行前に、サポート対象、元データの残存、再集計範囲を確認してください。

存在しないタグは、有効な再構築対象が準備された状況ではno-opになる場合があります。
成功応答だけで意図したタグを処理したと判断せず、実際の結果を比較してください。
元データが削除されている場合、元の統計は復元できません。

## クリーンアップ

```sql
DROP ROLLUP ch6_rebuild_custom;
DROP TABLE ch6_rebuild_dst;
DROP TABLE ch6_rebuild CASCADE;
```

Customの出力先は別途削除します。通常の定義自体を変更する必要がある場合や、このプロシージャの範囲外の場合は、
サポートされる新しい定義とデータ移行の手順を用意してください。
内部保存テーブルを任意に削除するSQLを、代替手順として提示しないでください。
正確な引数は[REBUILDリファレンス](../../reference/sql/syntax/rollup-rebuild-syntax/)を参照してください。

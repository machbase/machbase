---
type: docs
title: '7.10 _arrival_timeの時間モデル'
weight: 100
toc: true
---

元のログには昨日の時刻が記録されていても、クエリでは今日収集したデータとして扱われることがあります。
発生時刻と収集時刻を混同すると、正常に取り込まれたデータも欠落したように見えます。
LOGのクエリと保持ポリシーを設計するには、まずこの2つの時刻を区別します。

<a id="time-model-arrival-time"></a>

<a id="두-시각은-서로-다른-질문에-답합니다"></a>

## 発生時刻と到着時刻

`event_time`などのユーザー定義DATETIMEカラムは、イベントが発生した時刻を表します。
自動生成される`_arrival_time`は、LOGの時間範囲アクセスと保持期間に基づく削除の基準です。
省略するとサーバー時刻が使われますが、明示的な入力や時刻逆転の補正もあるため、
常に実際のネットワーク受信時刻を表すとは限りません。

DATETIMEはナノ秒単位の値を表現します。サーバーの時計が毎回ナノ秒精度で時刻を測定するという意味ではありません。
保存後にLOGテーブルのUPDATEで時刻を修正することもできません。

<a id="늦게-도착한-이벤트를-확인해-봅니다"></a>

## 遅延イベントの検索

次の例では、空の実習用テーブルに到着時刻を昇順で指定して挿入します。

```sql
CREATE LOG TABLE ch7_time (
    event_id   INTEGER,
    event_time DATETIME,
    message    VARCHAR(64)
);

INSERT INTO ch7_time(_arrival_time, event_id, event_time, message)
VALUES (TO_DATE('2026-01-02 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1,
        TO_DATE('2026-01-02 09:59:00', 'YYYY-MM-DD HH24:MI:SS'), 'normal arrival');
INSERT INTO ch7_time(_arrival_time, event_id, event_time, message)
VALUES (TO_DATE('2026-01-02 10:01:00', 'YYYY-MM-DD HH24:MI:SS'), 2,
        TO_DATE('2026-01-01 23:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'delayed arrival');

SELECT event_id
  FROM ch7_time
 WHERE event_time >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
   AND event_time <  TO_DATE('2026-01-02', 'YYYY-MM-DD')
 ORDER BY event_id;

SELECT event_id
  FROM ch7_time
 DURATION FROM TO_DATE('2026-01-02 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-02 10:01:00', 'YYYY-MM-DD HH24:MI:SS');
```

発生時刻による検索ではイベント2だけが、到着時刻による検索ではイベント1と2が選択されます。
遅れて到着したイベントの発生時刻を変更する必要はありません。

<a id="역전-입력은-그대로-저장되지-않을-수-있습니다"></a>

## 時刻逆転と補正

`DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE`は、直前の到着時刻より小さい値が入力された場合の処理を指定します。
現在のStandard実装の動作は次のとおりです。

| 値 | 時刻が逆転した入力の処理 |
|---|---|
| 1（デフォルト） | 直前に保存した`_arrival_time`より1ns大きい値に補正 |
| 0 | 時刻逆転エラーとして入力を拒否 |

同じ時刻は逆転に該当しないため、この規則だけで各行の時刻が一意になるわけではありません。
同時刻の行にも固定の順序が必要なら、イベント番号などの追加条件をORDER BYに指定してください。

次の任意の実習では、先ほどのテーブルを使います。
まず設定を確認し、値が1の検証環境でのみ実行してください。
この例のために本番サーバーの設定を変更しないでください。

```sql
SELECT NAME, VALUE FROM V$PROPERTY
 WHERE NAME = 'DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE';
```

```sql
-- 設定値1で実行します。値が0の場合は入力エラーが想定されます。
INSERT INTO ch7_time(_arrival_time, event_id, event_time, message)
VALUES (TO_DATE('2026-01-02 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3,
        TO_DATE('2026-01-02 08:59:00', 'YYYY-MM-DD HH24:MI:SS'), 'inverted arrival');

SELECT event_id,
       TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn') AS stored_time
  FROM ch7_time
 ORDER BY event_id;
```

設定値が1の場合、イベント3の保存時刻は入力した09:00ではなく、
`2026-01-02 10:01:00 000:000:001`になります。発生時刻は入力値のままです。
したがって、時刻逆転の「許可」は、過去の時刻を無条件に保持するという意味ではありません。

<a id="이관에서는-정렬과-대상-상태를-함께-확인하세요"></a>

## データ移行時の注意事項

元の`_arrival_time`を保持するには、空の移行先に昇順で入力することが基本です。
ソート済みでも、移行先により新しい時刻の行がある場合や、別の入力が割り込む場合は補正やエラーが発生し得ます。
同じテーブルで移行と通常のリアルタイム収集を混在させないでください。

`DURATION`は`event_time`ではなく`_arrival_time`を使用します。
タイムゾーンと日付書式を合わせても範囲が異なる場合は、クエリが参照する時間カラムを再確認してください。
境界と出力順序については、[クエリの実習](../query-analysis/)で説明します。

```sql
DROP TABLE ch7_time;
```

時刻に関する問題を問い合わせる際は、元の時刻、保存された時刻、設定値を用意してください。
3つを比較すると、変換と補正のどちらの段階で差が生じたかを判断しやすくなります。

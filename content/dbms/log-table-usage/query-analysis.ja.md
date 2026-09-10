---
type: docs
title: '7.5 クエリと分析'
weight: 50
toc: true
---

時間範囲を少し変えるだけでも検索件数は変わります。
特に日単位の集計では、終了時刻を両方の区間に含めると境界上の行が重複します。
この節では、固定時刻のデータで範囲と結果の順序を確認し、マスターデータを結合します。

<a id="original-85-select-data"></a>

<a id="경계에-걸리는-데이터를-준비합니다"></a>

## 実習データの準備

```sql
CREATE LOG TABLE ch7_query (
    event_id INTEGER,
    device   VARCHAR(32),
    value    DOUBLE
);

INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1, 'DEV-01', 10);
INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 'DEV-01', 20);
INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 'DEV-02', 30);
INSERT INTO ch7_query(_arrival_time, event_id, device, value)
VALUES (TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 4, 'DEV-02', 40);

SELECT _arrival_time, event_id, device, value
  FROM ch7_query
 ORDER BY _arrival_time, event_id;
```

結果はイベント1・2・3・4の順です。イベント2と3のように同時刻の行もあるため、
順序を固定するには、時刻に加えてイベント番号もソート条件に指定します。
この番号は例の中で明示的に管理する値で、LOGの自動的な一意キーではありません。

<a id="연속-구간에는-시작-포함끝-제외-조건이-편리합니다"></a>

## 連続区間と時間境界

```sql
SELECT event_id, value
  FROM ch7_query
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;
```

イベント1・2・3が選択されます。次の区間を12:00から始めると、イベント4はその区間でのみ集計されます。
`BETWEEN`は両端を含むため、このような連続区間とは意味が異なります。
ユーザー定義の`event_time`を基準に分析する場合も、同じWHEREパターンを使用できます。

<a id="original-85-select-time-data"></a>

<a id="duration은-log의-도착-시각을-사용합니다"></a>

## DURATIONによる検索

```sql
SELECT event_id FROM ch7_query
 DURATION 1 HOUR BEFORE TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;

SELECT event_id FROM ch7_query
 DURATION 1 HOUR AFTER TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;

SELECT event_id FROM ch7_query
 DURATION FROM TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;
```

| クエリ | 時間範囲 | 選択されるevent_id |
|---|---|---|
| 12:00以前の1時間 | 11:00～12:00、両端を含む | 2, 3, 4 |
| 10:00以後の1時間 | 10:00～11:00、両端を含む | 1, 2, 3 |
| 10:00から12:00まで | 両端を含む | 1, 2, 3, 4 |

`DURATION 1 HOUR`のように基準時刻を省略すると、現在時刻を基準にします。
そのため、過去の固定時刻を使う実習にそのまま適用すると、結果が得られない場合があります。
構文上の位置はWHEREの後、GROUP BY・ORDER BYの前です。

DURATIONがすべての時間カラムに適用される条件だと誤解しないでください。
DURATIONはLOG専用で、`_arrival_time`を使用します。
TAGの時間カラムやユーザー定義DATETIMEの条件はWHEREで指定してください。
詳細な構文は[相対時間・DURATIONリファレンス](/dbms/reference/sql/relative-time/#log-duration)を参照してください。

<a id="스캔-방향과-최종-정렬을-구분합니다"></a>

## スキャン方向とソート

DURATIONのBEFOREは新しい側から、AFTERは古い側から読み取る方向を指定します。
FROM … TOは、2つの時刻の順序によって方向が変わります。
次の例では、逆順の範囲と同時刻の境界を確認します。

```sql
SELECT event_id FROM ch7_query
 DURATION FROM TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id DESC;

SELECT event_id FROM ch7_query
 DURATION FROM TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
            TO TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;
```

最初の結果はイベント4・3・2・1、同じ時刻を指定した2番目の結果はイベント2・3です。
ここではスキャン方向とは別にORDER BYを明示し、出力順序を固定しています。

集計や結合を含む最終結果の順序が必要な場合は、ORDER BYを明示してください。
特にLIMITだけを指定して、どの行が返されるかを推測しないでください。

グローバル設定`TABLE_SCAN_DIRECTION`は他のクエリにも影響する場合があります。
画面の出力順序を変えるために、先にサーバー設定を変更しないでください。
[クエリチューニング](/dbms/performance-tuning/performance-query-tuning/)で実行計画を確認してから、必要なアクセス経路を調整してください。

<a id="original-85-simple-join"></a>

<a id="작은-lookup-테이블로-장치-설명을-붙입니다"></a>

## LOOKUPとの結合

```sql
CREATE LOOKUP TABLE ch7_query_device (
    device VARCHAR(32) PRIMARY KEY,
    label  VARCHAR(64)
);
INSERT INTO ch7_query_device VALUES ('DEV-01', 'Boiler');
INSERT INTO ch7_query_device VALUES ('DEV-02', 'Pump');

SELECT q.event_id, d.label, q.value
  FROM ch7_query q
  JOIN ch7_query_device d ON q.device = d.device
 WHERE q._arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND q._arrival_time <  TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY q.event_id;
```

結果は`(1, Boiler, 10)`、`(2, Boiler, 20)`、`(3, Pump, 30)`です。
LOGとLOOKUPを組み合わせるクエリのため、DURATIONの代わりにLOGカラムのWHERE範囲条件を使用します。
このINNER JOINでは、対応するマスターデータがないイベントは結果から除外される点も確認してください。

また、現在のLOOKUP値を結合しても、過去の機器説明が復元されるわけではありません。
履歴が必要なら、その時点の説明をイベントに保存するか、有効期間を持つ履歴を別途設計する必要があります。

```sql
DROP TABLE ch7_query_device;
DROP TABLE ch7_query;
```

検索件数が予想と異なる場合は、時間境界と結合前の件数を先に確認してください。
条件を1つずつ追加すると、どこで行が除外されるかを見つけやすくなります。

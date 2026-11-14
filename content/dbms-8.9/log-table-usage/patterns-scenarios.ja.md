---
type: docs
title: '7.9 活用パターンとシナリオ'
weight: 90
toc: true
---

実際の分析では、時刻、ホスト、重要度、メッセージを併せて確認します。
各機能を個別に試したら、「どのサーバーでどのエラーが増えたか」という問いに結び付けてみましょう。
この実習は、前の節のテーブルがなくても実行できます。

<a id="use-cases-log"></a>

<a id="먼저-원본-이벤트와-현재-상태를-구분합니다"></a>

## 元のイベントと現在の状態

LOGにはイベントが発生するたびに新しい行を追加します。
機器の現在の名前・場所などの変更可能なマスターデータはLOOKUPに分離できますが、
過去の状態も必要なら、その時点の値をイベントに記録するか、履歴を別途設計する必要があります。

セキュリティイベントや処理の追跡にも同じ方法を適用できます。
センサー名ごとの計測値の集計が中心ならTAG、業務行の更新やトランザクションが中心ならTRANSACTIONを先に検討してください。

<a id="storage-log-text-search-logs"></a>

<a id="분석할-로그와-인덱스를-준비합니다"></a>

## ログとインデックスの作成

実行日に依存せず時間条件を比較できるよう、到着時刻を明示します。
空のテーブルに昇順で入力する実習です。通常の収集では、元の発生時刻を別のDATETIMEカラムに保持することを推奨します。

```sql
CREATE LOG TABLE ch7_app (
    event_id INTEGER,
    host     VARCHAR(32),
    level    VARCHAR(16),
    message  TEXT
);
CREATE INDEX ch7_app_message ON ch7_app(message) INDEX_TYPE KEYWORD;

INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        1, 'web-01', 'INFO', 'service started');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:10:00', 'YYYY-MM-DD HH24:MI:SS'),
        2, 'web-01', 'WARN', 'slow response');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:20:00', 'YYYY-MM-DD HH24:MI:SS'),
        3, 'web-02', 'ERROR', 'database timeout');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 10:30:00', 'YYYY-MM-DD HH24:MI:SS'),
        4, 'web-02', 'ERROR', 'connection refused');
INSERT INTO ch7_app(_arrival_time, event_id, host, level, message)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        5, 'web-01', 'INFO', 'normal service');

EXEC TABLE_FLUSH(ch7_app);
EXEC INDEX_FLUSH(ch7_app);
SELECT COUNT(*) AS received_rows FROM ch7_app;
```

入力件数は5です。実習を繰り返す前に、最後のDROPまで実行したことを確認してください。
単純な再送は重複行につながる場合があります。

<a id="특정-오류를-찾고-같은-시간대의-상황을-봅니다"></a>

## エラーと時間帯による検索

```sql
SELECT event_id, host, message FROM ch7_app
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND message SEARCH 'timeout'
 ORDER BY event_id;

SELECT event_id, host, level, message FROM ch7_app
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND level = 'ERROR'
 ORDER BY event_id;
```

最初のクエリはweb-02のイベント3、2番目はイベント3と4を選択します。
特定の単語から検索を始め、分析では同じホスト・時間帯の他のエラーも確認する流れです。
検索範囲を広げるときは、時間条件をすべて外すのではなく、必要な区間だけを広げてください。

<a id="시간별등급별-건수를-비교합니다"></a>

## 時間別・重要度別の集計

```sql
SELECT TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24') AS event_hour,
       level, COUNT(*) AS event_count
  FROM ch7_app
 WHERE _arrival_time >= TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND _arrival_time <  TO_DATE('2026-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
 GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24'), level
 ORDER BY event_hour, level;
```

| event_hour | level | event_count |
|---|---|---|
| 2026-01-01 10 | ERROR | 2 |
| 2026-01-01 10 | INFO | 1 |
| 2026-01-01 10 | WARN | 1 |
| 2026-01-01 11 | INFO | 1 |

このクエリは元のLOGを読み取って集計します。TAGのROLLUPを自動的に使用するクエリではありません。
データが増えたら、検索区間と実行計画を確認し、事前集計が必要かを別途判断してください。

固定時刻のデータに`DURATION 1 HOUR`を適用しないよう注意してください。
この条件は現在時刻を基準にするため、実行日が変わるとサンプルが選択されない場合があります。
運用時の直近ログ検索と、再現用の固定時刻検索を区別してください。

<a id="수집과-보존을-연결합니다"></a>

## 収集と保持の管理

継続的な収集は[Append入力](../data-input-mutation/)を参照して構成できます。
長期運用では[保持ポリシー](../operations-lifecycle/)も定めてください。
元のログ、バックアップ、別途作成する集計データでは、必要な保持期間が異なる場合があります。

```sql
DROP TABLE ch7_app;
```

ここまでの結果が一致したら、実際のログ数件でフィールドとメッセージを置き換えてください。
収集全体を一度に移行するより、小さなサンプルで同じ問いに答えられるか確認すると、問題を見つけやすくなります。

---
type: docs
title: '16.1.4 相対時間式'
weight: 40
toc: true
---

相対時間式を使用すると、`NOW`や`SYSDATE`などの基準時点からの差をSQL文に直接記述できます。関数を別途呼び出さず、時系列ウィンドウを簡潔に表す場合に便利です。

> 相対時間リテラル（`now - 1h`形式）はMachbase 8.0.50以降でサポートします。月/年単位の調整には`ADD_TIME`、文字列の変換には`TO_DATE`を使用します。

## クイックリファレンス

| 式 | 例 | 説明 |
|------|------|------|
| `NOW` / `now` | `now` | 現在時刻（ナノ秒精度） |
| `SYSDATE` / `sysdate` | `sysdate` | 現在時刻（`NOW`と同じ） |
| `now - offset` | `now - 1h` | 現在時刻からオフセットを減算 |
| `now + offset` | `now + 30m` | 現在時刻にオフセットを加算 |
| ナノ秒整数の直接使用 | `value + 1000000000` | ナノ秒単位の整数をDATETIMEへ加算 |

## 相対時間単位（リテラルの接尾辞）

| 接尾辞 | 意味 | 例 |
|--------|------|------|
| `ns` | ナノ秒 | `500ns` |
| `us` | マイクロ秒 | `20us` |
| `ms` | ミリ秒 | `15ms` |
| `s` | 秒 | `45s` |
| `m` | 分 | `30m` |
| `h` | 時間 | `12h` |
| `d` | 日 | `7d` |
| `w` | 週 | `2w` (= 14日) |

> 月（`month`、`mo`）と年（`year`、`y`）の接尾辞は非対応です。暦上の月や年を移動するには
> `ADD_TIME()`を使用します。`30d`と`365d`は固定の日数のため、暦上の1か月・1年と常に一致するとは限りません。

## ADD_TIME関数

月・年など、相対時間リテラルにない暦の調整には`ADD_TIME()`を使用します。引数、形式、エラー条件は
[SQL関数辞典](../functions/functions-full/#add_time)を参照してください。

## TO_DATE関数

参照区間の開始と終了を日付文字列で指定するときは、`TO_DATE()`でDATETIME値を作成します。
日付形式と変換エラーは[SQL関数辞典](../functions/functions-full/#to_date)を参照してください。

## 利用パターン

### 時間区間の絞り込み

```sql
-- 直近1時間のデータ（相対時間リテラル）
SELECT * FROM sensor_tag WHERE time > now - 1h;

-- 直近1時間のデータ（ADD_TIME関数）
SELECT * FROM sensor_tag WHERE time > ADD_TIME(now, '0/0/0 -1:0:0');

-- 直近24時間の記録
SELECT * FROM app_log WHERE _arrival_time BETWEEN now - 1d AND now;

-- 直近10分以内のアラーム
SELECT alert_id, level, occurred_at FROM alert_log
 WHERE occurred_at >= sysdate - 10m;
```

### 複合時間式

```sql
-- 2日6時間15分後
SELECT * FROM maintenance_plan WHERE planned_at < now + 2d6h15m;

-- 秒未満の単位の組み合わせ
SELECT TO_CHAR(now + 3s125ms10us4ns, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn');
```

### TO_DATE結果へのオフセット適用

```sql
-- 日付文字列に3日を加算
SELECT TO_CHAR(TO_DATE('2024-05-01', 'YYYY-MM-DD') + 3d, 'YYYY-MM-DD');
-- 結果: 2024-05-04

-- 日付文字列から4時間15分を減算
SELECT TO_CHAR(
    TO_DATE('2024-05-01 08:00:00', 'YYYY-MM-DD HH24:MI:SS') - 4h15m,
    'YYYY-MM-DD HH24:MI:SS'
);
-- 結果: 2024-05-01 03:45:00
```

### ナノ秒整数の直接使用

数値リテラルはナノ秒として解釈します。

```sql
-- 1秒 = 1,000,000,000ナノ秒
SELECT event_time + 1000000000 AS event_time_plus_1s FROM events;

-- 250ナノ秒を減算
SELECT event_time - 250 AS event_time_minus_250ns FROM events;
```

## 制約

- 相対時間リテラル（`1h`、`30m`など）はMachbase 8.0.50以降でのみサポートします。
- 月（`mo`）と年（`y`）単位のリテラルは非対応です。`ADD_TIME()`の年/月の位置を使用してください。
- 文字列リテラルはinterval演算でDATETIMEへ暗黙変換されないため、先に`TO_DATE()`で変換してください。
- インターバル自体は`ORDER BY`句では使用できません。

## エラー処理

| 状況 | エラー | 対処方法 |
|------|------|-----------|
| 非対応の接尾辞(`1y`, `5mo`) | `ERR-02034` invalid time expression | 暦単位には`ADD_TIME()`、固定期間には`d`などの対応する接尾辞を使用 |
| 単位の省略(`now + 10`) | ナノ秒として解釈 | 意図する単位の接尾辞を明示 |
| 大きすぎる値(`1000000d`) | `ERR_OVERFLOW_INTERVAL` | 値の範囲を縮小 |

<a id="log-duration"></a>

## LOGのDURATION

相対時間リテラルとDURATIONは役割が異なります。`event_time >= now - 1h`は選択列のWHERE条件で、
DURATIONはLOGの`_arrival_time`範囲を指定します。TAGの時間列やユーザー定義DATETIME列にはWHERE条件を使用してください。

```text
SELECT ... FROM log_table
 [WHERE ...]
 DURATION n unit [BEFORE base_time | AFTER base_time]
 [GROUP BY ...] [HAVING ...] [ORDER BY ...] [LIMIT ...]

SELECT ... FROM log_table
 [WHERE ...]
 DURATION FROM from_time TO to_time
 [GROUP BY ...] [HAVING ...] [ORDER BY ...] [LIMIT ...]
```

上記は基本形式です。期間には`HOUR`、`MINUTE`、`DAY`などの単位を使用します。全範囲を表す`ALL`も使用できます。
DURATIONはWHEREの後、GROUP BY・ORDER BYの前に置きます。

| 形式 | 範囲 | 指定されるスキャン方向 |
|---|---|---|
| DURATION 1 HOUR | 現在時刻を基準とする直近1時間 | 新しい順 |
| DURATION 1 HOUR BEFORE t | t−1時間からtまで | 新しい順 |
| DURATION 1 HOUR AFTER t | tからt+1時間まで | 古い順 |
| DURATION FROM a TO b, a < b | aからbまで | 古い順 |
| DURATION FROM a TO b, a > b | bからaまで | 新しい順 |

範囲の両端を含みます。FROMとTOが同時刻なら、その時刻の行が対象です。スキャン方向と結合・集計後の
最終出力順は区別してください。結果順序が必要な場合はORDER BYを明示し、同時刻の複数行には追加のソートキーを指定します。

次の例では、終了時刻にある2番の行も選択されます。

```sql
CREATE LOG TABLE ch7_ref_duration (event_id INTEGER);
INSERT INTO ch7_ref_duration(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 1);
INSERT INTO ch7_ref_duration(_arrival_time, event_id)
VALUES (TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2);

SELECT event_id FROM ch7_ref_duration
 DURATION 1 HOUR BEFORE TO_DATE('2026-01-01 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
 ORDER BY event_id;

DROP TABLE ch7_ref_duration;
```

結果は1・2番です。連続する区間を日別に分ける場合、
`WHERE _arrival_time >= 開始 AND _arrival_time < 終了`のように半開区間を使用すると、境界行の二重集計を防げます。
LOGとLOOKUPが混在するクエリでは、DURATIONの代わりにLOG列のWHERE範囲を使用してください。

## 関連ドキュメント

- [LOG時間範囲の演習](/dbms/log-table-usage/query-analysis/) — 境界・ソート・結合結果の比較
- [相対時間式](/dbms-8.5/sql-reference/time-expressions/) — 8.5リファレンスの詳細

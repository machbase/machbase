---
title: '相対時間式'
type: docs
weight: 75
toc: true
---

## 概要 {#overview}

相対時間式は、基準時刻からのオフセットを SQL 内に直接記述します。補助関数なしで、最近のテレメトリーの抽出、将来の処理時刻の指定、時系列ウィンドウの調整ができます。

> **注意**：Machbase 8.0.50 以降でサポートされます。

## クイックスタート {#quick-start}

1. 直近 1 時間のレコードを検索：
   ```sql
   SELECT * FROM sensor_log WHERE event_time > now - 1h;
   ```
2. 2 日 6 時間後の時刻を計算：
   ```sql
   SELECT * FROM maintenance_plan WHERE planned_at < now + 2d6h;
   ```
3. 秒未満の精度で組み合わせ：
   ```sql
   SELECT to_char(now + 3s125ms10us4ns, 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn');
   ```

## 構文の概要 {#syntax-summary}

- `<数値><単位>` を空白なしで 1 つ以上連結します。
- 単位は小文字です。例：`2h30m`。
- 先頭に `+` または `-` を付けるか、`now - 90m`、`sample_time + 15s` のように計算します。
- 単位のない数値はナノ秒として扱います。
- 相対リテラルは `INTERVAL` です。`DATETIME` に加減算すると `DATETIME` になります。

## 対応する単位 {#supported-units}

| 接尾辞 | 意味 | 例 | 相当する時間 |
|--------|------------------|---------|---------------------|
| `ns` | ナノ秒 | `500ns` | 500 ナノ秒 |
| `us` | マイクロ秒 | `20us` | 0.00002 秒 |
| `ms` | ミリ秒 | `15ms` | 0.015 秒 |
| `s` | 秒 | `45s` | 45 秒 |
| `m` | 分 | `30m` | 30 分 |
| `h` | 時間 | `12h` | 12 時間 |
| `d` | 日 | `7d` | 7 日 |
| `w` | 週 | `2w` | 14 日 |

> **注意**：月と年は長さが一定でないため未サポートです。`1y`、`1mo` などは無効な時間式（`ERR-02034`）になります。

## 複合リテラルの作成 {#building-compound-literals}

- 読みやすくするため、大きい単位から記述します。例：`5d4h30m`。
- 0 の要素は省略します。`4h15m0s` より `4h15m` を推奨します。
- 順序を変えても指定できますが、統一すると誤りを減らせます。`1h30m` と `30m1h` は同じ間隔です。
- `'1d12h_30m'` のようなアンダースコア入りの値は、相対時間リテラルとして使用できません。複雑な間隔は `/* +1d12h30m */` のようなコメントや設定用の文字列で説明してください。

## 使用パターン {#usage-patterns}

### 時間範囲による抽出 {#filtering-windows-of-time}

```sql
-- 直近 24 時間のレコード
SELECT *
  FROM rtrollup
 WHERE time BETWEEN now - 1d AND now;

-- 直近 10 分のアラート
SELECT alert_id, level, occurred_at
  FROM alert_log
 WHERE occurred_at >= sysdate - 10m;
```

### 将来の処理時刻 {#scheduling-future-operations}

```sql
-- 現在から 1 日と 2 時間後までに予定されているタスク（営業日の判定は行わない）
SELECT job_id, scheduled_at
  FROM job_queue
 WHERE scheduled_at <= now + 1d2h;

-- 30 分後の保守予定を挿入
INSERT INTO device_schedule (device_id, maintenance_due)
VALUES ('device-001', now + 30m);
```

### 時刻による抽出と結合 {#time-based-filtering-and-joins}

```sql
-- 指定の時刻範囲で検索
SELECT device_id, ts, value
  FROM metrics_stream
 WHERE ts BETWEEN now - 15m AND now
   AND device_id = 'sensor-01';

-- 相対オフセットで 2 つの入力元を結合
SELECT a.ts, a.value AS raw_value, b.value AS calibrated
  FROM raw_metrics a
  JOIN calibration b
    ON b.ts BETWEEN a.ts - 500ms AND a.ts + 500ms;
```

### `DATETIME` と型変換 {#datetime-values-and-casting}

```sql
SELECT to_char(to_date('2024-05-01', 'YYYY-MM-DD') + 3d,
               'YYYY-MM-DD');                              -- 2024-05-04
SELECT to_char(to_date('2024-05-01 08:00:00',
                       'YYYY-MM-DD HH24:MI:SS') - 4h15m,
               'YYYY-MM-DD HH24:MI:SS');                   -- 2024-05-01 03:45:00
SELECT to_char(to_date('2024-05-01', 'YYYY-MM-DD') + 2h30m45s250ms,
               'YYYY-MM-DD HH24:MI:SS mmm');               -- 2024-05-01 02:30:45 250
```

文字列リテラルは、`INTERVAL` の演算で `DATETIME` に暗黙変換されません。
先に `TO_DATE` で変換してください。

### 単位のない数値との混在 {#mixing-with-plain-numbers}

```sql
-- 単位なしはナノ秒なので、正確に 1 秒を加算
SELECT event_time + 1000000000 AS event_time_plus_1s
  FROM events;

-- 250 ナノ秒を減算
SELECT event_time - 250 AS event_time_minus_250ns
  FROM events;
```

## 動作と制限 {#behaviour-and-limitations}

- 精度はナノ秒までです。64 ビットの範囲を超える値はオーバーフローします。
- 演算の優先順位は、括弧、乗除算、加減算の順です。複数の演算を組み合わせる場合は括弧を使用してください。
- 比較には結果の `DATETIME` を使用します。`INTERVAL` 単体は `ORDER BY` に指定できません。
- Standard Edition で利用できます。古いバージョンの対応状況はリリースノートを確認してください。

## エラー処理 {#error-handling}

| 状況 | エラー | 対処 |
|----------------------------------------|---------------------------|----------------------------------------------|
| 未対応の接尾辞（`1y`、`5mo`） | `ERR-02034`：無効な時間式 | `30d` など対応単位へ変更。 |
| 単位なし（`now + 10`） | ナノ秒として解釈 | 分や秒を意図するなら接尾辞を追加。 |
| オーバーフロー（`1000000d`） | `ERR_OVERFLOW_INTERVAL` | 値を減らすか、処理を反復に分割。 |
| 不正な文字（`1h3xm`） | 無効な時間式 | `1h3m` に修正。 |

## 推奨事項 {#best-practices}

- チーム内で小文字の単位に統一します。
- 頻用するオフセットを設定テーブルに保存し、再利用と監査に活用します。
- 複雑な式にはコメントを付け、保守しやすくします。例：`-- 営業日の 1 週間分を差し引く`。
- 動的にリテラルを作る場合は入力を検証し、未対応の単位が混入しないようにします。

## トラブルシューティング {#troubleshooting-checklist}

- **範囲が想定外**：`now` と計算した境界時刻の両方を表示して確認します。
- **単位の誤り**：数値だけならナノ秒です。秒、分、時間には `s`、`m`、`h` を追加します。
- **関数との併用**：ウィンドウ関数や集計フィルターと組み合わせる場合は、サブクエリーで評価し、文ごとに 1 回解決されるようにします。

## よくある質問 {#frequently-asked-questions}

- **`ADD_TIME` と併用できるか**：可能です。`ADD_TIME(now, '0/0/0 0:15:0') + 30s` のように使用します。
- **変数に格納できるか**：相対時間リテラルは実行時に評価され、変数には格納できません。繰り返し実行するクエリー内に直接記述できます。
- **営業日を差し引く方法**：相対リテラルは絶対的な経過時間を扱います。営業日の規則はアプリケーションまたはカレンダーテーブルで実装します。

## 早見表 {#reference-cheat-sheet}

```
式               意味
--------------  --------------------------------------------
now - 5m        正確に 5 分前の時刻
sysdate + 1d    翌日（システム時刻から 24 時間後）
col_ts + 90s    列の時刻を 90 秒進める
TO_DATE('2024-01-01','YYYY-MM-DD') + 2w  14 日を加算
value + 250     value に 250 ナノ秒を加算
```

相対時間式は、補助関数なしで正確で読みやすい日時演算を表します。`WHERE`、計算列、選択リスト、手続きコードなど、式を使用できる箇所で利用すると、分析 SQL を簡潔に保てます。

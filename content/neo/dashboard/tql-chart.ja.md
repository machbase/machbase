---
title: TQL チャート
type: docs
weight: 50
toc: true
---

## 概要

チャートタイプで **Tql chart** を選択すると、作成した TQL ファイルをダッシュボードのパネルとして使用できます。

{{< media slug="neo-dashboard/type-tql-chart" width="600" >}}

- **Tql path**: 使用する TQL ファイルを選択します。`Select file` で選ぶか、`Open file` でエディターを開きます。
- **Params**: TQL ファイルに渡すパラメーターを登録します。値を直接入力するか、ダッシュボードが提供する変数を使用できます。
- **Theme**: テーマは TQL ファイル内の `CHART( theme("...") )` で指定します。使用できるテーマ名は右側のパネルに表示されます。

SINK が `CHART` の TQL が一般的ですが、表（CSV）、Markdown、HTML、NDJSON、プレーンテキストを出力する TQL もパネルにそのまま表示されます。ただし、`CHART` 以外の出力を表示するパネルには自動更新（ダッシュボード・パネルの周期とも）が適用されず、更新ボタンを押すか時間範囲を変更したときに再検索します。

## 組み込み変数

**Time range** — ダッシュボードの他のパネルと時刻を合わせるために使用します。

| パラメーター | 説明 |
|:--|:--|
| {{from_str}} | 日時文字列（YYYY-MM-DD HH:MI:SS） |
| {{from_s}},{{from_ms}},{{from_us}},{{from_ns}} | UNIX タイムスタンプ（秒・ミリ秒・マイクロ秒・ナノ秒） |
| {{to_str}} | 日時文字列（YYYY-MM-DD HH:MI:SS） |
| {{to_s}},{{to_ms}},{{to_us}},{{to_ns}} | UNIX タイムスタンプ（秒・ミリ秒・マイクロ秒・ナノ秒） |

**period** — 時間範囲とパネルサイズから計算する X 軸の間隔です。

| パラメーター | 説明 |
|:--|:--|
| {{period}} | 期間表現（例: 10s） |
| {{period_value}} | 期間の値（例: 10） |
| {{period_unit}} | 期間の単位（例: sec） |

## TQL ファイルでのパラメーターの使用

TQL ファイル内では `param()` でダッシュボードから渡された値を受け取ります。

```sql
SQL(strSprintf(`
SELECT date_trunc('%s', TIME, %1.0f) as TIME, avg(VALUE) as VALUE
FROM EXAMPLE
WHERE TIME between FROM_UNIXTIME(%1.0f) and FROM_UNIXTIME(%1.0f) AND NAME IN ('%s')
GROUP BY TIME ORDER BY TIME`, 
(param('period_unit') ?? 'msec'), 
parseFloat(param('period_value') ?? 10), 
parseFloat(param('from') ?? 1703055573), 
parseFloat(param('to') ?? 1703055583),
(param('tag') ?? 'tag01')
))

CHART_LINE()
```

**SQL()** — `param()` と `strSprintf()` でクエリを動的に生成します。主なパラメーターは `period_unit`（デフォルト `msec`）、`period_value`（デフォルト 10）、`from`・`to`（検索期間）、`tag`（検索するタグ、デフォルト `tag01`）です。

**CHART_LINE()** — クエリ結果を折れ線チャートで描画します。

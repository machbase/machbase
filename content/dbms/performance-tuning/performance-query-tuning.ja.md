---
type: docs
title: '12.5 クエリと分析の性能調整'
weight: 50
toc: true
aliases:
  - /dbms/performance-tuning/query-analysis/
---

結果の正確さを維持しながら、読み出す行・パーティションとソート・集計の処理量を減らします。
変更前後は同じデータ、条件、同時実行数で、実行時間と結果件数を比較します。

## 基本原則

1. TAG・LOG のクエリは、必要な時間範囲を先に限定します。
2. 必要な列だけを選び、無制限の `SELECT *` を避けます。
3. 頻出する等価・範囲条件や JOIN キーに適したインデックスを検討します。
4. 繰り返す長期間の TAG 集計には ROLLUP を使用します。
5. ヒントや設定を変える前に `EXPLAIN` で実行計画を確認します。
6. 平均だけでなく遅延分布、読み出し行数、CPU・I/O、同時クエリへの影響を記録します。

## 検証用の例

次の例では LOG テーブルとインデックスを作成し、実行計画と結果を確認してから削除します。

```sql
CREATE LOG TABLE perf_event_demo (
    device_id VARCHAR(32),
    level     VARCHAR(16),
    code      INTEGER,
    message   VARCHAR(100)
);

CREATE INDEX idx_perf_event_code
ON perf_event_demo(code) INDEX_TYPE LSM;

INSERT INTO perf_event_demo VALUES ('DEV-01', 'WARN', 1001, 'temperature high');
INSERT INTO perf_event_demo VALUES ('DEV-02', 'INFO', 1000, 'started');
EXEC TABLE_FLUSH(perf_event_demo);

EXPLAIN
SELECT device_id, level, message
FROM perf_event_demo
WHERE code = 1001
  AND _ARRIVAL_TIME >= NOW - 60000000000;

SELECT device_id, level, message
FROM perf_event_demo
WHERE code = 1001
  AND _ARRIVAL_TIME >= NOW - 60000000000;

DROP TABLE perf_event_demo;
```

少量のサンプルから、インデックススキャンが常に速いと結論付けないでください。運用に近いデータ分布と
条件の選択性で、作成前後を比較します。

<a id="performance-tuning-select"></a>
<a id="select-join-optimizer"></a>

## SELECT と JOIN

- 大きな元テーブルは時間・キー条件で先に絞り込みます。
- JOIN 条件の両側で型と長さを合わせます。
- WHERE の列を関数で包み、インデックス範囲を使えなくしていないか確認します。
- outer JOIN を inner JOIN に変える前に、NULL で補完された行が失われないか比較します。
- 結果順序が必要なら `ORDER BY` を明示します。
- ページ分割では、大きな OFFSET より業務キー・時刻による継続読み出しを検討します。

オプティマイザーが SQL に書かれたテーブル順序に従うとは限りません。結合順序を強制するヒントは、
統計やデータ分布の変化で逆効果になる場合があるため、実行計画と結果を併せて検証します。

## EXPLAIN の利用

`EXPLAIN` はクエリを実行せずに計画を表示します。`EXPLAIN FULL` は実行を伴う場合があるため、
運用負荷のない限定的な環境で使用します。

実行計画では次を確認します。

| 項目 | 確認する問い |
|------|------|
| 対象テーブル | 意図したテーブルとビューが選ばれているか |
| スキャン方式 | 条件とインデックスに適したアクセス経路か |
| 時間範囲 | TAG・LOG のパーティション範囲が限定されるか |
| JOIN | 大きな入力に対して不要な結合が行われていないか |
| ソート・集計 | 大きな中間結果をソート・マテリアライズしていないか |

バージョンで変わり得る内部オブジェクト ID や実行計画全体の文字列を自動検査の固定値にしないでください。
テーブル名、スキャン方式、主要条件など、意味が安定した要素を検査します。

<a id="performance-cte"></a>

## CTE

CTE は複雑なクエリを読みやすくしますが、自動的に性能を改善するわけではありません。同じ CTE の再評価、
CTE 内へのフィルター適用、大きな中間結果の生成を実行計画で確認します。Machbase 8.7.0 は
Standard Edition で非再帰 SELECT CTE をサポートし、再帰 CTE はサポートしません。

構文と例は [CTE](/dbms/reference/sql/syntax/cte-syntax/)を参照してください。

<a id="performance-operators-tuning"></a>

## 検索演算子

| 条件 | 確認事項 |
|------|------|
| 等価・範囲比較 | 列の型とインデックスタイプが適合するか |
| `LIKE 'prefix%'` | 前方一致検索と文字列インデックスを利用するか |
| 先頭ワイルドカード | 全体スキャンのコストを許容できるか |
| `SEARCH`・`ESEARCH` | KEYWORD インデックスと構文が適合するか |
| `REGEXP` | 時間条件や他のインデックス条件で先に候補行を絞ったか |
| JSON パス | テーブルタイプと JSON インデックスの対応を確認したか |
| IP 範囲 | IPV4・IPV6 型とインデックスの対応を確認したか |

条件の正確な意味とインデックス利用条件は
[SEARCH・ESEARCH・REGEXP](/dbms/reference/sql/syntax/search-esearch-regexp-syntax/)と
[JSON 演算子](/dbms/reference/sql/functions/operators-json/)を参照してください。

<a id="performance-window-functions-considerations-pivot"></a>

<a id="window-function과-pivot"></a>

## ウィンドウ関数と PIVOT

ウィンドウのパーティションやソートキーが大きいと、ソート・メモリコストが増えることがあります。
まず時間と業務キーで入力を絞り、同じウィンドウを重複計算していないか確認します。
PIVOT は出力カテゴリ数を限定し、想定外カテゴリの処理方法を決めます。

構文は[ウィンドウ関数](/dbms/reference/sql/syntax/window-function-over-syntax/)と
[PIVOT](/dbms/reference/sql/syntax/pivot-syntax/)を参照してください。

## 変更前後のチェックリスト

- 結果行数と NULL 分布が同じか。
- 同じ時間範囲とタイムゾーンを使っているか。
- コールド・ウォームキャッシュを区別したか。
- 単独実行だけでなく同時クエリでも比較したか。
- 入力スループットやメモリへの副作用がないか。
- ロールバック用の DDL・設定値と基準測定値を記録したか。

<a id="관련-sql-정본"></a>

## 関連 SQL 文書

| トピック | 詳細文書 |
|---|---|
| SELECT・時間条件 | [SELECT 構文](/dbms/reference/sql/syntax/select-syntax/) |
| VIEW・CTE・集合演算 | [SQL 構文リファレンス](/dbms/reference/sql/syntax/) |
| ヒント | [SELECT ヒント](/dbms/reference/sql/syntax/select-hint-syntax/) |
| 関数・集計 | [関数リファレンス](/dbms/reference/sql/functions/) |

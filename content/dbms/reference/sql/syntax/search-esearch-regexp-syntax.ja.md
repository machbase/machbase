---
type: docs
title: 'SEARCH / ESEARCH / REGEXP'
weight: 50
toc: true
---

検索演算子は構文が似ていても検査対象が異なります。SEARCH・ESEARCHはKEYWORDインデックスの
トークンを使用し、LIKE・REGEXPは元のテキストに対して条件を評価します。
性能のために演算子を変更する前に、結果の意味が同じであることを確認してください。

## SEARCH

```text
column_name SEARCH 'search_term'
column_name NOT SEARCH 'search_term'
```

LOGのVARCHAR・TEXT列にKEYWORDインデックスが必要です。複数の単語はANDの意味で検索し、語順や
隣接性を保証するフレーズ検索ではありません。デフォルトモードでは一般的なASCII単語を小文字に正規化し、
ハングルなどは2-gramに分割します。すべての言語の形態素解析やUnicodeの大文字小文字処理を保証する機能ではありません。

次の独立した演習用テーブルを、このページ全体で使用します。

```sql
CREATE LOG TABLE ch7_ref_search (
    event_id INTEGER,
    message  VARCHAR(200),
    detail   VARCHAR(200)
);
CREATE INDEX ch7_ref_msg ON ch7_ref_search(message) INDEX_TYPE KEYWORD;
CREATE INDEX ch7_ref_detail ON ch7_ref_search(detail) INDEX_TYPE KEYWORD;
INSERT INTO ch7_ref_search VALUES (1, 'ERROR timeout occurred', 'connection reset');
INSERT INTO ch7_ref_search VALUES (2, 'pretimeout normal', 'port 8080');
INSERT INTO ch7_ref_search VALUES (3, NULL, NULL);
EXEC TABLE_FLUSH(ch7_ref_search);
EXEC INDEX_FLUSH(ch7_ref_search);

SELECT event_id FROM ch7_ref_search WHERE message SEARCH 'timeout' ORDER BY event_id;
SELECT event_id FROM ch7_ref_search
 WHERE message SEARCH 'error' AND detail SEARCH 'reset'
 ORDER BY event_id;
SELECT event_id FROM ch7_ref_search WHERE message NOT SEARCH 'timeout' ORDER BY event_id;
```

最初の2つのクエリは1番、最後のクエリは2番を選択します。NOT SEARCHはmessageがNULLの3番を含みません。
複数列を検索する場合は、各対象列に必要なインデックスを作成してください。

## ESEARCH

```text
column_name ESEARCH 'pattern%'
column_name ESEARCH '%pattern%'
```

インデックス化された単語にパターンを適用します。`pattern%`は単語の接頭辞、`%pattern%`は単語内の部分パターンです。
`%`が元テキスト全体の単語境界を自由に越えると解釈しないでください。次の例はASCIIキーワードパターンを使用します。

```sql
SELECT event_id FROM ch7_ref_search WHERE message ESEARCH 'time%' ORDER BY event_id;
SELECT event_id FROM ch7_ref_search WHERE message ESEARCH '%time%' ORDER BY event_id;
```

結果はそれぞれ1番、1・2番です。現在のESEARCHのASCIIパターン比較は大文字小文字を区別しません。
元テキストのLIKEを完全に代替する機能ではなく、パターンに一致するトークン数・行数によってコストが変わります。

`NOT ESEARCH`構文は非対応です。NOT SEARCH・NOT LIKEへ変更すると除外する行も変わる場合があるため、
結果とNULL処理を確認してください。

## LIKEとの比較

```sql
SELECT event_id FROM ch7_ref_search WHERE message LIKE '%TIMEOUT%' ORDER BY event_id;
SELECT event_id FROM ch7_ref_search WHERE message NOT LIKE '%timeout%' ORDER BY event_id;
```

最初のクエリは1・2番、2つ目は0件です。NULL行はNOT LIKEにも含まれません。
LIKEは現在のASCII比較では大文字小文字を区別しません。`%`は0文字以上、`_`は1文字を表します。

LIKE自体はKEYWORDインデックスを使用しません。ただし、常にテーブルのフルスキャンになるとは限りません。
時刻条件や他のインデックス条件によって先に対象行が制限される場合があります。

## REGEXP

```text
column_name REGEXP 'pattern'
column_name NOT REGEXP 'pattern'
```

正規表現パターンに一致する部分を検査します。デフォルトでは大文字小文字を区別します。
先頭・末尾を制限するには`^`・`$`を使用してください。

```sql
SELECT event_id FROM ch7_ref_search
 WHERE message REGEXP '^ERROR.*timeout'
 ORDER BY event_id;
SELECT event_id FROM ch7_ref_search
 WHERE message NOT REGEXP 'timeout'
 ORDER BY event_id;
```

最初のクエリは1番、2つ目は0件です。REGEXPはKEYWORDインデックスを直接使用しません。
SEARCHで先に対象を絞る場合は、その条件で必要な結果を除外しないことを確認してください。

### 関数形式のREGEXP

スカラー式でもREGEXP結果を使用できます。

```sql
SELECT 'abcde' REGEXP 'a[bcd]{1,10}e' FROM dual;
```

結果は1です。関数形式のREGEXP_LIKEは比較オプションも受け取ります。現在、関数の入力はVARCHAR、
パターンとオプションは定数のVARCHARである必要があります。TEXT列を受け取るREGEXP演算子と
入力型の制約が同じであると仮定しないでください。

```sql
SELECT event_id,
       REGEXP_LIKE(message, 'error') AS case_sensitive,
       REGEXP_LIKE(message, 'error', 'i') AS case_insensitive
  FROM ch7_ref_search
 WHERE event_id IN (1, 3)
 ORDER BY event_id;
```

1番の結果は0・1、3番はNULL・NULLです。`i`は大文字小文字を区別せず、`c`は区別します。
オプションを省略すると区別します。

## 性能上の推奨事項

| 目的 | 選択基準 |
|---|---|
| 単語の存在確認 | SEARCH |
| インデックス化された単語の接頭辞・部分パターン | ESEARCH |
| 元テキストの部分パターン | LIKE |
| 元テキストの形式・位置・複雑なパターン | REGEXP・REGEXP_LIKE |

インデックスの存在と構築完了は区別し、同じデータと時間範囲で比較してください。
演習が終わったらテーブルを削除します。

```sql
DROP TABLE ch7_ref_search;
```

## 関連ドキュメント

- [テキスト検索の演習](/dbms/log-table-usage/text-search-keyword-index/) — 複数単語・ハングル・NULL・TEXTの制約
- [INDEX構文](../index-syntax/) — KEYWORDインデックスの作成

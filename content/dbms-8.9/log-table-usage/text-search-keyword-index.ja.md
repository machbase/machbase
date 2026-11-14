---
type: docs
title: '7.11 テキスト検索とKEYWORDインデックス'
weight: 110
toc: true
---

メッセージに同じ文字が含まれていても、SEARCHとLIKEの結果は異なる場合があります。
SEARCHは索引化された単語を検索し、LIKEは元の文字列にパターンを適用するためです。
性能を比較する前に、どの行を検索するかを明確にします。

<a id="text-search"></a>
<a id="original-85-text-search"></a>
<a id="design-text-search"></a>

<a id="서로-다른-검색-결과를-만드는-표본을-준비합니다"></a>

## 検索データの準備

```sql
CREATE LOG TABLE ch7_search (
    event_id INTEGER,
    message  TEXT
);
CREATE INDEX ch7_search_msg ON ch7_search(message) INDEX_TYPE KEYWORD;

INSERT INTO ch7_search VALUES (1, 'ERROR connection timeout');
INSERT INTO ch7_search VALUES (2, 'connection slowly refused');
INSERT INTO ch7_search VALUES (3, 'pretimeout marker');
INSERT INTO ch7_search VALUES (4, 'normal service');
INSERT INTO ch7_search VALUES (5, NULL);
INSERT INTO ch7_search VALUES (6, '대한민국 연결 오류');
INSERT INTO ch7_search VALUES (7, 'ERR-1001 network');
INSERT INTO ch7_search VALUES (8, 'timeout refused connection');

EXEC TABLE_FLUSH(ch7_search);
EXEC INDEX_FLUSH(ch7_search);
```

サンプルの`event_id`で結果を比較します。メッセージはTEXTなので、ソート基準には使用しません。
LOGのVARCHARでも同じKEYWORD検索を使用できます。

<a id="search-not"></a>
<a id="text-search-search-not"></a>

<a id="search는-단어를-찾습니다"></a>

## SEARCHとNOT SEARCH

```sql
SELECT event_id FROM ch7_search WHERE message SEARCH 'timeout' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message SEARCH 'connection refused' ORDER BY event_id;
SELECT event_id FROM ch7_search
 WHERE message SEARCH 'connection' AND message SEARCH 'refused'
 ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message NOT SEARCH 'timeout' ORDER BY event_id;
```

| 条件 | 選択されるevent_id | 理由 |
|---|---|---|
| SEARCH 'timeout' | 1, 8 | pretimeoutは別の単語 |
| SEARCH 'connection refused' | 2, 8 | 両方の単語が存在する |
| 2つのSEARCH条件をANDで結合 | 2, 8 | 同じメッセージ内の両方の単語を確認 |
| NOT SEARCH 'timeout' | 2, 3, 4, 6, 7 | 対象の単語がなく、NULL行は除外 |

複数単語のSEARCHは、語順や隣接性を保証するフレーズ検索ではありません。
イベント2には間に別の単語があり、イベント8は逆順ですが、両方とも選択されます。
他のカラムにもSEARCHを使用するには、そのカラムにも対応するインデックスが必要です。

デフォルトのトークン化では、通常のASCII単語は小文字に正規化されます。
例えば、イベント1の`ERROR`は`SEARCH 'error'`でも検索されます。
これをすべてのUnicode文字に対する言語別の大文字・小文字処理と解釈しないでください。

<a id="한글은-토큰-분리-방식을-이해하면-편합니다"></a>

### 韓国語のトークン分割

```sql
SELECT event_id FROM ch7_search WHERE message SEARCH '대한' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message SEARCH '연결' ORDER BY event_id;
```

どちらもイベント6が選択されます。デフォルトモードでは、`대한민국`は`대한`、`한민`、`민국`のような
重複する2-gramとして索引化されます。形態素や文の意味を理解する検索ではありません。
空白・句読点・1文字の値・英語と韓国語の混在値ではトークン境界が変わる場合があるため、実際のサンプルで確認してください。
MODEなどのインデックスオプションを変更すると、トークン化も変わる場合があります。

<a id="esearch"></a>
<a id="text-search-esearch"></a>

<a id="esearch는-색인된-단어에-패턴을-적용합니다"></a>

## ESEARCHによる拡張検索

```sql
SELECT event_id FROM ch7_search WHERE message ESEARCH 'time%' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message ESEARCH '%time%' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message ESEARCH 'err%' ORDER BY event_id;
```

| パターン | 選択されるevent_id | 意味 |
|---|---|---|
| time% | 1, 8 | timeで始まる単語 |
| %time% | 1, 3, 8 | timeを含む単語 |
| err% | 1, 7 | errorやerrのようにerrで始まる単語 |

`time%`は単語の途中にあるtimeまで検索するものではありません。
また、ESEARCHは原文全体にLIKEを適用することと同じではありません。
空白や句読点をまたぐ原文パターンを、そのままESEARCHに移さないでください。
複雑な複数条件は、個別のSEARCH・ESEARCH条件をAND・ORで結合し、意味を明示してください。

現在の比較処理では、ESEARCHはASCIIの大文字と小文字を区別しません。
対象キーワードが広く一致するほど検索コストも増えるため、常にLIKEより高速とは限りません。
この例はASCIIキーワードのパターンを対象としています。

`NOT ESEARCH`構文はサポートしていません。`NOT SEARCH`や`NOT LIKE`に変更すると、検索の意味も変わります。
除外する行を再定義し、NULLの扱いまで確認してください。

<a id="like-not"></a>
<a id="text-search-like-not"></a>

<a id="like는-원문-문자열의-패턴을-검사합니다"></a>

## LIKEとNOT LIKE

```sql
SELECT event_id FROM ch7_search WHERE message LIKE '%TIMEOUT%' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message LIKE 'ERR-____' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message NOT LIKE '%timeout%' ORDER BY event_id;
```

最初のクエリはイベント1・3・8、2番目は0件、3番目はイベント2・4・6・7を返します。
イベント7のメッセージは`ERR-1001`の後にも文字列があるため、全体パターン`ERR-____`に一致しません。
`%`は0文字以上、`_`は1文字を表します。
リテラルの`%`・`_`・バックスラッシュを検索する場合は、バックスラッシュのエスケープ規則も確認してください。

LIKEも現在のASCII比較では大文字と小文字を区別しません。
KEYWORDインデックスは使用しませんが、WHEREの他の条件や時間範囲で検査する行を減らせます。
したがって、LIKEがあるという理由だけで常にテーブル全体を読むと説明するのも正確ではありません。

<a id="regex"></a>
<a id="regexp-not"></a>
<a id="regex-regexp-not"></a>

<a id="정규식은-형식과-위치를-검사할-때-사용합니다"></a>

## REGEXPとREGEXP_LIKE

```sql
SELECT event_id FROM ch7_search
 WHERE message REGEXP '^ERR-[0-9]+'
 ORDER BY event_id;

SELECT event_id FROM ch7_search
 WHERE message NOT REGEXP 'timeout'
 ORDER BY event_id;
```

最初のクエリはイベント7、2番目はイベント2・4・6・7を返します。
REGEXPは正規表現パターンに一致する部分があるかを検査します。
文字列の先頭や末尾を制限するには、`^`・`$`を明示してください。

<a id="regexp-like"></a>
<a id="regex-regexp-like"></a>

関数として使用する場合は`REGEXP_LIKE`を使用します。
現在、この関数の入力はVARCHARである必要があり、パターンとオプションも定数VARCHARである必要があります。
先ほどのTEXTカラムをそのまま渡すと型エラーになるため、別のサンプルを用意します。

```sql
CREATE LOG TABLE ch7_regexp_fn (event_id INTEGER, message VARCHAR(200));
INSERT INTO ch7_regexp_fn VALUES (1, 'ERROR connection timeout');
INSERT INTO ch7_regexp_fn VALUES (5, NULL);

SELECT event_id,
       REGEXP_LIKE(message, 'error') AS case_sensitive,
       REGEXP_LIKE(message, 'error', 'i') AS case_insensitive
  FROM ch7_regexp_fn
 WHERE event_id IN (1, 5)
 ORDER BY event_id;
```

イベント1の結果はそれぞれ0・1、メッセージがNULLのイベント5は両方ともNULLです。
デフォルトの正規表現比較は大文字と小文字を区別し、`i`オプションは区別しない比較です。
区別する比較を明示するには`c`を使用できます。

正規表現はKEYWORDインデックスで直接処理されません。
時間条件やSEARCHで対象を絞れますが、先行条件で必要な行を除外すると、後続の正規表現でその行を取り戻すことはできません。

<a id="저장-타입과-검색-성능을-혼동하지-마세요"></a>

## TEXTの制約と検索性能

TEXTは最大64MiBの原文を格納できますが、TEXT自体のORDER BY・GROUP BYはサポートしていません。
ソート・集計するデバイス・エラーコード・重要度は別カラムに格納してください。
同じデータでインデックスの有無、構築状態、検索範囲を確認してから性能を比較します。

```sql
DROP TABLE ch7_regexp_fn;
DROP TABLE ch7_search;
```

検索結果が異なる場合は、元の1行と使用したパターンを併せて確認してください。
単語を探すのか、原文の一部を探すのかを区別するだけで解決する場合も多くあります。

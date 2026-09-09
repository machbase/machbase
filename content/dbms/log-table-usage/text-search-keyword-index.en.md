---
type: docs
title: '7.11 Text Search and KEYWORD Index'
weight: 110
toc: true
---

SEARCH and LIKE can return different results even when messages contain the same characters. SEARCH
finds indexed words; LIKE applies a pattern to the raw string. Before comparing performance,
establish which rows each query should find.

<a id="text-search"></a>
<a id="original-85-text-search"></a>
<a id="design-text-search"></a>

<a id="서로-다른-검색-결과를-만드는-표본을-준비합니다"></a>

## Prepare Search Data

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

Compare results by the sample `event_id` values. The message column is TEXT and is not used for
sorting. The same KEYWORD search is available for LOG VARCHAR columns.

<a id="search-not"></a>
<a id="text-search-search-not"></a>

<a id="search는-단어를-찾습니다"></a>

## SEARCH and NOT SEARCH

```sql
SELECT event_id FROM ch7_search WHERE message SEARCH 'timeout' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message SEARCH 'connection refused' ORDER BY event_id;
SELECT event_id FROM ch7_search
 WHERE message SEARCH 'connection' AND message SEARCH 'refused'
 ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message NOT SEARCH 'timeout' ORDER BY event_id;
```

| Predicate | Selected event_id values | Reason |
|---|---|---|
| SEARCH 'timeout' | 1, 8 | pretimeout is a separate word |
| SEARCH 'connection refused' | 2, 8 | Both words are present |
| Two SEARCH predicates combined with AND | 2, 8 | Both words are checked in the same message |
| NOT SEARCH 'timeout' | 2, 3, 4, 6, 7 | The word is absent; NULL rows are excluded |

Multiword SEARCH is not phrase search: it does not guarantee word order or adjacency. Row 2 has an
intervening word and row 8 reverses the order, but both match. To SEARCH another column, that column
also needs the corresponding index.

Default tokenization normalizes ordinary ASCII words to lowercase. For example, `ERROR` in row 1
also matches `SEARCH 'error'`. Do not generalize this behavior to language-specific case handling
for all Unicode characters.

<a id="한글은-토큰-분리-방식을-이해하면-편합니다"></a>

### Korean Tokenization

```sql
SELECT event_id FROM ch7_search WHERE message SEARCH '대한' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message SEARCH '연결' ORDER BY event_id;
```

Both queries select row 6. In the default mode, `대한민국` is indexed as overlapping 2-grams such as
`대한`, `한민`, and `민국`. This is not morphological or semantic analysis. Test real samples because
spaces, punctuation, single characters, and mixed English/Korean values can affect token boundaries.
Index options such as MODE can also change tokenization.

<a id="esearch"></a>
<a id="text-search-esearch"></a>

<a id="esearch는-색인된-단어에-패턴을-적용합니다"></a>

## ESEARCH Extended Search

```sql
SELECT event_id FROM ch7_search WHERE message ESEARCH 'time%' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message ESEARCH '%time%' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message ESEARCH 'err%' ORDER BY event_id;
```

| Pattern | Selected event_id values | Meaning |
|---|---|---|
| time% | 1, 8 | Words starting with time |
| %time% | 1, 3, 8 | Words containing time |
| err% | 1, 7 | Words starting with err, such as error or err |

`time%` does not match time in the middle of a word. ESEARCH is also not equivalent to applying LIKE
to the entire raw string. Do not transfer raw patterns spanning spaces or punctuation directly to
ESEARCH. Make complex conditions explicit by combining separate SEARCH/ESEARCH predicates with AND
or OR.

ESEARCH is case-insensitive for ASCII in the current comparison path. Broader keyword matches
increase search cost, so it is not always faster than LIKE. This example uses ASCII keyword
patterns.

`NOT ESEARCH` syntax is unsupported. Substituting `NOT SEARCH` or `NOT LIKE` changes the search
semantics. Redefine which rows to exclude and check NULL handling.

<a id="like-not"></a>
<a id="text-search-like-not"></a>

<a id="like는-원문-문자열의-패턴을-검사합니다"></a>

## LIKE and NOT LIKE

```sql
SELECT event_id FROM ch7_search WHERE message LIKE '%TIMEOUT%' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message LIKE 'ERR-____' ORDER BY event_id;
SELECT event_id FROM ch7_search WHERE message NOT LIKE '%timeout%' ORDER BY event_id;
```

The first query selects rows 1, 3, and 8; the second returns 0 rows; the third selects 2, 4, 6, and
7. Row 7 has text after `ERR-1001`, so it does not match the whole-string pattern `ERR-____`. `%`
matches zero or more characters; `_` matches one character. Check backslash escaping rules when
searching for literal `%`, `_`, or backslashes.

LIKE is also case-insensitive for ASCII in the current comparison path. It does not use a KEYWORD
index, but other WHERE predicates or a time range can reduce the rows tested. It is therefore also
inaccurate to say that LIKE always scans the entire table.

<a id="regex"></a>
<a id="regexp-not"></a>
<a id="regex-regexp-not"></a>

<a id="정규식은-형식과-위치를-검사할-때-사용합니다"></a>

## REGEXP and REGEXP_LIKE

```sql
SELECT event_id FROM ch7_search
 WHERE message REGEXP '^ERR-[0-9]+'
 ORDER BY event_id;

SELECT event_id FROM ch7_search
 WHERE message NOT REGEXP 'timeout'
 ORDER BY event_id;
```

The first query selects row 7; the second selects 2, 4, 6, and 7. REGEXP checks for a matching
substring. Specify `^` or `$` to constrain a match to the start or end of the string.

<a id="regexp-like"></a>
<a id="regex-regexp-like"></a>

Use `REGEXP_LIKE` for the function form. Its input currently must be VARCHAR, and its pattern and
options must be constant VARCHAR values. Passing the preceding TEXT column directly causes a type
error, so prepare a separate sample.

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

Row 1 returns 0 and 1, respectively. Row 5, whose message is NULL, returns NULL for both results.
Regular expressions are case-sensitive by default; the `i` option makes comparison case-insensitive.
Use `c` for explicitly case-sensitive comparison.

Regular expressions are not processed directly by KEYWORD indexes. Time predicates or SEARCH can
narrow the candidates, but a regular expression cannot recover a row excluded by the preceding
predicate.

<a id="저장-타입과-검색-성능을-혼동하지-마세요"></a>

## TEXT Limitations and Search Performance

TEXT can hold raw content up to 64 MiB, but ORDER BY and GROUP BY on TEXT itself are unsupported.
Keep devices, error codes, and severity values for sorting and aggregation in separate columns.
Compare performance on the same data after checking index presence, build state, and query range.

```sql
DROP TABLE ch7_regexp_fn;
DROP TABLE ch7_search;
```

If search results differ, inspect one raw row alongside the pattern. Distinguishing word search from
substring search often resolves the discrepancy.

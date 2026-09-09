---
type: docs
title: 'SEARCH / ESEARCH / REGEXP'
weight: 50
toc: true
---

Search operators inspect different targets despite similar syntax.
SEARCH and ESEARCH use KEYWORD index tokens; LIKE and REGEXP evaluate the original text.
Before changing operators for performance, verify equivalent result semantics.

## SEARCH

```text
column_name SEARCH 'search_term'
column_name NOT SEARCH 'search_term'
```

LOG VARCHAR/TEXT columns require a KEYWORD index.
Multiple words use AND semantics; this is not phrase search guaranteeing word order or adjacency.
In default mode, ordinary ASCII words are normalized to lowercase and Korean text uses 2-grams.
This does not guarantee morphological analysis or Unicode case handling for every language.

The following standalone exercise table is used throughout this page.

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

The first two queries select row 1; the last selects row 2.
NOT SEARCH excludes row 3, whose message is NULL.
For searches across columns, create the required index on each target column.

## ESEARCH

```text
column_name ESEARCH 'pattern%'
column_name ESEARCH '%pattern%'
```

Applies patterns to indexed words. pattern% matches a word prefix;
%pattern% matches a substring within a word.
Do not interpret % as freely crossing word boundaries in the original text.
The following examples use ASCII keyword patterns.

```sql
SELECT event_id FROM ch7_ref_search WHERE message ESEARCH 'time%' ORDER BY event_id;
SELECT event_id FROM ch7_ref_search WHERE message ESEARCH '%time%' ORDER BY event_id;
```

Results are row 1 and rows 1/2, respectively.
Current ESEARCH ASCII pattern comparison is case-insensitive.
It does not fully replace original-text LIKE; cost depends on the tokens and rows matching the pattern.

NOT ESEARCH is unsupported.
Replacing it with NOT SEARCH or NOT LIKE can change excluded rows; check results and NULL handling.

## Comparison with LIKE

```sql
SELECT event_id FROM ch7_ref_search WHERE message LIKE '%TIMEOUT%' ORDER BY event_id;
SELECT event_id FROM ch7_ref_search WHERE message NOT LIKE '%timeout%' ORDER BY event_id;
```

The first query returns rows 1/2; the second returns zero rows. NOT LIKE also excludes NULL rows.
LIKE currently uses case-insensitive ASCII comparison.
% represents zero or more characters; _ represents one.

LIKE itself does not use KEYWORD indexes.
This does not necessarily mean a full table scan.
Time predicates or other index predicates may restrict target rows first.

## REGEXP

```text
column_name REGEXP 'pattern'
column_name NOT REGEXP 'pattern'
```

Tests for a substring matching the regular expression. Matching is case-sensitive by default.
Use ^ and $ to anchor the start and end.

```sql
SELECT event_id FROM ch7_ref_search
 WHERE message REGEXP '^ERROR.*timeout'
 ORDER BY event_id;
SELECT event_id FROM ch7_ref_search
 WHERE message NOT REGEXP 'timeout'
 ORDER BY event_id;
```

The first query returns row 1; the second returns zero rows.
REGEXP does not directly use KEYWORD indexes.
Before using SEARCH to narrow candidates, verify that it does not omit required results.

### REGEXP as an Expression

REGEXP results can also be used in scalar expressions.

```sql
SELECT 'abcde' REGEXP 'a[bcd]{1,10}e' FROM dual;
```

The result is 1. The REGEXP_LIKE function also accepts matching options.
Current function input must be VARCHAR; pattern and options must be constant VARCHAR.
Do not assume its input constraints are identical to the REGEXP operator, which accepts TEXT columns.

```sql
SELECT event_id,
       REGEXP_LIKE(message, 'error') AS case_sensitive,
       REGEXP_LIKE(message, 'error', 'i') AS case_insensitive
  FROM ch7_ref_search
 WHERE event_id IN (1, 3)
 ORDER BY event_id;
```

Row 1 returns 0/1; row 3 returns NULL/NULL.
i is case-insensitive and c is case-sensitive; omitting the option uses case-sensitive matching.

## Performance Guidelines

| Goal | Selection |
|---|---|
| Test for a word | SEARCH |
| Prefix/substring patterns within indexed words | ESEARCH |
| Substring patterns in original text | LIKE |
| Original-text format, position, or complex patterns | REGEXP/REGEXP_LIKE |

Distinguish index existence from completed index building. Compare on the same data and time range.
Drop the exercise table when finished.

```sql
DROP TABLE ch7_ref_search;
```

## Related Documentation

- [Text Search Exercise](/dbms/log-table-usage/text-search-keyword-index/) — Multiple words, Korean text, NULLs, and TEXT constraints
- [INDEX Syntax](../index-syntax/) — KEYWORD index creation

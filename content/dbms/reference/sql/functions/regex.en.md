---
type: docs
title: 'Regular Expression Functions'
weight: 30
toc: true
---

Machbase provides PCRE (Perl Compatible Regular Expressions) functions. All regular expression
functions operate only on `VARCHAR` columns.

## Quick Reference

| Function | Syntax | Description |
|------|------|------|
| REGEXP_LIKE | `REGEXP_LIKE(src, pat [, flag])` | Test for a pattern match |
| REGEXP_INSTR | `REGEXP_INSTR(src, pat [, pos [, occ [, ret [, flag]]]])` | Return the match position |
| REGEXP_SUBSTR | `REGEXP_SUBSTR(src, pat [, pos [, occ [, flag]]])` | Extract a matching substring |
| REGEXP_REPLACE | `REGEXP_REPLACE(src, pat [, repl [, pos [, occ [, flag]]]])` | Replace matching text |

### match_param (Common Parameter)

| Value | Description |
|----|------|
| `'c'` | Case-sensitive (default) |
| `'i'` | Case-insensitive |

---

## REGEXP_LIKE

Tests whether a string matches a regular expression. Commonly used in WHERE, it returns a Boolean (1/0).

```sql
REGEXP_LIKE(source, pattern)
REGEXP_LIKE(source, pattern, match_param)
```

- `source`: `VARCHAR` column or expression to test
- `pattern`: Constant `VARCHAR` regular expression
- `match_param`: `'c'` (case-sensitive, default) or `'i'` (case-insensitive)

```sql
-- Query messages containing 'error' or 'warn', ignoring case
SELECT *
  FROM sensor_text
 WHERE REGEXP_LIKE(message, 'error|warn', 'i');

-- Query codes starting with digits
SELECT *
  FROM event_log
 WHERE REGEXP_LIKE(code, '^[0-9]+');

-- Validate email format
SELECT name
  FROM users
 WHERE REGEXP_LIKE(email, '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');
```

---

## REGEXP_INSTR

Returns the position of a match, or `0` if none exists. Positions are 1-based.

```sql
REGEXP_INSTR(source, pattern)
REGEXP_INSTR(source, pattern, position)
REGEXP_INSTR(source, pattern, position, occurrence)
REGEXP_INSTR(source, pattern, position, occurrence, return_pos)
REGEXP_INSTR(source, pattern, position, occurrence, return_pos, match_param)
```

| Parameter | Description |
|---------|------|
| `source` | `VARCHAR` to search |
| `pattern` | Constant `VARCHAR` regular expression |
| `position` | Starting position (at least 1; default: 1) |
| `occurrence` | Match occurrence to find (at least 1; default: 1) |
| `return_pos` | `0`: Start position; `1`: Position after the match |
| `match_param` | `'c'` or `'i'` |

```sql
-- Position after the first 'The' match, ignoring case
SELECT REGEXP_INSTR('TechOnTheNet', 'The', 1, 1, 1, 'i');
-- Result: 10 (position after 'The')
```

---

## REGEXP_SUBSTR

Returns the substring matching the regular expression, or NULL if none exists.

```sql
REGEXP_SUBSTR(source, pattern)
REGEXP_SUBSTR(source, pattern, position)
REGEXP_SUBSTR(source, pattern, position, occurrence)
REGEXP_SUBSTR(source, pattern, position, occurrence, match_param)
```

| Parameter | Description |
|---------|------|
| `source` | `VARCHAR` to search |
| `pattern` | Constant `VARCHAR` regular expression |
| `position` | Starting position (at least 1; default: 1) |
| `occurrence` | Match occurrence to find (at least 1; default: 1) |
| `match_param` | `'c'` or `'i'` |

```sql
-- Extract the second vowel, ignoring case
SELECT REGEXP_SUBSTR('TechOnTheNet', 'a|e|i|o|u', 1, 2, 'i');
-- Result: 'O'

-- Extract the first octet from an IP address
SELECT REGEXP_SUBSTR(ip_str, '[0-9]+', 1, 1) FROM log_table;

-- Extract an error code from a log
SELECT REGEXP_SUBSTR(message, 'ERR-[0-9]+') FROM event_log;
```

---

## REGEXP_REPLACE

Replaces matching text with the specified string.

```sql
REGEXP_REPLACE(source, pattern)
REGEXP_REPLACE(source, pattern, replacement)
REGEXP_REPLACE(source, pattern, replacement, position)
REGEXP_REPLACE(source, pattern, replacement, position, occurrence)
REGEXP_REPLACE(source, pattern, replacement, position, occurrence, match_param)
```

| Parameter | Description |
|---------|------|
| `source` | Target `VARCHAR` |
| `pattern` | Constant `VARCHAR` regular expression |
| `replacement` | Replacement string; omitted means remove the match |
| `position` | Starting position (at least 1; default: 1) |
| `occurrence` | `0`: Replace all; positive n: replace the nth match only (default: 0) |
| `match_param` | `'c'` or `'i'` |

```sql
-- Replace the second vowel with 'Z', ignoring case
SELECT REGEXP_REPLACE('TechOnTheNet', 'a|e|i|o|u', 'Z', 1, 2, 'i');
-- Result: 'TechZnTheNet'

-- Remove all digits
SELECT REGEXP_REPLACE(code, '[0-9]', '') FROM log_table;

-- Normalize consecutive whitespace to one space
SELECT REGEXP_REPLACE(message, '\s+', ' ') FROM event_log;
```

---

## PCRE Basics

| Pattern | Description | Example |
|------|------|------|
| `.` | Any single character | `a.c` → abc, aXc |
| `*` | Zero or more repetitions | `ab*c` → ac, abc, abbc |
| `+` | One or more repetitions | `ab+c` → abc, abbc |
| `?` | Zero or one occurrence | `colou?r` → color, colour |
| `^` | Start of string | `^error` |
| `$` | End of string | `\.log$` |
| `[abc]` | Character class | `[aeiou]` |
| `[^abc]` | Negated character class | `[^0-9]` |
| `\d` | Digit (`[0-9]`) | `\d+` |
| `\w` | Word character | `\w+` |
| `\s` | Whitespace | `\s+` |
| `a\|b` | a or b | `error\|warn` |
| `(abc)` | Group | `(foo)+` |
| `{n,m}` | n to m repetitions | `\d{3,5}` |

---

## Comparison with SEARCH / ESEARCH

| Feature | REGEXP_LIKE | SEARCH / ESEARCH |
|------|:-----------:|:----------------:|
| Applicable Type | `VARCHAR` | `TEXT` (full-text index) |
| Regex support | O (PCRE) | X (keyword search) |
| Index use | X | O |
| Large text volumes | Limited | Recommended |

For keyword searches over large text volumes, `TEXT` and SEARCH provide better performance. Use
VARCHAR and REGEXP_LIKE when regex pattern matching is required.

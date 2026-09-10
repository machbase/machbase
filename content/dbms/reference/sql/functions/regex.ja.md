---
type: docs
title: '正規表現関数'
weight: 30
toc: true
---

MachbaseはPCRE（Perl Compatible Regular Expressions）に基づく正規表現関数を提供します。すべての正規表現関数は`VARCHAR`型の列でのみ動作します。

## クイックリファレンス

| 関数 | 構文 | 説明 |
|------|------|------|
| REGEXP_LIKE | `REGEXP_LIKE(src, pat [, flag])` | パターンの一致を確認 |
| REGEXP_INSTR | `REGEXP_INSTR(src, pat [, pos [, occ [, ret [, flag]]]])` | パターンが一致する位置を返す |
| REGEXP_SUBSTR | `REGEXP_SUBSTR(src, pat [, pos [, occ [, flag]]])` | パターンに一致する部分文字列を抽出 |
| REGEXP_REPLACE | `REGEXP_REPLACE(src, pat [, repl [, pos [, occ [, flag]]]])` | パターンに一致する文字列を置換 |

### match_param (共通パラメーター)

| 値 | 説明 |
|----|------|
| `'c'` | 大文字小文字を区別（デフォルト） |
| `'i'` | 大文字小文字を区別しない |

---

## REGEXP_LIKE

文字列が正規表現パターンに一致するか検査します。主に`WHERE`句で使用し、Boolean（1/0）を返します。

```sql
REGEXP_LIKE(source, pattern)
REGEXP_LIKE(source, pattern, match_param)
```

- `source`: 検査する`VARCHAR`列または式
- `pattern`: 定数の`VARCHAR`正規表現
- `match_param`: `'c'`（大文字小文字を区別、デフォルト）または`'i'`（区別しない）

```sql
-- 'error'または'warn'を含むメッセージを参照（大文字小文字を区別しない）
SELECT *
  FROM sensor_text
 WHERE REGEXP_LIKE(message, 'error|warn', 'i');

-- 数字で始まるコードを参照
SELECT *
  FROM event_log
 WHERE REGEXP_LIKE(code, '^[0-9]+');

-- メールアドレス形式の検証
SELECT name
  FROM users
 WHERE REGEXP_LIKE(email, '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');
```

---

## REGEXP_INSTR

正規表現に一致する位置を返します。一致する値がなければ`0`を返します。位置は1始まりです。

```sql
REGEXP_INSTR(source, pattern)
REGEXP_INSTR(source, pattern, position)
REGEXP_INSTR(source, pattern, position, occurrence)
REGEXP_INSTR(source, pattern, position, occurrence, return_pos)
REGEXP_INSTR(source, pattern, position, occurrence, return_pos, match_param)
```

| パラメーター | 説明 |
|---------|------|
| `source` | 検査する`VARCHAR` |
| `pattern` | 定数の`VARCHAR`正規表現 |
| `position` | 検索開始位置（1以上、デフォルト値: 1） |
| `occurrence` | 何番目の一致を探すか（1以上、デフォルト値: 1） |
| `return_pos` | `0`: 開始位置、`1`: 一致文字列の直後の位置 |
| `match_param` | `'c'`または`'i'` |

```sql
-- 最初の'The'の一致直後の位置を返す（大文字小文字を区別しない）
SELECT REGEXP_INSTR('TechOnTheNet', 'The', 1, 1, 1, 'i');
-- 結果: 10（一致文字列'The'の直後の位置）
```

---

## REGEXP_SUBSTR

正規表現に一致する部分文字列を返します。一致する値がなければNULLを返します。

```sql
REGEXP_SUBSTR(source, pattern)
REGEXP_SUBSTR(source, pattern, position)
REGEXP_SUBSTR(source, pattern, position, occurrence)
REGEXP_SUBSTR(source, pattern, position, occurrence, match_param)
```

| パラメーター | 説明 |
|---------|------|
| `source` | 検査する`VARCHAR` |
| `pattern` | 定数の`VARCHAR`正規表現 |
| `position` | 検索開始位置（1以上、デフォルト値: 1） |
| `occurrence` | 何番目の一致を探すか（1以上、デフォルト値: 1） |
| `match_param` | `'c'`または`'i'` |

```sql
-- 2番目の母音を抽出（大文字小文字を区別しない）
SELECT REGEXP_SUBSTR('TechOnTheNet', 'a|e|i|o|u', 1, 2, 'i');
-- 結果: 'O'

-- IPアドレスから最初のオクテットを抽出
SELECT REGEXP_SUBSTR(ip_str, '[0-9]+', 1, 1) FROM log_table;

-- ログからエラーコードを抽出
SELECT REGEXP_SUBSTR(message, 'ERR-[0-9]+') FROM event_log;
```

---

## REGEXP_REPLACE

正規表現に一致する文字列を指定の文字列に置き換えます。

```sql
REGEXP_REPLACE(source, pattern)
REGEXP_REPLACE(source, pattern, replacement)
REGEXP_REPLACE(source, pattern, replacement, position)
REGEXP_REPLACE(source, pattern, replacement, position, occurrence)
REGEXP_REPLACE(source, pattern, replacement, position, occurrence, match_param)
```

| パラメーター | 説明 |
|---------|------|
| `source` | 対象の`VARCHAR` |
| `pattern` | 定数の`VARCHAR`正規表現 |
| `replacement` | 置換文字列（省略すると一致文字列を削除） |
| `position` | 検索開始位置（1以上、デフォルト値: 1） |
| `occurrence` | `0`: すべての一致を置換、正数n: n番目の一致のみ置換（デフォルト値: 0） |
| `match_param` | `'c'`または`'i'` |

```sql
-- 2番目の母音を'Z'に置換（大文字小文字を区別しない）
SELECT REGEXP_REPLACE('TechOnTheNet', 'a|e|i|o|u', 'Z', 1, 2, 'i');
-- 結果: 'TechZnTheNet'

-- すべての数字を削除
SELECT REGEXP_REPLACE(code, '[0-9]', '') FROM log_table;

-- 空白の正規化（連続する空白を1つにする）
SELECT REGEXP_REPLACE(message, '\s+', ' ') FROM event_log;
```

---

## PCRE正規表現の基礎

| パターン | 説明 | 例 |
|------|------|------|
| `.` | 任意の1文字 | `a.c` → abc, aXc |
| `*` | 0回以上の繰り返し | `ab*c` → ac, abc, abbc |
| `+` | 1回以上の繰り返し | `ab+c` → abc, abbc |
| `?` | 0回または1回 | `colou?r` → color, colour |
| `^` | 文字列の先頭 | `^error` |
| `$` | 文字列の末尾 | `\.log$` |
| `[abc]` | 文字クラス | `[aeiou]` |
| `[^abc]` | 否定文字クラス | `[^0-9]` |
| `\d` | 数字（`[0-9]`） | `\d+` |
| `\w` | 単語文字 | `\w+` |
| `\s` | 空白文字 | `\s+` |
| `a\|b` | aまたはb | `error\|warn` |
| `(abc)` | グループ | `(foo)+` |
| `{n,m}` | n~m回の繰り返し | `\d{3,5}` |

---

## SEARCH / ESEARCHとの違い

| 機能 | REGEXP_LIKE | SEARCH / ESEARCH |
|------|:-----------:|:----------------:|
| 適用する型 | `VARCHAR` | `TEXT` (全文検索インデックス) |
| 正規表現のサポート | O (PCRE) | X (キーワード検索) |
| インデックスの利用 | X | O |
| 大量のテキスト | 限定的 | 推奨 |

大量のテキストでキーワード検索を行う場合は、`TEXT`型と`SEARCH`句が性能面で有利です。正規表現のパターン照合が必要な場合は、`VARCHAR`列と`REGEXP_LIKE`を使用します。

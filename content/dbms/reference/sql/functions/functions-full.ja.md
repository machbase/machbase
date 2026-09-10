---
type: docs
title: '完全な関数リファレンス'
weight: 70
toc: true
tocSort: true
---

## エラー処理

| エラーの種類 | コード | 発生条件 |
|---|---|---|
| 引数の型エラー | `ERR-02036`, `ERR-02037` | 非数値を渡した場合、または`PI`に引数を渡した場合 |
| 実行エラー | `ERR-02317` | `SQRT`への負数入力、`MOD`の0除算、`LOG`の無効な底/値、`EXP`/`POWER`の範囲超過など |

入力が`NULL`なら結果も`NULL`です。

## ABS

数値列の絶対値を実数で返します。

```sql
ABS(column_expr)
```

```sql
Mach> CREATE LOG TABLE abs_table (c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO abs_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO abs_table VALUES(2, 2.0, 'sqltest');
1 row(s) inserted.

Mach> INSERT INTO abs_table VALUES(3, 3.0, 'sqltest');
1 row(s) inserted.

Mach> SELECT ABS(c1), ABS(c2) FROM abs_table;
SELECT ABS(c1), ABS(c2) from abs_table;
ABS(c1)                     ABS(c2)
-----------------------------------------------------------
3                           3
2                           2
1                           1
[3] row(s) selected.
```


## ADD_TIME

DATETIME列に年/月/日/時/分/秒単位の加減算を行います。ミリ秒、マイクロ秒、ナノ秒単位はサポートしません。Diffの形式は`"Year/Month/Day Hour:Minute:Second"`で、各項目は正数または負数を使用できます。

```sql
ADD_TIME(column,time_diff_format)
```

```sql
Mach> CREATE LOG TABLE add_time_table (id INTEGER, dt DATETIME);
Created successfully.

Mach> INSERT INTO  add_time_table VALUES(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(2, TO_DATE('2000-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(3, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(4, TO_DATE('2013-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(5, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> INSERT INTO  add_time_table VALUES(6, TO_DATE('2014-12-30 23:22:33 444:555:666'));
1 row(s) inserted.

Mach> SELECT ADD_TIME(dt, '1/0/0 0:0:0') FROM add_time_table;
ADD_TIME(dt, '1/0/0 0:0:0')
----------------------------------
2015-12-30 23:22:33 444:555:666
2015-12-30 11:22:33 444:555:666
2014-11-11 01:02:03 004:005:006
2013-11-11 01:02:03 004:005:006
2001-11-11 01:02:03 004:005:006
2000-11-11 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '0/0/0 1:1:1') FROM add_time_table;
ADD_TIME(dt, '0/0/0 1:1:1')
----------------------------------
2014-12-31 00:23:34 444:555:666
2014-12-30 12:23:34 444:555:666
2013-11-11 02:03:04 004:005:006
2012-11-11 02:03:04 004:005:006
2000-11-11 02:03:04 004:005:006
1999-11-11 02:03:04 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '1/1/1 0:0:0') FROM add_time_table;
ADD_TIME(dt, '1/1/1 0:0:0')
----------------------------------
2016-01-31 23:22:33 444:555:666
2016-01-31 11:22:33 444:555:666
2014-12-12 01:02:03 004:005:006
2013-12-12 01:02:03 004:005:006
2001-12-12 01:02:03 004:005:006
2000-12-12 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '-1/0/0 0:0:0') FROM add_time_table;
ADD_TIME(dt, '-1/0/0 0:0:0')
----------------------------------
2013-12-30 23:22:33 444:555:666
2013-12-30 11:22:33 444:555:666
2012-11-11 01:02:03 004:005:006
2011-11-11 01:02:03 004:005:006
1999-11-11 01:02:03 004:005:006
1998-11-11 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '0/0/0 -1:-1:-1') FROM add_time_table;
ADD_TIME(dt, '0/0/0 -1:-1:-1')
----------------------------------
2014-12-30 22:21:32 444:555:666
2014-12-30 10:21:32 444:555:666
2013-11-11 00:01:02 004:005:006
2012-11-11 00:01:02 004:005:006
2000-11-11 00:01:02 004:005:006
1999-11-11 00:01:02 004:005:006
[6] row(s) selected.

Mach> SELECT ADD_TIME(dt, '-1/-1/-1 0:0:0') FROM add_time_table;
ADD_TIME(dt, '-1/-1/-1 0:0:0')
----------------------------------
2013-11-29 23:22:33 444:555:666
2013-11-29 11:22:33 444:555:666
2012-10-10 01:02:03 004:005:006
2011-10-10 01:02:03 004:005:006
1999-10-10 01:02:03 004:005:006
1998-10-10 01:02:03 004:005:006
[6] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-1/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
[2] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-2/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
4           2013-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT ADD_TIME(TO_DATE('2000-12-01 00:00:00 000:000:001'), '-1/0/0 0:0:-1') FROM add_time_table;
ADD_TIME(TO_DATE('2000-12-01 00:00:00 000:000:001'), '-1/0/0 0:0:-1')
------------------------------------------
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
1999-11-30 23:59:59 000:000:001
[6] row(s) selected.

Mach> SELECT * FROM add_time_table WHERE dt > ADD_TIME(TO_DATE('2014-12-30 11:22:33 444:555:666'), '-1/-2/-1 0:0:0');
ID          DT
-----------------------------------------------
6           2014-12-30 23:22:33 444:555:666
5           2014-12-30 11:22:33 444:555:666
4           2013-11-11 01:02:03 004:005:006
[3] row(s) selected.
```

## APPROX_PERCENTILE {#approx_percentile-family}

```
APPROX_PERCENTILE
APPROX_MEDIAN
APPROX_P05
APPROX_P10
APPROX_P90
APPROX_P95
```

これらの関数は、元の値をすべてソートせず、サイズを制限した要約情報を保持して分位点を近似します。入力データ量が非常に多く、わずかな誤差を許容できる場合に便利です。

```sql
APPROX_PERCENTILE(value, ratio)
APPROX_MEDIAN(value)
APPROX_P05(value)
APPROX_P10(value)
APPROX_P90(value)
APPROX_P95(value)
```

- `value`は数値型である必要があります。
- `ratio`は`0.0`以上`1.0`以下の定数である必要があります。
- 戻り値の型は`DOUBLE`です。
- `NULL`値は無視します。

`APPROX_MEDIAN(value)`は近似中央値です。`APPROX_P05`、`APPROX_P10`、`APPROX_P90`、`APPROX_P95`はよく使う分位点の短縮形です。

```sql
SELECT APPROX_PERCENTILE(latency_ms, 0.95) AS ap95,
       APPROX_MEDIAN(latency_ms) AS amedian,
       APPROX_P05(latency_ms) AS ap05
FROM api_log;
```

## ARRAY_LENGTH

`ARRAY_LENGTH(array_value)`は非NULLの`ARRAY`の宣言された要素数（cardinality）を返します。

```sql
SELECT ARRAY_LENGTH(ARRAY[10, NULL, 30]);
-- 3
```

全要素がNULLでもcardinalityを返します。配列全体がNULLならNULLを返し、型情報のない`ARRAY_LENGTH(NULL)`はエラーになります。ARRAYの構文と制約の詳細は[数値ARRAY型](/dbms/reference/sql/types/array/)を参照してください。

## ARRAY_SPARSE

`ARRAY_SPARSE`は固定長`ARRAY`で値のある位置だけを指定します。位置は0始まりで、省略した位置は要素のNULLになります。

```sql
-- 対象列で型とcardinalityを決定します。
INSERT INTO sensor_array (id, channels)
VALUES (1, ARRAY_SPARSE(0 => 10, 3 => 40));

-- 対象列のない式では型とcardinalityを明示します。
SELECT ARRAY_SPARSE(INT32[4], 0 => 10, 3 => 40);

-- 角括弧の省略形は最大position + 1からcardinalityを推論します。
SELECT [1 => 12, 33 => 23];
```

角括弧の省略形は、対象ARRAYがあればその型とcardinalityを使用します。単独の式では密なARRAYと同じ共通数値型を使用し、最大positionに1を加えてcardinalityを決定します。対象列のない全要素NULLの疎な配列、重複したposition、範囲外のpositionはエラーです。取り込み方法とSDKの疎なオブジェクトは[Sparse ARRAYと選択列Append API](/dbms/development-tools-integration/data-input-load-export/array-append/)を参照してください。


## AREA {#area}

`AREA(y, x)`は数値の`(x, y)`点からなる曲線の下の面積を正確に計算する集約関数です。

```sql
AREA(y, x)
```

- 両方の引数が数値型である必要があります。
- どちらかが`NULL`の行は無視します。
- 有効な点が2つ未満なら結果は`NULL`です。
- 戻り値の型は`DOUBLE`です。

```sql
SELECT AREA(power_kw, sample_sec)
FROM power_log;
```


## AVG

数値列の平均値を返す集約関数です。

```sql
AVG(column_name)
```

```sql
Mach> CREATE LOG TABLE avg_table (id1 INTEGER, id2 INTEGER);
Created successfully.

Mach> INSERT INTO avg_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO avg_table VALUES(null, 4);
1 row(s) inserted.

Mach> SELECT id1, AVG(id2) FROM avg_table GROUP BY id1;
id1         AVG(id2)
-------------------------------------------
2                2
NULL             4
1                2
```


## BITAND / BITOR

2つの整数値を64ビット符号付き整数へ変換し、ビット単位のAND/OR演算の結果を返します。入力は整数型である必要があり、出力も64ビット符号付き整数です。

0未満の整数ではプラットフォームによって結果が異なる場合があるため、uintegerとushort型のみの使用を推奨します。

```sql
BITAND (<expression1>, <expression2>)
BITOR (<expression1>, <expression2>)
```

```sql
Mach> CREATE LOG TABLE bit_table (i1 INTEGER, i2 UINTEGER, i3 FLOAT, i4 DOUBLE, i5 SHORT, i6 VARCHAR(10));
Created successfully.

Mach> INSERT INTO bit_table VALUES (-1, 1, 1, 1, 2, 'aaa');
1 row(s) inserted.

Mach> INSERT INTO bit_table VALUES (-2, 2, 2, 2, 3, 'bbb');
1 row(s) inserted.

Mach> SELECT BITAND(i1, i2) FROM bit_table;
BITAND(i1, i2)
-----------------------
2
1
[2] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i2, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
-1          1           1                           1                           2           aaa
[1] row(s) selected.

Mach> SELECT BITOR(i5, 1) FROM bit_table WHERE BITOR(i5, 1) = 3;
BITOR(i5, 1)
-----------------------
3
3
[2] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITOR(i2, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
-1          1           1                           1                           2           aaa
[1] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i3, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITAND(i4, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITAND(i5, 1) FROM bit_table WHERE BITAND(i5, 1) = 1;
BITAND(i5, 1)
-----------------------
1
[1] row(s) selected.

Mach> SELECT * FROM bit_table WHERE BITOR(i6, 1) = 1;
I1          I2          I3                          I4                          I5          I6
---------------------------------------------------------------------------------------------------------------
[ERR-02037 : Function [BITOR] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITOR(i1, i2) FROM bit_table;
BITOR(i1, i2)
-----------------------
-2
-1
[2] row(s) selected.

Mach> SELECT BITAND(i1, i3) FROM bit_table;
BITAND(i1, i3)
-----------------------
[ERR-02037 : Function [BITAND] argument data type is mismatched.]
[0] row(s) selected.

Mach> SELECT BITOR(i1, i6) FROM bit_table;
BITOR(i1, i6)
-----------------------
[ERR-02037 : Function [BITOR] argument data type is mismatched.]
[0] row(s) selected.
```


## CAST

<span class="badge-since">Machbase 8.7.0以降でサポート</span>

`CAST`は値、列、式を指定したデータ型へ明示的に変換します。`SELECT`、述語、`CASE`、`UNION ALL`、VIEW定義、プリペアドステートメントで使用できます。

### 構文

```sql
CAST(expression AS data_type)
CAST(expression AS data_type(length))
CAST(expression AS DECIMAL(precision[, scale]))
CAST(array_expression AS numeric_type[cardinality])
CAST(array_expression AS DECIMAL(precision[, scale])[cardinality])
```

- `expression`は変換する値、列、SQL式です。
- `array_expression`は数値`ARRAY`またはSQL `NULL`です。
- `data_type`は次の表の変換先の型または別名です。
- 型名は大文字小文字を区別しません。
- `length`、`precision`、`scale`は変換先の型で許可する場合のみ指定できます。
- ARRAYの入力と変換先の`cardinality`は完全に一致する必要があります。

### 対応する型と別名

| 分類 | 変換先の型 | 使用できる名前 |
|------|-----------|---------------------|
| 符号付き整数 | 16ビット | `INT16`, `SHORT` |
|  | 32ビット | `INT32`, `INT`, `INTEGER` |
|  | 64ビット | `INT64`, `LONG` |
| 符号なし整数 | 16ビット | `UINT16`, `USHORT` |
|  | 32ビット | `UINT32`, `UINTEGER` |
|  | 64ビット | `UINT64`, `ULONG` |
| 実数 | 単精度・倍精度 | `FLOAT`, `DOUBLE` |
| 固定小数点 | DECIMAL | `DECIMAL`, `NUMERIC`, `DEC`, `FIXED`, `NUMBER` |
| 文字 | 固定長・可変長 | `CHAR`, `VARCHAR` |
| 文字LOB | テキスト | `TEXT`, `CLOB` |
| 日付と時刻 | ナノ秒精度 | `DATETIME` |
| ネットワークアドレス | IPアドレス | `IPV4`, `IPV6` |
| バイナリ | バイナリ・バイナリLOB | `BINARY`, `BLOB` |
| ドキュメント | JSON | `JSON` |

同じ行の名前は同じ型として動作します。例えば`INTEGER`、`INT`、`INT32`はいずれも32ビット符号付き整数です。結果列の型メタデータには標準型名が表示される場合があります。

### 長さと精度

#### CHAR, VARCHAR, BINARY

| 型 | 長さ省略時のデフォルト値 | 許容する長さ | 長さ超過時の処理 |
|------|-------------------:|-----------|----------------|
| `CHAR(n)` | 1 byte | 1~32,767 byte | 先頭から`n` byteを保持 |
| `VARCHAR(n)` | 32,767 byte | 1~32,767 byte | 先頭から`n` byteを保持 |
| `BINARY(n)` | 1 byte | 1~67,108,864 byte | 先頭から`n` byteを保持 |

長さは文字数ではなくバイト数です。UTF-8文字列の変換ではマルチバイト文字が途中で切れる場合があるため、十分な長さを指定してください。`CHAR`は余った領域を空白で埋めません。`CAST(... AS CHAR(n))`の結果メタデータは現在`VARCHAR(n)`と表示されます。

```sql
SELECT '[' || CAST('abc' AS CHAR) || ']' AS char_default;
-- [a]

SELECT '[' || CAST('abc' AS CHAR(5)) || ']' AS char_value;
-- [abc]（空白を追加しない）

SELECT CAST('abcdef' AS VARCHAR(3)) AS varchar_value;
-- abc

SELECT CAST('414243' AS BINARY(2)) AS binary_value;
-- 4142
```

`TEXT`、`CLOB`、`BLOB`、`JSON`には`length`を指定できません。これらの型のCAST結果は現在最大32,767 byteをサポートします。許容長を超えて結果の意味が損なわれる場合は、自動で切り詰めずエラーを返します。

#### DECIMAL

| 構文 | 解釈 |
|------|------|
| `DECIMAL` | `DECIMAL(10,0)` |
| `DECIMAL(p)` | `DECIMAL(p,0)` |
| `DECIMAL(p,s)` | precision `p`, scale `s` |

- precision `p`は`1~65`です。
- scale `s`は`0~30`で、precisionを超えることはできません。
- 入力値の小数桁数がscaleを超える場合、中間値を0から遠ざかる方向へ丸めます。
- DECIMAL系以外の型にはprecisionやscaleを指定できません。

```sql
SELECT CAST('12.34' AS DECIMAL(5,2));
-- 12.34

SELECT CAST(123.456 AS NUMERIC(6,2));
-- 123.46
```

### NULLと空文字列

- 入力が`NULL`なら変換先の型の`NULL`を返します。
- Machbaseは長さ0の文字列リテラル`''`をSQL `NULL`として扱います。
- `''''`は単一引用符1文字を表す文字列であり、空文字列ではありません。

```sql
SELECT CAST(NULL AS INTEGER) AS null_integer;
SELECT CAST('' AS VARCHAR(10)) AS empty_value;
SELECT CAST('''' AS VARCHAR(10)) AS quote_value;
```

### 数値変換

数値型同士の変換や、数値として解釈できる文字列から数値型への変換ができます。

```sql
SELECT CAST('123' AS INTEGER);
SELECT CAST('1.25' AS DOUBLE);
SELECT CAST(12.9 AS SHORT);       -- 12
SELECT CAST(-12.9 AS INTEGER);    -- -12
SELECT CAST('9223372036854775806e0' AS LONG);
```

- 実数から整数への変換では、小数部を丸めず0方向へ切り捨てます。
- 整数文字列の指数表記も整数精度を維持して解釈します。
- 変換先の型の範囲外の値はエラーです。
- 符号なし整数への変換では負数の結果は許可しません。小数部を切り捨てた結果が0になる値は、0に変換できます。
- `NaN`、正の無限大、負の無限大は整数へ変換できません。

CASTで生成できる整数の範囲は次のとおりです。各型のNULL予約値は有効な結果範囲には含まれません。

| 変換先の型 | CAST結果の範囲 |
|-----------|----------------|
| `INT16`, `SHORT` | -32,767~32,767 |
| `UINT16`, `USHORT` | 0~65,534 |
| `INT32`, `INT`, `INTEGER` | -2,147,483,647~2,147,483,647 |
| `UINT32`, `UINTEGER` | 0~4,294,967,294 |
| `INT64`, `LONG` | -9,223,372,036,854,775,807~9,223,372,036,854,775,807 |
| `UINT64`, `ULONG` | 0~18,446,744,073,709,551,614 |

### 数値ARRAY全体の変換

同じcardinalityの数値`ARRAY`は全要素の型を変換できます。変換先には`INT16`、`UINT16`、`INT32`、`UINT32`、`INT64`、`UINT64`、`FLOAT`、`DOUBLE`、`DECIMAL`と、対応する型の表の数値別名を使用します。

```sql
SELECT CAST([1.9, NULL, -3.9] AS INT32[3]);
SELECT CAST([1.235, NULL, -2.345] AS DECIMAL(6,2)[3]);
```

- 配列全体のNULLは変換後も配列全体のNULLです。
- 要素のNULLは同じ位置の要素のNULLとして保持します。
- 各非NULL要素には、対応するスカラー数値CASTの切り捨て、丸め、範囲の規則を適用します。
- 1つでも変換できない要素があればCASTとそれを含む文全体が失敗します。変換済みの一部の要素や行を結果として残しません。
- `DECIMAL[N]`は`DECIMAL(10,0)[N]`、`DECIMAL(p)[N]`は`DECIMAL(p,0)[N]`として扱います。

プリペアドステートメントでもCASTの変換先がパラメーターの要素型、cardinality、DECIMALのprecision/scaleを決定します。同じステートメントに密なARRAY、疎なARRAY、配列全体のNULLを再バインドできます。

```sql
SELECT CAST(? AS INT32[3]);
SELECT CAST(? AS DECIMAL(12,4)[3]);
```

スカラーからARRAYへの展開やARRAYからスカラーへの縮小はできません。異なるcardinality間で埋め合わせや切り詰めは行わず、文字列、日付、IP、BINARY、JSONのARRAYを変換先に指定することはできません。

### 文字列とLOBの変換

数値、日付と時刻、IPアドレス、バイナリ、JSONを文字型へ変換できます。

- 整数とDECIMALは値の10進表現を返します。
- `FLOAT`は最大9桁、`DOUBLE`は最大17桁の有効数字で表します。
- `DATETIME`はセッションの日付形式とタイムゾーンに従って文字列化します。
- `IPV4`と`IPV6`は標準化されたアドレス文字列で表します。
- `BINARY`と`BLOB`は接頭辞なしの大文字16進文字列で表します。
- JSONは元のJSON表現を維持します。

```sql
SELECT CAST(123456 AS VARCHAR(8));
-- 123456

SELECT CAST(CAST('2001:db8::1' AS IPV6) AS VARCHAR(64));

SELECT CAST(CAST('0x00ff10' AS BLOB) AS VARCHAR(8));
-- 00FF10
```

文字列から`BINARY`または`BLOB`への変換には、接頭辞なしの偶数長16進数、または`0x`/`0X`接頭辞付きの偶数長16進数を使用します。

```sql
SELECT CAST('414243' AS BINARY(3));
SELECT CAST('0x00ff10' AS BLOB);
SELECT CAST(X'414243' AS VARCHAR(6));
```

`BINARY(n)`は先頭から`n` byteのみを保持します。16進数以外の文字や奇数長の16進数はエラーです。

### DATETIME変換

文字列または数値を`DATETIME`へ変換できます。

- 文字列はセッションのデフォルトの日付形式とタイムゾーンで解釈します。
- 数値はUnix epochからのナノ秒数として解釈します。
- 数値`-1`はDATETIMEのNULL表示用予約値のため変換できません。
- `DATETIME`から数値へ変換すると、Unix epochからのナノ秒値を返します。

```sql
SELECT CAST('2026-08-15 12:34:56' AS DATETIME);
SELECT CAST(1000000000 AS DATETIME);
SELECT CAST(CAST(1000000000 AS DATETIME) AS VARCHAR(40));
```

同じepoch値でも、セッションのタイムゾーンが異なれば文字列表示される日付と時刻が異なる場合があります。

### IPV4とIPV6への変換

文字列を`IPV4`または`IPV6`へ変換できます。アドレス全体が正しい形式である必要があります。

```sql
SELECT CAST('127.0.0.1' AS IPV4);
SELECT CAST('2001:db8::1' AS IPV6);
```

無効なアドレスや、変換先の型に一致しないアドレス形式はエラーです。

### JSON変換

文字列を`JSON`へ変換するには、入力全体が有効なJSONである必要があります。オブジェクトと配列に加えて、JSON文字列、数値、`true`、`false`、`null`も使用できます。

```sql
SELECT CAST('{"ok":true}' AS JSON);
SELECT CAST('[1,2,3]' AS JSON);
SELECT CAST('"abc"' AS JSON);
SELECT CAST(CAST('"abc"' AS JSON) AS VARCHAR(16));
-- "abc"
```

一部のみ有効なJSONや、末尾にJSON以外の文字が残る入力は変換できません。

### 式と結果メタデータ

CASTは通常のSQL式のため、WHERE条件、`CASE`、`UNION ALL`、VIEW定義でも使用できます。

```sql
SELECT CASE
         WHEN reading >= 0 THEN CAST(reading AS VARCHAR(32))
         ELSE 'invalid'
       END AS reading_text
  FROM sensor_log;

CREATE VIEW sensor_cast_view AS
SELECT CAST(sensor_id AS VARCHAR(100)) AS sensor_id_text,
       CAST(value AS DECIMAL(12,3)) AS value_decimal
  FROM sensor_log;
```

プリペアドステートメントでもCAST構文は同じです。入力値は`?`またはSDKの名前付きマーカーで渡し、変換先の型とprecision/scaleはSQLで宣言します。

```sql
SELECT CAST(? AS DECIMAL(12,2)) AS amount;
```

CAST結果の型、バイト長、DECIMALのprecisionとscaleは、結果メタデータとVIEW列情報に反映されます。結果のNULL許容性は入力式のNULL許容性に従います。

`CASE`や`UNION ALL`でARRAY結果を組み合わせるには、要素型、cardinality、DECIMALのprecision/scaleがすべて一致する必要があります。異なる場合は、各結果を明示的に同じARRAY型へCASTしてから組み合わせます。

各SDKは既存の結果メタデータAPIでCAST結果を確認します。CAST専用のSDK APIは提供しません。

| SDK | CAST結果メタデータAPI |
|-----|------------------------|
| Machbase SQLCLI | `SQLDescribeCol()`, `SQLColAttribute()` |
| ODBC | `SQLDescribeCol()`, `SQLColAttribute()` |
| JDBC | `ResultSetMetaData` |
| Python | `cursor.description` |
| Node.js | `ColumnMeta` |
| .NET | `GetSchemaTable()` |
| Go (native) | native column metadata |
| Go (`database/sql`) | `ColumnTypeNullable()` および `ColumnType` API |

### エラーが発生する場合

| 原因 | 例 |
|------|-----|
| 非対応の変換先の型 | `CAST('1' AS UNKNOWN_TYPE)` |
| 許容されないlengthまたはprecision/scale | `CAST('1' AS INTEGER(2))`, `CAST('1' AS DECIMAL(2,3))` |
| 数値の範囲超過またはNULL予約値 | `CAST('65535' AS USHORT)` |
| 符号なし整数へ変換する負数 | `CAST('-1' AS UINTEGER)` |
| 数値へ変換できない文字列 | `CAST('12x' AS INTEGER)` |
| スカラーとARRAY間の変換 | `CAST(1 AS INT32[1])`, `CAST([1] AS INT32)` |
| ARRAYのcardinality不一致 | `CAST([1, 2] AS INT32[3])` |
| 非対応のARRAY変換先の型 | `CAST([1] AS VARCHAR[1])` |
| 無効なIPアドレス | `CAST('999.1.1.1' AS IPV4)` |
| 奇数長または16進数以外のバイナリ文字列 | `CAST('123' AS BINARY(4))`, `CAST('GG' AS BLOB)` |
| 無効なJSON | `CAST('{bad}' AS JSON)` |
| 許容サイズを超えるLOBまたはJSON結果 | 32,767 byteを超える `TEXT`, `CLOB`, `BLOB`, `JSON` 結果 |

### 互換性

CAST関数と数値ARRAY全体のCASTはMachbase 8.7.0でサポートします。Standard EditionとCluster Editionで使用できます。Cluster Editionでは、全ノードをCASTに対応した同じバージョンにそろえる必要があります。CASTに非対応の旧ノードとの混在実行はサポートしません。

### 関連ドキュメント

- [SQL構文辞典](../../syntax/)
- [データ型辞典](../../types/)
- [数値ARRAY型](../../types/array/)
- [DECIMALとNUMERIC固定小数点型](../../types/decimal-numeric-fixed-point/)

## COUNT

列のレコード数を求める集約関数です。

```sql
COUNT(column_name)
```

```sql
Mach> CREATE LOG TABLE count_table (id1 INTEGER, id2 INTEGER);
Created successfully.

Mach> INSERT INTO count_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO count_table VALUES(null, 4);
1 row(s) inserted.

Mach> SELECT COUNT(*) FROM count_table;
COUNT(*)
-----------------------
7
[1] row(s) selected.

Mach> SELECT COUNT(id1) FROM count_table;
COUNT(id1)
-----------------------
6
[1] row(s) selected.
```


## CUME_DIST {#cume_dist}

`CUME_DIST(value, threshold)`は、`value`が`threshold`以下の行の累積比率を返します。

```sql
CUME_DIST(value, threshold)
```

- ウィンドウ関数ではなく集約関数です。
- 両方の引数が数値型である必要があります。
- `threshold`は定数である必要があります。
- 戻り値は`0.0`以上`1.0`以下の`DOUBLE`です。

```sql
SELECT CUME_DIST(latency_ms, 100)
FROM api_log;
```


<a id="current-session-user"></a>
<a id="current_user"></a>
<a id="session_user"></a>
<a id="current_user_id"></a>
<a id="session_user_id"></a>

## CURRENT_USER / SESSION_USER / CURRENT_USER_ID / SESSION_USER_ID

<span class="badge-since">Machbase 8.7.0以降でサポート</span>

現在のSQL実行に適用される実効権限ユーザーと接続セッションユーザーを、名前または内部IDで参照します。Standard EditionとCluster Editionの両方でサポートします。

| 関数 | 戻り値の型 | 説明 |
|---|---|---|
| `CURRENT_USER()` | `VARCHAR` | 現在のSQL実行に適用する実効権限ユーザー名 |
| `SESSION_USER()` | `VARCHAR` | 現在の接続セッションの認証ユーザー名 |
| `CURRENT_USER_ID()` | `INTEGER` | 実効権限ユーザーの内部ID |
| `SESSION_USER_ID()` | `INTEGER` | 認証セッションユーザーの内部ID |

4つの関数は引数を取らず、括弧を付けて呼び出します。括弧なしの`CURRENT_USER`キーワードや、`USER`、`SYSTEM_USER`、`CURRENT_SCHEMA`の別名はサポートしません。

```sql
SELECT CURRENT_USER() AS current_name,
       SESSION_USER() AS session_name,
       CURRENT_USER_ID() AS current_id,
       SESSION_USER_ID() AS session_id;
```

通常のSQLでは、current userとsession userは同じです。

```text
CURRENT_NAME  SESSION_NAME  CURRENT_ID  SESSION_ID
SYS           SYS           1           1
```

### VIEWのユーザーコンテキスト

別のユーザーが所有する定義者権限のVIEWを参照すると、VIEW内部のSQLは所有者の権限で実行されます。

- `CURRENT_USER()`と`CURRENT_USER_ID()`はVIEW所有者を返します。
- `SESSION_USER()`と`SESSION_USER_ID()`はVIEWを呼び出した接続セッションユーザーを返します。

再現可能な所有者/呼び出し元の例は、[VIEW構文](../../syntax/view-syntax/#view-user-context)を参照してください。

### ユーザーが削除されたアクティブセッション

別の管理者セッションが現在接続中のユーザーを`DROP USER`しても、既存の接続は即座には終了しません。既存セッションの4つの関数は、ログイン時に保持したユーザー名とIDを返し続けます。削除されたユーザーは新規接続できず、`M$SYS_USERS`にも表示されません。

ユーザーIDはMachbaseメタデータの内部識別子です。長期保存する業務用ユーザーキーとして使用せず、現在のメタデータの比較や結合にのみ使用します。

```sql
SELECT COUNT(*)
  FROM M$SYS_USERS
 WHERE NAME = SESSION_USER()
   AND USER_ID = SESSION_USER_ID();
```

### エラー

関数に引数を渡すと`ERR-02036`を返します。他の3つの関数も同じ規則を適用します。

```sql
SELECT CURRENT_USER(1);
-- ERR-02036: Function [CURRENT_USER] has an invalid argument.
```

関連するアカウントのライフサイクルは[アカウント管理](../../../../security-access-control/account/)を参照してください。


## DATE_TRUNC

DATETIME値を指定時間単位に切り捨てて返します。

```sql
DATE_TRUNC (field, date_val [, count])
```

```sql
Mach> CREATE LOG TABLE trunc_table (i1 INTEGER, i2 DATETIME);
Created successfully.

Mach> INSERT INTO trunc_table VALUES (1, TO_DATE('1999-11-11 1:2:0 4:5:1'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (2, TO_DATE('1999-11-11 1:2:0 5:5:2'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (3, TO_DATE('1999-11-11 1:2:1 6:5:3'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (4, TO_DATE('1999-11-11 1:2:1 7:5:4'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (5, TO_DATE('1999-11-11 1:2:2 8:5:5'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (6, TO_DATE('1999-11-11 1:2:2 9:5:6'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (7, TO_DATE('1999-11-11 1:2:3 10:5:7'));
1 row(s) inserted.

Mach> INSERT INTO trunc_table VALUES (8, TO_DATE('1999-11-11 1:2:3 11:5:8'));
1 row(s) inserted.

Mach> SELECT COUNT(*), DATE_TRUNC('second', i2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('second', i2, 2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
4                    1999-11-11 01:02:00 000:000:000
4                    1999-11-11 01:02:02 000:000:000
[2] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('nanosecond', i2, 2) tm FROM trunc_table group by tm ORDER BY 2;
COUNT(*)             tm
--------------------------------------------------------
1                    1999-11-11 01:02:00 004:005:000
1                    1999-11-11 01:02:00 005:005:002
1                    1999-11-11 01:02:01 006:005:002
1                    1999-11-11 01:02:01 007:005:004
1                    1999-11-11 01:02:02 008:005:004
1                    1999-11-11 01:02:02 009:005:006
1                    1999-11-11 01:02:03 010:005:006
1                    1999-11-11 01:02:03 011:005:008
[8] row(s) selected.

Mach> SELECT COUNT(*), DATE_TRUNC('nsec', i2, 1000000000) tm FROM trunc_table group by tm ORDER BY 2; //Same as DATE_TRUNC('sec', i2, 1)
COUNT(*)             tm
--------------------------------------------------------
2                    1999-11-11 01:02:00 000:000:000
2                    1999-11-11 01:02:01 000:000:000
2                    1999-11-11 01:02:02 000:000:000
2                    1999-11-11 01:02:03 000:000:000
[4] row(s) selected.
```

時間単位別に許容する範囲は次のとおりです。

* nanosecond、microsecond、millisecond単位とその略称は5.5.6以降で使用できます。
* weekは日曜日から始まります。

|時間単位|時間範囲|
|--|--|
|nanosecond (nsec)|1000000000 (1 second)|
|microsecond (usec)|60000000 (60 seconds)|
|millisecond (msec)|60000 (60 seconds)|
|second (sec)|86400 (1 day)|
|minute (min)|1440 (1 day)|
|hour|24 (1 day)|
|day|1|
|week|1|
|month|1|
|year|1|

例えばDATE_TRUNC('second', time, 120)の結果は**2分単位**となり、DATE_TRUNC('minute', time, 2)と同じです。

## DATE_BIN
指定した基準時刻`origin`を基点に、DATETIME値を`time unit`と`time range`の区間（bin）に割り当てます。

```sql
DATE_BIN(field, count, source [, origin])
```

- `origin`を指定すると、その時刻を基点にバケットを計算します。
- `origin`を省略すると、サーバーのローカルタイムゾーンの`1970-01-01 00:00:00`を基点に計算します。
- `count`は1以上の整数である必要があります。

`DATE_TRUNC()`や`ROLLUP()`と同じローカルタイムゾーンの境界にそろえるには、`origin`を省略した3引数形式を使用します。サーバーのタイムゾーンに関係なく常に同じ境界を使用するには、4引数形式で`origin`を明示してください。

例えばサーバーのタイムゾーンが`UTC+09:00`の場合、従来は`DATE_BIN(..., 0)`の代わりにタイムゾーン補正済みの`origin`値を直接指定してローカル時刻の境界にそろえる必要がありました。現在は`DATE_BIN(field, count, source)`だけで同じ結果を得られます。

```sql
Mach> CREATE LOG TABLE log (time DATETIME);
Created successfully.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 00:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 01:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 02:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 03:00:00'));
1 row(s) inserted.

Mach> INSERT INTO log VALUES (TO_DATE('2000-01-01 04:00:00'));
1 row(s) inserted.

Mach> SELECT TIME, DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00')) FROM log ORDER BY time;
TIME                            DATE_BIN('hour', 2, time, TO_DATE('2020-01-01 00:00:00'))
---------------------------------------------------------------------------------------------
2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 01:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 02:00:00 000:000:000 2000-01-01 02:00:00 000:000:000
2000-01-01 03:00:00 000:000:000 2000-01-01 02:00:00 000:000:000
2000-01-01 04:00:00 000:000:000 2000-01-01 04:00:00 000:000:000
[5] row(s) selected.
```

ローカルタイムゾーンの境界でバケットを計算する例は次のとおりです。

```sql
Mach> CREATE LOG TABLE t3521 (ts DATETIME);
Created successfully.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 00:30:00'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 02:59:59'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 03:00:00'));
1 row(s) inserted.

Mach> INSERT INTO t3521 VALUES (TO_DATE('2000-01-01 08:00:00'));
1 row(s) inserted.

Mach> SELECT ts,
             DATE_BIN('hour', 3, ts) AS date_bin_3arg,
             DATE_TRUNC('hour', ts, 3) AS date_trunc_3arg
        FROM t3521
    ORDER BY ts;
ts                              date_bin_3arg                   date_trunc_3arg
----------------------------------------------------------------------------------------------------
2000-01-01 00:30:00 000:000:000 2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 02:59:59 000:000:000 2000-01-01 00:00:00 000:000:000 2000-01-01 00:00:00 000:000:000
2000-01-01 03:00:00 000:000:000 2000-01-01 03:00:00 000:000:000 2000-01-01 03:00:00 000:000:000
2000-01-01 08:00:00 000:000:000 2000-01-01 06:00:00 000:000:000 2000-01-01 06:00:00 000:000:000
[4] row(s) selected.
```

時間単位別の許容範囲は次のとおりです。

* nanosecond、microsecond、millisecond単位とその略称は5.5.6以降で使用できます。
* weekは7日と同じです。

|時間単位|
|----:|
|nanosecond (nsec)|
|microsecond (usec)|
|millisecond (msec)|
|second (sec)|
|minute (min)|
|hour|
|day|
|week|
|month|
|year|


## DAYOFWEEK

DATETIME値の曜日を整数で返します。

[TO_CHAR (time, 'DAY')](#to_char)と意味は同じですが、この関数は整数を返します。

```sql
DAYOFWEEK(date_val)
```

返される整数は、次の表の曜日を表します。

| 戻り値 | 曜日 |
|--|--|
|0|日曜日|
|1|月曜日|
|2|火曜日|
|3|水曜日|
|4|木曜日|
|5|金曜日|
|6|土曜日|


## DECODE

列値をsearch値と比較し、一致すると対応するreturn値を返します。一致するsearch値がなければdefault値を、defaultを省略した場合はNULLを返します。

```sql
DECODE(column, [search, return],.. default)
```

```sql
Mach> CREATE LOG TABLE decode_table (id1 VARCHAR(11));
Created successfully.

Mach> INSERT INTO decode_table VALUES('decodetest1');
1 row(s) inserted.

Mach> INSERT INTO decode_table VALUES('decodetest2');
1 row(s) inserted.

Mach> SELECT id1, DECODE(id1, 'decodetest1', 'result1', 'decodetest2', 'result2', 'DEFAULT') FROM decode_table;
id1          DECODE(id1, 'decodetest1', 'result1', 'decodetest2', 'result2', 'DEFAULT')
---------------------------------------------------------
decodetest2  result2
decodetest1  result1
[2] row(s) selected.

Mach> SELECT id1, DECODE(id1, 'codetest', 2, 99) FROM decode_table;
id1          DECODE(id1, 'codetest', 2, 99)
-----------------------------------------------
decodetest2  99
decodetest1  99
[2] row(s) selected.

Mach> SELECT DECODE(id1, 'decodetest1', 2) FROM decode_table;
DECODE(id1, 'decodetest1', 2)
--------------------------------
NULL
2
[2] row(s) selected.

Mach> SELECT DECODE(id1, 'codetest', 2) FROM decode_table;
DECODE(id1, 'codetest', 2)
-----------------------------
NULL
NULL
[2] row(s) selected.
```


## EXTRACT_*

バイナリフレームからビットを抽出する関数群です。`EXTRACT_*`はビッグエンディアン、`EXTRACT_LE_*`はリトルエンディアンを使用します。すべての関数は`BINARY/VARBINARY`を入力に取り、frameがNULLなら結果もNULLです。

**エンディアンモデル**

- `EXTRACT_*`: MSB優先（`bit 0`は`byte[0]`のMSB）
- `EXTRACT_LE_*`: LSB優先（`bit 0`は`byte[0]`のLSB）
- ビットの添字はフレーム全体を基準とする0始まりです。

**共通規則**

- 単一ビット: `0 <= bit_pos < frame_bits`
- 範囲抽出: `start_bit >= 0`、`1 <= bit_count <= 64`、`start_bit + bit_count <= frame_bits`
- `EXTRACT_FLOAT*`は32ビット、`EXTRACT_DOUBLE*`は64ビットを読み取ります。
- 符号付き抽出は2の補数（two's complement）として解釈し、64ビットへ符号拡張します。
- 範囲エラー: `ERR_QP_INVALID_ARG_VALUE`（`ERR-02229`系）
- 引数の型エラー: `ERR_QP_FUNCTION_ARG_TYPE`

### EXTRACT_BIT

```
EXTRACT_BIT(frame, bit_pos) / EXTRACT_LE_BIT(frame, bit_pos) → TINYINT
```

単一ビットを0または1で返します。

```sql
-- frame = 0x80 (1000 0000)
SELECT EXTRACT_BIT(frame, 0)    AS be_bit0,
       EXTRACT_LE_BIT(frame, 0) AS le_bit0
FROM t;
```

### EXTRACT_LONG, EXTRACT_ULONG

```
EXTRACT_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LE_ULONG(frame, start_bit, bit_count) → BIGINT UNSIGNED
EXTRACT_LONG(frame, start_bit, bit_count) → BIGINT
EXTRACT_LE_LONG(frame, start_bit, bit_count) → BIGINT
```

1~64ビットを符号なし整数、または2の補数の整数として読み取ります。

```sql
-- frame = 0x12 34
SELECT EXTRACT_ULONG(frame, 0, 16)    AS be_u16,  -- 0x1234
       EXTRACT_LE_ULONG(frame, 0, 16) AS le_u16   -- 0x3412
FROM t;
```

### EXTRACT_FLOAT,EXTRACT_DOUBLE

```
EXTRACT_FLOAT(frame, start_bit) → FLOAT
EXTRACT_LE_FLOAT(frame, start_bit) → FLOAT
EXTRACT_DOUBLE(frame, start_bit) → DOUBLE
EXTRACT_LE_DOUBLE(frame, start_bit) → DOUBLE
```

32/64ビットをIEEE754のfloat/doubleとして再解釈します。指定したビット範囲はframe内に収まる必要があります。

```sql
SELECT EXTRACT_FLOAT(frame, 0)      AS be_f32,
       EXTRACT_LE_FLOAT(frame, 0)   AS le_f32,
       EXTRACT_DOUBLE(frame, 64)    AS be_f64,
       EXTRACT_LE_DOUBLE(frame, 64) AS le_f64
FROM sensor_bin;
```

### EXTRACT_SCALED_DOUBLE

```
EXTRACT_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
EXTRACT_LE_SCALED_DOUBLE(frame, start_bit, bit_count, signed, scale, offset) → DOUBLE
```

1~64ビットを、`signed=0`なら符号なし値、`signed=1`なら2の補数の符号付き値として読み取り、`raw * scale + offset`を返します。

```sql
-- 20ビットのセンサー値、scale 0.01、offset -40.0
SELECT EXTRACT_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0)    AS be_value,
       EXTRACT_LE_SCALED_DOUBLE(frame, 0, 20, 0, 0.01, -40.0) AS le_value
FROM t_bin;
```


## FIRST / LAST

各グループを基準値でソートしたとき、最初または最後のレコードの特定の値を返す集約関数です。

* FIRST: ソート順で最初のレコードの値を返します。
* LAST: ソート順で最後のレコードの値を返します。

```sql
FIRST(sort_expr, return_expr)
LAST(sort_expr, return_expr)
```

```sql
Mach> create table firstlast_table (id integer, name varchar(20), group_no integer);
Created successfully.
Mach> insert into firstlast_table values (1, 'John', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (2, 'Grey', 1);
1 row(s) inserted.
Mach> insert into firstlast_table values (5, 'Ryan', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (4, 'Andrew', 0);
1 row(s) inserted.
Mach> insert into firstlast_table values (7, 'Kyle', 1);
1 row(s) inserted.
Mach> insert into firstlast_table values (6, 'Ross', 1);
1 row(s) inserted.

Mach> select group_no, first(id, name) from firstlast_table group by group_no;
group_no    first(id, name)
-------------------------------------
1           Grey
0           John
[2] row(s) selected.


Mach> select group_no, last(id, name) from firstlast_table group by group_no;
group_no    last(id, name)
-------------------------------------
1           Kyle
0           Ryan
```


## FROM_TIMESTAMP

1970-01-01 00:00:00 UTCからの経過ナノ秒数をdatetime型へ変換します。

TO_TIMESTAMP()は、datetime型を同じ基準時点からの経過ナノ秒数へ変換します。

基準時点はUTC+09:00では1970-01-01 09:00:00と表示されます。次の例の日付と時刻はUTC+09:00基準です。

```sql
FROM_TIMESTAMP(nanosecond_time_value)
```

```sql
Mach> SELECT FROM_TIMESTAMP(1562302560007248869);
FROM_TIMESTAMP(1562302560007248869)
--------------------------------------
2019-07-05 13:56:00 007:248:869
```

`SYSDATE`と`NOW`は現在時刻を表すDATETIME値です。次の例は現在時刻をそのまま変換する場合と、1ミリ秒（1,000,000ナノ秒）を引く場合を示します。

```sql
Mach> select sysdate, from_timestamp(sysdate) from test_tbl;
sysdate                         from_timestamp(sysdate)
-------------------------------------------------------------------
2019-07-05 14:00:59 722:822:443 2019-07-05 14:00:59 722:822:443
[1] row(s) selected.

Mach> select sysdate, from_timestamp(sysdate-1000000) from test_tbl;
sysdate                         from_timestamp(sysdate-1000000)
-------------------------------------------------------------------
2019-07-05 14:01:05 130:939:525 2019-07-05 14:01:05 129:939:525      -- 1 ms (1,000,000 ns) の差がある
[1] row(s) selected.
```


## FROM_UNIXTIME

整数で入力した32ビットUNIXTIME値をdatetime型へ変換します。UNIX_TIMESTAMPはdatetimeデータを32ビットUNIXTIME整数へ変換します。

次の例の日付と時刻はUTC+09:00基準です。

```sql
FROM_UNIXTIME(unix_timestamp_value)
```

```sql
Mach> SELECT FROM_UNIXTIME(315540671) FROM TEST;
FROM_UNIXTIME(315540671)
----------------------------------
1980-01-01 11:11:11 000:000:000

Mach> SELECT FROM_UNIXTIME(UNIX_TIMESTAMP('2001-01-01')) FROM unix_table;
FROM_UNIXTIME(UNIX_TIMESTAMP('2001-01-01'))
------------------------------------------
2001-01-01 00:00:00 000:000:000
```


## GROUP_CONCAT

グループ内の列値を文字列として連結して返す集約関数です。

{{< callout type="warning" >}}
Cluster Editionでは使用できません。
{{< /callout >}}

```sql
GROUP_CONCAT(
     [DISTINCT] column
     [ORDER BY { unsigned_integer | column }
     [ASC | DESC] [, column ...]]
     [SEPARATOR str_val]
)
```

* DISTINCT: 重複値は1回のみ連結します。
* ORDER BY: 指定列の値で連結順序をソートします。
* SEPARATOR: 列値の連結に使用する区切り文字列です。デフォルトはカンマ（,）です。

構文に関する注意事項は次のとおりです。

* 指定できる列は1つのみです。複数列を連結する場合は、TO_CHAR()とCONCAT演算子（||）で1つの式にまとめてください。
* ORDER BYには連結対象以外の列も指定でき、複数列の指定も可能です。
* SEPARATORには文字列定数のみ指定でき、文字列列は指定できません。

```sql
Mach> CREATE LOG TABLE concat_table(id1 INTEGER, id2 DOUBLE, name VARCHAR(10));
Created successfully.

Mach> INSERT INTO concat_table VALUES (1, 2, 'John');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (2, 1, 'Ram');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (3, 2, 'Zara');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (4, 2, 'Jill');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (5, 1, 'Jack');
1 row(s) inserted.

Mach> INSERT INTO concat_table VALUES (6, 1, 'Jack');
1 row(s) inserted.


Mach> SELECT GROUP_CONCAT(name) AS G_NAMES FROM concat_table GROUP BY id2;
G_NAMES
------------------------------------------------------------------------------------
Jack,Jack,Ram
Jill,Zara,John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(DISTINCT name) AS G_NAMES FROM concat_table GROUP BY Id2;
G_NAMES
------------------------------------------------------------------------------------
Jack,Ram
Jill,Zara,John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(name SEPARATOR '.') G_NAMES FROM concat_table GROUP BY Id2;
G_NAMES
------------------------------------------------------------------------------------
Jack.Jack.Ram
Jill.Zara.John
[2] row(s) selected.

Mach> SELECT GROUP_CONCAT(name ORDER BY id1) G_NAMES, GROUP_CONCAT(id1 ORDER BY id1) G_SORTID FROM concat_table GROUP BY id2;
G_NAMES
------------------------------------------------------------------------------------
G_SORTID
------------------------------------------------------------------------------------
Ram,Jack,Jack
2,5,6
John,Zara,Jill
1,3,4
[2] row(s) selected.
```


## INSTR

対象文字列内でパターン文字列が始まる位置を返します。位置は1始まりです。

* パターンがなければ0を返します。
* 検索パターンの長さが0、またはNULLの場合はNULLを返します。

```sql
INSTR(target_string, pattern_string)
```

```sql
Mach> CREATE LOG TABLE string_table(c1 VARCHAR(20));
Created successfully.

Mach> INSERT INTO string_table VALUES ('abstract');
1 row(s) inserted.

Mach> INSERT INTO string_table VALUES ('override');
1 row(s) inserted.

Mach> SELECT c1, INSTR(c1, 'act') FROM string_table;
c1                    INSTR(c1, 'act')
------------------------------------------
override              0
abstract              6
[2] row(s) selected.
```


## LEAST / GREATEST

複数の列/値を入力すると、LEASTは最小値、GREATESTは最大値を返します。

入力値が1つ、またはない場合はエラーです。入力値がNULLならNULLを返すため、入力が列の場合は事前に関数で変換してください。比較できない列（BLOB、TEXTなど）が含まれる場合や、比較のための型変換ができない場合はエラーです。

```sql
LEAST(value_list, value_list,...)
GREATEST(value_list, value_list,...)
```

```sql
Mach> CREATE LOG TABLE lgtest_table(c1 INTEGER, c2 LONG, c3 VARCHAR(10), c4 VARCHAR(5));
Created successfully.

Mach> INSERT INTO lgtest_table VALUES (1, 2, 'abstract', 'ace');
1 row(s) inserted.

Mach> INSERT INTO lgtest_table VALUES (null, 100, null, 'bag');
1 row(s) inserted.

Mach> SELECT LEAST (c1, c2) FROM lgtest_table;
LEAST (c1, c2)
-----------------------
NULL
1
[2] row(s) selected.

Mach> SELECT LEAST (c1, c2, -1) FROM lgtest_table;
LEAST (c1, c2, -1)
-----------------------
NULL
-1
[2] row(s) selected.

Mach> SELECT GREATEST(c3, c4) FROM lgtest_table;
GREATEST(c3, c4)
--------------------
NULL
ace
[2] row(s) selected.

Mach> SELECT LEAST(c3, c4) FROM lgtest_table;
LEAST(c3, c4)
-----------------
NULL
abstract
[2] row(s) selected.

Mach> SELECT LEAST(NVL(c3, 'aa'), c4) FROM lgtest_table;
LEAST(NVL(c3, 'aa'), c4)
----------------------------
aa
abstract
[2] row(s) selected.
```


## LENGTH

文字列列の長さを返します。戻り値は英字（ASCII）を基準とするバイト数です。

```sql
LENGTH(column_name)
```

```sql
Mach> CREATE LOG TABLE length_table (id1 INTEGER, id2 DOUBLE, name VARCHAR(15));
Created successfully.

Mach> INSERT INTO length_table VALUES(1, 10, 'Around the Horn');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(NULL, 20, 'Alfreds Futterkiste');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(3, NULL, 'Antonio Moreno');
1 row(s) inserted.

Mach> INSERT INTO length_table VALUES(4, 40, NULL);
1 row(s) inserted.

Mach> select * FROM length_table;
ID1         ID2                         NAME
-------------------------------------------------------------
4           40                          NULL
3           NULL                        Antonio Moreno
NULL        20                          Alfreds Futterk
1           10                          Around the Horn
[4] row(s) selected.

Mach> select id1 * 10 FROM length_table;
id1 * 10
-----------------------
40
30
NULL
10
[4] row(s) selected.

Mach> select * FROM length_table Where id1 > 1 and id2 < 50;
ID1         ID2                         NAME
-------------------------------------------------------------
4           40                          NULL
[1] row(s) selected.

Mach> select name || ' with null concat' FROM length_table;
name || ' with null concat'
------------------------------------
NULL
Antonio Moreno with null concat
Alfreds Futterk with null concat
Around the Horn with null concat
[4] row(s) selected.

Mach> select LENGTH(name) FROM length_table;
LENGTH(name)
---------------
NULL
14
15
15
[4] row(s) selected.
```


## LOWER

英字文字列を小文字へ変換します。

```sql
LOWER(column_name)
```

```sql
Mach> CREATE LOG TABLE lower_table (name VARCHAR(20));
Created successfully.

Mach> INSERT INTO lower_table VALUES('');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('James Backley');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('Alfreds Futterkiste');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES('Antonio MORENO');
1 row(s) inserted.

Mach> INSERT INTO lower_table VALUES (NULL);
1 row(s) inserted.

Mach> SELECT LOWER(name) FROM lower_table;
LOWER(name)
------------------------
NULL
antonio moreno
alfreds futterkiste
james backley
NULL
[5] row(s) selected.
```


## LPAD / RPAD

入力文字列が指定の長さになるまで、左側（LPAD）または右側（RPAD）に文字を埋めます。

最後のパラメーターcharは省略可能で、省略すると空白（' '）で埋めます。入力が指定長より長い場合は文字を追加せず、先頭から指定の長さだけ返します。

```sql
LPAD(str, len, padstr)
RPAD(str, len, padstr)
```

```sql
Mach> CREATE LOG TABLE pad_table (c1 integer, c2 varchar(15));
Created successfully.

Mach> INSERT INTO pad_table VALUES (1, 'Antonio');
1 row(s) inserted.

Mach> INSERT INTO pad_table VALUES (25, 'Johnathan');
1 row(s) inserted.

Mach> INSERT INTO pad_table VALUES (30, 'M');
1 row(s) inserted.

Mach> SELECT LPAD(to_char(c1), 5, '0') FROM pad_table;
LPAD(to_char(c1), 5, '0')
-----------------------------
00030
00025
00001
[3] row(s) selected.

Mach> SELECT RPAD(to_char(c1), 5, '0') FROM pad_table;
RPAD(to_char(c1), 5, '0')
-----------------------------
30000
25000
10000
[3] row(s) selected.

Mach> SELECT LPAD(c2, 5) FROM pad_table;
LPAD(c2, 5)
---------------
    M
Johna
Anton
[3] row(s) selected.

Mach> SELECT RPAD(c2, 5) FROM pad_table;
RPAD(c2, 5)
---------------
M
Johna
Anton
[3] row(s) selected.

Mach> SELECT RPAD(c2, 10, '***') FROM pad_table;
RPAD(c2, 10, '***')
-----------------------
M*********
Johnathan*
Antonio***
[3] row(s) selected.
```


## LTRIM / RTRIM

第1引数からパターン文字列に含まれる文字を削除します。LTRIMは左から、RTRIMは右から検査し、パターンにない文字に達すると停止します。すべての文字がパターンに含まれる場合はNULLを返します。

パターンを省略すると、空白（' '）を削除します。

```sql
LTRIM(column_name, pattern)
RTRIM(column_name, pattern)
```

```sql
Mach> CREATE LOG TABLE trim_table1(name VARCHAR(10));
Created successfully.

Mach> INSERT INTO trim_table1 VALUES ('   smith   ');
1 row(s) inserted.

Mach> SELECT ltrim(name) FROM trim_table1;
ltrim(name)
---------------
smith
[1] row(s) selected.

Mach> SELECT rtrim(name) FROM trim_table1;
rtrim(name)
---------------
   smith
[1] row(s) selected.

Mach> SELECT ltrim(name, ' s') FROM trim_table1;
ltrim(name, ' s')
---------------------
mith
[1] row(s) selected.

Mach> SELECT rtrim(name, 'h ') FROM trim_table1;
rtrim(name, 'h ')
---------------------
   smit
[1] row(s) selected.

Mach> CREATE LOG TABLE trim_table2 (name VARCHAR(10));
Created successfully.

Mach> INSERT INTO trim_table2 VALUES ('ddckaaadkk');
1 row(s) inserted.

Mach> SELECT ltrim(name, 'dc') FROM trim_table2;
ltrim(name, 'dc')
---------------------
kaaadkk
[1] row(s) selected.

Mach> SELECT rtrim(name, 'dk') FROM trim_table2;
rtrim(name, 'dk')
---------------------
ddckaaa
[1] row(s) selected.

Mach> SELECT ltrim(name, 'dckak') FROM trim_table2;
ltrim(name, 'dckak')
------------------------
NULL
[1] row(s) selected.

Mach> SELECT rtrim(name, 'dckak') FROM trim_table2;
rtrim(name, 'dckak')
------------------------
NULL
[1] row(s) selected.
```


## MAX

指定した数値列の最大値を返す集約関数です。

```sql
MAX(column_name)
```

```sql
Mach> CREATE LOG TABLE max_table (c INTEGER);
Created successfully.

Mach> INSERT INTO max_table VALUES(10);
1 row(s) inserted.

Mach> INSERT INTO max_table VALUES(20);
1 row(s) inserted.

Mach> INSERT INTO max_table VALUES(30);
1 row(s) inserted.

Mach> SELECT MAX(c) FROM max_table;
MAX(c)
--------------
30
[1] row(s) selected.
```


## MEDIAN {#median}

`MEDIAN(value)`は数値式の正確な中央値を返し、`PERCENTILE_CONT(value, 0.5)`と同じ方式で動作します。

```sql
MEDIAN(value)
```

- `value`は数値型である必要があります。
- `NULL`値は無視します。
- 戻り値の型は`DOUBLE`です。

```sql
SELECT MEDIAN(temp_c)
FROM sensor_log;
```


## MIN

指定した数値列の最小値を返す集約関数です。

```sql
MIN(column_name)
```

```sql
Mach> CREATE LOG TABLE min_table(c1 INTEGER);
Created successfully.

Mach> INSERT INTO min_table VALUES(1);
1 row(s) inserted.

Mach> INSERT INTO min_table VALUES(22);
1 row(s) inserted.

Mach> INSERT INTO min_table VALUES(33);
1 row(s) inserted.

Mach> SELECT MIN(c1) FROM min_table;
MIN(c1)
--------------
1
[1] row(s) selected.
```


## NVL

列値がNULLなら指定値で置き換え、NULLでなければ元の値を返します。

```sql
NVL(string1, replace_with)
```

```sql
Mach> CREATE LOG TABLE nvl_table (c1 varchar(10));
Created successfully.

Mach> INSERT INTO nvl_table VALUES ('Johnathan');
1 row(s) inserted.

Mach> INSERT INTO nvl_table VALUES (NULL);
1 row(s) inserted.

Mach> SELECT NVL(c1, 'Thomas') FROM nvl_table;
NVL(c1, 'Thomas')
---------------------
Thomas
Johnathan
```

## NEXTVAL

`NEXTVAL(sequence_column)`は、LookupテーブルのSequence列の次の値を返します。

```sql
NEXTVAL(sequence_column)
```

- `NEXTVAL`は`INSERT`文でのみ使用できます。
- 引数は`PROPERTY(SEQUENCE=...)`で設定された列である必要があります。
- Sequence列の作成と例は[Sequence Column](/dbms/lookup-table-usage/sequence-column/)を参照してください。

```sql
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-a');
```


## ROUND

入力値の指定桁（入力桁数+1）を丸めた結果を返します。桁数を省略すると小数点以下0桁に丸めます。負数を指定して整数部の桁で丸めることもできます。

```sql
ROUND(column_name, [decimals])
```

```sql
Mach> CREATE LOG TABLE round_table (c1 DOUBLE);
Created successfully.

Mach> INSERT INTO round_table VALUES (1.994);
1 row(s) inserted.

Mach> INSERT INTO round_table VALUES (1.995);
1 row(s) inserted.

Mach> SELECT c1, ROUND(c1, 2) FROM round_table;
c1                          ROUND(c1, 2)
-----------------------------------------------------------
1.995                       2
1.994                       1.99
```


## ROWNUM

SELECTの結果行に番号を付けます。

SELECTで使用するサブクエリやインラインビュー内でも使用できます。インラインビューの選択リストでROWNUM()を使用する場合は、外側から参照できるように別名を指定してください。

```sql
ROWNUM()
```

**使用できる句**

SELECTの選択リスト、GROUP BY、ORDER BY句で使用できます。WHEREとHAVING句では使用できません。結果の番号でWHERE/HAVINGを制御するには、インラインビューでROWNUM()を計算してから外側のクエリで参照します。

|使用できる句|使用できない句|
|--|--|
|Target List / GROUP BY / ORDER BY|WHERE / HAVING|

```sql
Mach> CREATE LOG TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO rownum_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(2, 2.0, 'Second Row');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(3, 3.3, 'Third Row');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(4, 4.3, 'Fourth Row');
1 row(s) inserted.

Mach> SELECT INNER_RANK, c3 AS NAME
    2 FROM   (SELECT ROWNUM() AS INNER_RANK, * FROM rownum_table)
    3 WHERE  INNER_RANK < 3;
INNER_RANK           NAME
------------------------------------
1                    Fourth Row
2                    Third Row
[2] row(s) selected.
```

**ソートによる結果番号の変化**

SELECTにORDER BY句がある場合、選択リストのROWNUM()結果が連番にならない場合があります。ROWNUM()がORDER BYより先に処理されるためです。連番が必要な場合は、ORDER BYを含むクエリをインラインビューにして、外側のSELECTでROWNUM()を呼び出してください。

```sql
Mach> CREATE LOG TABLE rownum_table(c1 INTEGER, c2 DOUBLE, c3 VARCHAR(10));
Created successfully.

Mach> INSERT INTO rownum_table VALUES(1, 1.0, '');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(2, 2.0, 'John');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(3, 3.3, 'Sarah');
1 row(s) inserted.

Mach> INSERT INTO rownum_table VALUES(4, 4.3, 'Micheal');
1 row(s) inserted.

Mach> SELECT ROWNUM(), c2 AS SORT, c3 AS NAME
    2 FROM   ( SELECT * FROM rownum_table ORDER BY c3 );
ROWNUM()             SORT                        NAME
-----------------------------------------------------------------
1                    1                           NULL
2                    2                           John
3                    4.3                         Micheal
4                    3.3                         Sarah
[4] row(s) selected.
```


## SERIESNUM

`SERIES BY`で区別した連続区間のうち、各行が属する区間の番号を返します。同じ区間の行には同じ番号を付けるため、区間内の行番号とは異なります。戻り値の型はBIGINTで、`SERIES BY`句を使用しない場合は常に1を返します。

```sql
SERIESNUM()
```

```sql
Mach> CREATE LOG TABLE T1 (C1 INTEGER, C2 INTEGER);
Created successfully.

Mach> INSERT INTO T1 VALUES (0, 1);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (2, 3);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (3, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (4, 1);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (5, 2);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (6, 3);
1 row(s) inserted.

Mach> INSERT INTO T1 VALUES (7, 1);
1 row(s) inserted.


Mach> SELECT SERIESNUM(), C1, C2 FROM T1 ORDER BY C1 SERIES BY C2 > 1;
SERIESNUM() C1 C2
-------------------------------------------------
1 1 2
1 2 3
1 3 2
2 5 2
2 6 3
[5] row(s) selected.
```


## STDDEV / STDDEV_POP

入力列の標本標準偏差（STDDEV）と母標準偏差（STDDEV_POP）を返す集約関数です。それぞれVARIANCE、VAR_POPの平方根です。

```sql
STDDEV(column)
STDDEV_POP(column)
```

```sql
Mach> CREATE LOG TABLE stddev_table(c1 INTEGER, C2 DOUBLE);

Mach> INSERT INTO stddev_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (2, 1);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (3, 2);
1 row(s) inserted.

Mach> INSERT INTO stddev_table VALUES (4, 2);
1 row(s) inserted.

Mach> SELECT c2, STDDEV(c1) FROM stddev_table GROUP BY c2;
c2                          STDDEV(c1)
-----------------------------------------------------------
1                           0.707107
2                           0.707107
[2] row(s) selected.

Mach> SELECT c2, STDDEV_POP(c1) FROM stddev_table GROUP BY c2;
c2                          STDDEV_POP(c1)
-----------------------------------------------------------
1                           0.5
2                           0.5
[2] row(s) selected.
```


## SUBSTR

文字列列のSTART位置からSIZEの長さの部分文字列を返します。

* STARTは1始まりで、0の場合はNULLを返します。
* SIZEがSTART位置からの残りの文字列長より大きい場合は、START位置から末尾まで返します。
SIZEは省略可能で、省略すると文字列長を使用します。

```sql
SUBSTRING(column_name, start, [length])
```

```sql
Mach> CREATE LOG TABLE substr_table (c1 VARCHAR(10));
Created successfully.

Mach> INSERT INTO substr_table values('ABCDEFG');
1 row(s) inserted.

Mach> INSERT INTO substr_table values('abstract');
1 row(s) inserted.

Mach> SELECT SUBSTR(c1, 1, 1) FROM substr_table;
SUBSTR(c1, 1, 1)
--------------------
a
A
[2] row(s) selected.

Mach> SELECT SUBSTR(c1, 3, 3) FROM substr_table;
SUBSTR(c1, 3, 3)
--------------------
str
CDE
[2] row(s) selected.

Mach> SELECT SUBSTR(c1, 2) FROM substr_table;
SUBSTR(c1, 2)
-----------------
bstract
BCDEFG
[2] row(s) selected.

Mach> drop table substr_table;
Dropped successfully.

Mach> CREATE LOG TABLE substr_table (c1 VARCHAR(10));
Created successfully.

Mach> INSERT INTO substr_table values('ABCDEFG');
1 row(s) inserted.

Mach> SELECT SUBSTR(c1, 1, 1) FROM substr_table;
SUBSTR(c1, 1, 1)
--------------------
A
[1] row(s) selected.

Mach> SELECT SUBSTR(c1, 3, 3) FROM substr_table;
SUBSTR(c1, 3, 3)
--------------------
CDE
[1] row(s) selected.

Mach> SELECT SUBSTR(c1, 2) FROM substr_table;
SUBSTR(c1, 2)
-----------------
BCDEFG
[1] row(s) selected.
```


## SUBSTRING_INDEX

指定したcount回だけ区切り文字delimを見つけるまでの部分文字列を返します。countが負数の場合は文字列の末尾から区切り文字を探し、見つけた位置から末尾まで返します。

countが0ならNULLを返します。countが0以外で文字列に区切り文字がなければ、入力文字列全体を返します。

```sql
SUBSTRING_INDEX(expression, delim, count)
```

```sql
Mach> CREATE LOG TABLE substring_table (url VARCHAR(30));
Created successfully.

Mach> INSERT INTO substring_table VALUES('www.machbase.com');
1 row(s) inserted.

Mach> SELECT SUBSTRING_INDEX(url, '.', 1) FROM substring_table;
SUBSTRING_INDEX(url, '.', 1)
----------------------------------
www
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', 2) FROM substring_table;
SUBSTRING_INDEX(url, '.', 2)
----------------------------------
www.machbase
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', -1) FROM substring_table;
SUBSTRING_INDEX(url, '.', -1)
----------------------------------
com
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(url, '.', 2), '.', -1) FROM substring_table;
SUBSTRING_INDEX(SUBSTRING_INDEX(url, '.', 2), '.', -1)
-------------------------------------------
machbase
[1] row(s) selected.

Mach> SELECT SUBSTRING_INDEX(url, '.', 0) FROM substring_table;
SUBSTRING_INDEX(url, '.', 0)
----------------------------------
NULL
[1] row(s) selected.
```


## SUM

数値列の合計を返す集約関数です。

```sql
SUM(column_name)
```

```sql
Mach> CREATE LOG TABLE sum_table (c1 INTEGER, c2 INTEGER);
Created successfully.

Mach> INSERT INTO sum_table VALUES(1, 1);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(1, 2);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(1, 3);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 1);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 2);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(2, 3);
1 row(s) inserted.

Mach> INSERT INTO sum_table VALUES(3, 4);
1 row(s) inserted.

Mach> SELECT c1, SUM(c1) from sum_table group by c1;
c1          SUM(c1)
------------------------------------
2           6
3           3
1           3
[3] row(s) selected.

Mach> SELECT c1, SUM(c2) from sum_table group by c1;
c1          SUM(c2)
------------------------------------
2           6
3           4
1           6
[3] row(s) selected.
```


## SUMSQ

SUMSQは数値の二乗和を返します。

```sql
SUMSQ(value)
```

```sql
Mach> CREATE LOG TABLE sumsq_table (c1 INTEGER, c2 INTEGER);
Created successfully.

Mach> INSERT INTO sumsq_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (1, 3);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (2, 4);
1 row(s) inserted.

Mach> INSERT INTO sumsq_table VALUES (2, 5);
1 row(s) inserted.

Mach> SELECT c1, SUMSQ(c2) FROM sumsq_table GROUP BY c1;
c1          SUMSQ(c2)
------------------------------------
2           41
1           14
[2] row(s) selected.
```


## SYSDATE / NOW

SYSDATEは関数ではなく疑似列で、現在のシステム時刻を返します。

NOWはSYSDATEと同じ機能で、利便性のために提供します。

```sql
SYSDATE
NOW
```

```sql
Mach> SELECT SYSDATE, NOW FROM t1;

SYSDATE                         NOW
-------------------------------------------------------------------
2017-01-16 14:14:53 310:973:000 2017-01-16 14:14:53 310:973:000
```


## TO_CHAR

指定データ型を文字列型へ変換します。型に応じてformat_stringを指定できますが、バイナリ型には使用できません。

```sql
TO_CHAR(column)
```

**TO_CHAR: 基本データ型**

基本データ型は次のように文字列へ変換します。

```sql
Mach> CREATE LOG TABLE fixed_table (id1 SHORT, id2 INTEGER, id3 LONG, id4 FLOAT, id5 DOUBLE, id6 IPV4, id7 IPV6, id8 VARCHAR (128));
Created successfully.

Mach> INSERT INTO fixed_table values(200, 19234, 1234123412, 3.14, 7.8338, '192.168.0.1', '::127.0.0.1', 'log varchar');
1 row(s) inserted.

Mach> SELECT '[ ' || TO_CHAR(id1) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id1) || ' ]'
------------------------------------------------------------------------------------
[ 200 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id2) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id2) || ' ]'
------------------------------------------------------------------------------------
[ 19234 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id3) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id3) || ' ]'
------------------------------------------------------------------------------------
[ 1234123412 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id4) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id4) || ' ]'
------------------------------------------------------------------------------------
[ 3.140000 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id5) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id5) || ' ]'
------------------------------------------------------------------------------------
[ 7.833800 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id6) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id6) || ' ]'
------------------------------------------------------------------------------------
[ 192.168.0.1 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id7) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id7) || ' ]'
------------------------------------------------------------------------------------
[ 0000:0000:0000:0000:0000:0000:7F00:0001 ]
[1] row(s) selected.

Mach> SELECT '[ ' || TO_CHAR(id8) || ' ]' FROM fixed_table;
'[ ' || TO_CHAR(id8) || ' ]'
------------------------------------------------------------------------------------
[ log varchar ]
[1] row(s) selected.
```

**TO_CHAR: 浮動小数点数**

* バージョン5.5.6以降でサポート

floatとdouble値を文字列へ変換します。書式指定子は繰り返して使用できず、'[letter][number]'形式で指定します。

| 書式指定子 | 説明 |
|--|--|
|F / f|列値の小数桁数を指定します。最大値は30です。|
|N / n|小数桁数を指定し、整数部の3桁ごとにカンマ（,）を挿入します。最大値は30です。|

```sql
Mach> create table float_table (i1 float, i2 double);
Created successfully.

Mach> insert into float_table values (1.23456789, 1234.5678901234567890);
1 row(s) inserted.

Mach> select TO_CHAR(i1, 'f8'), TO_CHAR(i2, 'N9') from float_table;
TO_CHAR(i1, 'f8')       TO_CHAR(i2, 'N9')
--------------------------------------------------------------
1.23456788              1,234.567890123
[1] row(s) selected.
```

**TO_CHAR: DATETIME型**

datetime列の値を指定形式の文字列へ変換する関数です。さまざまな文字列を生成し、組み合わせることができます。

format_stringを省略すると、デフォルトは"YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn"です。

| 書式指定子 | 説明 |
|--|--|
|YYYY|年を4桁の数値へ変換します。|
|YY|年を2桁の数値へ変換します。|
|MM|月を2桁の数値へ変換します。|
|MON|月を英語3文字の略称へ変換します（例: JAN, FEB, MAY, ...）。|
|DD|日を2桁の数値へ変換します。|
|DAY|曜日を英語3文字の略称へ変換します（例: SUN, MON, ...）。|
|IW|ISO 8601に従い、曜日を考慮して年内の週番号を`1~53`へ変換します。<br> - 週は月曜日から始まります。<br> - 最初の週を前年の最終週とみなす場合があります。同様に、最終週を翌年の最初の週とみなす場合もあります。<br>詳細はISO 8601を参照してください。|
|WW|曜日を考慮せず、年内の週番号を`1~53`へ変換します。<br>例えば`1月1日~1月7日`は1になります。|
|W|曜日を考慮せず、月内の週番号を`1~5`へ変換します。<br>例えば`3月1日~3月7日`は1になります。|
|HH|時を2桁の数値へ変換します。|
|HH12|時を`1~12`の範囲の2桁の数値へ変換します。|
|HH24|時を`00~23`の範囲の2桁の数値へ変換します。|
|HH2, HH3, HH6|HHの後の数値単位で時を切り捨てます。<br><br>例えばHH6では`0~5`を0、`6~11`を6と表示します。<br>時系列統計の計算に便利です。<br>24時間制で表示します。|
|MI|分を2桁の数値で表示します。|
|MI2, MI5, MI10, MI20, MI30|MIの後の数値単位で分を切り捨てます。<br><br>例えばMI30では`0~29`分を0、`30~59`分を30と表示します。<br>時系列統計の計算に便利です。|
|SS|秒を2桁の数値で表示します。|
|SS2, SS5, SS10, SS20, SS30|SSの後の数値単位で秒を切り捨てます。<br><br>例えばSS30では`0~29`秒を0、`30~59`秒を30と表示します。<br>時系列統計の計算に便利です。|
|AM|時刻をAM/PMで表示します。|
|mmm|ミリ秒を3桁の数値で表示します。<br><br>範囲は`0~999`です。|
|uuu|マイクロ秒を3桁の数値で表示します。<br><br>範囲は`0~999`です。|
|nnn|ナノ秒を3桁の数値で表示します。<br><br>範囲は`0~999`です。|

```sql
Mach> CREATE LOG TABLE datetime_table (id integer, dt datetime);
Created successfully.

Mach> INSERT INTO  datetime_table values(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(2, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(3, TO_DATE('2013-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  datetime_table values(4, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> SELECT id, dt FROM datetime_table WHERE dt > TO_DATE('2000-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 11:22:33 444:555:666
3           2013-11-11 01:02:03 004:005:006
2           2012-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT id, dt FROM datetime_table WHERE dt > TO_DATE('2013-11-11 1:2:3') and dt < TO_DATE('2014-11-11 1:2:3');
id          dt
-----------------------------------------------
3           2013-11-11 01:02:03 004:005:006
[1] row(s) selected.

Mach> SELECT id, TO_CHAR(dt) FROM datetime_table;
id          TO_CHAR(dt)
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33 444:555:666
3           2013-11-11 01:02:03 004:005:006
2           2012-11-11 01:02:03 004:005:006
1           1999-11-11 01:02:03 004:005:006
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY')
-------------------------------------------------------------------------------------------------
4           2014
3           2013
2           2012
1           1999
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM')
-------------------------------------------------------------------------------------------------
4           2014-12
3           2013-11
2           2012-11
1           1999-11
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD')
-------------------------------------------------------------------------------------------------
4           2014-12-30
3           2013-11-11
2           2012-11-11
1           1999-11-11
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD TO_CHAR') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD TO_CHAR')
-------------------------------------------------------------------------------------------------
4           2014-12-30 TO_CHAR
3           2013-11-11 TO_CHAR
2           2012-11-11 TO_CHAR
1           1999-11-11 TO_CHAR
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS')
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33
3           2013-11-11 01:02:03
2           2012-11-11 01:02:03
1           1999-11-11 01:02:03
[4] row(s) selected.

Mach> SELECT id, TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.uuu.nnn') FROM datetime_table;
id          TO_CHAR(dt, 'YYYY-MM-DD HH24:MI:SS mmm.
-------------------------------------------------------------------------------------------------
4           2014-12-30 11:22:33 444.555.666
3           2013-11-11 01:02:03 004.005.006
2           2012-11-11 01:02:03 004.005.006
1           1999-11-11 01:02:03 004.005.006
[4] row(s) selected.
```

**TO_CHAR: 非対応の型**

現在TO_CHARはバイナリ型をサポートしません。

通常の文字列に変換できないためです。画面で確認するには、TO_HEX()関数で16進値を表示してください。


## TO_DATE

指定した書式文字列に従って文字列をdatetime型へ変換します。

format_stringを省略すると、デフォルトは"YYYY-MM-DD HH24: MI: SS mmm: uuu: nnn"です。

```sql
-- default format is "YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn" if no format exists.
TO_DATE(date_string [, format_string])
```

```sql
Mach> CREATE LOG TABLE to_date_table (id INTEGER, dt datetime);
Created successfully.

Mach> INSERT INTO  to_date_table VALUES(1, TO_DATE('1999-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(2, TO_DATE('2012-11-11 1:2:3 4:5:6'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(3, TO_DATE('2014-12-30 11:22:33 444:555:666'));
1 row(s) inserted.

Mach> INSERT INTO  to_date_table VALUES(4, TO_DATE('2014-12-30 23:22:34 777:888:999', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn'));
1 row(s) inserted.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('1999-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 23:22:34 777:888:999
3           2014-12-30 11:22:33 444:555:666
2           2012-11-11 01:02:03 004:005:006
1           1999-11-11 01:02:03 004:005:006
[4] row(s) selected.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('2000-11-11 1:2:3 4:5:0');
id          dt
-----------------------------------------------
4           2014-12-30 23:22:34 777:888:999
3           2014-12-30 11:22:33 444:555:666
2           2012-11-11 01:02:03 004:005:006
[3] row(s) selected.

Mach> SELECT id, dt FROM to_date_table WHERE dt > TO_DATE('2012-11-11 1:2:3','YYYY-MM-DD HH24:MI:SS') and dt < TO_DATE('2014-11-11 1:2:3','YYYY-MM-DD HH24:MI:SS');
id          dt
-----------------------------------------------
2           2012-11-11 01:02:03 004:005:006
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999', 'YYYY') FROM to_date_table LIMIT 1;
id          TO_DATE('1999', 'YYYY')
-----------------------------------------------
4           1999-01-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12', 'YYYY-MM') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12', 'YYYY-MM')
-----------------------------------------------
4           1999.12.01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999', 'YYYY') FROM to_date_table LIMIT 1;
id          TO_DATE('1999', 'YYYY')
-----------------------------------------------
4           1999-01-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12', 'YYYY-MM') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12', 'YYYY-MM')
-----------------------------------------------
4           1999-12-01 00:00:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12', 'YYYY-MM-DD HH24:MI') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12', 'YYYY-MM-DD HH24:MI')
-------------------------------------------------------
4           1999-12-31 13:12:00 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32', 'YYYY-MM-DD HH24:MI:SS')
-------------------------------------------------------
4           1999-12-31 13:12:32 000:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123', 'YYYY-MM-DD HH24:MI:SS mmm') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32 123', 'YYYY-MM-DD HH24:MI:SS mmm')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:000:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123:456', 'YYYY-MM-DD HH24:MI:SS mmm:uuu') FROM to_date_table LIMIT 1;
id          TO_DATE('1999-12-31 13:12:32 123:456', 'YYYY-MM-DD HH24:MI:SS mmm:uuu')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:456:000
[1] row(s) selected.

Mach> SELECT id, TO_DATE('1999-12-31 13:12:32 123:456:789', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn') FROM to_date_table LIMIT 1;
id           TO_DATE('1999-12-31 13:12:32 123:456:789', 'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn')
-------------------------------------------------------
4           1999-12-31 13:12:32 123:456:789
[1] row(s) selected.
```


## TO_DATE_SAFE

TO_DATE()と同様ですが、変換に失敗するとエラーを出さずNULLを返します。

```sql
TO_DATE_SAFE(date_string [, format_string])
```

```sql
Mach> CREATE LOG TABLE date_table (ts DATETIME);
Created successfully.

Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-01-01', 'YYYY-MM-DD'));
1 row(s) inserted.
Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-01-02', 'YYYY'));
1 row(s) inserted.
Mach> INSERT INTO date_table VALUES (TO_DATE_SAFE('2016-12-32', 'YYYY-MM-DD'));
1 row(s) inserted.

Mach> SELECT ts FROM date_table;
ts
----------------------------------
NULL
NULL
2016-01-01 00:00:00 000:000:000
[3] row(s) selected.
```


## TO_HEX

列値がNULLならNULLを返し、NULLでなければ元の値を16進文字列で返します。出力の一貫性のため、short、int、long型はBIG ENDIANへ変換します。

```sql
TO_HEX(column)
```

```sql
Mach> CREATE LOG TABLE hex_table (id1 SHORT, id2 INTEGER, id3 VARCHAR(10), id4 FLOAT, id5 DOUBLE, id6 LONG, id7 IPV4, id8 IPV6, id9 TEXT, id10 BINARY,
id11 DATETIME);
Created successfully.

Mach> INSERT INTO hex_table VALUES(256, 65535, '0123456789', 3.141592, 1024 * 1024 * 1024 * 3.14, 13513135446, '192.168.0.1', '::192.168.0.1', 'textext',
'binary', TO_DATE('1999', 'YYYY'));
1 row(s) inserted.

Mach> SELECT TO_HEX(id1), TO_HEX(id2), TO_HEX(id3), TO_HEX(id4), TO_HEX(id5), TO_HEX(id6), TO_HEX(id7), TO_HEX(id8), TO_HEX(id9), TO_HEX(id10), TO_HEX(id11)
FROM hex_table;
TO_HEX(id1)  TO_HEX(id2)  TO_HEX(id3)            TO_HEX(id4)  TO_HEX(id5)        TO_HEX(id6)        TO_HEX(id7)
-------------------------------------------------------------------------------------------------------------------------
TO_HEX(id8)                          TO_HEX(id9)
--------------------------------------------------------------------------------------------------------------------------
TO_HEX(id10)                                                                      TO_HEX(id11)
--------------------------------------------------------------------------------------------------------
0100   0000FFFF   30313233343536373839   D80F4940   1F85EB51B81EE941   0000000325721556   04C0A80001
06000000000000000000000000C0A80001   74657874657874
62696E617279                                                                      0CB325846E226000
[1] row(s) selected.
```


## TO_INET_STR

`TO_INET_STR(ipv4_value)`は`IPV4`値をドット区切りの10進文字列へ変換します。

```sql
TO_INET_STR(ipv4_value)
```

```sql
SELECT TO_INET_STR(TO_IPV4('192.168.0.1'));
```


## TO_IPV4 / TO_IPV4_SAFE

指定した文字列をIPv4型へ変換します。文字列を数値へ変換できない場合、TO_IPV4()はエラーを返して処理を停止します。

TO_IPV4_SAFE()はエラー時にNULLを返すため、処理を継続できます。

```sql
TO_IPV4(string_value)
TO_IPV4_SAFE(string_value)
```

```sql
Mach> CREATE LOG TABLE ipv4_table (c1 varchar(100));
Created successfully.

Mach> INSERT INTO ipv4_table VALUES('192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipv4_table VALUES('     192.168.0.2    ');
1 row(s) inserted.

Mach> INSERT INTO ipv4_table VALUES(NULL);
1 row(s) inserted.

Mach> SELECT c1 FROM ipv4_table;
c1
------------------------------------------------------------------------------------
NULL
     192.168.0.2
192.168.0.1
[3] row(s) selected.

Mach> SELECT TO_IPV4(c1) FROM ipv4_table;
TO_IPV4(c1)
------------------
NULL
192.168.0.2
192.168.0.1
[3] row(s) selected.

Mach> INSERT INTO ipv4_table VALUES('192.168.0.1.1');
1 row(s) inserted.

Mach> SELECT TO_IPV4(c1) FROM ipv4_table limit 1;
TO_IPV4(c1)
------------------
[ERR-02068 : Invalid IPv4 address format (192.168.0.1.1).]
[0] row(s) selected.

Mach> SELECT TO_IPV4_SAFE(c1) FROM ipv4_table;
TO_IPV4_SAFE(c1)
-------------------
NULL
NULL
192.168.0.2
192.168.0.1
[4] row(s) selected.
```


## TO_IPV6 / TO_IPV6_SAFE

指定した文字列をIPv6型へ変換します。文字列を数値型へ変換できない場合、TO_IPV6()はエラーを返して処理を停止します。

TO_IPV6_SAFE()はエラー時にNULLを返すため、処理を継続できます。

```sql
TO_IPV6(string_value)
TO_IPV6_SAFE(string_value)
```

```sql
Mach> CREATE LOG TABLE ipv6_table (id varchar(100));
Created successfully.

Mach> INSERT INTO ipv6_table VALUES('::0.0.0.0');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0' || '.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('   ::127.0.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('::127.0.0.4  ');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('   ::FFFF:255.255.255.255   ');
1 row(s) inserted.

Mach> INSERT INTO ipv6_table VALUES('21DA:D3:0:2F3B:2AA:FF:FE28:9C5A');
1 row(s) inserted.

Mach> SELECT TO_IPV6(id) FROM ipv6_table;
TO_IPV6(id)
---------------------------------------------------------------
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.2
::127.0.0.1
::
[7] row(s) selected.

Mach> INSERT INTO ipv6_table VALUES('127.0.0.10.10');
1 row(s) inserted.

Mach> SELECT TO_IPV6(id) FROM ipv6_table limit 1;
TO_IPV6(id)
---------------------------------------------------------------
[ERR-02148 : Invalid IPv6 address format.(127.0.0.10.10)]
[0] row(s) selected.

Mach> SELECT TO_IPV6_SAFE(id) FROM ipv6_table;
TO_IPV6_SAFE(id)
---------------------------------------------------------------
NULL
21da:d3::2f3b:2aa:ff:fe28:9c5a
::ffff:255.255.255.255
::127.0.0.4
::127.0.0.3
::127.0.0.2
::127.0.0.1
::
[8] row(s) selected.
```


## TO_NUMBER / TO_NUMBER_SAFE

指定した文字列を数値（double）へ変換します。文字列を数値へ変換できない場合、TO_NUMBER()はエラーを返して処理を停止します。

TO_NUMBER_SAFE()はエラー時にNULLを返すため、処理を継続できます。

```sql
TO_NUMBER(string_value)
TO_NUMBER_SAFE(string_value)
```

```sql
Mach> CREATE LOG TABLE number_table (id varchar(100));
Created successfully.

Mach> INSERT INTO number_table VALUES('10');
1 row(s) inserted.

Mach> INSERT INTO number_table VALUES('20');
1 row(s) inserted.

Mach> INSERT INTO number_table VALUES('30');
1 row(s) inserted.

Mach> SELECT TO_NUMBER(id) from number_table;
TO_NUMBER(id)
------------------------------
30
20
10
[3] row(s) selected.

Mach> CREATE LOG TABLE safe_table (id varchar(100));
Created successfully.

Mach> INSERT INTO safe_table VALUES('invalidnumber');
1 row(s) inserted.

Mach> SELECT TO_NUMBER(id) from safe_table;
TO_NUMBER(id)
------------------------------
[ERR-02145 : The string cannot be converted to number value.(invalidnumber)]
[0] row(s) selected.

Mach> SELECT TO_NUMBER_SAFE(id) from safe_table;
TO_NUMBER_SAFE(id)
------------------------------
NULL
[1] row(s) selected.
```


## TOP_K {#top_k}

`TOP_K(value, k)`は、頻度の高い`k`個の数値を`value:count`形式の文字列で返します。

```sql
TOP_K(value, k)
```

- `value`は数値型である必要があります。
- `k`は正の整数定数である必要があります。
- `NULL`値は無視します。
- 戻り値の型は`VARCHAR`です。
- 頻度の降順、頻度が同じ場合は値の昇順でソートします。

```sql
SELECT TOP_K(alarm_code, 3)
FROM event_log;
```

結果例:

```text
101:532,205:317,301:90
```


## TO_TIMESTAMP

datetime型を1970-01-01 00:00:00 UTCからの経過ナノ秒数へ変換します。

次の例の日付と時刻はUTC+09:00基準です。

```sql
TO_TIMESTAMP(datetime_value)
```

```sql
Mach> create table datetime_tbl (c1 datetime);
Created successfully.

Mach> insert into datetime_tbl values ('2010-01-01 10:10:10');
1 row(s) inserted.

Mach> select to_timestamp(c1) from datetime_tbl;
to_timestamp(c1)
-----------------------
1262308210000000000
[1] row(s) selected.
```


## TRUNC

TRUNC関数は、小数点以下n桁で切り捨てた値を返します。

nを省略すると0とみなし、小数部をすべて取り除きます。nが負数の場合は小数点より前の対応する桁で切り捨てます。

```sql
TRUNC(number [, n])
```

```sql
Mach> CREATE LOG TABLE trunc_table (i1 DOUBLE);
Created successfully.

Mach> INSERT INTO trunc_table VALUES (158.799);
1 row(s) inserted.

Mach> SELECT TRUNC(i1, 1), TRUNC(i1, -1) FROM trunc_table;
TRUNC(i1, 1)                TRUNC(i1, -1)
-----------------------------------------------------------
158.7                       150
[1] row(s) selected.

Mach> SELECT TRUNC(i1, 2), TRUNC(i1, -2) FROM trunc_table;
TRUNC(i1, 2)                TRUNC(i1, -2)
-----------------------------------------------------------
158.79                      100
[1] row(s) selected.
```


## TS_CHANGE_COUNT

特定列の値の変更回数を求める集約関数です。

入力データの時刻順を保証できないため、1) JOIN、2) インラインビューとは併用できません。VARCHAR型はサポートしません。

* **Cluster Editionでは使用できません。**

```sql
TS_CHANGE_COUNT(column)
```

```sql
Mach> CREATE LOG TABLE ipcount_table (id INTEGER, ip IPV4);
Created successfully.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.1');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (1, '192.168.0.2');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.3');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.4');
1 row(s) inserted.

Mach> INSERT INTO ipcount_table VALUES (2, '192.168.0.4');
1 row(s) inserted.

Mach> SELECT id, TS_CHANGE_COUNT(ip) from ipcount_table GROUP BY id;
id          TS_CHANGE_COUNT(ip)
------------------------------------
2           2
1           4
[2] row(s) selected.
```


## UNIX_TIMESTAMP

UNIX_TIMESTAMPは、Unixのtime()システムコールを基準にdate型の値を32ビット整数へ変換する関数です。FROM_UNIXTIMEは逆に整数値をdate型へ変換します。

```sql
UNIX_TIMESTAMP(datetime_value)
```

```sql
Mach> CREATE table unix_table (c1 int);
Created successfully.

Mach> INSERT INTO unix_table VALUES (UNIX_TIMESTAMP('2001-01-01'));
1 row(s) inserted.

Mach> SELECT * FROM unix_table;
C1
--------------
978274800
[1] row(s) selected.
```


## UPPER

英字文字列を大文字へ変換します。

```sql
UPPER(string_value)
```

```sql
Mach> CREATE LOG TABLE upper_table(id INTEGER,name VARCHAR(10));
Created successfully.

Mach> INSERT INTO upper_table VALUES(1, '');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(2, 'James');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(3, 'sarah');
1 row(s) inserted.

Mach> INSERT INTO upper_table VALUES(4, 'THOMAS');
1 row(s) inserted.

Mach> SELECT id, UPPER(name) FROM upper_table;
id          UPPER(name)
----------------------------
4           THOMAS
3           SARAH
2           JAMES
1           NULL
[4] row(s) selected.
```


## VARIANCE / VAR_POP

指定した数値列の分散を返す集約関数です。VARIANCEは標本分散、VAR_POPは母分散を返します。

```sql
VARIANCE(column_name)
VAR_POP(column_name)
```

```sql
Mach> CREATE LOG TABLE var_table(c1 INTEGER, c2 DOUBLE);
Created successfully.

Mach> INSERT INTO var_table VALUES (1, 1);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (2, 1);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (1, 2);
1 row(s) inserted.

Mach> INSERT INTO var_table VALUES (2, 2);
1 row(s) inserted.

Mach> SELECT VARIANCE(c1) FROM var_table;
VARIANCE(c1)
------------------------------
0.333333
[1] row(s) selected.

Mach> SELECT VAR_POP(c1) FROM var_table;
VAR_POP(c1)
------------------------------
0.25
[1] row(s) selected.
```


## YEAR / MONTH / DAY

入力datetime列から年、月、日をそれぞれ抽出して整数で返します。

```sql
YEAR(datetime_col)
MONTH(datetime_col)
DAY(datetime_col)
```

```sql
Mach> CREATE LOG TABLE extract_table(c1 DATETIME, c2 INTEGER);
Created successfully.

Mach> INSERT INTO extract_table VALUES (to_date('2001-01-01 12:30:00 000:000:000'), 1);
1 row(s) inserted.

Mach> SELECT YEAR(c1), MONTH(c1), DAY(c1) FROM extract_table;
year(c1)    month(c1)   day(c1)
----------------------------------------
2001        1           1
```


## ISNAN / ISINF

引数の数値がNaNまたはInfか判定します。NaNまたはInfなら1、それ以外は0を返します。

```sql
ISNAN(number)
ISINF(number)
```

次の例は、テーブルにすでに`NaN`と`Inf`値がある場合を想定します。SQL `INSERT`文で`nan`や`inf`トークンを直接値として取り込むことはできません。

```sql
Mach> SELECT * FROM test;
I1                          I2                          I3
------------------------------------------------------------------------
1                           1                           1
nan                         inf                         0
NULL                        NULL                        NULL
[3] row(s) selected.


Mach> SELECT ISNAN(i1), ISNAN(i2), ISNAN(i3), i3 FROM test ;
ISNAN(i1)   ISNAN(i2)   ISNAN(i3)   i3
-----------------------------------------------------
0           0           0           1
1           0           0           0
NULL        NULL        NULL        NULL
[3] row(s) selected.

Mach> SELECT * FROM test WHERE ISNAN(i1) = 1;
I1                          I2                          I3
------------------------------------------------------------------------
nan                         inf                         0
[1] row(s) selected.
```

## JSON_SET

JSONドキュメントの指定パスにSQLスカラー値をJSONスカラーとして保存します。

```sql
JSON_SET(json_doc, path, scalar)
```

```sql
Mach> SELECT JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE') FROM dual;
JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE')
--------------------------------------------------------------------------------
{"ship":{"status":"DONE"}}
[1] row(s) selected.
```

注意事項:

- `path`には完全なJSONPathを使用してください。
- `JSON_SET(..., path, NULL)`はJSONの`null`を保存します。
- JSONドキュメント引数が`NULL`なら結果はSQL `NULL`です。
- `path`が`NULL`や空文字列ならエラーになります。
- オブジェクトのパスを中心にサポートします。
- 配列要素の更新（例: `$.items[0]`）はサポートしません。

## JSON_SET_JSON

第3引数をJSON文字列として解析し、オブジェクトまたは配列のサブツリーを保存します。

```sql
JSON_SET_JSON(json_doc, path, json_text)
```

```sql
Mach> SELECT JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}') FROM dual;
JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}')
----------------------------------------------------------------------------
{"ship":{"owner":{"name":"machbase"}}}
[1] row(s) selected.
```

注意事項:

- `path`には完全なJSONPathを使用してください。
- 第3引数がSQL `NULL`なら結果はSQL `NULL`です。
- 無効なJSON文字列はエラーになります。
- オブジェクトのパスを中心にサポートします。
- 配列要素の更新はサポートしません。

## JSON_REMOVE

JSONドキュメントから指定メンバーまたは下位パスを削除します。

```sql
JSON_REMOVE(json_doc, path)
```

```sql
Mach> SELECT JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team') FROM dual;
JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team')
--------------------------------------------------------------------------
{"owner":{"name":"machbase"}}
[1] row(s) selected.
```

注意事項:

- `path`には完全なJSONPathを使用してください。
- 存在しないパスは何も変更しません。
- `JSON_REMOVE(..., '$')`は許可しません。
- JSONドキュメント引数が`NULL`なら結果はSQL `NULL`です。

## PI() {#pi}

π定数を`DOUBLE`型で返します。

```sql
SELECT PI();
```

```sql
Mach> SELECT PI();
PI()
------------------------------
3.141592653589793
[1] row(s) selected.
```

## SQRT() {#sqrt}

平方根を返します。

```sql
SELECT SQRT(9), SQRT(2.25), SQRT(16.0);
```

```sql
Mach> SELECT SQRT(9), SQRT(2.25), SQRT(16.0);
SQRT(9)   SQRT(2.25)         SQRT(16.0)
-----------------------------------------------
3         1.5000000000000000  4
[1] row(s) selected.
```

## POWER() {#power}

`base`の`exponent`乗を返します。

```sql
SELECT POWER(2, 3), POWER(9, 0.5), POWER(4, -1);
```

```sql
Mach> SELECT POWER(2, 3), POWER(9, 0.5), POWER(4, -1);
POWER(2, 3)   POWER(9, 0.5)   POWER(4, -1)
------------------------------------------------
8             3.0000000000000000 0.2500000000000000
[1] row(s) selected.
```

## POW() {#pow}

`POWER()`の別名です。

```sql
SELECT POW(2, 3), POW(2, -1), POW(10, 0);
```

```sql
Mach> SELECT POW(2, 3), POW(2, -1), POW(10, 0);
POW(2, 3)   POW(2, -1)   POW(10, 0)
-----------------------------------------
8           0.5           1
[1] row(s) selected.
```

## LOG() {#log}

`LOG(n)`は自然対数、`LOG(base, n)`は指定した底の対数を計算します。

```sql
SELECT LOG(2, 8), LOG(100), LOG(10, 1000);
```

```sql
Mach> SELECT LOG(2, 8), LOG(100), LOG(10, 1000);
LOG(2, 8)   LOG(100)             LOG(10, 1000)
------------------------------------------------
3           4.605170185988092     3
[1] row(s) selected.
```

## LN() {#ln}

自然対数`ln(n)`を返します。

```sql
SELECT LN(1), LN(10), LN(1000);
```

```sql
Mach> SELECT LN(1), LN(10), LN(1000);
LN(1)      LN(10)         LN(1000)
-----------------------------------
0          2.302585092994046 6.907755278982137
[1] row(s) selected.
```

## EXP() {#exp}

`e^n`を返します。

```sql
SELECT EXP(0), EXP(1), EXP(-1);
```

```sql
Mach> SELECT EXP(0), EXP(1), EXP(-1);
EXP(0)      EXP(1)         EXP(-1)
-----------------------------------
1           2.718281828459045 0.36787944117144233
[1] row(s) selected.
```

## FLOOR() {#floor}

負の無限大方向へ切り捨てます。

```sql
SELECT FLOOR(-1.2), FLOOR(3.9), FLOOR(-3.0);
```

```sql
Mach> SELECT FLOOR(-1.2), FLOOR(3.9), FLOOR(-3.0);
FLOOR(-1.2)  FLOOR(3.9)  FLOOR(-3.0)
-----------------------------------------
-2            3           -3
[1] row(s) selected.
```

## CEIL() {#ceil}

正の無限大方向へ切り上げます。

```sql
SELECT CEIL(-1.2), CEIL(3.2), CEIL(-3.0);
```

```sql
Mach> SELECT CEIL(-1.2), CEIL(3.2), CEIL(-3.0);
CEIL(-1.2)  CEIL(3.2)  CEIL(-3.0)
-------------------------------------
-1           4          -3
[1] row(s) selected.
```

## SIN() {#sin}

ラジアンの入力から正弦を返します。

```sql
SELECT SIN(0), SIN(PI()/2), SIN(PI());
```

```sql
Mach> SELECT SIN(0), SIN(PI()/2), SIN(PI());
SIN(0)      SIN(PI()/2)   SIN(PI())
------------------------------------
0           1             0
[1] row(s) selected.
```

## SLOPE {#slope}

`SLOPE(y, x)`は、数値の`(x, y)`点に対する線形回帰直線の傾きを計算します。

```sql
SLOPE(y, x)
```

- 両方の引数が数値型である必要があります。
- `NULL`値は無視します。
- 有効なデータが不足する場合や`x`の分散が0の場合、結果は`NULL`です。
- 戻り値の型は`DOUBLE`です。

```sql
SELECT SLOPE(temp_c, sample_sec)
FROM sensor_log;
```

## COS() {#cos}

ラジアンの入力から余弦を返します。

```sql
SELECT COS(0), COS(PI()), COS(PI()/2);
```

```sql
Mach> SELECT COS(0), COS(PI()), COS(PI()/2);
COS(0)      COS(PI())   COS(PI()/2)
-------------------------------------
1           -1          0
[1] row(s) selected.
```

## TAN() {#tan}

ラジアンの入力から正接を返します。

```sql
SELECT TAN(0), TAN(PI()/4), TAN(PI());
```

```sql
Mach> SELECT TAN(0), TAN(PI()/4), TAN(PI());
TAN(0)      TAN(PI()/4)  TAN(PI())
-----------------------------------
0           1            0
[1] row(s) selected.
```

## MOD() {#mod}

商を0方向へ切り捨てて余りを計算します。

```sql
SELECT MOD(10, 3), MOD(11, 4), MOD(-10, 3), MOD(3.5, 0.5);
```

```sql
Mach> SELECT MOD(10, 3), MOD(11, 4), MOD(-10, 3), MOD(3.5, 0.5);
MOD(10, 3)  MOD(11, 4)  MOD(-10, 3)  MOD(3.5, 0.5)
-------------------------------------------------------
1           3           -1           0
[1] row(s) selected.
```

## MODE {#mode}

`MODE(value)`は入力集合で最も頻度の高い数値を返します。

```sql
MODE(value)
```

- `value`は数値型である必要があります。
- `NULL`値は無視します。
- 最頻値が複数あれば、最小の値を返します。
- 戻り値の型は`DOUBLE`です。

```sql
SELECT MODE(alarm_code)
FROM event_log;
```

## P05 / P10 / P90 / P95 {#p05-p10-p90-p95}

よく使う分位点を簡潔に表す、正確な分位点計算の短縮関数です。

```sql
P05(value)
P10(value)
P90(value)
P95(value)
```

- `value`は数値型である必要があります。
- `NULL`値は無視します。
- 戻り値の型は`DOUBLE`です。

`P05`、`P10`、`P90`、`P95`はそれぞれ`PERCENTILE_CONT(value, 0.05)`、`0.10`、`0.90`、`0.95`と同じ意味です。

```sql
SELECT P05(response_ms),
       P10(response_ms),
       P90(response_ms),
       P95(response_ms)
FROM web_log;
```

## PERCENTILE_CONT / PERCENTILE_DISC {#percentile_cont-percentile_disc}

数値入力の正確な分位点を計算する集約関数です。

```sql
PERCENTILE_CONT(value, ratio)
PERCENTILE_DISC(value, ratio)
```

- `value`は数値型である必要があります。
- `ratio`は`0.0`以上`1.0`以下の定数である必要があります。
- `PERCENTILE_CONT`は必要に応じてソート済みの隣接値間を補間します。
- `PERCENTILE_DISC`は対象順位に対応する実際の観測値を選択します。
- 両関数とも戻り値の型は`DOUBLE`です。

```sql
SELECT PERCENTILE_CONT(latency_ms, 0.95) AS pcont95,
       PERCENTILE_DISC(latency_ms, 0.95) AS pdisc95
FROM api_log;
```

## QUANTILE {#quantile}

`QUANTILE(value, ratio)`は数値入力の正確な連続分位点を計算します。

```sql
QUANTILE(value, ratio)
```

- `value`は数値型である必要があります。
- `ratio`は`0.0`以上`1.0`以下の定数である必要があります。
- 戻り値の型は`DOUBLE`です。
- `PERCENTILE_CONT`と同じ連続分位点の規則を使用します。

```sql
SELECT QUANTILE(cpu_usage, 0.75)
FROM host_metric;
```

## RAND() {#rand}

乱数値を生成します。

```sql
SELECT RAND(5) = RAND(5) AS same_seed, RAND(7) = RAND(8) AS diff_seed, RAND() = RAND() AS diff_default;
```

```sql
Mach> SELECT RAND(5) = RAND(5) AS same_seed, RAND(7) = RAND(8) AS diff_seed, RAND() = RAND() AS diff_default FROM m$sys_users WHERE name = 'SYS';
same_seed   diff_seed   diff_default
------------------------------------
1           0           0
[1] row(s) selected.
```

`RAND(seed)`は同じシードで同じ値を返します。`RAND()`はセッションの内部状態に基づいて`[0,1)`の範囲の値を生成します。

## REGEXP_LIKE

`REGEXP_LIKE`は文字列が正規表現パターンに一致するか検査します。Boolean値を返し、主に`WHERE`句で使用します。

```sql
REGEXP_LIKE(source, pattern)
REGEXP_LIKE(source, pattern, match_param)
```

- `source`は`VARCHAR`である必要があります。
- `pattern`は定数の`VARCHAR`正規表現である必要があります。
- `match_param`は省略可能で、定数の`VARCHAR`を指定します。`c`は大文字小文字を区別し、`i`は区別しません。デフォルトは`c`です。

```sql
SELECT *
FROM sensor_text
WHERE REGEXP_LIKE(message, 'error|warn', 'i');
```

## REGEXP_INSTR

`REGEXP_INSTR`は正規表現に一致する位置を1始まりで返します。一致する値がなければ`0`を返します。

```sql
REGEXP_INSTR(source, pattern[, position[, occurrence[, return_pos[, match_param]]]])
```

- `source`は`VARCHAR`である必要があります。
- `pattern`は定数の`VARCHAR`正規表現である必要があります。
- `position`と`occurrence`は`1`以上の整数定数です。
- `return_pos`は整数定数です。`0`は開始位置、`1`は一致した文字列の直後の位置を返します。
- `match_param`は`c`または`i`を使用できます。デフォルトは`c`です。

```sql
SELECT REGEXP_INSTR('TechOnTheNet', 'The', 1, 1, 1, 'i');
```

## REGEXP_SUBSTR

`REGEXP_SUBSTR`は正規表現に一致する部分文字列を返します。

```sql
REGEXP_SUBSTR(source, pattern[, position[, occurrence[, match_param]]])
```

- `source`は`VARCHAR`である必要があります。
- `pattern`は定数の`VARCHAR`正規表現である必要があります。
- `position`と`occurrence`は`1`以上の整数定数です。
- `match_param`は`c`または`i`を使用できます。デフォルトは`c`です。

```sql
SELECT REGEXP_SUBSTR('TechOnTheNet', 'a|e|i|o|u', 1, 2, 'i');
```

## REGEXP_REPLACE

`REGEXP_REPLACE`は正規表現に一致する文字列を置換します。

```sql
REGEXP_REPLACE(source, pattern[, replacement[, position[, occurrence[, match_param]]]])
```

- `source`は`VARCHAR`である必要があります。
- `pattern`と`replacement`は定数の`VARCHAR`値である必要があります。
- `replacement`を省略すると一致文字列を削除します。
- `position`は`1`以上の整数定数です。
- `occurrence`は整数定数です。`0`はすべての一致を置換し、正の値はその番号の一致のみ置換します。
- `match_param`は`c`または`i`を使用できます。デフォルトは`c`です。

```sql
SELECT REGEXP_REPLACE('TechOnTheNet', 'a|e|i|o|u', 'Z', 1, 2, 'i');
```

<a id="support-type-of-built-in-function"></a>
## 組み込み関数の対応する型

| |Short|Integer|Long|Float|Double|Varchar|Text|Ipv4|Ipv6|Datetime|Binary|
|--|--|--|--|--|--|--|--|--|--|--|--|
|ABS|o|o|o|o|o|x|x|x|x|x|x|
|ADD_TIME|x|x|x|x|x|x|x|x|x|o|x|
|APPROX_PERCENTILE / APPROX_MEDIAN / APPROX_P05 / APPROX_P10 / APPROX_P90 / APPROX_P95|o|o|o|o|o|x|x|x|x|x|x|
|AREA|o|o|o|o|o|x|x|x|x|x|x|
|AVG|o|o|o|o|o|x|x|x|x|x|x|
|BITAND / BITOR|o|o|o|x|x|x|x|x|x|x|x|
|COUNT|o|o|o|o|o|o|x|o|o|o|x|
|CUME_DIST|o|o|o|o|o|x|x|x|x|x|x|
|DATE_TRUNC|x|x|x|x|x|x|x|x|x|o|x|
|DECODE|o|o|o|o|o|o|x|o|x|o|x|
|FIRST / LAST|o|o|o|o|o|o|x|o|o|o|x|
|FROM_TIMESTAMP|o|o|o|o|o|x|x|x|x|x|x|
|FROM_UNIXTIME|o|o|o|o|o|x|x|x|x|x|x|
|GROUP_CONCAT|o|o|o|o|o|o|x|o|o|o|x|
|INSTR|x|x|x|x|x|o|o|x|x|x|x|
|LEAST / GREATEST|o|o|o|o|o|o|x|x|x|x|x|
|LENGTH|x|x|x|x|x|o|o|x|x|x|o|
|LOWER|x|x|x|x|x|o|x|x|x|x|x|
|LPAD / RPAD|x|x|x|x|x|o|x|x|x|x|x|
|LTRIM / RTRIM|x|x|x|x|x|o|x|x|x|x|x|
|MAX|o|o|o|o|o|o|x|o|o|o|x|
|MEDIAN|o|o|o|o|o|x|x|x|x|x|x|
|MIN|o|o|o|o|o|o|x|o|o|o|x|
|MODE|o|o|o|o|o|x|x|x|x|x|x|
|NVL|x|x|x|x|x|o|x|o|x|x|x|
|P05 / P10 / P90 / P95|o|o|o|o|o|x|x|x|x|x|x|
|PERCENTILE_CONT / PERCENTILE_DISC|o|o|o|o|o|x|x|x|x|x|x|
|QUANTILE|o|o|o|o|o|x|x|x|x|x|x|
|REGEXP_LIKE|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_INSTR|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_SUBSTR|x|x|x|x|x|o|x|x|x|x|x|
|REGEXP_REPLACE|x|x|x|x|x|o|x|x|x|x|x|
|SLOPE|o|o|o|o|o|x|x|x|x|x|x|
|TOP_K|o|o|o|o|o|x|x|x|x|x|x|
|ROUND|o|o|o|o|o|x|x|x|x|x|x|
|ROWNUM|o|o|o|o|o|o|o|o|o|o|o|
|SERIESNUM|o|o|o|o|o|o|o|o|o|o|o|
|STDDEV / STDDEV_POP|o|o|o|o|o|x|x|x|x|x|x|
|SUBSTR|x|x|x|x|x|o|x|x|x|x|x|
|SUBSTRING_INDEX|x|x|x|x|x|o|o|x|x|x|x|
|SUM|o|o|o|o|o|x|x|x|x|x|x|
|SYSDATE / NOW|x|x|x|x|x|x|x|x|x|x|x|
|TO_CHAR|o|o|o|o|o|o|x|o|o|o|x|
|TO_DATE / TO_DATE_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_HEX|o|o|o|o|o|o|o|o|o|o|o|
|TO_INET_STR|x|x|x|x|x|x|x|o|x|x|x|
|TO_IPV4 / TO_IPV4_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_IPV6 / TO_IPV6_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_NUMBER / TO_NUMBER_SAFE|x|x|x|x|x|o|x|x|x|x|x|
|TO_TIMESTAMP|x|x|x|x|x|x|x|x|x|o|x|
|TRUNC|o|o|o|o|o|x|x|x|x|x|x|
|TS_CHANGE_COUNT|o|o|o|o|o|x|x|o|o|o|x|
|UNIX_TIMESTAMP|x|x|x|x|x|x|x|x|x|o|x|
|UPPER|x|x|x|x|x|o|x|x|x|x|x|
|VARIANCE / VAR_POP|o|o|o|o|o|x|x|x|x|x|x|
|YEAR / MONTH / DAY|x|x|x|x|x|x|x|x|x|o|x|
|ISNAN / ISINF|o|o|o|o|o|x|x|x|x|x|x|


<a id="json-related-function"></a>
## JSON関連関数

これらの関数はJSONデータ型を引数に取ります。

| 関数名 | 説明 | 備考 |
|--|--|--|
|JSON_EXTRACT(JSON column name, 'json path')|値を文字列型で返します。<br>値がなければERRORを返します。| - JSON object or array: すべてのオブジェクトを文字列へ変換して返します。<br> - String type: そのまま返します。<br> - Numeric type: 文字列へ変換して返します。<br> - boolean type: "True"または"False"を返します。|
|JSON_EXTRACT_DOUBLE(JSON column name, 'json path')|値を64ビットdouble型で返します。<br>値がなければNULLを返します。| - JSON object or array: NULLを返します。<br> - String type: 変換可能なら変換して返し、不可能ならNULLを返します。<br> - Numeric type: 64ビット実数で返します。<br> - boolean type: "True"は1.0、"False"は0.0を返します。|
|JSON_EXTRACT_INTEGER(JSON column name, 'json path')|値を64ビット整数型で返します。<br>値がなければNULLを返します。| - JSON object or array: NULLを返します。<br> - String type: 変換可能なら変換して返し、不可能ならNULLを返します。<br> - Numeric type: 64ビット整数で返します。<br> - boolean type: "True"は1、"False"は0を返します。|
|JSON_EXTRACT_STRING(JSON column name, 'json path')|値を文字列型で返します。<br>値がなければNULLを返します。<br>矢印演算子（→）と同じ結果を返します。| - JSON object or array: すべてのオブジェクトを文字列へ変換して返します。<br> - String type: そのまま返します。<br> - Numeric type: 文字列へ変換して返します。<br> - boolean type: "True"または"False"を返します。|
|JSON_SET(json_doc, path, scalar)|指定パスにSQLスカラー値をJSONスカラーとして保存した新しいJSONドキュメントを返します。| - `path`は完全なJSONPathを使用します。<br> - `NULL`値はJSONの`null`として保存します。<br> - オブジェクトのパスのみサポートします。|
|JSON_SET_JSON(json_doc, path, json_text)|指定パスにJSON文字列をオブジェクトまたは配列のサブツリーとして保存した新しいJSONドキュメントを返します。| - `path`は完全なJSONPathを使用します。<br> - 第3引数がSQL `NULL`なら結果はSQL `NULL`です。<br> - 無効なJSON文字列はエラーになります。|
|JSON_REMOVE(json_doc, path)|指定パスのメンバーまたはサブツリーを削除した新しいJSONドキュメントを返します。| - `path`は完全なJSONPathを使用します。<br> - 存在しないパスは何も変更しません。<br> - `JSON_REMOVE(..., '$')`は許可しません。|
|JSON_IS_VALID('json string')|JSON文字列が正しい形式か確認します。| - 0: False<br> - 1: True|
|JSON_TYPEOF(JSON column name, 'json path')|値の型を返します。| - None: キーが存在しない<br> - Object: オブジェクト型<br> - Integer: 整数型<br> - Real: 実数型<br> - String: 文字列型<br> - True/False: Boolean<br> - Array: 配列型<br> - Null: NULL|

```sql
Mach> CREATE LOG TABLE jsontbl (name VARCHAR(20), jval JSON);
Created successfully.

Mach> INSERT INTO jsontbl VALUES("name1", '{"name":"test1"}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name2", '{"name":"test2", "value":123}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name3", '{"name":{"class1": "test3"}}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name4", '{"myarray": [1, 2, 3, 4]}');
1 row(s) inserted.
Mach> INSERT INTO jsontbl VALUES("name5", '{"name":"error"');
[ERR-02233: Error occurred at column (2): (Error in json load.)]

Mach> SELECT name, JSON_EXTRACT_STRING(jval, '$.name') FROM jsontbl;
name                  JSON_EXTRACT_STRING(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 {"class1": "test3"}
name2                 test2
name1                 test1
[4] row(s) selected.

Mach> SELECT name, JSON_EXTRACT_INTEGER(jval, '$.myarray[1]') FROM jsontbl;
name                  JSON_EXTRACT_INTEGER(jval, '$.myarray[1]')
--------------------------------------------------------------------
name4                 2
name3                 NULL
name2                 NULL
name1                 NULL
[4] row(s) selected.

Mach> SELECT name, JSON_TYPEOF(jval, '$.name') FROM jsontbl;
name                  JSON_TYPEOF(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 None
name3                 Object
name2                 String
name1                 String
[4] row(s) selected.
```


<a id="json-operator"></a>
## JSON演算子

`->`演算子はJSONデータのオブジェクトへのアクセスに使用します。

JSON_EXTRACT_STRING関数と同じ結果を返します。

```sql
json_col -> 'json path'
```

JSON列のメンバー値には、JSONPathを使用する`->`演算子とドットの省略構文でアクセスできます。

```sql
-- JSONPathの矢印構文
jval->'$.sensor.temperature'

-- JSONドット省略構文
jval.sensor.temperature
```

2つの式は同じJSON値を参照します。既存の`->`演算子は引き続き使用でき、ドット構文は同じ値をより短く表すための追加構文です。

```sql
Mach> SELECT name, jval->'$.name' FROM jsontbl;
name                  JSON_EXTRACT_STRING(jval, '$.name')
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 {"class1": "test3"}
name2                 test2
name1                 test1
[4] row(s) selected.

Mach> SELECT name, jval->'$.myarray[1]' FROM jsontbl;
name                  JSON_EXTRACT_INTEGER(jval, '$.myarray[1]')
--------------------------------------------------------------------
name4                 2
name3                 NULL
name2                 NULL
name1                 NULL
[4] row(s) selected.

Mach> SELECT name, jval->'$.name.class1' FROM jsontbl;
name                  jval->'$.name.class1'
-----------------------------------------------------------------------------------------------------------
name4                 NULL
name3                 test3
name2                 NULL
name1                 NULL
[4] row(s) selected
```

### JSONPathの矢印構文

矢印構文はJSONPath文字列を使用します。

```sql
jval->'$.name'
jval->'$.sensor.temperature'
jval->'$.items[0].name'
```

角括弧でJSONキーを直接指定することもできます。キー名にドット（`.`）を含む場合は角括弧構文を使用します。

```sql
-- キー名がa.bの場合
jval->'$["a.b"]'
jval->'$[a.b]'

-- 複数階層のキーを角括弧で指定
jval->'$[Plant1][Line1][Temperature]'

-- ドットを含む1つのキー名
jval->'$[Plant1.Line1.Temperature]'
```

`$[Plant1.Line1.Temperature]`は`Plant1.Line1.Temperature`という1つのキーを検索します。`Plant1`、`Line1`、`Temperature`を階層ごとのキーとして検索するには、`$[Plant1][Line1][Temperature]`または`$.Plant1.Line1.Temperature`を使用します。

キー名に特殊文字やドットを含む場合は、次のように引用符付きの角括弧構文を推奨します。

```sql
jval->'$["a.b"]["c.d"]["e.f"]'
```

次の構文はサポートしません。

```sql
jval->'$."a.b"'
```

### JSONドット省略構文

JSON列の後にメンバー名を付けてJSON値を参照できます。

```sql
-- 単一メンバー
jval.name

-- 入れ子のメンバー
jval.sensor.temperature

-- 配列の添字
jval.items[0].name

-- 特殊文字を含むキー
jval.items[0]."product-id"
```

ドット構文で二重引用符で囲んだキーは、大文字小文字と特殊文字をそのまま保持します。

```sql
SELECT name, jval."Camel-Key", jval.items[0]."product-id"
  FROM jsontbl
 ORDER BY name;
```

### WHERE句での型比較

JSONメンバーのアクセス結果は参照時に文字列のように表示されます。ただし、`WHERE`句で数値型の値と比較すると、JSON値を数値として解析し、数値比較を行います。

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.value' > 100
 ORDER BY name;

SELECT name
  FROM jsontbl
 WHERE jval.value BETWEEN 10 AND 30
 ORDER BY name;

SELECT name
  FROM jsontbl
 WHERE jval.value IN (10, 20, 30)
 ORDER BY name;
```

次の比較に対応します。

- JSON integer値とSQL integer値の比較
- JSON real/double値とSQL numeric値の比較
- JSON数値文字列とSQL numeric値の比較
- JSON boolean値と文字列`'true'`、`'false'`の比較
- `=`、`<>`、`<`、`<=`、`>`、`>=`、`BETWEEN`、リテラルの`IN (...)`

SQL integer値との比較ではJSON integerを整数として比較するため、`9007199254740992`と`9007199254740993`のようにdoubleの精度範囲を超える値も区別できます。

文字型の値との比較では、従来どおり文字列比較を行います。

```sql
SELECT name
  FROM jsontbl
 WHERE jval->'$.name' = 'test1'
 ORDER BY name;
```

数値比較でJSON値を数値として解釈できない場合、その条件には一致せず、エラーにはなりません。通常の`VARCHAR`列と数値の比較ポリシーは変更せず、自動数値比較はJSONメンバーアクセス式にのみ適用します。

### 名前解決規則

通常のSQL列名の解決は、JSONドットの解釈より優先されます。

```sql
SELECT t.jval.name
  FROM jsontbl t;
```

上記の式は、最初に通常の列名として解決を試みます。通常の列として解決できず、`jval`がJSON列であれば、`jval.name`をJSONメンバーへのアクセスとして扱います。

JSONドットアクセスは、JSON列を基点としてのみ使用できます。

```sql
-- 非対応
(jval->'$.sensor').temperature
name.member
```

### 制約

次の構文はサポートしません。

- ワイルドカード: `jval.items[*].name`
- 再帰的下降: `jval..name`
- フィルター式: `jval.items[?(@.price > 10)]`
- 負数の配列添字: `jval.items[-1]`
- 単一引用符のキー: `jval.'product-id'`
- ドット構文と矢印構文の混在: `jval.items->'$.name'`
- JSON以外の列へのドットアクセス: `name.member`
- 任意の式の後のドットアクセス: `(jval->'$.sensor').temperature`
- 矢印パス内の引用符付きメンバー: `jval->'$."a.b"'`

`IN (SELECT ...)`形式のサブクエリINでは、JSONメンバー値の自動数値比較はサポートしません。リテラルの`IN (...)`を使用してください。

<a id="window-function"></a>
## ウィンドウ関数

ウィンドウ関数は、行間の比較、計算、定義を行う関数で、分析関数やランキング関数とも呼ばれます。

SELECT文でのみ使用できます。

### ウィンドウ関数の構文

ウィンドウ関数には必ずOVER句を含めます。

```
WINDOW_FUNCTION (ARGUMENTS) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

* WINDOW_FUNCTION: ウィンドウ関数名
* ARGUMENTS: 関数に応じて0~N個の引数を指定できます。
* PARTITION BY clause: 全体集合を基準に応じて小さなグループへ分割します（省略可能）。
* ORDER BY clause: ソート基準となるORDER BY句を指定します（省略可能）。

### ウィンドウ関数一覧

#### LAG

パーティションごとのウィンドウからN行前の値を取得します。

対象行がなければNULLを返します。

```
LAG(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE LOG TABLE lag_table (name varchar(10), dt datetime, value INTEGER);
Created successfully.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-01'), 1);
1 row(s) inserted.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-02'), 2);
1 row(s) inserted.

Mach> INSERT INTO lag_table VALUES('name1', TO_DATE('2024-01-03'), 3);
1 row(s) inserted.

-- Divide the set by name, sort by dt, and retrieve the first previous value.
Mach> SELECT name, dt, value, LAG(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lag_table;
name        dt                              value       LAG(value, 1)
---------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           NULL
name1       2024-01-02 00:00:00 000:000:000 2           1
name1       2024-01-03 00:00:00 000:000:000 3           2
[3] row(s) selected.
```


#### LEAD

パーティションごとのウィンドウからN行後の値を取得します。

対象行がなければNULLを返します。

```
LEAD(column_name, N) OVER ([PARTITION BY column_name] [ORDER BY column_name])
```

```
Mach> CREATE LOG TABLE lead_table (name varchar(10), dt datetime, value INTEGER);
Created successfully.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-01'), 1);
1 row(s) inserted.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-02'), 2);
1 row(s) inserted.

Mach> INSERT INTO lead_table VALUES('name1', TO_DATE('2024-01-03'), 3);
1 row(s) inserted.

-- Divide the set by name, sort by dt, and retrieve the first and subsequent values.
Mach> SELECT name, dt, value, LEAD(value, 1) OVER(PARTITION BY name ORDER BY dt) FROM lead_table;
name        dt                              value       LEAD(value, 1)
----------------------------------------------------------------------------
name1       2024-01-01 00:00:00 000:000:000 1           2
name1       2024-01-02 00:00:00 000:000:000 2           3
name1       2024-01-03 00:00:00 000:000:000 3           NULL
[3] row(s) selected.
```


#### NTILE

`NTILE(n)`はソートされた行を可能な限り均等に`n`個のバケットへ分け、各行が属するバケット番号を返します。

```
NTILE(n) OVER ([PARTITION BY column_name] ORDER BY column_name)
```

- `n`は正の定数である必要があります。
- `OVER (...)`内の`ORDER BY`は必須です。
- 行数が均等に分かれない場合、先頭側のバケットが1行ずつ多くなります。

```
Mach> SELECT user_id,
             score,
             NTILE(4) OVER (ORDER BY score) AS score_band
      FROM exam_result;
```

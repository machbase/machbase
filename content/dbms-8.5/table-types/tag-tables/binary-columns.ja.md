---
title: 'バイナリー列'
type: docs
weight: 95
toc: true
---

## 概要 {#overview}

Tag テーブルの `BINARY(n)` は、センサーフレームなどの固定長バイナリー値を保存します。
他のテーブル型やプロトコルでは拒否されます。長さは `1` ～ 32K-`1`、
つまり `1` ～ 32767 バイトです。バイナリー列にはインデックスを作成できません。

Machbase SQL は、`BINARY` 値の挿入時に明示的なバイナリーリテラルをサポートします。

## DDL の規則 {#ddl-rules}

```sql
CREATE TAG TABLE t1(
  name VARCHAR(32) PRIMARY KEY,
  time DATETIME BASETIME,
  frame BINARY(4)
);
```

- 有効な長さ：`1 <= n <= 32767`（32K-`1`）。
- 範囲外のサイズは、作成時にエラーになります。例：`BINARY(0)`。
- `DESC` とテーブルメタデータは、16 進数の桁数ではなく、宣言したバイト長を表示します。
  SQL の `LENGTH(binary_col)` は表示値の長さを返し、短い入力を埋めるために
  末尾へ追加されたゼロパディングは含みません。

## サポートする入力形式 {#supported-input-formats}

```sql
X'hex_digits'
x'hex_digits'
B'bit_digits'
b'bit_digits'
O'octal_digits'
o'octal_digits'
```

| 形式 | 意味 | 単位 |
| --- | --- | --- |
| `X'...'`, `x'...'` | 16 進リテラル | 16 進数 2 桁 = `1` バイト |
| `B'...'`, `b'...'` | ビットリテラル | 8 ビット = `1` バイト |
| `O'...'`, `o'...'` | 8 進リテラル | 8 進数 3 桁 = `1` バイト |

接頭辞には大文字と小文字のどちらも使用できます。

```sql
CREATE TAG TABLE t_bin (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_bin VALUES('hex1', '2024-01-01 00:00:00', X'0A');
INSERT INTO t_bin VALUES('hex2', '2024-01-01 00:00:01', x'00010203');
INSERT INTO t_bin VALUES('bit1', '2024-01-01 00:00:02', B'00001010');
INSERT INTO t_bin VALUES('oct1', '2024-01-01 00:00:03', O'012');
```

`X'0A'`、`B'00001010'`、`O'012'` は、すべて同じ `1` バイトの値である
`0x0A` を表します。

## バイナリーリテラルの規則 {#binary-literal-rules}

### 16 進リテラル {#hexadecimal-literal}

`X'...'` と `x'...'` には、`0-9`、`A-F`、`a-f` を使用できます。

```sql
X'00'
X'0AFF'
x'abcdef'
```

桁数は偶数である必要があります。16 進数 2 桁で
`1` バイトを表します。

### ビットリテラル {#bit-literal}

`B'...'` と `b'...'` には `0` と `1` だけを使用できます。

```sql
B'00000000'  -- 0x00
B'00001010'  -- 0x0A
b'11111111'  -- 0xFF
```

ビット数は 8 の倍数である必要があります。8 ビットで `1` バイトを表します。

### 8 進リテラル {#octal-literal}

`O'...'` と `o'...'` には `0-7` だけを使用できます。

```sql
O'000'  -- 0x00
O'012'  -- 0x0A
o'377'  -- 0xFF
```

3 桁単位で指定します。各 3 桁の値は、`1` バイトの範囲である
`000` ～ `377` である必要があります。

### 空の値 {#empty-value}

空の引用符で、長さ `0` のバイナリー値を表します。

```sql
X''
B''
O''
```

## 長さの制限 {#length-limit}

`BINARY(n)` 列には、最大 `n` バイトを格納できます。

```sql
CREATE TAG TABLE t_limit (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(2)
);

INSERT INTO t_limit VALUES('ok_hex', '2024-01-01 00:00:00', X'0AFF');
INSERT INTO t_limit VALUES('ok_bit', '2024-01-01 00:00:01', B'0000101011111111');
INSERT INTO t_limit VALUES('ok_oct', '2024-01-01 00:00:02', O'012377');

INSERT INTO t_limit VALUES('bad_hex', '2024-01-01 00:00:03', X'000102'); -- 失敗：3 バイト
```

最終的なバイナリー値が `BINARY(n)` の長さを超えると、入力元の形式にかかわらず
挿入は失敗します。バイナリーリテラル、通常の文字列、
従来の `'0x...'` 文字列入力、他の `BINARY` 列からの
`INSERT ... SELECT` にも適用されます。

```sql
CREATE TAG TABLE t_src (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(8)
);

CREATE TAG TABLE t_dst (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_src VALUES('k1', '2024-01-01 00:00:00', X'0102030405060708');
INSERT INTO t_dst SELECT name, time, value FROM t_src; -- 失敗：8 バイトを BINARY(4) に入力
```

`CASE`、`INSERT ... SELECT`、ビューなどの SQL 式内で生成した
バイナリー値にも、同じ長さ制限が適用されます。

## 無効な入力 {#invalid-input}

次の入力は無効です。

```sql
X'0'        -- 16 進数の桁数が奇数
X'0G'       -- G は 16 進数の文字ではない
B'0101'     -- ビット数が 8 の倍数ではない
B'00000002' -- 2 はビットの値ではない
O'12'       -- 8 進数が 3 桁単位ではない
O'400'      -- 1 バイトの範囲を超える
X'0102      -- 閉じ引用符がない
```

無効な値や長さの上限を超える値は、次のエラーになります。

```text
[ERR-02233: Error occurred at column (n): (Invalid insert value.)]
```

## 従来の文字列入力との違い {#difference-from-legacy-string-input}

互換性のため、`'0x...'` 形式の文字列入力も引き続きサポートします。
ただし、`'0x...'` は `BINARY` 列へ変換される文字列リテラルです。
一方、`X'...'`、`B'...'`、`O'...'` は、SQL 内で値を明示的に
バイナリーリテラルとして指定します。

通常の文字列も `BINARY(n)` 列に挿入できますが、バイト長が `n` を超えると
失敗します。新しい SQL では、意味が明確な明示的バイナリーリテラルを
使用してください。

`'0b...'`、`'0o...'`、引用符なしの `0x...`、`0b...`、`0o...` は、
バイナリーリテラルとしてサポートされません。

## 出力とツールに関する注意 {#output-and-tooling-notes}

- machsql は、`0x` 接頭辞なしの大文字の 16 進数で表示します。短い入力に付加した
  末尾のゼロパディングは、テキスト出力に表示されません。
- machloader：スキーマに `BINARY(n)` を宣言します。無効な値や長さの上限を超える
  値はエラーになります。
- REST append：JSON 文字列を 16 進数としてデコードします。16 進数の解析に失敗した
  場合のみ、従来の base64 処理にフォールバックします。
- CLI/ODBC/Java/C#/Node ドライバーは固定長バッファーを送受信します。メタデータの
  `LENGTH` はバイト長です。

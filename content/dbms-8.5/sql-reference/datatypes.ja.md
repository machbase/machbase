---
title : 'データ型'
type: docs
weight: 10
toc: true
---

# 目次 {#index}

* [データ型一覧](#data-type-table)
* [SQL データ型の対応](#sql-datatype-table)

## データ型一覧 {#data-type-table}

| 型名 | 説明 | 値の範囲 | NULL 値 |
|--|--|--|--|
|short|16 ビット符号付き整数|-32767 ~ 32767|-32768|
|ushort|16 ビット符号なし整数|0 ~ 65534|65535|
|integer|32 ビット符号付き整数|-2147483647 ~ 2147483647|-2147483648|
|uinteger|32 ビット符号なし整数|0 ~ 4294967294|4294967295|
|long|64 ビット符号付き整数|-9223372036854775807 ~ 9223372036854775807|-9223372036854775808|
|ulong|64 ビット符号なし整数|0~18446744073709551614|18446744073709551615|
|float|32 ビット浮動小数点|-|-|
|double|64 ビット浮動小数点|-|-|
|datetime|日時|1970-01-01 00:00:00 000:000:000 ~ 2262-04-11 23:47:16.854:775:807|-|
|varchar|可変長文字列（UTF-8）|長さ： 1 ~ 32768 (32K)|-|
|ipv4|IPv4 アドレス（4 バイト）|"0.0.0.0" ~ "255.255.255.255"|-|
|ipv6|IPv6 アドレス（16 バイト）|"0000:0000:0000:0000:0000:0000:0000:0000" ~ "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF"|-|
|text|テキスト（キーワードインデックスを作成可能）|長さ： 0 ~ 64M|-|
|binary|バイナリー（Log：0～64M）/ Tag の固定長（1～32K-1）|Log: 0 ~ 64M<br>Tag: 1 ~ 32767 バイト|-|
|json|JSON データ|JSON データの長さ : 1 ~ 32768 (32K)<br><br>JSON パスの長さ : 1 ~ 512|-|

### short {#short}

C の 16 ビット符号付き整数と同じです。最小の負の値は NULL として扱います。int16 と表示される場合があります。

### integer {#integer}

C の 32 ビット符号付き整数と同じです。最小の負の値は NULL として扱います。int32 または int と表示される場合があります。

### long {#long}

C の 64 ビット符号付き整数と同じです。最小の負の値は NULL として扱います。int64 と表示される場合があります。

### float {#float}

C の 32 ビット浮動小数点型 float と同じです。正の最大値は NULL として扱います。

### double {#double}

C の 64 ビット浮動小数点型 double と同じです。正の最大値は NULL として扱います。

### datetime {#datetime}

1970 年 1 月 1 日の午前 0 時からの経過時間をナノ秒で保持します。

日時関連の関数では、ナノ秒単位まで処理できます。

### varchar {#varchar}

最大 32K バイトの可変長文字列型です。

長さは英字 1 文字を 1 バイトとして数えるため、UTF-8 の表示文字数とは異なります。必要なバイト数で指定してください。

### IPv4 {#ipv4}

Internet Protocol version 4 のアドレスを保存します。

内部では 4 バイトを使用し、0.0.0.0 ～ 255.255.255.255 を表します。

### IPv6 {#ipv6}

Internet Protocol version 6 のアドレスを保存します。

内部では 16 バイトを使用し、0000:0000:0000:0000:0000:0000:0000:0000 ～ FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF を表します。
入力時は、: を使用した次の省略形式もサポートします。

* ::FFFF:1232：先頭の連続したゼロを省略
* ::FFFF:192.168.0.3：IPv4 互換の表現
* ::192.168.3.1：旧式の IPv4 互換表現

### text {#text}

VARCHAR のサイズを超えるテキストや文書を保存します。

キーワードインデックスで検索でき、最大 64 MB を保存できます。
主に大きなテキストファイルを個別の列として保存、検索する場合に使用します。

### binary {#binary}

Log テーブルの `BINARY` は、画像や文書などの非構造化データを保存します。
TEXT と同じ最大 64 MB です。Lookup と Volatile には
`BINARY` 列を定義できません。

Tag テーブルの `BINARY(n)` は、センサーフレーム用の固定長型です。
有効なサイズは 1 ～ 32K-1（32767）バイトです。SQL では `X'...'`、`B'...'`、
`O'...'` のバイナリーリテラルをサポートし、接頭辞は小文字でも指定できます。
従来の `'0x...'` 形式の文字列入力も互換性のためにサポートします。入力元にかかわらず、
対象の `BINARY(n)` の長さを超えると、挿入は次のエラーになります。
`[ERR-02233: Error occurred at column (n): (Invalid insert value.)]`。
メタデータは宣言したバイト長を返します。一方、SQL の `LENGTH(binary_col)` と
machsql のテキスト出力は、短い入力の末尾に付加したゼロパディングを除外します。
machsql は `0x` 接頭辞なしの大文字の 16 進数で表示します。固定長の
`BINARY(n)` は Tag テーブルでのみ使用できます。詳細は
[バイナリー列](../../table-types/tag-tables/binary-columns/)を参照してください。

### json {#json}

JSON データを保存する型です。

JSON はキーと値の組からなるオブジェクトを、テキストで表現する形式です。

最大サイズは VARCHAR と同じ 32K バイトです。


## SQL データ型の対応 {#sql-datatype-table}

Machbase の型に対応する SQL 型と C 型を示します。

| Machbase 型 | Machbase CLI 型 | SQL 型 | C 型 | C の基本型 | 説明 |
|--|--|--|--|--|--|
|short|SQL_SMALLINT|SQL_SMALLINT|SQL_C_SSHORT|int16_t (short)|16 ビット符号付き整数|
|ushort|SQL_USMALLINT|SQL_SMALLINT|SQL_C_USHORT|uint16_t (unsigned short)|16 ビット符号なし整数|
|integer|SQL_INTEGER|SQL_INTEGER|SQL_C_SLONG|int32_t (int)|32 ビット符号付き整数|
|uinteger|SQL_UINTEGER|SQL_INTEGER|SQL_C_ULONG|uint32_t (unsigned int)|32 ビット符号なし整数|
|long|SQL_BIGINT|SQL_BIGINT|SQL_C_SBIGINT|int64_t (long long)|64 ビット符号付き整数|
|ulong|SQL_UBIGINT|SQL_BIGINT|SQL_C_UBIGINT|uint64_t (unsigned long long)|64 ビット符号なし整数|
|float|SQL_FLOAT|SQL_REAL|SQL_C_FLOAT|float|32 ビット浮動小数点|
|double|SQL_DOUBLE|SQL_FLOAT, SQL_DOUBLE|SQL_C_DOUBLE|double|64 ビット浮動小数点|
|datetime|SQL_TIMESTAMP<br><br>SQL_TIME|SQL_TYPE_TIMESTAMP<br><br>SQL_BIGINT<br><br>SQL_TYPE_TIME|SQL_C_TYPE_TIMESTAMP<br><br>SQL_C_UBIGINT<br><br>SQL_C_TIME|char * (YYYY-MM-DD HH24:MI:SS)<br><br>int64_t (タイムスタンプ：ナノ秒)<br>struct tm|日時|
|varchar|SQL_VARCHAR|SQL_VARCHAR|SQL_C_CHAR|char *|文字列|
|ipv4|SQL_IPV4|SQL_VARCHAR|SQL_C_CHAR|char * (IP 文字列)<br><br>unsigned char[4]|IPv4 アドレス|
|ipv6|SQL_IPV6|SQL_VARCHAR|SQL_C_CHAR|char * (IP 文字列)<br><br>unsigned char[16]|IPv6 アドレス|
|text|SQL_TEXT|SQL_LONGVARCHAR|SQL_C_CHAR|char *|テキスト|
|binary|SQL_BINARY|SQL_BINARY|SQL_C_BINARY|char *|バイナリーデータ|
|json|SQL_JSON|SQL_JSON|SQL_C_CHAR|json_t|JSON データ|

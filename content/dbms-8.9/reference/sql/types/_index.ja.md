---
type: docs
title: '16.1.2 データ型辞典'
weight: 20
toc: true
---

MachbaseがサポートするSQLデータ型を説明します。

型は保存する値の範囲と精度に合わせて選択します。整数の最小値や最大値など、NULL表現に予約された値は
通常のデータとして使用できません。次の表の`NULL値`は内部表現です。SQLでは`NULL`を挿入し、
`IS NULL`で検査します。

## データ型の概要

| 型 | サイズ | 値の範囲 | NULL値 |
|------|------|---------|---------|
| `SHORT` | 2 bytes | -32,767 ~ 32,767 | -32,768 |
| `USHORT` | 2 bytes | 0 ~ 65,534 | 65,535 |
| `INTEGER` | 4 bytes | -2,147,483,647 ~ 2,147,483,647 | -2,147,483,648 |
| `UINTEGER` | 4 bytes | 0 ~ 4,294,967,294 | 4,294,967,295 |
| `LONG` | 8 bytes | -9,223,372,036,854,775,807 ~ 9,223,372,036,854,775,807 | -9,223,372,036,854,775,808 |
| `ULONG` | 8 bytes | 0 ~ 18,446,744,073,709,551,614 | 18,446,744,073,709,551,615 |
| `FLOAT` | 4 bytes | 32ビット単精度浮動小数点 | 正の最大値 |
| `DOUBLE` | 8 bytes | 64ビット倍精度浮動小数点 | 正の最大値 |
| `DECIMAL(M,D)` | precisionにより可変 | exact fixed-point, M: 1~65, D: 0~30 | - |
| `ARRAY` | 要素型と要素数により可変 | 固定長1次元数値配列、要素数1~1024 | 配列全体のNULLと要素のNULLを区別 |
| `DATETIME` | 8 bytes | 1970-01-01 ~ 2262-04-11 (ナノ秒精度) | - |
| `VARCHAR(n)` | 可変 | 最大nバイト（LOGの宣言範囲: 1~32,767） | - |
| `IPV4` | 4 bytes | 0.0.0.0 ~ 255.255.255.255 | - |
| `IPV6` | 16 bytes | 0000:...:0000 ~ FFFF:...:FFFF | - |
| `TEXT` | 可変 | 0 ~ 64MB（全文検索インデックス対応） | - |
| `BINARY` | 可変 | LOG: 0~64MB / TAG: 1~32,767 bytes (固定長) | - |
| `JSON` | 可変 | JSONドキュメント: 1~32,768 bytes / path: 1~512 bytes | - |

---

## 整数型

### SHORT

16ビット符号付き整数型です。保存サイズはCの`int16_t`と同じですが、最小値（-32,768）は
NULL表現に予約されています。SQLでは別名`INT16`も使用できます。

```sql
CREATE LOG TABLE t (c1 SHORT);
INSERT INTO t VALUES (-32767);  -- 有効な最小値
INSERT INTO t VALUES (-32768);  -- NULLとして処理
```

### USHORT

16ビット符号なし整数（`uint16_t`）です。最大値（65,535）はNULLとして認識されます。

### INTEGER

32ビット符号付き整数型です。保存サイズはCの`int32_t`と同じですが、最小値はNULL表現に予約されています。
SQLでは別名`INT32`または`INT`も使用できます。

### UINTEGER

32ビット符号なし整数（`uint32_t`）です。

### LONG

64ビット符号付き整数型です。保存サイズはCの`int64_t`と同じですが、最小値はNULL表現に予約されています。
SQLでは別名`INT64`も使用できます。

### ULONG

64ビット符号なし整数（`uint64_t`）です。

---

## 浮動小数点型

### FLOAT

C言語の32ビット浮動小数点型`float`と同じです。正の最大値はNULLとして認識されます。

### DOUBLE

C言語の64ビット浮動小数点型`double`と同じです。正の最大値はNULLとして認識されます。

---

## 固定小数点型

### DECIMAL / NUMERIC

宣言した精度と小数桁数の範囲で10進数を正確に保存する固定小数点型です。入力値の小数桁数が
宣言範囲を超えると丸めが発生する場合があるため、金額や比率を保存する場合は必要な桁数を
事前に決めてください。`NUMERIC`、`DEC`、`FIXED`、`NUMBER`は`DECIMAL`の別名です。

```sql
CREATE TRANSACTION TABLE invoice (
    id     LONG PRIMARY KEY,
    amount DECIMAL(18,2),
    rate   NUMERIC(7,4)
);
```

`DECIMAL`は`DECIMAL(10,0)`、`DECIMAL(M)`は`DECIMAL(M,0)`と解釈します。宣言規則、丸め、
インデックス、集計、クライアントマッピングは[DECIMALとNUMERIC固定小数点型](decimal-numeric-fixed-point/)を
参照してください。

---

## ARRAY型

Machbase DBMS 8.7.0は、数値要素を決まった個数保存する固定長1次元の`ARRAY`型をサポートします。
要素型の後に要素数（cardinality）を指定します。

```sql
CREATE LOG TABLE sensor_array (
    id INTEGER,
    location DOUBLE[2],
    acceleration FLOAT[3]
);
```

対応する要素型、NULLの区別、取り込み・参照構文、SDK別の表現は
[数値ARRAY型](array/)を参照してください。

---

## 日付/時刻型

### DATETIME

1970年1月1日午前0時からの経過時間をナノ秒値で内部保存します。表現範囲は1970-01-01 00:00:00 000:000:000 ~ 2262-04-11 23:47:16.854:775:807です。

- ナノ秒単位まで処理可能
- 内部表現: 8バイト整数 (nanoseconds since epoch)
- 文字列表現: `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`

```sql
-- 文字列からDATETIMEへ変換
SELECT TO_DATE('2024-01-15 10:30:00 000:000:000');

-- DATETIMEから文字列へ変換
SELECT TO_CHAR(ts, 'YYYY-MM-DD HH24:MI:SS') FROM t;
```

---

## 文字列型

### VARCHAR(n)

可変長文字列型です。`n`は文字数ではなく保存できるバイト数で、LOGでの宣言範囲は1~32,767です。
UTF-8では文字によって必要なバイト数が異なるため、ハングルや絵文字などを保存する場合は、
実際のエンコーディングサイズを考慮して長さを指定してください。

```sql
CREATE LOG TABLE t (name VARCHAR(100), description VARCHAR(1000));
```

### TEXT

VARCHARのサイズを超える大容量テキストを保存する型で、最大64MBを保存できます。
テキスト保存のサポートとKEYWORDインデックスのサポートは別です。
インデックスの使用可否はテーブルタイプによって異なります。

- LOGとStandard EditionのTRANSACTIONテーブルでサポート
- LOGテーブルはKEYWORDインデックスと`SEARCH`演算子でキーワード検索が可能
- TAG、LOOKUP、VOLATILEテーブルでは非対応

LOGのTEXT列そのものにはORDER BY・GROUP BYを適用できません。
これは性能上の推奨事項ではなく、クエリ検証で拒否される制約です。
ソート・集計に使用するデバイス、エラーコード、重要度などは別のVARCHAR列や数値列に保存してください。
TEXTをVARCHARへ変更するための`MODIFY COLUMN`もサポートしません。

```sql
CREATE LOG TABLE log_table (ts DATETIME, message TEXT);
-- キーワードインデックスの作成
CREATE INDEX idx_msg ON log_table (message) INDEX_TYPE KEYWORD;
```

---

## バイナリ型

### BINARY

画像や文書などの非構造化バイナリデータを保存する型です。

- **LOGテーブル**: 可変長、最大64MB
- **TRANSACTIONテーブル**: 可変長バイナリ値をサポート（Standard Edition）
- **TAGテーブル**: `BINARY(n)`形式の固定長型、1 ~ 32,767 bytes
- LOOKUP、VOLATILEテーブルでは非対応

TAGテーブルの`BINARY(n)`:
- `X'...'`、`B'...'`、`O'...'`リテラルをサポート（小文字の接頭辞にも対応）
- 互換性のために`'0x...'`形式もサポート
- 宣言した長さを超えると`ERR-02233`エラーが発生

---

## ネットワークアドレス型

### IPV4

IPv4アドレスを保存する型です。内部で4バイトを使用し、`"0.0.0.0"` ~ `"255.255.255.255"`の範囲を表します。

```sql
CREATE LOG TABLE access_log (ts DATETIME, src_ip IPV4, dst_ip IPV4);
INSERT INTO access_log VALUES (NOW, '192.168.0.1', '10.0.0.1');
SELECT * FROM access_log WHERE src_ip = TO_IPV4('192.168.0.1');
```

### IPV6

IPv6アドレスを保存する型です。内部で16バイトを使用します。省略表記にも対応します。

- `"::FFFF:1232"` — 先頭の0を省略
- `"::FFFF:192.168.0.3"` — IPv4互換表記
- `"::192.168.3.1"` — IPv4互換表記 (deprecated)

```sql
CREATE LOG TABLE v6_log (ts DATETIME, src_ip IPV6);
INSERT INTO v6_log VALUES (NOW, '21DA:D3:0:2F3B:2AA:FF:FE28:9C5A');
```

---

## JSON型

JSONドキュメントを保存する型です。キーと値のペアで構成されるJSONデータをテキスト形式で保存します。

- データの最大サイズ: 32,768 bytes
- JSONパスの最大長: 512 bytes
- TAG、LOG、LOOKUP、TRANSACTIONテーブルでサポート
- VOLATILEテーブルではJSON列の作成不可
- LOOKUPテーブルのJSON列は主キーとして使用不可

```sql
CREATE LOG TABLE sensor_data (
    ts   DATETIME,
    data JSON
);
INSERT INTO sensor_data VALUES (NOW, '{"temp":23.5,"hum":60}');
SELECT data -> 'temp' AS temperature FROM sensor_data;
```

テーブルタイプ別のJSONサポート範囲の詳細は、[JSON型のテーブルタイプ別サポート範囲](table-types-type-support-scope-json/)を参照してください。

---

## SQLデータ型のマッピング

Machbaseのデータ型とSQL標準型、C型の対応関係です。

| Machbase 型 | Machbase CLI 型 | SQL 型 | C 型 | C基本型 |
|--------------|------------------|----------|--------|------------|
| `short` | SQL_SMALLINT | SQL_SMALLINT | SQL_C_SSHORT | `int16_t` |
| `ushort` | SQL_USMALLINT | SQL_SMALLINT | SQL_C_USHORT | `uint16_t` |
| `integer` | SQL_INTEGER | SQL_INTEGER | SQL_C_SLONG | `int32_t` |
| `uinteger` | SQL_UINTEGER | SQL_INTEGER | SQL_C_ULONG | `uint32_t` |
| `long` | SQL_BIGINT | SQL_BIGINT | SQL_C_SBIGINT | `int64_t` |
| `ulong` | SQL_UBIGINT | SQL_BIGINT | SQL_C_UBIGINT | `uint64_t` |
| `float` | SQL_FLOAT | SQL_REAL | SQL_C_FLOAT | `float` |
| `double` | SQL_DOUBLE | SQL_FLOAT, SQL_DOUBLE | SQL_C_DOUBLE | `double` |
| `decimal` | SQL_DECIMAL | SQL_DECIMAL, SQL_NUMERIC | SQL_C_NUMERIC | decimal-preserving value |
| `datetime` | SQL_TIMESTAMP | SQL_TYPE_TIMESTAMP | SQL_C_TYPE_TIMESTAMP | `char *` (YYYY-MM-DD ...) |
| `varchar` | SQL_VARCHAR | SQL_VARCHAR | SQL_C_CHAR | `char *` |
| `ipv4` | SQL_IPV4 | SQL_VARCHAR | SQL_C_CHAR | `char *` (IP文字列) |
| `ipv6` | SQL_IPV6 | SQL_VARCHAR | SQL_C_CHAR | `char *` (IP文字列) |
| `text` | SQL_TEXT | SQL_LONGVARCHAR | SQL_C_CHAR | `char *` |
| `binary` | SQL_BINARY | SQL_BINARY | SQL_C_BINARY | `char *` |
| `json` | SQL_JSON | SQL_JSON | SQL_C_CHAR | `json_t` |

---

## テーブルタイプ別の対応データ型

| 型 | TAG | LOG | LOOKUP | VOLATILE | TRANSACTION |
|------|:---:|:---:|:------:|:--------:|:---:|
| SHORT | O | O | O | O | O |
| USHORT | O | O | O | O | O |
| INTEGER | O | O | O | O | O |
| UINTEGER | O | O | O | O | O |
| LONG | O | O | O | O | O |
| ULONG | O | O | O | O | O |
| FLOAT | O | O | O | O | O |
| DOUBLE | O | O | O | O | O |
| DECIMAL / NUMERIC | O | O | O | O | O |
| DATETIME | O | O | O | O | O |
| VARCHAR | O | O | O | O | O |
| IPV4 | O | O | O | O | O |
| IPV6 | O | O | O | O | O |
| TEXT | X | O | X | X | O |
| JSON | O | O | O | X | O |
| BINARY | O (固定長) | O | X | X | O |

DECIMALはすべての公開テーブルタイプでサポートします。TRANSACTIONテーブル自体はStandard Editionで
使用し、Cluster EditionではLOG/TAGテーブルのDECIMAL列とDDL伝播をサポートします。

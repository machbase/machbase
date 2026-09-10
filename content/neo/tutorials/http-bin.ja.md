---
toc: true
title: HTTPのBinary列チュートリアル
type: docs
weight: 35
---

{{< callout emoji="📌">}}
このチュートリアルでは、HTTPの`write` APIと`query` APIで`binary`列を保存・検索する方法を説明します。
{{< /callout >}}

{{< neo_since ver="8.5.2" />}}

## サンプルテーブルの作成 {#예제-테이블-생성}

```sql
CREATE TAG TABLE IF NOT EXISTS example (
  name varchar(100) primary key,
  time datetime basetime,
  value double,
  bindata binary
);
```

HTTP APIでは、`binary`列を文字列で表現します。書き込みAPIは入力文字列からエンコーディングを判別し、検索APIは`binaryformat`パラメーターで出力形式を選択します。

## Binary文字列の規則 {#binary-문자열-규칙}

書き込みAPIに`binary`列の文字列を渡すと、以下の規則でデコードします。

| 入力文字列 | 意味 |
| --- | --- |
| `0x0102` | `0x`または`0X`の接頭辞があるため、16進文字列としてデコードします。 |
| `AQI=` | `0x`の接頭辞がないため、標準のbase64文字列としてデコードします。 |

検索APIの既定の出力は16進文字列です。

| `binaryformat` | 出力例 | 説明 |
| --- | --- | --- |
| 省略または`hex` | `0x0102` | すべてのバイトを16進文字列で出力します。 |
| `base64` | `AQI=` | 標準のbase64文字列で出力します。 |
| `bytes` | `[1 2]` | バイト値を10進数の配列形式で出力します。 |
| `preview` | `0x0102030405..` | 先頭部分のみを16進文字列で出力します。長い値の確認に使用します。 |

以下の例では、次の値を使用します。

- `0x0102`と`AQI=`は、同じバイト値を表します。
- `0x0304`と`AwQ=`は、同じバイト値を表します。

## JSONによるbinaryデータの入力 {#json으로-binary-데이터-입력}

この例では、HTTP Write APIに`method=insert`を指定します。JSON入力では、16進文字列とbase64文字列の両方を使用できます。

~~~
```http
POST http://127.0.0.1:5654/db/write/example
  ?timeformat=s
  &method=insert
Content-Type: application/json

{
  "data": {
    "columns": ["name", "time", "value", "bindata"],
    "rows": [
      ["json-hex", 1713675600, 1.23, "0x0102"],
      ["json-base64", 1713675601, 2.34, "AwQ="]
    ]
  }
}
```
~~~

## CSVによるbinaryデータの入力 {#csv로-binary-데이터-입력}

この例では、HTTP Write APIに`method=append`を指定します。CSV入力でも`binary`列の値は文字列で、`0x`の接頭辞があれば16進数、なければbase64としてデコードします。

~~~
```http
POST http://127.0.0.1:5654/db/write/example
  ?timeformat=s
  &method=append
  &header=columns
Content-Type: text/csv

name,time,value,bindata
csv-hex,1713675610,10.5,0x0102
csv-base64,1713675611,20.5,AwQ=
```
~~~

## 既定の形式でのデータ検索 {#기본-형식으로-데이터-조회}

Query APIに`format=json`を指定します。`binaryformat`を省略すると、`bindata`列は16進文字列で返されます。

~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select name,time,value,bindata from example where name in ('json-hex','json-base64','csv-hex','csv-base64')
  &timeformat=s
  &format=json
```
~~~

```json
{
  "data": {
    "rows": [
      ["json-hex", 1713675600, 1.23, "0x0102"],
      ["json-base64", 1713675601, 2.34, "0x0304"],
      ["csv-hex", 1713675610, 10.5, "0x0102"],
      ["csv-base64", 1713675611, 20.5, "0x0304"]
    ]
  }
}
```

## Base64形式でのデータ検索 {#base64-형식으로-데이터-조회}

base64文字列でレスポンスを受け取るには、`binaryformat=base64`を指定します。このオプションは、`format=csv`、`format=ndjson`、`format=box`にも適用されます。

~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select name,time,value,bindata from example where name in ('json-hex','json-base64','csv-hex','csv-base64')
  &timeformat=s
  &format=csv
  &binaryformat=base64
```
~~~

```csv
NAME,TIME,VALUE,BINDATA
json-hex,1713675600,1.23,AQI=
json-base64,1713675601,2.34,AwQ=
csv-hex,1713675610,10.5,AQI=
csv-base64,1713675611,20.5,AwQ=
```

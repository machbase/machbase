---
title: 時刻に関する例
type: docs
weight: 100
toc: true
---

{{< callout emoji="📌" >}}
実習の前に以下のクエリを実行し、テーブルとデータを準備してください。
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12 12:00:00 123:456:789'), 10);
INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-13 12:00:00 123:456:789'), 11);
```


TQLには、さまざまな `Time` 関連関数があります。

## 時刻関数 {#시간-함수}

### Now

`time("now")` は現在時刻を返します。

```js
SQL(`select to_char(time), value from example where time < ?`, time('now'))
CSV()
```

`結果`

```
2021-08-12 12:00:00 123:456:789,10
2021-08-13 12:00:00 123:456:789,11
```

### Timestamp

`time(epoch)` は、ナノ秒単位のUnixエポック値をtimeに変換します。
```js
SQL(`select to_char(time), value from example where time = ?`, time(1628737200123456789))
CSV()
```


## 時刻の変換 {#시간-변환}

TQLを使うと、`Timestamp` と `時刻文字列` を簡単に相互変換できます。

### Timestamp → 時刻文字列 {#timestamp--시간-문자열}

以下のコードを `time_to_format.tql` として保存します。

```js
STRING(param("format_time") ?? "808210800", separator('\n'))
SCRIPT({
    epoch = parseInt($.values[0])
    time = new Date(epoch*1000)
    $.yield(epoch, time.toISOString())
})
CSV()
```

[http://127.0.0.1:5654/db/tql/time_to_format.tql?format_time=808210800000000001](http://127.0.0.1:5654/db/tql/time_to_format.tql?format_time=808210800000000001)

### 時刻文字列 → Timestamp {#시간-문자열--timestamp}

以下のコードを `format_to_time.tql` として保存します。

```js
STRING(param("timestamp") ?? "1995-08-12T00:00:00.000Z", separator('\n'))
SCRIPT({
    ts = new Date(Date.parse($.values[0]));
    epoch = ts.getTime() / 1000;
    $.yield(epoch, ts.toISOString())
})
CSV()
```

`http://127.0.0.1:5654/db/tql/format_to_time.tql?timestamp=1995-08-12T00:00:00.000Z`


## 出力形式 {#출력-포맷}

出力時の時刻値の表現形式を指定できます。

### None（既定） {#none-기본}

```js
SQL(`select to_char(time), time from example`)
CSV()
```

`結果`

```
2021-08-12 12:00:00 123:456:789,1628737200123456789
2021-08-13 12:00:00 123:456:789,1628823600123456789
```

### Default

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,2021-08-12 03:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 03:00:00.123
```
#### その他のDefault形式 {#additional-default-types}
| 型     | 説明 |
|:-----------------|:-------------|
|DEFAULT_MS | 2006-01-02 15:04:05.999|
|DEFAULT_US | 2006-01-02 15:04:05.999999|
|DEFAULT_NS | 2006-01-02 15:04:05.999999999|
|DEFAULT.MS | 2006-01-02 15:04:05.000|
|DEFAULT.US | 2006-01-02 15:04:05.000000|
|DEFAULT.NS | 2006-01-02 15:04:05.000000000|

### Numeric形式 {#numeric-포맷}

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('NUMERIC'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,08/12 03:00:00AM '21 +0000
2021-08-13 12:00:00 123:456:789,08/13 03:00:00AM '21 +0000
```

### Ansic形式 {#ansic-포맷}

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('ANSIC'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,Thu Aug 12 03:00:00 2021
2021-08-13 12:00:00 123:456:789,Fri Aug 13 03:00:00 2021
```

### Unix形式 {#unix-포맷}

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('NUMERIC'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,Thu Aug 12 03:00:00 UTC 2021
2021-08-13 12:00:00 123:456:789,Fri Aug 13 03:00:00 UTC 2021
```

### RFC822形式 {#rfc822-포맷}

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('RFC822'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,12 Aug 21 03:00 UTC
2021-08-13 12:00:00 123:456:789,13 Aug 21 03:00 UTC
```

### RFC3339形式 {#rfc3339-포맷}

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('RFC3339'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,2021-08-12T03:00:00Z
2021-08-13 12:00:00 123:456:789,2021-08-13T03:00:00Z
```

## タイムゾーン {#시간대}

`tz()` 関数でタイムゾーンを指定できます。

### Local

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('local'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,2021-08-12 12:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 12:00:00.123
```

### UTC

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('UTC'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,2021-08-12 03:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 03:00:00.123
```

### Seoul

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('Asia/Seoul'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,2021-08-12 12:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 12:00:00.123
```

### EST

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('EST'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,2021-08-11 22:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-12 22:00:00.123
```

### Paris

```js
SQL(`select to_char(time), time from example`)
CSV(timeformat('DEFAULT'), tz('Europe/Paris'))
```

`結果`

```
2021-08-12 12:00:00 123:456:789,2021-08-12 05:00:00.123
2021-08-13 12:00:00 123:456:789,2021-08-13 05:00:00.123
```

---
title: ユーティリティ関数
type: docs
weight: 41
toc: true
---

ユーティリティ関数は、さまざまな関数の引数として共通に使用できます。

## 定数 {#constants}

| 定数        | 説明                         |
|:---------------- | :---------------------------------- |
| `NULL`           | null値                          |
| `PI`             | 3.141592....   https://oeis.org/A000796 |

## コンテキスト {#context}

### key()

*構文*: `key()`

現在のレコードのキーを返します。

### value()

*構文*: `value( [index] )`

- `index` *integer*：値配列のインデックス（省略可）

現在のレコードの値全体を配列として返します。
インデックスを指定すると、その位置の要素を返します。

たとえば、現在の値が `[0, true, "hello", "world"]` の場合：

- `value()` は、値配列全体の `[0, true, "hello", "world"]` を返します。
- `value(0)` は、先頭の要素 `0` を返します。
- `value(3)` は、最後の要素 `"world"` を返します。

### payload()

*構文*: `payload()`

*tql* スクリプトの呼び出し元から送信された、現在の入力ストリームを返します。
HTTPで呼び出した場合、`payload()` はPOSTリクエスト本文のストリームを返します。
MQTTで呼び出した場合、`payload()` はPUBLISHメッセージのペイロードを返します。

### param()

*構文*: `param( name )`

- `name` *string*：クエリパラメーター名

HTTPで *tql* スクリプトを呼び出した場合、`param()` でリクエストのクエリパラメーターを取得できます。

### context()

*構文*: `context()`

スクリプトランタイムのコンテキストオブジェクトを返します。

## 文字列 {#string}

### escapeParam()

*構文*: `escapeParam( str ) : string` {{< neo_since ver="8.0.7" />}}

`escapeParam()` は、文字列をURLクエリで安全に使用できるようにエスケープします。

```js {linenos=table,hl_lines=["3"],linenostart=1}
CSV(
    file(`http://127.0.0.1:5654/db/query?format=csv&q=`+
        escapeParam(`select count(*) from example`)
    )
)
CSV()
```

### strTrimSpace()

*構文*: `strTrimSpace(str) : string` {{< neo_since ver="8.0.7" />}}

`strTrimSpace` は、文字列strの前後の空白をすべて除去した部分文字列を返します。

### strTrimPrefix()

*構文*: `strTrimPrefix(str, prefix) : string` {{< neo_since ver="8.0.7" />}}

`strTrimPrefix` は、strの先頭から指定したprefixを除去します。strがprefixで始まらない場合、そのまま返します。

### strTrimSuffix()

*構文*: `strTrimSuffix(str, suffix) : string` {{< neo_since ver="8.0.7" />}}

`strTrimSuffix` は、strの末尾から指定したsuffixを除去します。strがsuffixで終わらない場合、そのまま返します。

### strHasPrefix()

*構文*: `strHasPrefix(str, prefix) : boolean` {{< neo_since ver="8.0.7" />}}

`strHasPrefix` は、文字列strがprefixで始まるかを判定します。

### strHasSuffix()

*構文*: `strHasSuffix(str, suffix) : boolean` {{< neo_since ver="8.0.7" />}}

`strHasSuffix` は、文字列sがsuffixで終わるかを判定します。

### strReplaceAll()

*構文*: `strReplaceAll(str, old, new) : string` {{< neo_since ver="8.0.7" />}}

`strReplaceAll` は、文字列s内の重なり合わないすべてのoldをnewに置換したコピーを返します。
oldが空の場合、文字列の先頭と各UTF-8シーケンスの後に一致し、
k個のルーンからなる文字列では最大k+1回置換します。

### strReplace()

*構文*: `strReplace(str, old, new, n) : string` {{< neo_since ver="8.0.7" />}}

- `str` *string*
- `old` *string*
- `new` *string*
- `n` *integer*

`strReplace` は、文字列s内の重なり合わないoldを先頭からn個だけnewに置換したコピーを返します。
oldが空の場合、文字列の先頭と各UTF-8シーケンスの後に一致し、
k個のルーンからなる文字列では最大k+1回置換します。
n < 0の場合、置換回数に制限はありません。

### strSub()

*構文*: `strSub(str, offset [, count]) : string` {{< neo_since ver="8.0.7" />}}

`strSub` は、strの部分文字列を返します。

### strIndex()

*構文*: `strIndex(str, substr) : number` {{< neo_since ver="8.0.15" />}}

str内でsubstrが最初に現れるインデックスを返します。見つからない場合は-1を返します。

### strLastIndex()

*構文*: `strLastIndex(str, substr) : number` {{< neo_since ver="8.0.15" />}}

str内でsubstrが最後に現れるインデックスを返します。見つからない場合は-1を返します。

### strToUpper()

*構文*: `strToUpper(str) : string` {{< neo_since ver="8.0.7" />}}

`strToUpper` は、strのすべてのUnicode文字を大文字に変換して返します。

### strToLower()

*構文*: `strToLower(str) : string` {{< neo_since ver="8.0.7" />}}

`strToLower` は、strのすべてのUnicode文字を小文字に変換して返します。

### strSprintf()

*構文*: `strSprintf(fmt, args...) : string` {{< neo_since ver="8.0.7" />}}

`strSprintf()` は、書式指定子に従って整形した文字列を返します（Goの `fmt.Sprintf` に相当）。

書式文字列 `fmt` の構文は `%[flags][width][.precision]verb` です。

末尾のverbは、対応する引数の型と解釈方法を定義します。

| verb  | 説明     |
| :---- | :-------------- |
| f     | 10進浮動小数点数、小文字 |
| F     | 10進浮動小数点数、大文字 |
| e     | 指数表記（仮数と指数）、小文字 |
| E     | 指数表記（仮数と指数）、大文字 |
| g     | %eまたは%fのうち短い表現 |
| G     | %Eまたは%Fのうち短い表現 |
| q     | 引用符で囲んだ文字列 |
| t     | trueまたはfalse |
| s     | 文字列 |
| v     | 既定の形式 |
| %%    | 1つの% |

```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE( csv(`world,3.141792`) )
MAPVALUE(1, parseFloat(value(1)))
MAPVALUE(2, strSprintf(`hello %s? %1.2f`, value(0), value(1)))
CSV()
```

```csv
world,3.141792,hello world? 3.14
```

### strTime()

*構文*: `strTime(time, format [, tz]) : string` {{< neo_since ver="8.0.7" />}}

- `time` *time*
- `format` *string*|*sqlTimeformat()*
- `tz` *tz()*：タイムゾーン（省略可）。既定値は `tz('UTC')` です。

`strTime()` は、時刻値を指定した形式とタイムゾーンの文字列に変換します。

```js
MAPVALUE(0, strTime(time("now"), "2006/01/02 15:04:05.999", tz("UTC")), "result")
```

**数値形式のtimeformat**

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), "2006/01/02 15:04:05.999", tz("UTC")), "result")
MARKDOWN(rownum(true))
```

**sqlTimeformat()**

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), sqlTimeformat("YYYY/MM/DD HH24:MI:SS.nnn"), tz("UTC")), "result")
MARKDOWN(rownum(true))
```

|ROWNUM|result|
|:-----|:-----|
|1|2024/01/10 07:27:29.667|

**名前付きtimeformat**

{{< neo_since ver="8.0.12" />}}

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), "RFC822", tz("UTC")), "time")
MARKDOWN(rownum(true))
```

|ROWNUM|time|
|:-----|:-----|
|1|10 Jan 24 07:23 UTC|


### parseFloat()

*構文*: `parseFloat( str )  : number` {{< neo_since ver="8.0.7" />}}

- `str` *string*

`str` を浮動小数点数に変換します。

{{< tabs >}}
{{< tab name="コード" >}}
```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( csv(`world,3.141792`) )
MAPVALUE(1, parseFloat(value(1)))
JSON()
```
{{< /tab >}}
{{< tab name="結果" >}}
```json
{
    "data": {
        "columns": [ "column0", "column1" ],
        "types": [ "string", "double" ],
        "rows": [ [ "world", 3.141792 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "140.125µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### parseBool()

*構文*: `parseBool( str ) : boolean` {{< neo_since ver="8.0.7" />}}

- `str` *string*

文字列 "1"、"t"、"T"、"TRUE"、"true"、"True"、"0"、"f"、"F"、"FALSE"、"false"、"False" を受け取り、
対応するブール値trueまたはfalseに変換します。それ以外の文字列ではエラーを返します。

{{< tabs >}}
{{< tab name="コード" >}}
```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( csv(`world,True`) )
MAPVALUE(1, parseBool(value(1)))
JSON()
```
{{< /tab >}}
{{< tab name="結果" >}}
```json
{
    "data": {
        "columns": [ "column0", "column1" ],
        "types": [ "string", "bool" ],
        "rows": [ [ "world", true ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "122.667µs"
}
```
{{< /tab >}}
{{< /tabs >}}

## 文字列のパターン照合 {#string-match}

### glob()

*構文*: `glob(pattern, text) : boolean` {{< neo_since ver="8.0.7" />}}

`glob` は、`text` が `pattern` に一致する場合にtrueを返します。

```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE( linspace(1, 4, 4))
PUSHVALUE(0, "map."+value(0))
WHEN( glob("*.3", value(0)), doLog("found", value(1)))
CSV()
```

### regexp()

*構文*: `regexp(expression, text) : boolean` {{< neo_since ver="8.0.7" />}}

`regexp` は、`text` が `expression` に一致する場合にtrueを返します。

```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE( linspace(1, 4, 4))
PUSHVALUE(0, "map."+value(0))
WHEN( regexp(`^map\.[2,3]$`, value(0)), doLog("found", value(1)))
CSV()
```

## 時刻 {#time}

### time()

*構文*: `time( number|string ) : time`

- `time('now')` は、現在時刻を返します。
- `time('now -10s50ms')` は、現在より10.05秒前の時刻を返します。
- `time(1672531200*1000000000)` は、2023年1月1日午前0時00分00秒の時刻を返します。

{{< tabs >}}
{{< tab name="time('now')" >}}
```js {linenos=table}
SQL(`select to_char(time), value from example where time < ?`, time('now'))
CSV()
```
{{< /tab >}}
{{< tab name="time(epoch)" >}}
```js
SQL(`select to_char(time), value from example where time = ?`, time(1628737200123456789))
CSV()
```
{{< /tab >}}
{{< /tabs >}}

### timeYear()

*構文*: `timeYear( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeYear()は、*time* の年を返します。

### timeMonth()

*構文*: `timeMonth( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeMonth()は、*time* の月を返します。

### timeDay()

*構文*: `timeDay( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeDay()は、*time* の日を返します。

### timeHour()

*構文*: `timeHour( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeHour()は、*time* の時を[0, 23]の範囲で返します。

### timeMinute()

*構文*: `timeMinute( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeMinute()は、*time* の分を[0, 59]の範囲で返します。

### timeSecond()

*構文*: `timeSecond( time ) : number`  {{< neo_since ver="8.0.15" />}}

timeSecond()は、*time* の秒を[0, 59]の範囲で返します。

### timeNanosecond()

*構文*: `timeNanosecond( time ) : number`  {{< neo_since ver="8.0.15" />}}

timeNanosecond()は、*time* の秒内のナノ秒部分を[0, 999999999]の範囲で返します。

### timeISOYear()

*構文*: `timeISOYear( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeISOYear()は、指定した時刻のISO 8601の年番号を返します。

### timeISOWeek()

*構文*: `timeISOWeek( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeISOWeek()は、*time* のISO 8601の週番号を返します。
週番号の範囲は1から53です。n年の1月1日から3日は、
n-1年の第52週または第53週に属し、12月29日から31日は、
n+1年の第1週に属する場合があります。

暦年の最初の暦週は、その年の最初の木曜日を含む週です。
最後の暦週は、
翌暦年の最初の暦週の直前の週です。
詳細は https://www.iso.org/obp/ui#iso:std:iso:8601:-1:ed-1:v1:en:term:3.1.1.23 を参照してください。

### timeYearDay()

*構文*: `timeYearDay( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeYearDay()は、*time* の年初からの日数を返します。平年は[1,365]、閏年は[1,366]の範囲です。

### timeWeekDay()

*構文*: `timeWeekDay( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeWeekDay()は、*time* の曜日を返します（日曜日 = 0、...）。

```js {{linenos=table,hl_lines=[3]}}
FAKE(arrange(1, 7, 1))
MAPVALUE(0, time(strSprintf("now - %.fd",value(0))))
GROUP( lazy(true), by(timeWeekDay(value(0))), count(value(0)) )
CSV()
```

### timeUnix()

*構文*: `timeUnix( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnix* は、`time` をUnix時刻、すなわち
1970年1月1日UTCからの経過秒数として返します。結果は、
`time` に関連付けられたタイムゾーンに依存しません。

### timeUnixMilli()

*構文*: `timeUnixMilli( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnixMilli* は、`time` をUnix時刻、すなわち
1970年1月1日UTCからの経過ミリ秒数として返します。結果は、
`time` に関連付けられたタイムゾーンに依存しません。

### timeUnixMicro()

*構文*: `timeUnixMicro( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnixMicro* は、`time` をUnix時刻、すなわち
1970年1月1日UTCからの経過マイクロ秒数として返します。結果は、
`time` に関連付けられたタイムゾーンに依存しません。

### timeUnixNano()

*構文*: `timeUnixNano( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnixNano* は、`time` をUnix時刻、すなわち
1970年1月1日UTCからの経過ナノ秒数として返します。結果は、
`time` に関連付けられたタイムゾーンに依存しません。

### timeAdd()

*構文*: `timeAdd( number|string|time [, timeExpression] ) : time`

*例*

- `timeAdd('now', 0)` は、現在時刻を返します。
- `timeAdd('now', '-10s50ms')` は、現在より10.05秒前の時刻を返します。
- `timeAdd(value(0), '1m')` は、value(0)がtimeの場合、その1分後の時刻を返します。

{{< tabs >}}
{{< tab name="timeAdd('now')" >}}
```js {linenos=table}
SQL(`select to_char(time), value from example where time < ?`, timeAdd('now', '-10s'))
CSV()
```
{{< /tab >}}
{{< tab name="timeAdd(epoch)" >}}
```js
SQL(`select to_char(time), value from example where time = ?`, timeAdd(1628737200123456789, '-5s'))
CSV()
```
{{< /tab >}}
{{< /tabs >}}

### roundTime()

*構文*: `roundTime( time, duration ) : time`

Unixエポックからの経過時間を指定間隔の整数倍に切りそろえます。`1h` や `1s` などの単位を指定します。

*例*

- `roundTime(time('now'), '1h')`
- `roundTime(value(0), '1s')`

### parseTime()

*構文*: `parseTime( time, format [, timezone] ) : time`

- `time` *string*：時刻表現
- `format` *string*：時刻の形式。`"DEFAULT"`、`"RFC3339"` などの定義済みの値や、`sqlTimeformat()` などを使用できます。
- `timezone` *tz*：タイムゾーン。`tz()` で必要な地域を取得します。省略時は `tz("UTC")` です。

*例*

- `parseTime("2023-03-01 14:01:02", "DEFAULT", tz("Asia/Tokyo"))`
- `parseTime("2023-03-01 14:01:02", "DEFAULT", tz("local"))`

### tz()

*構文*: `tz( name ) : timeZone`

指定した名前に一致するタイムゾーンを返します。

*例*
- `tz('local')`
- `tz('UTC')`
- `tz('EST')`
- `tz("Europe/Paris")`

<a id="timeformat-sqltimeformat-ansitimeformat"></a>

### timeformat()

*構文*: `timeformat( format )`

- `format` *string*

```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV(timeformat("DEFAULT"), tz("Asia/Seoul"))
```

```
2023-11-30 20:50:32.123,10
2023-11-30 20:50:43.219,11
```

| 形式         | 時刻の出力形式                          |
|:---------------|:------------------------------------------------- |
| DEFAULT        | 2006-01-02 15:04:05.999                           |
| NUMERIC        | 01/02 03:04:05PM '06 -0700                        |
| ANSIC          | Mon Jan _2 15:04:05 2006                          |
| UNIX           | Mon Jan _2 15:04:05 MST 2006                      |
| RUBY           | Mon Jan 02 15:04:05 -0700 2006                    |
| RFC822         | 02 Jan 06 15:04 MST                               |
| RFC822Z        | 02 Jan 06 15:04 -0700                             |
| RFC850         | Monday, 02-Jan-06 15:04:05 MST                    |
| RFC1123        | Mon, 02 Jan 2006 15:04:05 MST                     |
| RFC1123Z       | Mon, 02 Jan 2006 15:04:05 -0700                   |
| RFC3339        | 2006-01-02T15:04:05Z07:00                         |
| RFC3339NANO    | 2006-01-02T15:04:05.999999999Z07:00               |
| KITCHEN        | 3:04:05PM                                         |
| STAMP          | Jan _2 15:04:05                                   |
| STAMPMILLI     | Jan _2 15:04:05.000                               |
| STAMPMICRO     | Jan _2 15:04:05.000000                            |
| STAMPNANO      | Jan _2 15:04:05.000000000                         |
| s              | Unixエポック秒 |
| ms             | Unixエポックミリ秒 |
| us             | Unixエポックマイクロ秒 |
| ns             | Unixエポックナノ秒 |
| s_ms           | 秒とミリ秒（05.999） |
| s_us           | 秒とマイクロ秒（05.999999） |
| s_ns           | 秒とナノ秒（05.999999999） |
| s.ms           | 秒とミリ秒、ゼロ埋め（05.000） |
| s.us           | 秒とマイクロ秒、ゼロ埋め（05.000000） |
| s.ns           | 秒とナノ秒、ゼロ埋め（05.000000000） |

### sqlTimeformat()

*構文*: `sqlTimeformat( format )`

- `format` *string*

| 形式         | 時刻の出力形式                          |
|:---------------|:------------------------------------------------- |
| YYYY           | 4桁の年 |
| YY             | 2桁の年 |
| MM             | 01から12の2桁の月 |
| MMM            | 曜日 |
| DD             | 01から31の2桁の日 |
| HH24           | 00から23の2桁の時 |
| HH12           | 01から12の2桁の時 |
| HH             | 1から12の時（ゼロ埋めなし） |
| MI             | 00から59の2桁の分 |
| SS             | 0から59の2桁の秒 |
| AM             | AM/PM                                             |
| nnn...         | 秒の小数部分（1から9桁） |

```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV( sqlTimeformat("YYYY-MM-DD HH24:MI:SS.nnnnnn"), tz("Asia/Seoul") )
```

```
2023-11-30 20:50:32.123456,10
2023-11-30 20:50:43.219876,11
```

### ansiTimeformat()

*構文*: `ansiTimeformat( format )`

- `format` *string*

```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV( ansiTimeformat("yyyy-mm-dd hh:nn:ss.ffffff"), tz("UTC"))
```

```
2023-11-30 11:50:32.123456,10
2023-11-30 11:50:43.219876,11
```

| 形式         | 時刻の出力形式                          |
|:---------------|:------------------------------------------------- |
| yyyy           | 4桁の年 |
| mm             | 01から12の2桁の月 |
| dd             | 01から31の2桁の日 |
| hh             | 00から23の2桁の時 |
| nn             | 00から59の2桁の分 |
| ss             | 0から59の2桁の秒 |
| fff...         | 秒の小数部分（1から9桁） |


## 数学 {#math}

数学関数です。{{< neo_since ver="8.0.6" />}}

> システムアーキテクチャ間で、ビット単位で同一の結果になる保証はありません。

| 関数         | 説明                         |
|:---------------- | :---------------------------------- |
| `abs(x)`         | xの絶対値 |
| `acos(x)`        | xの逆余弦（ラジアン） |
| `acosh(x)`       | xの逆双曲線余弦 |
| `asin(x)`        | xの逆正弦（ラジアン） |
| `asinh(x)`       | xの逆双曲線正弦 |
| `atan(x)`        | xの逆正接（ラジアン） |
| `atanh(x)`       | xの逆双曲線正接 |
| `ceil(x)`        | x以上の最小の整数値 |
| `cos(x)`         | ラジアンで指定したxの余弦 |
| `cosh(x)`        | xの双曲線余弦 |
| `exp(x)`         | e**x、底がeの指数関数 |
| `exp2(x)`        | 2**x、底が2の指数関数 |
| `floor(x)`       | x以下の最大の整数値 |
| `log(x)`         | xの自然対数 |
| `log2(x)`        | xの2を底とする対数。特殊な場合の動作はlogと同じ |
| `log10(x)`       | xの常用対数。特殊な場合の動作はlogと同じ |
| `max(x,y)`       | xとyの大きい方 |
| `min(x,y)`       | xとyの小さい方 |
| `mod(x,y)`       | x/yの浮動小数点の剰余。<br/>結果の絶対値はyの絶対値未満で、符号はxと同じ |
| `pow(x, y)`      | x**y、底がxの指数関数 |
| `pow10(x)`       | 10**x、底が10の指数関数 |
| `remainder(x,y)` | x/yのIEEE 754浮動小数点の剰余 |
| `round(x)`       | 最も近い整数値。中間値はゼロから遠い方に丸める |
| `sin(x)`         | ラジアンで指定したxの正弦 |
| `sinh(x)`        | xの双曲線正弦 |
| `sqrt(x)`        | xの平方根 |
| `tan(x)`         | ラジアンで指定したxの正接 |
| `tanh(x)`        | xの双曲線正接 |
| `trunc(x)`       | xの整数部分 |

`MAPVALUE` で数学関数を使用する例です。

{{< tabs >}}
{{< tab name="コード" >}}
```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE(meshgrid(linspace(-4,4,100), linspace(-4,4, 100)))
MAPVALUE(2,
    sin(pow(value(0), 2) + pow(value(1), 2)) / (pow(value(0), 2) + pow(value(1), 2))
)
MAPVALUE(0, list(value(0), value(1), value(2)))
POPVALUE(1, 2)
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        grid3D:{},
        xAxis3D:{},
        yAxis3D:{},
        zAxis3D:{},
        series:[
            {type: "line3D", data: column(0)},
        ]
    })
)
```
{{< /tab >}}
{{< tab name="結果" >}}
{{< figure src="/neo/tql/img/tql-math-example.jpg" width="380px" >}}
{{< /tab >}}
{{< /tabs >}}

### random()

*構文*: `random() : number` {{< neo_since ver="8.0.7" />}}

`random()` は、半開区間[0.0,1.0)内の浮動小数点の疑似乱数を返します。

### simplex()

*構文*: `simplex(seed, dim1 [, dim2 [, dim3 [, dim4]]]) : number` {{< neo_since ver="8.0.7" />}}

- `seed` *int*：シード値
- `dim1` ～ `dim4`：*float number*

`simplex()` は、指定したシードと次元値に基づくSimplexノイズ（[Wikipedia](https://en.wikipedia.org/wiki/Simplex_noise)）を返します。

{{< tabs >}}
{{< tab name="コード" >}}
```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE(
    meshgrid(
        linspace(0, 10, 100), linspace(0, 10, 100)
    )
)
MAPVALUE(2, abs( simplex(123, value(0), value(1)) ) * 10)
MAPVALUE(0, list(value(0), value(1), value(2)))
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        visualMap: {
            max: 8,
            inRange:{ color:[ 
                    "#313695", "#74add1", "#e0f3f8",
                    "#fee090",  "#f46d43", "#a50026"]}
        },
        grid3D:{ boxWidth:100, boxDepth:100, boxHeight:20},
        xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
        series:[
            {type: "bar3D", data: column(0), itemStyle:{opacity:1.0}},
        ]
    })
)
```
{{< /tab >}}
{{< tab name="結果" >}}
{{< figure src="/neo/tql/img/map_simplex.jpg" width="430px" >}}
{{< /tab >}}
{{< /tabs >}}

## リスト {#list}

### count()

*構文*: `count( array|tuple ) : number`

要素数を返します。

### list()

*構文*: `list(args...) : list` {{< neo_since ver="8.0.7" />}}

`list()` は、`args` を要素とする新しいタプルを返します。

### dict()

*構文*: `dict( name1, value1 [, name2, value2 ...]) : dictionary` {{< neo_since ver="8.0.8" />}}

`dict()` は、name*n*:value*n* のペアからなる新しい辞書を返します。

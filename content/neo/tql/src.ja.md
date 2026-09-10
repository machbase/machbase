---
title: SRC
type: docs
weight: 11
toc: true
---

すべての *tql* スクリプトは、少なくとも1つのデータソース関数で開始する必要があります。

SRC 関数には複数の種類があります。`SQL()` は Machbase Neo、またはブリッジ接続した外部データベースで
SQL を実行してレコードを生成します。`FAKE()` はテストデータ、`CSV()` は CSV ファイルを読み込み、
`BYTES()` はファイルシステム・HTTP リクエスト・MQTT ペイロードからバイナリデータを取得します。

![tql_src](/neo/tql/img/tql_src.jpg)

## SQL()

*構文*: `SQL( [bridge(),] sqltext [, params...])`

- `bridge()` *bridge('name')*: 指定したブリッジで SQL を実行します。
- `sqltext` *string*: データベースで実行する SELECT 文。複数行にはバッククォート（`）を使います。
- `params`: バインドパラメーターを渡す可変長引数。

**例**

- Machbase のクエリ

```js
SQL (`
    SELECT time, value 
    FROM example 
    WHERE name ='temperature'
    LIMIT 10000
`)
```

- 位置パラメーターを使う可変長引数のクエリ

```js
SQL(`SELECT time, value FROM example WHERE name = ? LIMIT ?`,
    param('name') ?? 'temperature',
    param('limit') ?? 10)
```

- 名前付きパラメーターのクエリ

{{< neo_since ver="8.7.0" />}}

```js
SQL(`SELECT time, value FROM example WHERE name = :name LIMIT :limit`,
    named('name', param('name') ?? 'temperature'),
    named('limit', param('limit') ?? 10))
```

- ブリッジ先データベースのクエリ

```js
SQL( bridge('sqlite'), `SELECT * FROM EXAMPLE`)
```

```js
SQL(
    bridge('sqlite'),
    `SELECT time, value FROM example WHERE name = ?`,
    param('name') ?? "temperature")
```

### named() {{< neo_since ver="8.7.0" />}}

*構文*: `named( name, value )`

SQL の `:name` など、名前付きバインドプレースホルダーへ渡すパラメーターを指定します。

- `name` *string*: SQL の `:name` プレースホルダーに対応するパラメーター名。
- `value` *any*: バインドする値。

**例**

```js
SQL("SELECT time, value FROM tag_simple WHERE name = :name LIMIT :one",
    named("name", "tag1"),
    named("one", 1))
```

```js
SQL(`
    SELECT * FROM example
    WHERE name = :name
      AND time BETWEEN :from AND :to
`,
    named("name", "microwave"),
    named("from", "2023-03-01 14:00:00"),
    named("to", "2023-03-01 14:10:00"))
```

## SQL_SELECT()

*構文*: `SQL_SELECT( fields..., from(), between() [, limit()] )` {{< neo_since ver="8.0.15" />}}

- `fields` *string*: 取得する列名。複数指定できます。

*SQL_SELECT()* は `SQL()` と同じ機能を、SQL 文ではなくオプション関数で指定できます。
特に時間範囲を簡潔に記述できます。

次の例は、内部で `SELECT time, value FROM example WHERE NAME = 'temperature' AND time BETWEEN ...`
という形式の SQL を生成します。

```js
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    between('last-10s', 'last')
)
```

上のコードは次の SQL に相当します。

```js
SQL(`SELECT
        time, value
    FROM
        EXAMPLE
    WHERE
        name = 'temperature'
    AND time BETWEEN (
        SELECT MAX_TIME-10000000000
        FROM V$EXAMPLE_STAT
        WHERE name = 'temperature')
    AND (
        SELECT MAX_TIME
        FROM V$EXAMPLE_STAT
        WHERE name = 'temperature')
    LIMIT 0, 1000000
`)
```

### from()

*構文*: `from( table, tag [, time_column [, name_column] ] )`

テーブル名とタグ名を指定します。内部では `... FROM <table> WHERE NAME = <tag> ...` を構成します。

- `table` *string*: テーブル名。
- `tag` *string*: タグ名。
- `time_column` *string*: 時刻列名。デフォルトは `'time'`。
- `name_column` *string*: タグ列名。デフォルトは `'name'`。{{< neo_since ver="8.0.5" />}}

### between()

*構文*: `between( fromTime, toTime [, period] )`

時間範囲を指定します。内部では `... WHERE ... TIME BETWEEN <fromTime> AND <toTime> ...` を構成します。

- `fromTime` *string|number*: `'now'`、`'last'` などの式、またはナノ秒単位の Unix epoch。
- `toTime` *string|number*: 終了時刻。
- `period` *string|number*: 区間の長さ。期間文字列またはナノ秒の数値で指定し、正の値だけが有効です。

例えば `'now-1h30m'` は現在から1時間30分前、`'last-30s'` は最新時刻から30秒前を表します。

`period` を指定すると、`GROUP BY time` と集計関数を含む SQL を生成します。
この場合、`fields` に基準時刻列を含める必要があります。

日時文字列は `parseTime()` でナノ秒タイムスタンプに変換してください。詳細は
[parseTime()](/neo/tql/utilities/#parsetime)を参照してください。

```js
between( parseTime("2023-03-01 14:00:00", "DEFAULT", tz("Local")),
         parseTime("2023-03-01 14:05:00", "DEFAULT", tz("Local")))
```

### limit()

*構文*: `limit( [offset ,] count )`

`SELECT ... LIMIT offset, count` を生成します。

- `offset` *number*: デフォルト `0`。
- `count` *number*。

## CSV()

*構文*: `CSV( file(file_path_string) | payload() [, charset()] [,field()...[, header()]] )`

CSV を読み込み、キーと値からなるレコードを生成します。キーは連番、値は CSV のフィールドです。
`file()` には絶対パスを指定します。`payload()` は HTTP POST 本文から直接 CSV を読み込めるため、
リモートクライアントから受信したデータをすぐに保存する API の作成に便利です。

- `file() | payload()`: 入力ストリーム。
- `field(idx, type, name)`: フィールド定義。
- `header(bool)`: 先頭行をヘッダーとして扱うか。
- `charset(string)`: UTF-8 以外の CSV の文字セット。{{< neo_since ver="8.0.8" />}}
- `logProgress([int])`: `n` 行ごとに進捗ログを出力。省略時は500,000行。{{< neo_since ver="8.0.29" />}}

```js
// HTTP リクエスト本文から CSV を読み込む例
// 例:
// barn,1677646800,0.03135
// dew_point,1677646800,24.4
// dishwasher,1677646800,3.33e-05
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('s'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
APPEND(table('example'))
```

`CSV()` と `APPEND()` を組み合わせると、簡潔で実用的な API を作れます。
コマンドラインの import と比べて約5倍遅いものの、HTTP リクエストごとに数千件以上を処理する場合は
`INSERT()` より高速です。

HTTP POST がない場合にも動作させるには、`??` 演算子を使用できます。

```js
CSV(payload() ?? file('/absolute/path/to/data.csv'),
    field(0, floatType(), 'freq'),
    field(1, floatType(), 'ampl')
)
CHART_LINE()
```

### file()

*構文*: `file(path)`

指定パスのファイルを開き、入力ストリームを返します。HTTP URL のリソースも取得できます
{{< neo_since ver="8.0.7" />}}。

- `path` *string*: ファイルの絶対パス、または HTTP/HTTPS URL。

```js
CSV( file(`http://127.0.0.1:5654/db/query?`+
        `format=csv&`+
        `q=`+escapeParam(`select * from example limit 10`)
))
CSV() // または JSON()
```

### payload()

*構文*: `payload()`

HTTP POST または MQTT PUBLISH で渡された本文を入力ストリームとして返します。

### field()

*構文*: `field(idx, typefunc, name)`

CSV フィールドの型を指定します。

- `idx` *number*: 0始まりのフィールドインデックス。
- `typefunc`: フィールドの型を指定する関数。
- `name` *string*: フィールド名。

| 型関数 | 型 |
|:------------------|:---------|
| `stringType()` | string |
| `doubleType()` | double |
| `datetimeType()` | datetime |
| `boolType()` | boolean {{< neo_since ver="8.0.20" />}} |
| ~~`floatType()`~~ | *非推奨。`doubleType()` を使用* {{< neo_since ver="8.0.20" />}} |
| ~~`timeType()`~~ | *非推奨。`datetimeType()` を使用* {{< neo_since ver="8.0.20" />}} |

`stringType()` と `boolType()` は引数を取りません。`datetimeType()` は時刻の単位や形式を指定できます。

Unix epoch を使う場合は、次のように単位を指定します。

- `datetimeType('s')`
- `datetimeType('ms')`
- `datetimeType('us')`
- `datetimeType('ns')`

人が読む日時形式を使う場合は、形式とタイムゾーンを併せて指定します。

- `datetimeType('DEFAULT', 'Local')`

```js
CSV(payload() ??
`name,2006-01-02 15:04:05.999,10`,
field(1, datetimeType('DEFAULT', 'Local'), 'time'))
CSV()
```

- `datetimeType('RFC3339', 'EST')`

```js
CSV(payload() ??
`name,2006-01-02T15:04:05.999Z,10`,
field(1, datetimeType('RFC3339', 'EST'), 'time'))
CSV()
```

タイムゾーンの省略時は `UTC` です。

- `datetimeType('RFC822')`

第1引数は `timeformat()` と同じ形式を使います。詳細は
[timeformat](../utilities/#timeformat-sqltimeformat-ansitimeformat)を参照してください。

### charset()

*構文*: `charset(name)` {{< neo_since ver="8.0.8" />}}

- `name` *string*: 文字セット名。

サポートする文字セット:

UTF-8, ISO-2022-JP, EUC-KR, SJIS, CP932, SHIFT_JIS, EUC-JP, UTF-16, UTF-16BE, UTF-16LE,
CP437, CP850, CP852, CP855, CP858, CP860, CP862, CP863, CP865, CP866, LATIN-1,
ISO-8859-1, ISO-8859-2, ISO-8859-3, ISO-8859-4, ISO-8859-5, ISO-8859-6, ISO-8859-7,
ISO-8859-8, ISO-8859-10, ISO-8859-13, ISO-8859-14, ISO-8859-15, ISO-8859-16,
KOI8R, KOI8U, MACINTOSH, MACINTOSHCYRILLIC, WINDOWS1250, WINDOWS1251, WINDOWS1252,
WINDOWS1253, WINDOWS1254, WINDOWS1255, WINDOWS1256, WINDOWS1257, WINDOWS1258, WINDOWS874,
XUSERDEFINED, HZ-GB2312

## SCRIPT()

ユーザー定義のスクリプト言語をサポートします。例は [SCRIPT](../script/)を参照してください。

## HTTP()

簡潔な DSL で HTTP リクエストを送信できます。例は [HTTP](../http/)を参照してください。

## BYTES(), STRING()

*構文*: `BYTES( src [, separator(char), trimspace(boolean) ] )`

*構文*: `STRING( src [, separator(char), trimspace(boolean) ] )`

- `src`: データソース。`payload()`、`file()`、文字列定数を指定できます。
- `separator(char)`: 任意。`separator("\n")` のように指定すると行ごとに分割します。
- `trimspace(boolean)`: 任意。空白を除去するか。デフォルトは `false`。

入力を区切り文字で分割してレコードを生成します。キーは増加する整数です。

**例**

- `STRING('A,B,C', separator(","))` → `["A"]`、`["B"]`、`["C"]` の3レコード。
- `STRING('A,B,C')` → `["A,B,C"]` の1レコード。

`BYTES()` と `STRING()` は戻り値の型だけが異なり、前者はバイト配列、後者は文字列を返します。

```js
STRING(payload() ?? `12345
                    23456
                    78901`, separator("\n"))
```

上のコードは `["12345"]`、`["          23456"]`、`["          78901"]` の3レコードを生成します。

```js
STRING(payload() ?? `12345
                    23456
                    78901`, separator("\n"), trimspace(true))
```

空白を除去すると、`["12345"]`、`["23456"]`、`["78901"]` になります。

```js
STRING( file(`http://example.com/data/words.txt`), separator("\n") )
```

HTTP アドレスからデータを取得する例です。`file()` は HTTP URL をサポートします
{{< neo_since ver="8.0.7" />}}。

## ARGS()

*構文*: `ARGS()` {{< neo_since ver="8.0.7" />}}

親 TQL フローから渡された引数を値とするレコードを生成します。主に `WHEN...do()` サブフローの SRC に使います。

```js {linenos=table,hl_lines=[6],linenostart=1}
FAKE( json({
    [ 1, "hello" ],
    [ 2, "world" ]
}))
WHEN( value(0) == 2, do( value(0), strToUpper(value(1)), {
    ARGS()
    WHEN( true, doLog("OUTPUT:", value(0), value(1)) )
    DISCARD()
}))
CSV()
```

実行すると、コンソールに次のように出力されます。

```
OUTPUT: 2 WORLD
```

## FAKE()

*構文*: `FAKE( generator )`

- `generator`: `oscillator()`、`meshgrid()`、`linspace()`、`arrange()`、`csv()`、`json()` のいずれか。

指定したジェネレーターでテストデータを生成します。

### oscillator()

*構文*: `oscillator( freq() [, freq()...], range() )`

周波数と時間範囲を指定して波形データを生成します。複数の `freq()` を指定すると合成波形になります。

{{< tabs >}}
{{< tab name="ノイズなし" >}}
```js {{linenos=table,hl_lines=[1],linenostart=1}}
FAKE( oscillator( freq(3, 1.0), range("now-3s", "3s", "5ms") ))
// | 0        1
// | time     amplitude
MAPVALUE(0, list(value(0), value(1)))
// | 0                  1
// | (time, amplitude)  amplitude
POPVALUE(1)
// | 0
// | (time, amplitude)
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        series:[ { type: "line", data: column(0) } ]
    })
)
```
{{< /tab >}}
{{< tab name="ノイズを追加" >}}
```js {{linenos=table,hl_lines=[4],linenostart=1}}
FAKE( oscillator( freq(3, 1.0), range("now-3s", "3s", "5ms") ))
// | 0        1
// | time     amplitude
MAPVALUE(1, value(1) + (random()-0.5) * 0.2 )
// | 0        1
// | time     amplitude
MAPVALUE(0, list(value(0), value(1)))
// | 0                  1
// | (time, amplitude)  amplitude
POPVALUE(1)
// | 0
// | (time, amplitude)
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        series:[ { type: "line", data: column(0) } ]
    })
)
```
{{< /tab >}}
{{< /tabs >}}

#### freq()

*構文*: `freq( frequency, amplitude [, bias, phase])`

`amplitude * SIN( 2*Pi * frequency * time + phase) + bias` の正弦波を生成します。

- `frequency` *number*: 周波数（Hz）。
- `amplitude` *number*。
- `bias` *number*。
- `phase` *number*: ラジアン。

#### range()

*構文*: `range( fromTime, duration, period )`

`fromTime` から `fromTime + duration` までの時間範囲を定義します。

- `fromTime` *string|number*: `'now'`、`'last'`、またはナノ秒単位の epoch。
- `duration` *string|number*: 期間。例: `'-1d2h30m'`、`'1s100ms'`。
- `period` *string|number*: サンプル間隔。期間文字列またはナノ秒の数値で指定し、正の値だけが有効です。

### arrange()

*構文*: `arrange(start, stop, step)` {{< neo_since ver="8.0.12" />}}

- `start` *number*
- `stop` *number*
- `step` *number*

```js {{linenos="table",hl_lines=[2]}}
FAKE(
   arrange(1, 2, 0.5)
)
CSV()
```

```csv
1
1.5
2
```

### linspace()

*構文*: `linspace(start, stop, num)`

1次元の等間隔シーケンスを生成します。

{{< tabs >}}
{{< tab name="CSV" >}}
```js {{linenos="table",hl_lines=[2]}}
FAKE(
   linspace(1, 3, 3)
)
CSV()
```

```csv
1
2
3
```
{{< /tab >}}
{{< tab name="CHART" >}}

```js {{linenos="table",hl_lines=[1]}}
FAKE( linspace(0,4*PI,100) )
MAPVALUE(1, sin(value(0)))
MAPVALUE(2, cos(value(0)))
CHART(
  theme("dark"),
  size("600px", "340px"),
  chartOption({
    title: {text: "sin-cos"},
    xAxis:{ data: column(0) },
    yAxis:{},
    series: [
      { name:"SIN", type: "line", data: column(1), 
          markLine:{ data: [{yAxis: 0.5}], label:{show: true, formatter: "half {c} "} } },
      { name:"COS", type: "line", data: column(2) },
    ]
  })
)
```

{{< figure src="/neo/tql/img/linspace_chart.jpg" width="600px" >}}

{{< /tab >}}
{{< /tabs >}}

### meshgrid()

*構文*: `meshgrid(xseries, yseries)`

x軸とy軸の値を組み合わせたメッシュデータを生成します。

{{< tabs >}}
{{< tab name="CSV" >}}
```js {{linenos="table",hl_lines=[2]}}
FAKE(
    meshgrid( linspace(1, 3, 3), linspace(10, 30, 3) )
)
CSV()
```

```csv
1,10
1,20
1,30
2,10
2,20
2,30
3,10
3,20
3,30
```
{{< /tab >}}
{{< tab name="CHART" >}}
```js {{linenos="table",hl_lines=[1]}}
FAKE(meshgrid(linspace(0,2*3.1415,30), linspace(0, 3.1415, 20)))

SET(x, cos(value(0))*sin(value(1)))
SET(y, sin(value(0))*sin(value(1)))
SET(z, cos(value(1)))
MAPVALUE(0, list($x, $y, $z))
POPVALUE(1)

CHART(
  plugins("gl"),
  size("600px", "600px"),
  chartOption({
    grid3D:{},
    xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
    visualMap:[{ 
      min:-1, max:1, 
      inRange:{color:["#313695",  "#74add1", "#ffffbf","#f46d43", "#a50026"]
    }}],
    series:[
      { type:"scatter3D", data: column(0)}
    ]
  })
)
```

{{< figure src="/neo/tql/img/meshgrid_chart.jpg" width="350px" >}}

{{< /tab >}}
{{< /tabs >}}

### csv()

*構文*: `csv(content)` {{< neo_since ver="8.0.7" />}}

- `content` *string*: CSV 文字列。

指定した CSV 内容をレコードへ変換します。

```js {{linenos="table",hl_lines=["2-6"]}}
FAKE(
    csv( strTrimSpace(`
        A,1,true
        B,2,false
        C,3,true
    `))
)
MAPVALUE(0, strTrimSpace(value(0)))
MAPVALUE(1, parseFloat(value(1))*10)
MAPVALUE(2, parseBool(value(2)))
CSV()
```

```csv
A,10,true
B,20,false
C,30,true
```

### json()

*構文*: `json({...})` {{< neo_since ver="8.0.7" />}}

複数の JSON 配列をレコードへ変換します。

```js {{linenos="table",hl_lines=["2-6"]}}
FAKE(
    json({
        ["A", 1, true],
        ["B", 2, false],
        ["C", 3, true]
    })
)
MAPVALUE(1, value(1)*10)
CSV()
```

```csv
A,10,true
B,20,false
C,30,true
```

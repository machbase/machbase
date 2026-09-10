---
title: インポートとエクスポート
type: docs
weight: 600
toc: true
---

## CSV のインポート

```sh
curl -o - https://docs.machbase.com/assets/example/example.csv.gz | \
machbase-neo shell import   \
    --input -               \
    --compress gzip         \
    --timeformat s          \
    EXAMPLE
```
`curl` でリモート Web サーバーから圧縮 CSV をダウンロードします。`-o -` は取得した圧縮バイナリーを標準出力へ書き込み、パイプで `machbase-neo shell import` に渡します。import は `--input -` で標準入力を読み取ります。

パイプ（`|`）で接続すると、一時ファイルを作成せずに処理でき、ローカルストレージを節約できます。

次の結果は、1,000 件のレコードをインポートできたことを示します。

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  5352  100  5352    0     0   547k      0 --:--:-- --:--:-- --:--:-- 5226k
import total 1000 record(s) inserted
```

ファイルをローカルに保存してからインポートすることもできます。

```sh
curl -o data.csv.gz https://docs.machbase.com/assets/example/example.csv.gz
```

CSV は圧縮の有無にかかわらずインポートできます。ローカルファイルを `--input <ファイル>` で指定し、gzip 圧縮の場合は `--compress gzip` を追加してください。

`-v /mnt=.` は、現在のディレクトリ（`.`）をシェルの実行環境の `/mnt` にマウントします。ローカルファイルには、マウント後のパス（例: `/mnt/data.csv.gz`）でアクセスします。

```sh
machbase-neo shell -v /mnt=. \
    import \
    --input /mnt/data.csv.gz \
    --compress gzip         \
    --timeformat s        \
    EXAMPLE
```

インポート結果を確認します。

```sh
machbase-neo shell "select * from example order by time desc limit 5"
```
```
 ROWNUM  NAME      TIME(UTC)            VALUE     
──────────────────────────────────────────────────
 1       wave.sin  2023-02-15 03:47:50  0.994540  
 2       wave.cos  2023-02-15 03:47:50  -0.104353 
 3       wave.sin  2023-02-15 03:47:49  0.951002  
 4       wave.cos  2023-02-15 03:47:49  0.309185  
 5       wave.cos  2023-02-15 03:47:48  0.669261  
```

サンプルには 1,000 件のレコードがあります。インポート後のテーブルにも同じ件数が格納されていることを確認します。

```sh
machbase-neo shell "select count(*) from example"
```
```
 ROWNUM  COUNT(*) 
──────────────────
 1       1000     
```

## CSV のエクスポート

`--output` で出力先のファイルパスを、`--format csv` で CSV 形式を指定します。`--timeformat ns` は DATETIME 列をナノ秒単位の UNIX エポック時刻で出力します。

```sh
machbase-neo shell export --output ./example_out.csv --format csv --timeformat ns EXAMPLE
```

## エクスポートとインポートによるテーブルのコピー

エクスポートとインポートをパイプで接続すると、ローカルの一時ファイルなしでデータをコピーできます。

まず、コピー先のテーブルを作成します。

```sh
machbase-neo shell \
    "create tag table EXAMPLE_COPY (name varchar(100) primary key, time datetime basetime, value double)"
```

次に、export と import をパイプで接続します。

```sh
machbase-neo shell export       \
    --output -                  \
    --no-header                 \
    --format csv                \
    --timeformat ns             \
    EXAMPLE  |  \
machbase-neo shell import       \
    --input -                   \
    --format csv                \
    --timeformat ns             \
    EXAMPLE_COPY
```

コピー先の件数を確認します。

```sh
 machbase-neo shell "select count(*) from EXAMPLE_COPY"
```
```
 ROWNUM  COUNT(*) 
──────────────────
 1       1000     
```

この方法は、データベース A から B へのコピーにも使用できます。`--server <アドレス>` でリモートの machbase-neo を指定し、export と import を別々のサーバーに対して実行できます。

## クエリ結果のインポート

SELECT の結果を直接 import に渡すこともできます。

```sh
machbase-neo shell sql \
    --output -         \
    --format csv       \
    --no-rownum        \
    --no-header       \
    --timeformat ns    \
    "select * from example where name = 'wave.sin' order by time" | \
machbase-neo shell import \
    --input -             \
    --format csv          \
    EXAMPLE_COPY
```

この例は `wave.sin` タグのデータを `EXAMPLE_COPY` にインポートします。入力 CSV のフィールド数と型を一致させるため、sql に `--no-rownum` と `--no-header` を指定します。

## HTTP API によるクエリ結果の取り込み

machbase-neo の HTTP API から取得したクエリ結果を、別のテーブルに取り込めます。

```sh
curl -o - http://127.0.0.1:5654/db/query        \
    --data-urlencode "q=select * from EXAMPLE order by time desc limit 100" \
    --data-urlencode "format=csv"                \
    --data-urlencode "heading=false" |           \
curl http://127.0.0.1:5654/db/write/EXAMPLE_COPY \
    -H "Content-Type: text/csv"                  \
    -X POST --data-binary @- 
```

## インポート方式: insert と append

デフォルトの `--method insert` は `INSERT INTO ...` を使用します。少量のデータでは差が小さいものの、数十万件以上の大量データでは `--method append` が効率的です。

## 例

データファイルをテーブルに取り込む例を示します。

{{< callout emoji="📌" >}}
先に次のクエリでテーブルを準備してください。
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

### CSV のインポート

次の内容で `data.csv` を作成します。

```
name-0,1687405320000000000,123.456
name-1,1687405320000000000,234.567000
name-2,1687405320000000000,345.678000
```

データをインポートします。

```sh
machbase-neo shell import \
    --input ./data.csv    \
    --timeformat ns        \
    EXAMPLE
```

データを検索します。

```sh
machbase-neo shell "SELECT * FROM EXAMPLE";

 ROWNUM  NAME    TIME(LOCAL)          VALUE   
──────────────────────────────────────────────
      1  name-0  2023-06-22 12:42:00  123.456 
      2  name-1  2023-06-22 12:42:00  234.567 
      3  name-2  2023-06-22 12:42:00  345.678 
3 rows fetched.
```

### TQL によるインポート

**テキストのインポート**

以下の結果例は、空の EXAMPLE テーブルに各入力を 1 回ずつ取り込んだ場合です。時刻と表示順序は実行時によって変わります。

次の内容で `import-data.csv` を作成します。

```
1,100,value,10
2,200,value,11
3,140,value,12
```

次のコードを TQL エディターに入力し、`import-tql-csv.tql` として保存します。

```js
STRING(payload() ?? `1,100,value,10
2,200,value,11
3,140,value,12`, separator('\n'))

SCRIPT({
    str =  $.values[0].trim().split(',');
    $.yield(
        "tag-" + str[0],
        (new Date().getTime()*1000000),
        parseInt(str[1])+parseInt(str[3])
    )
})
APPEND(table("example"))
```

作成した TQL に CSV を送信します。

```sh
curl -o - --data-binary @import-data.csv http://127.0.0.1:5654/db/tql/import-tql-csv.tql

append 3 rows (success 3, fail 0).
```

データを検索します。

```sh
machbase-neo shell "select * from example";

 ROWNUM  NAME   TIME(LOCAL)          VALUE 
───────────────────────────────────────────
      1  tag-1  <実行時刻>           110   
      2  tag-2  <実行時刻>           211   
      3  tag-3  <実行時刻>           152   
3 rows fetched.
```

**JSON のインポート**

`import-data.json` を作成します。

```json
{
  "tag": "pump",
  "data": {
    "string": "Hello TQL?",
    "number": "123.456",
    "time": 1687405320,
    "boolean": true
  },
  "array": ["elements", 234.567, 345.678, false]
}
```

次のコードを TQL エディターに入力し、`import-tql-json.tql` として保存します。

```js
STRING( payload() ?? {
    {
        "tag": "pump",
        "data": {
            "string": "Hello TQL?",
            "number": "123.456",
            "time": 1687405320,
            "boolean": true
        },
        "array": ["elements", 234.567, 345.678, false]
    }
})
SCRIPT({
    obj = JSON.parse($.values[0]);
    $.yield(obj.tag+"_0", obj.data.time*1000000000, parseFloat(obj.data.number))
    $.yield(obj.tag+"_1", obj.data.time*1000000000, obj.array[1])
    $.yield(obj.tag+"_2", obj.data.time*1000000000, obj.array[2])
    for (i = 0; i < obj.array.length; i++) {
    }
})
APPEND(table("example"))
```

作成した TQL に JSON を送信します。

```sh
curl -o - --data-binary @import-data.json http://127.0.0.1:5654/db/tql/import-tql-json.tql

append 3 rows (success 3, fail 0).
```

データを検索します。

```sh
machbase-neo shell "select * from example";

 ROWNUM  NAME    TIME(LOCAL)          VALUE
──────────────────────────────────────────────
      1  tag-1   <実行時刻>           110
      2  pump_2  2023-06-22 12:42:00  345.678
      3  tag-2   <実行時刻>           211
      4  tag-3   <実行時刻>           152
      5  pump_1  2023-06-22 12:42:00  234.567
      6  pump_0  2023-06-22 12:42:00  123.456
6 rows fetched.
```


### ブリッジからのインポート

**事前準備**

```sh
bridge add -t sqlite mem file::memory:?cache=shared;

bridge exec mem create table if not exists mem_example(name varchar(20), time datetime, value double);

bridge exec mem insert into mem_example values('tag0', '2021-08-12', 10);
bridge exec mem insert into mem_example values('tag0', '2021-08-13', 11);
```

**ブリッジのデータのインポート**

TQL エディターで次のコードを実行します。

```js
SQL(bridge('mem'), "select * from mem_example")
APPEND(table('example'))
```

データを検索します。

```sh
machbase-neo shell "select * from example";

 ROWNUM  NAME  TIME(LOCAL)          VALUE 
──────────────────────────────────────────
      1  tag0  2021-08-12 09:00:00  10    
      2  tag0  2021-08-13 09:00:00  11    
2 rows fetched.
```

### CSV のエクスポート

データをエクスポートします。

```sh
machbase-neo shell export      \
    --output ./data_out.csv    \
    --format csv               \
    --timeformat ns            \
    EXAMPLE
```

出力したファイルを確認します。

```sh
cat data_out.csv 

TAG0,1628694000000000000,100
TAG0,1628780400000000000,110
```

### JSON のエクスポート

データをエクスポートします。

```sh
machbase-neo shell export      \
    --output ./data_out.json   \
    --format json              \
    --timeformat ns            \
    EXAMPLE
```

出力したファイルを確認します。

```sh
cat data_out.json

{
  "data": {
    "columns": [
      "NAME",
      "TIME",
      "VALUE"
    ],
    "types": [
      "string",
      "datetime",
      "double"
    ],
    "rows": [
      [
        "TAG0",
        1628694000000000000,
        100
      ],
      [
        "TAG0",
        1628780400000000000,
        110
      ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.847207ms"
}
```

### TQL によるエクスポート

**CSV のエクスポート**

```js
SQL(`select * from example`)
CSV()
```

**JSON のエクスポート**

```js
SQL(`select * from example`)
JSON()
```

**TQL スクリプトで CSV をエクスポート**

次のコードを TQL エディターに入力し、`export-tql-csv.tql` として保存します。

```js
SQL( 'select * from example limit 30' )
SCRIPT({
    if  ($.values[2] % 2 == 0) {
        r_value = "even"
    } else {
        r_value = "odd"
    }

    $.yield($.key + "-tql", $.values[2],  r_value)
})
CSV()
```

[TQL の URL](http://127.0.0.1:5654/db/tql/export-tql-csv.tql) をブラウザーで開くか、ターミナルから curl で取得します。

```sh
TAG1-tql,11,odd
TAG0-tql,10,even
```

### ブリッジへのエクスポート

**事前準備**

```sh
bridge add -t sqlite mem file::memory:?cache=shared;

bridge exec mem create table if not exists mem_example(name varchar(20), time datetime, value double);
```

**ブリッジへのデータのエクスポート**

次のコードを TQL エディターで実行します。

```js
SQL("select * from example")
INSERT(bridge('mem'), table('mem_example'), 'name', 'time', 'value')
```

ブリッジのテーブルを検索します。

```sh
machbase-neo shell bridge query mem "select * from mem_example";

┌──────┬───────────────────────────────┬───────┐
│ NAME │ TIME                          │ VALUE │
├──────┼───────────────────────────────┼───────┤
│ TAG0 │ 2021-08-12 00:00:00 +0900 KST │    10 │
│ TAG1 │ 2021-08-13 00:00:00 +0900 KST │    11 │
└──────┴───────────────────────────────┴───────┘
```

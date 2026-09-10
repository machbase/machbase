---
toc: true
title: 波形データの作成
type: docs
weight: 10
---

このチュートリアルは、シェルスクリプトだけでデータベースを読み書きする方法を説明します。

{{< callout emoji="📌">}}
この例を実行する前に、以下のテーブルを作成してください。
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE  (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
``` 

## データの書き込み {#데이터-쓰기}

machbase-neoにデータを書き込む最も簡単な方法は、コマンドラインツール`machbase-neo shell`を使う方法です。
このツールで、テーブルのインポート、エクスポート、検索を行えます。

### データの生成 {#데이터-생성}

この例では、1秒ごとにサイン・コサイン値を出力する簡単なシェルスクリプトを使用します。

以下のスクリプトをコピーし、`gen_wave.sh`として保存してください。

```sh
#!/bin/bash
angle=0
step_angle=24
sinval=0
cosval=0
PI=3.14159

while [ 1 ]
do
    ts=`date +"%s"`
    sinval=$(awk "BEGIN{ printf \"%.6f\", (sin($angle*($PI/180)))}")
    cosval=$(awk "BEGIN{ printf \"%.6f\", (cos($angle*($PI/180)))}")
    echo "wave.sin,$ts,$sinval"
    echo "wave.cos,$ts,$cosval"
    sleep 1
    angle=$((angle+step_angle))
done
```

### スクリプトの実行 {#스크립트-실행}

作成したスクリプトを実行します。

```sh
sh ./gen_wave.sh
```

スクリプトは毎秒、`wave.sin`、`wave.cos`の名前と、Unixタイムスタンプ、値をCSV形式で出力します。
この出力は、`machbase-neo shell`でそのまま使用できます。

停止するには、`Ctrl+C`を押してください。

![wave-write-sh01](/images/wave-write-sh01.gif)

出力CSVの列順は、テーブルの構造に合わせる必要があります。

テーブルの構造は、次のコマンドで確認できます。

```sh
machbase-neo shell desc EXAMPLE
```

`desc <table>`サブコマンドは、テーブル情報を表示します。

```
TABLE    EXAMPLE
TYPE     Tag Table
TAGS     wave.cos, wave.sin
┌───┬───────┬──────────┬────────┐
│ # │ NAME  │ TYPE     │ LENGTH │
├───┼───────┼──────────┼────────┤
│ 1 │ NAME  │ varchar  │    100 │
│ 2 │ TIME  │ datetime │      8 │
│ 3 │ VALUE │ double   │      8 │
└───┴───────┴──────────┴────────┘
```

CSVをテーブルにインポートする場合は、列順とデータ型をテーブル定義に必ず合わせてください。

### スクリプトとコマンドの組み合わせ {#스크립트와-명령어-결합}

スクリプトの出力を、`machbase-neo shell`の入力に使用します。

```sh
sh gen_wave.sh | machbase-neo shell import --timeformat=s EXAMPLE
```

{{< callout type="info">}}
**timeformat**<br/> machbase-neoは、すべてのタイムスタンプをナノ秒単位で扱います。
シェルスクリプトは`date`コマンドで秒単位のタイムスタンプを生成するため、
`--timeformat`オプションで、CSVデータの時刻が秒単位であることを明示する必要があります。<br/>
詳細は、`machbase-neo shell help timeformat`を参照してください。
{{< /callout >}}

シェルスクリプトが生成したCSVの各行は、`machbase-neo shell import`で処理され、`EXAMPLE`テーブルに取り込まれます。

同じ方式で、データを直接入力することもできます。

```
echo "wave.pi,1674860125,3.141592" | machbase-neo shell import -t s EXAMPLE
```

または

```
echo "wave.pi,`date +%s`,3.141592" | machbase-neo shell import -t s EXAMPLE
```

最新の値を検索します。

```sh
machbase-neo shell "select * from EXAMPLE where NAME='wave.pi' order by time desc limit 1"
```

![wave-write-sh02](/images/wave-write-sh02.gif)


## データの読み取り {#데이터-읽기}

{{% steps %}}

### SQLクエリ {#sql-쿼리}

スクリプトの実行中に、

```sh
sh gen_wave.sh | machbase-neo shell import --timeformat=s EXAMPLE
``` 

SQLクエリでデータを出力します。

```sh
machbase-neo shell "select * from EXAMPLE order by time desc"
```

```
 #     NAME      TIME(UTC)            VALUE
────────────────────────────────────────────────
 1     wave.sin  2023-01-28 14:03:59  0.214839
 2     wave.cos  2023-01-28 14:03:59  -0.976649
 3     wave.sin  2023-01-28 14:03:58  0.593504
 4     wave.cos  2023-01-28 14:03:58  -0.804831
  ...
```

![img](/images/shell-sql.gif)

上記の例では、`machbase-neo shell`に`sql`サブコマンドを明示しなくても、クエリが正常に実行されます。
追加の引数やオプションがない場合は、既定で`sql`サブコマンドを使用するためです。
つまり、`machbase-neo shell "select..."`と`machbase-neo shell sql "select..."`は同じです。

オプションを使用する場合は、以下のように`sql`サブコマンドを明示してください。

```sh
machbase-neo shell sql \
    --tz America/Los_Angeles \
    "select * from EXAMPLE order by time desc limit 4"
```

```
 #  NAME      TIME(AMERICA/LOS_ANGELES)  VALUE
───────────────────────────────────────────────────
 1  wave.sin  2023-01-28 06:03:59        0.214839
 2  wave.cos  2023-01-28 06:03:59        -0.976649
 3  wave.cos  2023-01-28 06:03:58        -0.804831
 4  wave.sin  2023-01-28 06:03:58        0.593504
```

Machbaseは、既定で時刻をUTCで表示します。
他のタイムゾーンで表示するには、`--tz`オプションを使用します。
`local`、または`Europe/Paris`などのTZデータベース文字列を指定できます。

```sh
machbase-neo shell sql \
    --tz local \
    "select * from EXAMPLE order by time desc limit 4"
```
```
 #  NAME      TIME(LOCAL)          VALUE
─────────────────────────────────────────────
 1  wave.sin  2023-01-28 23:03:59  0.214839
 2  wave.cos  2023-01-28 23:03:59  -0.976649
 3  wave.cos  2023-01-28 23:03:58  -0.804831
 4  wave.sin  2023-01-28 23:03:58  0.593504
 ```

{{% /steps %}}

### 表形式の表示 {#table-view}

以下のように「walk」コマンドで、クエリ結果を前後に移動して表示できます。

```sh
machbase-neo shell walk "select * from EXAMPLE order by time desc"
```

キーボードで上下にスクロールし、`ESC`で表の表示を終了します。

`r`を押すと、クエリを再実行して結果を更新します。データが継続的に書き込まれる場合、`order by time desc`でソートしたクエリで最新値を確認する際に便利です。

![img](/images/shell-walk.gif)


### クエリの出力形式 {#query-output-format}

#### JSON {#json}

`--format json`オプションを使用します。

```sh
machbase-neo shell sql \
    --format json \
    "select * from EXAMPLE order by time desc limit 4"
```

```json
{
  "data": {
    "columns": ["ROWNUM","NAME","TIME(UTC)","VALUE"],
    "types": ["string","string","datetime","double"],
    "rows": [
      [1,"wave.sin","2023-01-28 14:03:59",0.214839],
      [2,"wave.cos","2023-01-28 14:03:59",-0.976649],
      [3,"wave.cos","2023-01-28 14:03:58",-0.804831],
      [4,"wave.sin","2023-01-28 14:03:58",0.593504]
    ]
  }
}
```

#### CSV {#csv}

`--format csv`オプションを使用します。

```sh
machbase-neo shell sql  \
    --format csv \
    "select * from EXAMPLE order by time desc limit 4"
```

```
#,NAME,TIME(UTC),VALUE
1,wave.sin,2023-01-28 14:03:59,0.214839
2,wave.cos,2023-01-28 14:03:59,-0.976649
3,wave.cos,2023-01-28 14:03:58,-0.804831
4,wave.sin,2023-01-28 14:03:58,0.593504
```

先頭のヘッダー行を除くには、`--no-heading`オプションを使用します。 

```sh
machbase-neo shell sql \
    --format csv \
    --no-heading \
    "select * from EXAMPLE order by time desc limit 4"
```

```
1,wave.sin,2023-01-28 14:03:59,0.214839
2,wave.cos,2023-01-28 14:03:59,-0.976649
3,wave.cos,2023-01-28 14:03:58,-0.804831
4,wave.sin,2023-01-28 14:03:58,0.593504
```

### クエリの時刻形式 {#query-time-format}

時刻の出力形式は、`--timeformat`オプションで指定します。

`help timeformat`を実行すると、定義済みの形式とカスタム形式の構文を表示します。

```sh
machbase-neo shell help timeformat
```

#### 定義済みの時刻形式 {#pre-defined-timeformats}

| 名前          | 形式                                    |
|:--------------|:------------------------------------------|
| Default,-     |    2006-01-02 15:04:05.999                |
| ns, us, ms, s | （UNIXエポック時刻をナノ秒、マイクロ秒、ミリ秒、秒単位のint64で表現） |
| Numeric       |    01/02 03:04:05PM '06 -0700             |
| RFC822        |    02 Jan 06 15:04 MST                    |
| RFC850        |    Monday, 02-Jan-06 15:04:05 MST         |
| RFC3339       |    2006-01-02T15:04:05Z07:00              |
| Kitchen       |    3:04:05PM                              |
| Stamp         |    Jan _2 15:04:05                        |
| …その他…       | `machbase-neo shell help timeformat`を参照 |

`--timeformat numeric`形式を試します。

```sh
machbase-neo shell sql \
    --timeformat numeric \
    "select * from example where name='wave.sin' order by time desc limit 1"
```

```
 #  NAME      TIME(UTC)                   VALUE
───────────────────────────────────────────────────
 1  wave.sin  01/28 02:03:59PM '23 +0000  0.214839
```

`-t`は、`--timeformat`の短い別名です。

```sh
machbase-neo shell sql \
    -t ms \
    "select * from example where name='wave.sin' order by time desc limit 1"
```

```
 #  NAME      TIME(UTC)      VALUE
──────────────────────────────────────
 1  wave.sin  1674914639000  0.214839
```

#### カスタム時刻形式 {#custom-time-format}

独自の形式を指定することもできます。

```sh
machbase-neo shell sql \
    --timeformat "2006.01.02 (15:04:05.000)" \
    "select * from example where name='wave.sin' order by time desc limit 1"
```

```
 #  NAME      TIME(UTC)                    VALUE
────────────────────────────────────────────────────
 1  wave.sin  "2023.01.28 (14:03:59.000)"  0.214839
```

| 値      | 記号                                    |
|:-----------|:------------------------------------------|
| 年       | 2006                                      |
| 月      | 01                                        |
| 日        | 02                                        |
| 時       | 03または15                                  |
| 分     | 04                                        |
| 秒     | 05、または小数秒を含む'05.999'、'05.000'|


#### 時刻形式とタイムゾーンの組み合わせ {#combine-time-format-and-time-zone}

```sh
machbase-neo shell sql \
    --tz Europe/Paris \
    --timeformat "2006.01.02 (15:04:05.000)" \
    "select * from example where name='wave.sin' order by time desc limit 1"
```

```
 #  NAME      TIME(EUROPE/PARIS)           VALUE
────────────────────────────────────────────────────
 1  wave.sin  "2023.01.28 (15:03:59.000)"  0.214839
```

{{< callout type="info" >}}
`s`、`ms`、`us`、`ns`形式は、UNIXエポック時刻を表します。 
これらの形式では、`--tz`オプションは無視されます。
エポック時刻は常にUTCに基づくためです。
{{< /callout >}}

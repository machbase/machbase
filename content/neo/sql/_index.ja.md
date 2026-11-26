---
toc: true
title: SQL
type: docs
weight: 22
---

新しいタブの画面で `SQL` カードを選択すると、新しいSQLエディターが開きます。

{{< figure src="/images/web-sql-pick.png" width="600px" >}}

## SQL {#sql}

### テーブルの作成 {#테이블-생성}

画面の左側がSQLエディター、右側が結果パネル（`RESULT`・`CHART`）です。実行ログは下部のコンソールに表示されます。

以下のDDL文をコピーして、エディターに貼り付けます。

```sql
CREATE TAG TABLE IF NOT EXISTS example (
  name varchar(100) primary key,
  time datetime basetime,
  value double summarized
);
```

エディター左上の<img src="/neo/sql/img/sql_run_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">をクリックするか、`Ctrl+Enter`（macOS では `Cmd+Enter`）を押して実行します。文末のセミコロンを忘れずに入力してください。

{{< figure src="/images/web-cretable.png" >}}

### データの挿入 {#데이터-삽입}

以下の文を実行して、1件のレコードを挿入します。

```sql
INSERT INTO example VALUES('my-car', now, 1.2345);
```

{{< figure src="/images/web-insert.png" >}}

### データの検索 {#데이터-조회}

以下のSELECT文を実行すると、右側の表形式のパネルに結果が表示されます。

```sql
SELECT time, value FROM example WHERE name = 'my-car';
```

{{< figure src="/images/web-select.png" >}}

### 名前付き引数の使用 {#named-args-사용}

SQLエディターでは、`:name`、`:value`などの名前付き引数を使用できます。
名前付き引数の値は、SQL文の前に`-- env:`コメントで指定します。
複数のSQL文で同じ値を繰り返し使用する場合や、テスト値をすばやく変更して実行する場合に便利です。

```sql
-- env: named.name='my-car' named.value=1.5432
INSERT INTO example VALUES(:name, now, :value);

SELECT * FROM example WHERE name = :name;
-- env: reset
```

上記の例では、`name`引数に`'my-car'`、`value`引数に`1.5432`を設定し、
INSERT文とSELECT文で、それぞれ`:name`、`:value`として参照します。
`-- env: reset`を実行すると、SQLエディターに設定した名前付き引数がリセットされます。

`-- env:`で指定した設定は、`-- env: reset`を実行するまで累積されます。

```sql
--env: named.name=my-car
--env: named.time='2026-09-10 12:28:26.197719833'
--env: named.layout='YYYY-MM-DD HH24:MI:SS.mmmuuunnn'
SELECT * FROM example
  WHERE name = :name AND time=to_date(:time, :layout);

--env: named.new_value=9.876
UPDATE example SET value = :new_value
  WHERE name = :name AND time=to_date(:time, :layout);
--env: reset
```

#### 名前付き引数の型を指定する

型を明示しない値は、`007`のように数値に見える場合も文字列として渡されます。
SQL関数や比較演算で特定の型が必要な場合は、`型(値)`で指定します。

```sql
-- env: named.epoch=long(1793577127279628041)
SELECT from_timestamp(:epoch);

-- env: tz=Asia/Seoul named.since=datetime('2026-11-02 10:32:07.197719833')
SELECT * FROM example WHERE time >= :since;
```

`long(...)`はUnixエポックからのナノ秒を64ビット整数として渡します。
`datetime(...)`は日時そのものを渡すため、`DATETIME`列と直接比較できます。
空白を含む日時は、括弧の内側で引用符で囲みます。オフセットを省略すると、
宣言時点の`tz`が使われます。`tz`が未設定の場合はUTCになります。
`datetime(2026-11-02T10:32:07+09:00)`のように明示したオフセットが優先されます。

| 型 | 別名 |
|---|---|
| `short`, `ushort` | `int16`, `uint16` |
| `int`, `uinteger` | `integer`または`int32`, `uint32` |
| `long`, `ulong` | `int64`, `uint64` |
| `float`, `double` | `float32`, `float64` |
| `datetime` | — |

`uinteger(...)`と`uint32(...)`には`0`から`4294967294`まで、
`ulong(...)`と`uint64(...)`には`0`から`18446744073709551614`まで指定できます。
各範囲の上限の次の値はMachbaseの`NULL`用に予約されており、数値として指定できません。

`long(123)`を文字列として渡すには、`named.label="long(123)"`のように値全体を
引用符で囲むか、`named.label=string('long(123)')`と指定します。
`short(32768)`のように指定した型の範囲を超えた値はエラーになります。
TQLの`named()`にも同じ規則が適用されます。たとえば
`named('epoch', 'long(1793577127279628041)')`は整数を、
`named('label', "string('long(123)')")`は文字列をバインドします。

### データの変更 {#데이터-수정}

先ほど作成した `example` TAG テーブルにテストレコードを1件追加し、同じレコードを
更新してから削除します。上から順に実行してください。`int64(...)`は Unix エポックからの
ナノ秒を整数として渡します。すべての文で同じ `:name` と `:time` を再利用します。
TAG テーブルの時系列データの更新には Machbase Standard Edition が必要です。

```sql
-- env: named.name='my-car' named.time=int64(1793577127279628041)
INSERT INTO example (name, time, value)
VALUES (:name, :time, 1.50);

UPDATE example SET value = 1.61
WHERE name = :name AND time = :time;

SELECT name, time, value FROM example
WHERE name = :name AND time = :time;

DELETE FROM example
WHERE name = :name AND time = :time;

SELECT name, time, value FROM example
WHERE name = :name AND time = :time;
-- env: reset
```

最初の `SELECT` で、更新後の `value` が `1.61` になっていることを確認します。
削除後、2番目の `SELECT` では該当するレコードが表示されません。`DELETE` を実行する前に、
`WHERE` 句が意図したタグと時刻を指定していることを確認してください。
最後の `-- env: reset` で名前付き引数をリセットします。

### グラフの描画 {#차트-그리기}

INSERT文を繰り返し実行して、データを追加します。

```sql
INSERT INTO example VALUES('my-car', now, 1.2345*1.1);
INSERT INTO example VALUES('my-car', now, 1.2345*1.2);
INSERT INTO example VALUES('my-car', now, 1.2345*1.3);
```

その後、保存した`my-car`のレコードを検索します。

```sql
SELECT time, value FROM example WHERE name = 'my-car';
```
{{< figure src="/images/web-select-multi.png" >}}

右側のパネルで `CHART` タブをクリックすると、結果を折れ線グラフで確認できます。1 列目が X 軸、2 列目が Y 軸になり、`X Axis`・`Y Axis` で列を変えてから横の ▶ ボタンを押すと描き直します。

{{< figure src="/images/web-select-chart.jpg" width="560px" >}}

### CSVファイルのダウンロード {#csv-파일-다운로드}

結果パネル右上の<img src="/neo/sql/img/sql_download_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">をクリックすると、クエリ結果を CSV ファイルとしてダウンロードします。結果表は 50 行ずつ表示しますが、CSV ファイルにはクエリが返すすべての行がヘッダー行付きで保存され、時刻の値はエディターの時刻形式・タイムゾーン設定に従います。

{{< figure src="/neo/sql/img/web-select-download.png" width="570px" >}}

### テーブルの削除 {#테이블-삭제}

*DELETE*文でレコードを削除します。

```sql
DELETE FROM example WHERE name = 'my-car';
```

テーブルを作り直す場合は、テーブルを削除します。

```sql
DROP TABLE example;
```

## Non-SQL {#non-sql}

### show tables {#show-tables}

`M$SYS_TABLES`を検索する短縮コマンドです。

```
show tables;
```

{{< figure src="/neo/sql/img/web-show-tables.png" >}}

### desc _table_name_ {#desc-_table_name_}

テーブルの列とインデックスの情報を確認します。

```
desc example;
```

{{< figure src="/neo/sql/img/web-desc-table.png" >}}

### show tags _table_name_ {#show-tags-_table_name_}

```
show tags example;
```

TAGテーブルに保存されたタグの一覧を確認します。

{{< figure src="/neo/sql/img/web-show-tags.png" >}}


## SQLガイド {#sql-가이드}

以下の節では、TAGテーブルの主要な概念と機能を簡単に紹介します。詳細は、[DBMSリファレンス](https://docs.machbase.com/ja/dbms/)を参照してください。

{{< children_toc />}}

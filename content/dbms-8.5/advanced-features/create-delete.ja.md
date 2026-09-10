---
title : ストリームの作成と削除
type: docs
weight: 10
toc: true
---

## ストリームの作成 {#create-stream}

> **エディションに関する注意**：ストリームプロシージャは Standard Edition でサポートされます。Cluster Edition では、ストリーム/CQL 文が拒否される場合があります。

ストリームクエリーは INSERT ... SELECT 形式でのみ作成できます。作成時に、クエリーを正常に実行できるか検証されます。
次のストアドプロシージャでストリームを作成します。

作成が成功しても、実行はすぐには開始されません。詳細は「ストリームの開始と停止」を参照してください。

```sql
EXEC STREAM_CREATE(stream_name, stream_query_string);
```

基本のストリームクエリーは、データが入力されるたびに実行されます。この場合、SUM や AVG などの集計クエリーは使用できません。

```sql
EXEC STREAM_CREATE(normal_query, 'INSERT INTO CEP_LOG_TABLE SELECT * FROM EVENT WHERE C1 = 0');
```

ただし、INSERT ... SELECT 文の末尾で実行間隔を指定すると、入力データに対する集計クエリーを一定間隔で実行できます。

```sql
EXEC STREAM_CREATE(aggr_1_sec, 'insert into aggr select sum(i1), i2 from base group by i2 BY 1 SECOND');
```

上記のクエリーは毎秒、前回の実行後に入力されたデータに対して GROUP BY を実行し、結果を Log テーブル aggr に挿入します。

実行タイミングをユーザーが指定する場合は、実行間隔の指定箇所に次のように記述します。

ユーザーが明示的に呼び出すまで、ストリームクエリーは実行されません。

```sql
EXEC STREAM_CREATE(base_trig, 'insert into aggr select sum(i1), i2 from base group by i2 BY USER');
```

実行条件が BY USER の場合、STREAM_EXECUTE プロシージャで明示的に呼び出すまで実行されません。

STREAM_EXECUTE で呼び出すと、前回までに読み取ったデータを除き、新たに追加された差分データだけにストリームクエリーを実行します。

## ストリームの削除 {#delete-stream}

作成済みのストリームは V$STREAMS メタテーブルで確認できます。削除するには、作成時に指定したストリーム名を引数として次のストアドプロシージャを実行します。

```sql
EXEC STREAM_DROP(stream_name);
```

実行中のストリームは削除できません。先に停止してください。詳細は「ストリームの開始と停止」を参照してください。


## V$STREAMS {#vstreams}

DB サーバーに登録されたストリームの現在の状態を確認するメタテーブルです。詳細は、仮想テーブルの説明を参照してください。

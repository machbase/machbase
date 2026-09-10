---
title : ストリームの開始と停止
type: docs
weight: 20
toc: true
---

## ストリームの開始 {#stream-startup}

> **エディションに関する注意**：ストリームプロシージャは Standard Edition でサポートされます。Cluster Edition では、ストリーム/CQL 文が拒否される場合があります。

ストアドプロシージャを使用して、登録済みのストリームを開始します。開始後は継続的に実行されます。サーバーを再起動しても、前回の実行後に挿入されたデータに対してストリームクエリーが実行されます。

```sql
EXEC STREAM_START(stream_name);
```

## ストリームの明示的な実行 {#direct-execution-of-the-stream}

実行条件が BY USER のストリームは、ユーザーが明示的に呼び出すまで実行されません。次のストアドプロシージャで実行します。

```sql
EXEC STREAM_EXECUTE(stream_name);
```

BY USER 条件で作成されていないストリーム、または STREAM_START で開始していないストリームを呼び出すと、エラーになります。


## ストリームの停止 {#stream-shutdown}

実行中のストリームを停止するには、次のストアドプロシージャを使用します。

```sql
EXEC STREAM_STOP(stream_name);
```

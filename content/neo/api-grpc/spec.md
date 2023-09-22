---
title: proto file
type: docs
weight: 90
---

The latest version of .proto file is hosted in github. 

Please [find it from github](https://github.com/machbase/neo-grpc/tree/main/proto/machrpc.proto).

```proto
service Machbase {
    rpc Exec(ExecRequest) returns(ExecResponse) {}
    rpc QueryRow(QueryRowRequest) returns(QueryRowResponse) {}
    rpc Query(QueryRequest) returns(QueryResponse) {}
    rpc Columns(RowsHandle) returns (ColumnsResponse) {}
    rpc RowsFetch(RowsHandle) returns(RowsFetchResponse) {}
    rpc RowsClose(RowsHandle) returns (RowsCloseResponse) {}
    rpc Appender(AppenderRequest) returns (AppenderResponse){}
    rpc Append(stream AppendData) returns(AppendDone) {}
}
```
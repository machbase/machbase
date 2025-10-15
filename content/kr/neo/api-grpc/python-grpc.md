---
title: Python gRPC 클라이언트
type: docs
weight: 54
draft: true
---

## 준비

### Python gRPC

파이썬용 gRPC 컴파일러를 설치합니다.

```sh
pip3 install grpcio grpcio-tools
```

### `machrpc.proto` 다운로드 및 코드 생성

작업 디렉터리를 생성합니다.

```sh
mkdir machrpc-py && cd machrpc-py
```

proto 파일을 내려받습니다.

```sh
curl -o machrpc.proto https://raw.githubusercontent.com/machbase/neo-server/main/api/proto/machrpc.proto
```

proto 파일을 파이썬 코드로 컴파일합니다.

```sh
python3 -m grpc_tools.protoc \
    -I . \
    --python_out=. \
    --grpc_python_out=. \
    ./machrpc.proto
```

완료되면 `machrpc_pb2.py`, `machrpc_pb2_grpc.py` 두 개의 파이썬 파일이 생성됩니다.

## 쿼리

### `any` 타입 변환기

Machbase Neo gRPC는 데이터 타입으로 `google/protobuf/any.proto` 패키지를 사용합니다.
따라서 타입 변환 함수를 정의해야 합니다.

아래 함수는 protobuf Any 타입을 적절한 파이썬 타입으로 변환합니다.


### protobuf.Any 값을 파이썬 타입으로 변환

```python
from google.protobuf.any_pb2 import Any
import google.protobuf.timestamp_pb2 as pb_ts
import google.protobuf.wrappers_pb2 as pb_wp
import time
from datetime import datetime

def convpb(v):
    if v.type_url == "type.googleapis.com/google.protobuf.StringValue":
        r = pb_wp.StringValue()
        v.Unpack(r)
        return r.value
    elif v.type_url == "type.googleapis.com/google.protobuf.Timestamp":
        r = pb_ts.Timestamp()
        v.Unpack(r)
        dt = datetime.fromtimestamp(r.seconds)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif v.type_url == "type.googleapis.com/google.protobuf.DoubleValue":
        r = pb_wp.DoubleValue()
        v.Unpack(r)
        return str(r.value)
```

### 연결

gRPC 런타임 패키지와 생성된 파일을 임포트합니다.

```python
import grpc
import machrpc_pb2_grpc
import machrpc_pb2
```

서버로 gRPC 채널을 생성한 뒤 Machbase Neo API 스텁을 만듭니다.

```python
channel = grpc.insecure_channel('127.0.0.1:5655')
mach_stub = machrpc_pb2_grpc.MachbaseStub(channel)
```

### 쿼리 실행

스텁을 사용해 SQL 쿼리를 실행합니다.

```python
sqlText = "select * from example order by time limit 10"
rsp = mach_stub.Query(machrpc_pb2.QueryRequest(sql=sqlText))
```

### 결과 컬럼 정보 가져오기

쿼리 실행 후 결과 컬럼 메타 정보를 조회할 수 있습니다.

```python
cols = mach_stub.Columns(rsp.rowsHandle)
if cols.success:
    header = ['RowNum']
    for c in cols.columns:
        header.append(f"{c.name}({c.type})  ")
    print('   '.join(header))
```

### 결과 읽기

`Fetch`를 호출해 결과 레코드를 가져옵니다.

```python
nrow = 0
while True:
    fetch = mach_stub.RowsFetch(rsp.rowsHandle)
    if fetch.hasNoRows:
        break
    nrow+=1
    line = []
    line.append(str(nrow))
    for i, c in enumerate(cols.columns):
        v = fetch.values[i]
        if c.type == "string":
            line.append(convpb(v))
        elif c.type == "datetime":
            line.append(convpb(v))
        elif c.type == "double":
            line.append(convpb(v))
        else:
            line.append(f"unknown {str(v)}")
    print('     '.join(line))
_ = mach_stub.RowsClose(rsp.rowsHandle)
```
 
{{< callout type="warning" >}}
**RowsClose 호출**<br/>
`RowsClose(handle)`을 호출해 행 핸들을 반드시 닫아야 합니다.
{{< /callout >}}

## Append

### 임포트

```python
import grpc
import machrpc_pb2 as mach
import machrpc_pb2_grpc as machrpc
import numpy as np 
import time
import google.protobuf.wrappers_pb2 as pb_wp
from google.protobuf.any_pb2 import Any
```

### 프로토버퍼 `Any` 타입 변환기

```python
def AnyString(str: str):
    pbstr = pb_wp.StringValue()
    pbstr.value = str
    anystr = Any()
    anystr.Pack(pbstr)
    return anystr

def AnyInt64(iv: int):
    pbint = pb_wp.Int64Value()
    pbint.value = iv
    anyint = Any()
    anyint.Pack(pbint)
    return anyint

def AnyFloat(fv: float):
    pbfloat = pb_wp.DoubleValue()
    pbfloat.value = fv
    anyfloat = Any()
    anyfloat.Pack(pbfloat)
    return anyfloat
```

### 데이터 생성

```python
sample_rate = 100
start_time = 0
end_time = 1000

timeseries = np.arange(start_time, end_time, 1/sample_rate)
frequency = 3
ts = time.time_ns()

data = list[list[Any]]()
for i, t in enumerate(timeseries):
    nanot = ts + int(t*1000000000)
    value = np.sin(2 * np.pi * frequency * t)
    data.append([AnyString("python.value"), AnyInt64(nanot), AnyFloat(value)])
```

### 서버 연결

```python
channel = grpc.insecure_channel('127.0.0.1:5655')
mach_stub = machbase_proto_pb2_grpc.MachbaseStub(channel)
```

### 새 앱팬더 준비

```python
appender = stub.Appender(mach.AppenderRequest(tableName="example"))
```

### 스트리밍 방식으로 데이터 쓰기

```python
def ToStream(rows: list[list[Any]]):
    for row in rows:
        yield mach.AppendData(handle = appender.handle, params = row)

stub.Append(ToStream(data))
```

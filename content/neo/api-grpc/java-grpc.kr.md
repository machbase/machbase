---
title: Java gRPC 클라이언트
type: docs
weight: 51
draft: true
---

## 준비

### 프로젝트 디렉터리 생성

```sh
mkdir machrpc-java && cd machrpc-java
```


### machrpc.proto 다운로드

```sh
mkdir -p src/main/proto
curl -o src/main/proto/machrpc.proto https://raw.githubusercontent.com/machbase/neo-server/main/api/proto/machrpc.proto
```

proto 파일을 내려받은 뒤에는 `java_package` 옵션을 추가해야 합니다.

```proto
option java_package = "com.machbase.neo.rpc";
```

이제 `machrpc.proto`에서 gRPC 클라이언트 코드를 생성해야 합니다. gRPC Java 플러그인이 포함된 `protoc`를 사용합니다.

Gradle이나 Maven을 사용하면 빌드 플러그인이 빌드 과정에서 필요한 코드를 생성해 줍니다.
`.proto` 파일에서 코드를 생성하는 방법은 [grpc-java README](https://github.com/grpc/grpc-java/blob/master/README.md)를 참고해 주십시오.

### `pom.xml`에 의존성 추가

```xml
<dependencies>
    <dependency>
        <groupId>io.grpc</groupId>
        <artifactId>grpc-netty-shaded</artifactId>
        <version>1.63.0</version>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>io.grpc</groupId>
        <artifactId>grpc-protobuf</artifactId>
        <version>1.63.0</version>
    </dependency>
    <dependency>
        <groupId>io.grpc</groupId>
        <artifactId>grpc-stub</artifactId>
        <version>1.63.0</version>
    </dependency>
    <dependency> <!-- necessary for Java 9+ -->
        <groupId>org.apache.tomcat</groupId>
        <artifactId>annotations-api</artifactId>
        <version>6.0.53</version>
        <scope>provided</scope>
    </dependency>
</dependencies>
```

### 소스 파일 작성

아래 링크의 소스 코드를 내려받거나 `src/main/java/com/machbase/neo/example/Example.java`에 붙여 넣으십시오.

{{< callout type="info">}}
전체 예제 소스 코드는 [여기]({{< neo_examples_url >}}/java/grpc)에서 확인하실 수 있습니다.
{{< /callout >}}

### .proto로부터 코드 생성

Maven이 필요한 의존성과 gRPC 도구를 내려받고 스텁 코드를 생성합니다.

```
mvn compile
```

## 쿼리

### 서버 연결

채널을 닫지 않으면 내부 스레드가 종료되지 않으므로 반드시 닫아야 합니다.

```java
ManagedChannel channel = Grpc.newChannelBuilder("127.0.0.1:5655", InsecureChannelCredentials.create()).build();
MachbaseBlockingStub stub = MachbaseGrpc.newBlockingStub(channel);
try {
    // do job
} finally {
    channel.shutdown();
}
```

### 쿼리 실행

```java
QueryRequest.Builder builder = Machrpc.QueryRequest.newBuilder();
builder.setSql("select * from example order by time desc limit ?");
builder.addParams(Any.pack(Int32Value.of(10)));

QueryRequest req = builder.build();
QueryResponse rsp = stub.query(req);
```

### 결과 컬럼 정보 가져오기

```java
ColumnsResponse cols = stub.columns(rsp.getRowsHandle());
ArrayList<String> headers = new ArrayList<String>();
headers.add("RowNum");
for (int i = 0; i < cols.getColumnsCount(); i++) {
    Column c = cols.getColumns(i);
    headers.add(c.getName() + "(" + c.getType() + ")");
}
```

### 결과 읽기

```java
int nrow = 0;
RowsFetchResponse fetch = null;
while (true) {
    fetch = stub.rowsFetch(rsp.getRowsHandle());
    if (fetch == null || fetch.getHasNoRows()) {
        break;
    }
    nrow++;

    ArrayList<String> line = new ArrayList<String>();
    line.add(Integer.toString(nrow, 10));
    List<Any> row = fetch.getValuesList();
    for (Any anyv : row) {
        line.add(convpb(anyv));
    }
    System.out.println(String.join("    ", line));
}
```

### `com.google.protobuf.Any` 변환

```java
static DateTimeFormatter sdf = DateTimeFormatter.ofPattern("yyyy.MM.dd HH:mm:ss.SSS");

static String convpb(Any any) {
    try {
        switch (any.getTypeUrl()) {
            case "type.googleapis.com/google.protobuf.StringValue": {
                StringValue v = any.unpack(StringValue.class);
                return v.getValue();
            }
            case "type.googleapis.com/google.protobuf.Timestamp": {
                Timestamp v = any.unpack(Timestamp.class);
                LocalDateTime ldt = java.time.LocalDateTime.ofEpochSecond(v.getSeconds(), v.getNanos(), ZoneOffset.UTC);
                return ldt.format(sdf);
            }
            case "type.googleapis.com/google.protobuf.DoubleValue": {
                DoubleValue v = any.unpack(DoubleValue.class);
                return Double.toString(v.getValue());
            }
            default:
                return "unsupported " + any.getTypeUrl();
        }
    } catch (Exception e) {
        return "error " + e.getMessage();
    }
}
```

### 실행 결과

```
$ mvn exec:java -Dexec.mainClass=com.machbase.neo.example.Example

[INFO] --- exec:3.1.0:java (default-cli) @ example ---
1    python.value    2023.02.09 04:38:41.919    -0.18738131458371082
2    python.value    2023.02.09 04:38:41.909    -0.36812455270521627
3    python.value    2023.02.09 04:38:41.899    -0.535826794993456
4    python.value    2023.02.09 04:38:41.889    -0.6845471059163379
5    python.value    2023.02.09 04:38:41.879    -0.8090169943791776
6    python.value    2023.02.09 04:38:41.869    -0.9048270524669701
7    python.value    2023.02.09 04:38:41.859    -0.9685831611279518
8    python.value    2023.02.09 04:38:41.849    -0.9980267284277884
9    python.value    2023.02.09 04:38:41.839    -0.9921147013124169
10    python.value    2023.02.09 04:38:41.829    -0.9510565162916061
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
```

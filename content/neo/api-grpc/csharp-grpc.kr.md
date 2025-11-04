---
title: C# gRPC 클라이언트
type: docs
weight: 53
draft: true
---

## 준비

### dotnet-sdk 설치

```sh
brew install dotnet-sdk
```

### 프로젝트 디렉터리 생성

```sh
mkdir example-csharp && cd example-csharp
```

### 콘솔 프로젝트 생성

```sh
dotnet new console --framework net7.0
```

### gRPC 패키지 추가

```sh
dotnet add package Grpc.Tools
dotnet add package Grpc.Net.Client
dotnet add package Google.Protobuf
```

### machrpc.proto 다운로드

```sh
curl -o machrpc.proto https://raw.githubusercontent.com/machbase/neo-server/main/api/proto/machrpc.proto
```

proto 파일을 내려받은 뒤에는 `csharp_namespace` 옵션을 추가해야 합니다.

```proto
option csharp_namespace = "MachRpc";
```

### `example-csharp.csproj` XML에 ItemGroup 추가

```xml
  <ItemGroup>
    <Protobuf Include="machrpc.proto" GrpcServices="Client"/>
  </ItemGroup>
```

## TLS용 X.509 인증서

gRPC 연결은 기본적으로 TLS를 사용합니다.
클라이언트용 애플리케이션 키를 생성합니다.

아래 명령을 실행하면 새 키를 만들고 서버에 자동으로 등록합니다.

```sh
machbase-neo shell --server 127.0.0.1:5655 key gen "csharp-client" --output "csharp-client"
```

이 명령은 `csharp-client_cert.pem`, `csharp-client_key.pem`, `csharp-client_token`을 생성합니다. 클라이언트 프로그램은 두 개의 *.pem 파일이 필요합니다.

또한 클라이언트는 CA로 사용할 Machbase Neo 서버 인증서를 준비해야 합니다.

```sh
machbase-neo shell --server 127.0.0.1:5655 key server-cert --output "csharp-server.pem"
```

총 세 개의 .pem 파일이 필요합니다.

- `csharp-client_cert.pem`: Machbase Neo 서버가 서명한 클라이언트 X.509 인증서
- `csharp-client_key.pem`: 클라이언트 비공개 키
- `csharp-server.pem`: Machbase Neo 서버의 X.509 인증서(자체 서명)

다음 명령으로 서버에 등록된 인증서를 확인할 수 있습니다.

```sh
$ machbase-neo shell key list

╭────────┬───────────────┬───────────────────────────────┬───────────────────────────────╮
│ ROWNUM │ ID            │ VALID FROM                    │ EXPIRE                        │
├────────┼───────────────┼───────────────────────────────┼───────────────────────────────┤
│      1 │ csharp-client │ 2023-12-21 07:32:30 +0000 UTC │ 2033-12-18 07:32:30 +0000 UTC │
╰────────┴───────────────┴───────────────────────────────┴───────────────────────────────╯
```

## 서버 연결 

### TLS

```csharp
var handler = new HttpClientHandler();
handler.SslProtocols = System.Security.Authentication.SslProtocols.Tls12;
handler.ClientCertificateOptions = ClientCertificateOption.Manual;
handler.ClientCertificates.Add(x509);
handler.UseProxy = false;
handler.ServerCertificateCustomValidationCallback = (HttpRequestMessage msg, X509Certificate2? cert, X509Chain? chain, SslPolicyErrors sslPolicyErrors) =>
{
    if (serverCert.Equals(cert)) {
        return true;
    } else {
        System.Console.WriteLine("Server cert, got " + cert!.SubjectName.Name);
        return false;
    }
};

var channel = GrpcChannel.ForAddress("https://127.0.0.1:5655", new GrpcChannelOptions()
{
    HttpHandler = handler,
    DisposeHttpClient = true
});

var client = new MachRpc.Machbase.MachbaseClient(channel);
```

### DB 연결

```c#
connReq = new MachRpc.ConnRequest
{
    User = "sys",
    Password = "manager",
};
connRsp = client.Conn(connReq);
```

## 쿼리

### 쿼리 실행

```c#
queryReq = new MachRpc.QueryRequest
{
    Conn = connRsp.Conn,
    Sql = "select * from example order by time limit ?",
    Params = { Any.Pack(new Int32Value { Value = 10 }) }
};
queryRsp = client.Query(queryReq);
```

### 결과 컬럼 정보 가져오기

```c#
var cols = client.Columns(queryRsp.RowsHandle);
var headers = new List<string> { "RowNum" };
if (cols.Success)
{
    foreach (var c in cols.Columns)
    {
        headers.Add($"{c.Name}({c.Type})");
    }
}
Console.WriteLine(String.Join("   ", headers));
```

위 코드가 컬럼 레이블을 출력합니다.

```
NAME(string)   TIME(datetime)   VALUE(double)
```

### 결과 읽기

```c#
int nrow = 0;
while (true)
{
    var fetch = client.RowsFetch(queryRsp.RowsHandle);
    if (fetch.HasNoRows)
    {
        break;
    }
    nrow++;
    var line = new List<string> { $"{nrow}   " };
    foreach (Any v in fetch.Values)
    {
        line.Add(convpb(v));
    };
    Console.WriteLine(String.Join("    ", line));
}
```

{{< callout type="warning" >}}
**Close rows**<br/>
Do not forget to close rows by calling `RowsClose()`.
{{< /callout >}}


### Google.Protobuf.WellKnownTypes.Any를 문자열로 변환

```c#
static string convpb(Any v)
{
    if (v.TypeUrl == "type.googleapis.com/google.protobuf.StringValue")
    {
        var sval = v.Unpack<StringValue>();
        return sval.Value;
    }
    else if (v.TypeUrl == "type.googleapis.com/google.protobuf.Timestamp")
    {
        var ts = v.Unpack<Timestamp>();
        return ts.ToDateTime().ToString("MM/dd/yyyy HH:mm:ss");
    }
    else if (v.TypeUrl == "type.googleapis.com/google.protobuf.DoubleValue")
    {
        var fv = v.Unpack<DoubleValue>();
        return fv.Value.ToString();
    }
    else
    {
        throw new Exception($"Unsupported type {v.TypeUrl}");
    }
}
```

### 실행 결과

```
$ dotnet run
RowNum   NAME(string)   TIME(datetime)   VALUE(double)
1       wave.sin    2023. 02. 08 11:36:38    -0.994521
2       wave.cos    2023. 02. 08 11:36:38    -0.104538
3       wave.sin    2023. 02. 08 11:36:37    -0.866021
4       wave.cos    2023. 02. 08 11:36:37    -0.500008
5       wave.cos    2023. 02. 08 11:36:36    -0.809022
6       wave.sin    2023. 02. 08 11:36:36    -0.587778
7       wave.cos    2023. 02. 08 11:36:35    -0.978149
8       wave.sin    2023. 02. 08 11:36:35    -0.207904
9       wave.cos    2023. 02. 08 11:36:34    -0.978146
10       wave.sin    2023. 02. 08 11:36:34    0.207919
```

### 전체 소스 코드

```csharp
using Grpc.Net.Client;
using Google.Protobuf.WellKnownTypes;
using System.Security.Cryptography.X509Certificates;

internal class Program
{
    private static void Main(string[] args)
    {
        var keyPem = File.ReadAllText("csharp-client_key.pem");
        var certPem = File.ReadAllText("csharp-client_cert.pem");
        var x509 = X509Certificate2.CreateFromPem(certPem, keyPem);
        var serverCert = X509Certificate2.CreateFromCertFile("csharp-server.pem");

        var handler = new HttpClientHandler();
        handler.SslProtocols = System.Security.Authentication.SslProtocols.Tls12;
        handler.ClientCertificateOptions = ClientCertificateOption.Manual;
        handler.ClientCertificates.Add(x509);
        handler.UseProxy = false;
        handler.ServerCertificateCustomValidationCallback = (HttpRequestMessage msg, X509Certificate2? cert, X509Chain? chain, SslPolicyErrors sslPolicyErrors) =>
        {
            if (serverCert.Equals(cert)) {
                return true;
            } else {
                System.Console.WriteLine("Server cert, got " + cert!.SubjectName.Name);
                return false;
            }
        };

        
        var channel = GrpcChannel.ForAddress("https://127.0.0.1:5655", new GrpcChannelOptions()
        {
            HttpHandler = handler,
            DisposeHttpClient = true
        });

        var client = new MachRpc.Machbase.MachbaseClient(channel);

        MachRpc.ConnRequest connReq;
        MachRpc.ConnResponse? connRsp = null;
        MachRpc.QueryRequest queryReq;
        MachRpc.QueryResponse? queryRsp = null;
        try
        {

            connReq = new MachRpc.ConnRequest
            {
                User = "sys",
                Password = "manager",
            };
            connRsp = client.Conn(connReq);
            Console.WriteLine(String.Join("    ", connRsp));

            queryReq = new MachRpc.QueryRequest
            {
                Conn = connRsp.Conn,
                Sql = "select * from example order by time limit ?",
                Params = { Any.Pack(new Int32Value { Value = 10 }) }
            };
            queryRsp = client.Query(queryReq);
            Console.WriteLine(String.Join("    ", queryRsp));

            var cols = client.Columns(queryRsp.RowsHandle);
            var headers = new List<string> { "RowNum" };
            if (cols.Success)
            {
                foreach (var c in cols.Columns)
                {
                    headers.Add($"{c.Name}({c.Type})");
                }
            }
            Console.WriteLine(String.Join("   ", headers));

            int nrow = 0;
            while (true)
            {
                var fetch = client.RowsFetch(queryRsp.RowsHandle);
                if (fetch.HasNoRows)
                {
                    break;
                }
                nrow++;
                var line = new List<string> { $"{nrow}   " };
                foreach (Any v in fetch.Values)
                {
                    line.Add(convpb(v));
                };
                Console.WriteLine(String.Join("    ", line));
            }
        }
        finally
        {
            if (queryRsp != null)
            {
                client.RowsClose(queryRsp.RowsHandle);
            }
            if (connRsp != null)
            {
                client.ConnClose(new MachRpc.ConnCloseRequest { Conn = connRsp.Conn });
            }
        }
    }

    static string convpb(Any v)
    {
        if (v.TypeUrl == "type.googleapis.com/google.protobuf.StringValue")
        {
            var sval = v.Unpack<StringValue>();
            return sval.Value;
        }
        else if (v.TypeUrl == "type.googleapis.com/google.protobuf.Timestamp")
        {
            var ts = v.Unpack<Timestamp>();
            return ts.ToDateTime().ToString("yyyy/MM/dd HH:mm:ss");
        }
        else if (v.TypeUrl == "type.googleapis.com/google.protobuf.DoubleValue")
        {
            var fv = v.Unpack<DoubleValue>();
            return fv.Value.ToString();
        }
        else
        {
            throw new Exception($"Unsupported type {v.TypeUrl}");
        }
    }
}
```

## Append

### 새 앱팬더 준비

연결에서 앱팬더를 생성합니다.

```c#
var appender = client.Appender(new MachRpc.AppenderRequest
{
    Conn = connRsp.Conn,
    TableName = "example",
});
var stream = client.Append();
```

스트림을 닫는 것을 잊지 마십시오.

```c#
try {
    // code that use stream & appender.Handle
}
finally {
    await stream.RequestStream.CompleteAsync();
}
```

비동기 작업을 위해 `Main()`을 `async Task Main()`으로 선언하십시오.

```c#
private static async Task Main(string[] args) {
    /// use await
}
```

### 고속으로 데이터 쓰기

```c#
for (int i = 0; i < 100000; i++)
{
    var fieldName = new MachRpc.AppendDatum() { VString = "csharp.value" };
    var fieldTime = new MachRpc.AppendDatum() { VTime = TimeUtils.GetNanoseconds() };
    var fieldValue = new MachRpc.AppendDatum() { VDouble = 0.1234 };

    var record = new MachRpc.AppendRecord();
    record.Tuple.Add(fieldName);
    record.Tuple.Add(fieldTime);
    record.Tuple.Add(fieldValue);

    var data = new MachRpc.AppendData { Handle = appender.Handle };
    data.Records.Add(record);
    await stream.RequestStream.WriteAsync(data);
}
```

### 실행 및 적재 레코드 확인

```sh
dotnet run
```

```sh
machbase-neo shell "select count(*) from example where name = 'csharp.value'"
 #  COUNT(*)
─────────────
 1  100000
```


### 전체 소스 코드

```csharp
using Grpc.Net.Client;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
using System.Diagnostics;

internal class Program
{
    private static async Task Main(string[] args)
    {
        var keyPem = File.ReadAllText("csharp-client_key.pem");
        var certPem = File.ReadAllText("csharp-client_cert.pem");
        var x509 = X509Certificate2.CreateFromPem(certPem, keyPem);
        var serverCert = X509Certificate2.CreateFromCertFile("csharp-server.pem");

        var handler = new HttpClientHandler();
        handler.SslProtocols = System.Security.Authentication.SslProtocols.Tls12;
        handler.ClientCertificateOptions = ClientCertificateOption.Manual;
        handler.ClientCertificates.Add(x509);
        handler.UseProxy = false;
        handler.ServerCertificateCustomValidationCallback = (HttpRequestMessage msg, X509Certificate2? cert, X509Chain? chain, SslPolicyErrors sslPolicyErrors) =>
        {
            if (serverCert.Equals(cert)) {
                return true;
            } else {
                System.Console.WriteLine("Server cert, got " + cert!.SubjectName.Name);
                return false;
            }
        };

        var channel = GrpcChannel.ForAddress("https://127.0.0.1:5655", new GrpcChannelOptions()
        {
            HttpHandler = handler,
            DisposeHttpClient = true
        });

        var client = new MachRpc.Machbase.MachbaseClient(channel);

        var connReq = new MachRpc.ConnRequest
        {
            User = "sys",
            Password = "manager",
        };
        var connRsp = client.Conn(connReq);
        Console.WriteLine(String.Join("    ", connRsp));

        var appender = client.Appender(new MachRpc.AppenderRequest
        {
            Conn = connRsp.Conn,
            TableName = "example",
        });
        var stream = client.Append();

        var stopwatch = new Stopwatch();
        stopwatch.Start();
        try
        {
            for (int i = 0; i < 100000; i++)
            {
                var fieldName = new MachRpc.AppendDatum() { VString = "csharp.value" };
                var fieldTime = new MachRpc.AppendDatum() { VTime = TimeUtils.GetNanoseconds() };
                var fieldValue = new MachRpc.AppendDatum() { VDouble = 0.1234 };

                var record = new MachRpc.AppendRecord();
                record.Tuple.Add(fieldName);
                record.Tuple.Add(fieldTime);
                record.Tuple.Add(fieldValue);

                var data = new MachRpc.AppendData { Handle = appender.Handle };
                data.Records.Add(record);
                await stream.RequestStream.WriteAsync(data);
            }
        }
        finally
        {
            await stream.RequestStream.CompleteAsync();
            stopwatch.Stop();
            var elapsed_time = stopwatch.ElapsedMilliseconds;
            Console.WriteLine($"Elapse {elapsed_time}ms.");

            if (connRsp != null)
            {
                client.ConnClose(new MachRpc.ConnCloseRequest { Conn = connRsp.Conn });
            }
        }
    }

    public static class TimeUtils
    {
        public static long GetNanoseconds()
        {
            double timestamp = Stopwatch.GetTimestamp();
            double nanoseconds = 1_000_000_000.0 * timestamp / Stopwatch.Frequency;
            return (long)nanoseconds;
        }
    }
}
```

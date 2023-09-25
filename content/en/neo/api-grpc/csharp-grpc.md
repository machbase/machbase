---
title: gRPC client in C#
type: docs
weight: 53
---

## Setup

### Install dotnet-sdk

```sh
brew install dotnet-sdk
```

### Create project directory

```sh
mkdir example-csharp && cd example-csharp
```

### Create console project

```sh
dotnet new console --framework net7.0
```

### Add gRPC packages

```sh
dotnet add package Grpc.Tools
dotnet add package Grpc.Net.Client
dotnet add package Google.Protobuf
```

### Download machrpc.proto

```sh
curl -o machrpc.proto https://raw.githubusercontent.com/machbase/neo-grpc/main/proto/machrpc.proto
```

After downloading proto file, it is required to add csharp_namespace option in the file.

```proto
option csharp_namespace = "MachRpc";
```

### Add ItemGroup in `example-csharp.csproj` XML file

```xml
  <ItemGroup>
    <Protobuf Include="machrpc.proto" GrpcServices="Client"/>
  </ItemGroup>
```

## Query

### Connect to server 

```csharp
var channel = GrpcChannel.ForAddress("http://127.0.0.1:5655");
var client = new MachRpc.Machbase.MachbaseClient(channel);
```

### Execute query

```c#
var req = new MachRpc.QueryRequest
{
    Sql = "select * from example order by time limit ?",
    Params = { Any.Pack(new Int32Value { Value = 10 }) }
};
var rsp = client.Query(req);
```

### Get columns info of result set

```c#
var cols = client.Columns(rsp.RowsHandle);
var headers = new List<string>{"RowNum"};
if (cols.Success) {
    foreach (var c in cols.Columns) {
        headers.Add($"{c.Name}({c.Type})");
    }
}
Console.WriteLine(String.Join("   ", headers));
```

This will print column labels.

```
NAME(string)   TIME(datetime)   VALUE(double)
```

### Fetch results

```c#
int nrow = 0;
try
{
    while (true)
    {
        var fetch = client.RowsFetch(rsp.RowsHandle);
        if (fetch.HasNoRows)
        {
            break;
        }
        nrow++;
        var line = new List<string> { $"{nrow}   "};
        foreach (Any v in fetch.Values)
        {
            line.Add(convpb(v));
        };
        Console.WriteLine(String.Join("    ", line));
    }
}
finally
{
    if (rsp.Success && rsp.RowsHandle != null)
    {
        client.RowsClose(rsp.RowsHandle);
    }
}
```

{:.warning-title}
>Close rows
>
> Do not forget to close rows by calling `RowsClose()`.


### Convert Google.Protobuf.WellKnownTypes.Any to string

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

### Output

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

### Full source code

```csharp
using Grpc.Net.Client;
using Google.Protobuf.WellKnownTypes;

internal class Program
{
    private static void Main(string[] args)
    {
        var channel = GrpcChannel.ForAddress("http://127.0.0.1:5655");
        var client = new MachRpc.Machbase.MachbaseClient(channel);
        var req = new MachRpc.QueryRequest
        {
            Sql = "select * from example order by time limit ?",
            Params = { Any.Pack(new Int32Value { Value = 10 }) }
        };
        var rsp = client.Query(req);

        var cols = client.Columns(rsp.RowsHandle);
        var headers = new List<string>{"RowNum"};
        if (cols.Success)
        {
            foreach (var c in cols.Columns)
            {
                headers.Add($"{c.Name}({c.Type})");
            }
        }
        Console.WriteLine(String.Join("   ", headers));

        int nrow = 0;
        try
        {
            while (true)
            {
                var fetch = client.RowsFetch(rsp.RowsHandle);
                if (fetch.HasNoRows)
                {
                    break;
                }
                nrow++;
                var line = new List<string> { $"{nrow}   "};
                foreach (Any v in fetch.Values)
                {
                    line.Add(convpb(v));
                };
                Console.WriteLine(String.Join("    ", line));
            }
        }
        finally
        {
            if (rsp.Success && rsp.RowsHandle != null)
            {
                client.RowsClose(rsp.RowsHandle);
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

### Connect to server 

```c#
var channel = GrpcChannel.ForAddress("http://127.0.0.1:5655");
var client = new MachRpc.Machbase.MachbaseClient(channel);
```

### Prepare new appender

```c#
var appender = client.Appender(new MachRpc.AppenderRequest { TableName = "example" });
var stream = client.Append();
```

```c#
try {
    // code that use stream & appender.Handle
}
finally {
    await stream.RequestStream.CompleteAsync();
}
```

Make `Main()` as `async Task Main()` to allow awiat for async operation.

```c#
private static async Task Main(string[] args) {
    /// use await
}
```

### Write data in high speed

```c#
for (int i = 0; i < 100000; i++)
{
    var ts = new Timestamp();
    var value = 0.1234;

    long tick = TimeUtils.GetNanoseconds();
    long secs = 1_000_000_000;
    ts.Seconds = Convert.ToInt32(tick / secs);
    ts.Nanos = Convert.ToInt32(tick % secs);

    var data = new MachRpc.AppendData { Handle = appender.Handle};
    data.Params.Add(Any.Pack(new StringValue { Value = "csharp.value" }));
    data.Params.Add(Any.Pack(ts));
    data.Params.Add(Any.Pack(new DoubleValue{ Value = value }));

    await stream.RequestStream.WriteAsync(data);
}
```

### Run and count written records

```sh
dotnet run
```

```sh
machbase-neo shell "select count(*) from example where name = 'csharp.value'"
 #  COUNT(*)
─────────────
 1  100000
```


### Full source code

```csharp
using Grpc.Net.Client;
using Google.Protobuf.WellKnownTypes;
using System.Diagnostics;

internal class Program
{
    private static async Task Main(string[] args)
    {
        var channel = GrpcChannel.ForAddress("http://127.0.0.1:5655");
        var client = new MachRpc.Machbase.MachbaseClient(channel);

        // Appender example
        var appender = client.Appender(new MachRpc.AppenderRequest { TableName = "example" });
        var stream = client.Append();
        
        var stopwatch = new Stopwatch();
        stopwatch.Start();
        try
        {
            for (int i = 0; i < 100000; i++)
            {
                var ts = new Timestamp();
                var value = 0.1234;

                long tick = TimeUtils.GetNanoseconds();
                long secs = 1_000_000_000;
                ts.Seconds = Convert.ToInt32(tick / secs);
                ts.Nanos = Convert.ToInt32(tick % secs);

                var data = new MachRpc.AppendData { Handle = appender.Handle};
                data.Params.Add(Any.Pack(new StringValue { Value = "csharp.value" }));
                data.Params.Add(Any.Pack(ts));
                data.Params.Add(Any.Pack(new DoubleValue{ Value = value }));
                await stream.RequestStream.WriteAsync(data);
            }
        }
        finally
        {
            await stream.RequestStream.CompleteAsync();

            stopwatch.Stop();
            var elapsed_time = stopwatch.ElapsedMilliseconds;
            Console.WriteLine($"Elapse {elapsed_time}ms.");
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
---
toc: true
title: C# クライアント
type: docs
weight: 64
---

## 準備 {#준비}

### dotnet-sdkのインストール {#dotnet-sdk-설치}

```sh
brew install dotnet-sdk
```

### プロジェクトディレクトリの作成 {#프로젝트-디렉터리-생성}

```sh
mkdir csharp-mqtt && cd csharp-mqtt
```

### コンソールプロジェクトの作成 {#콘솔-프로젝트-생성}

```sh
dotnet new console --framework net7.0
```

### MQTTnetパッケージの追加 {#mqttnet-패키지-추가}

```sh
dotnet add package MQTTnet --version 4.3.3.952
```

## 接続（TLSなし） {#연결-비-tls}

MQTTの平文ソケットでmachbase-neoに接続します。

```c#
var mqttFactory = new MqttFactory();
var mqttClient = mqttFactory.CreateMqttClient();
var connectOptions = new MqttClientOptionsBuilder().WithTcpServer("127.0.0.1", 5653).Build();
var connAck = await mqttClient.ConnectAsync(connectOptions, CancellationToken.None);

connAck.DumpToConsole();
```

## 切断 {#연결-종료}

```c#
var mqttClientDisconnectOptions = mqttFactory.CreateClientDisconnectOptionsBuilder().Build();
await mqttClient.DisconnectAsync(mqttClientDisconnectOptions, CancellationToken.None);
```

## メッセージの発行 {#메시지-발행}

```c#
var msg = new MqttApplicationMessageBuilder()
.WithTopic("db/append/example")
.WithPayload(@"[
                [""temperature"",1677033057000000000,21.1],
                [""humidity"",1677033057000000000,0.53]
            ]")
.Build();

await mqttClient.PublishAsync(msg, CancellationToken.None);
```

## ソースコード全体 {#전체-소스-코드}


```c#
using MQTTnet;
using MQTTnet.Client;
using System.Text.Json;

namespace MqttTest
{
    internal class Program
    {
        private static async Task Main()
        {
            var mqttFactory = new MqttFactory();
            var mqttClient = mqttFactory.CreateMqttClient();
            var connectOptions = new MqttClientOptionsBuilder().WithTcpServer("127.0.0.1", 5653).Build();
            var connAck = await mqttClient.ConnectAsync(connectOptions, CancellationToken.None);
            
            connAck.DumpToConsole();

            var msg = new MqttApplicationMessageBuilder()
                .WithTopic("db/append/example")
                .WithPayload(@"[
                                [""temperature"",1677033057000000000,21.1],
                                [""humidity"",1677033057000000000,0.53]
                            ]")
                .Build();

            await mqttClient.PublishAsync(msg, CancellationToken.None);

            var mqttClientDisconnectOptions = mqttFactory.CreateClientDisconnectOptionsBuilder().Build();
            await mqttClient.DisconnectAsync(mqttClientDisconnectOptions, CancellationToken.None);
        }
    }
}

internal static class ObjectExtensions
{
    public static TObject DumpToConsole<TObject>(this TObject @object)
    {
        var output = "NULL";
        if (@object != null)
        {
            output = JsonSerializer.Serialize(@object, new JsonSerializerOptions
            {
                WriteIndented = true
            });
        }
        
        Console.WriteLine($"[{@object?.GetType().Name}]:\r\n{output}");
        return @object;
    }
}
```

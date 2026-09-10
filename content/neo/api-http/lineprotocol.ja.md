---
toc: true
title: ILPラインプロトコル
type: docs
weight: 50
params:
    tabs:
        sync: true
---

Machbase Neoは、データの取り込み用にInfluxDataのラインプロトコル形式のメッセージを受信する互換APIを提供します。
telegrafなど、ラインプロトコルのメッセージを生成する既存のクライアントソフトウェアをそのまま利用できます。

{{< callout emoji="📢">}}
MachbaseとInfluxDBはスキーマが異なるため、一部の項目は自動変換されます。
{{< /callout >}}

**変換規則**

| Machbase            | InfluxDBのラインプロトコル                   |
| ------------------- | ------------------------------------------- |
| table               | db                                          |
| tag name            | measurement + `.` + field name              |
| time                | timestamp                                   |
| value               | フィールド値（数値型以外は無視され、取り込まれません） |

**ラインプロトコルの例**

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/metrics/write?db=example&precision=ms

my-car speed=87.6 1782878977000
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - -X POST "http://127.0.0.1:5654/metrics/write?db=example&precision=ms" \
  --data-binary 'my-car speed=87.6 1782878977000'
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.post(
  "http://127.0.0.1:5654/metrics/write",
  params={"db": "example", "precision":"ms"},
  data="my-car speed=87.6 1782878977000",
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function writeLineProtocol() {
  const response = await fetch("http://127.0.0.1:5654/metrics/write?db=example&precision=ms", {
    method: "POST",
    body: "my-car speed=87.6 1782878977000",
  });

  console.log(await response.text());
}

writeLineProtocol();
```
{{< /tab >}}
{{< tab name="C#" >}}
```csharp
using System.Net.Http;
using System.Text;

using var client = new HttpClient();
using var content = new StringContent("my-car speed=87.6 1782878977000", Encoding.UTF8);

var response = await client.PostAsync("http://127.0.0.1:5654/metrics/write?db=example&precision=ms", content);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

上記の例は、`name`=`my-car.speed`、`value`=87.6、`time`=1782878977000を`example`テーブルに挿入します。

**telegraf.conf 例**

telegrafの出力先にMachbase NeoのHTTPポートを指定すると、
収集したメトリクスが直接Machbase Neoに取り込まれます。

```
[[outputs.http]]
url = "http://127.0.0.1:5654/metrics/write?db=example"
data_format = "influx"
content_encoding = "gzip"
```

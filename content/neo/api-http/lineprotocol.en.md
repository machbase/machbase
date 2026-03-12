---
title: ILP line protocol
type: docs
weight: 50
params:
    tabs:
        sync: true
---

Machbase Neo provides a compatibility api that accepts messages in a format of influxdata lineprotocol for writing data.
This api is convenient way to utilize existing client softwares that produce lineprotocol messages (e.g telegraf).

{{< callout emoji="📢">}}
Since Machbase has a different scheme from influxdb, some translations will be automatically occurred.
{{< /callout >}}

**Translation**

| Machbase            | line protocol of influxdb                   |
| ------------------- | ------------------------------------------- |
| table               | db                                          |
| tag name            | measurement + `.` + field name              |
| time                | timestamp                                   |
| value               | value of the field (if it is not a number type, will be ignored and not inserted) |

**Line protocol example**

{{< tabs >}}
{{< tab name="HTTP" >}}
~~~
```http
POST http://127.0.0.1:5654/metrics/write?db=tagdata

my-car speed=87.6 167038034500000
```
~~~
{{< /tab >}}
{{< tab name="cURL" >}}
```sh
curl -o - -X POST "http://127.0.0.1:5654/metrics/write?db=tagdata" \
  --data-binary 'my-car speed=87.6 167038034500000'
```
{{< /tab >}}
{{< tab name="Python" >}}
```python
import requests

response = requests.post(
  "http://127.0.0.1:5654/metrics/write",
  params={"db": "tagdata"},
  data="my-car speed=87.6 167038034500000",
)
print(response.text)
```
{{< /tab >}}
{{< tab name="Javascript" >}}
```javascript
async function writeLineProtocol() {
  const response = await fetch("http://127.0.0.1:5654/metrics/write?db=tagdata", {
    method: "POST",
    body: "my-car speed=87.6 167038034500000",
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
using var content = new StringContent("my-car speed=87.6 167038034500000", Encoding.UTF8);

var response = await client.PostAsync("http://127.0.0.1:5654/metrics/write?db=tagdata", content);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());
```
{{< /tab >}}
{{< /tabs >}}

This example inserts data into table `tagdata` with `name`='my-car.speed', `value`=87.6 and `time`=167038034500000

**telegraf.conf example**

As set telegraf's output config to use http port of Machbase Neo,
the metrics that collected by telegraf are directly inserted into Machbase Neo.

```
[[outputs.http]]
url = "http://127.0.0.1:5654/metrics/write?db=tagdata"
data_format = "influx"
content_encoding = "gzip"
```

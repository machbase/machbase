---
toc: true
title: Python クライアント
type: docs
weight: 62
---

## 検索 {#조회}

### GET CSV {#get-csv}

```python
import requests
params = {"q":"select * from example", "format":"csv", "heading":"false"} 
response = requests.get("http://127.0.0.1:5654/db/query", params)
print(response.text)
```

## 書き込み {#쓰기}

### POST CSV {#post-csv}

```python
import requests
csvdata = """temperature,1677033057000000000,21.1
humidity,1677033057000000000,0.53
"""
response = requests.post(
    "http://127.0.0.1:5654/db/write/example?heading=false", 
    data=csvdata, 
    headers={'Content-Type': 'text/csv'})
print(response.json())
```

## 例 - matplotlib {#예시---matplotlib}

{{< callout emoji="📌" >}}
テストデータを取り込むには、[シェルスクリプトによる波形の書き込み](/neo/tutorials/shellscript-waves)の以下のコマンドを使用します。
{{< /callout >}}

```sh
sh gen_wave.sh | machbase-neo shell import --timeformat=s EXAMPLE
```

**Pythonコード**

```python
import requests
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np

url = "http://127.0.0.1:5654/db/query"
querystring = {"q":"select * from example order by time limit 200"} 
response = requests.request("GET", url, params=querystring)
data = json.loads(response.text)

sinTs, sinSeries, cosTs, cosSeries = [], [], [], []
for row in data["data"]["rows"]:
    ts = datetime.datetime.fromtimestamp(row[1]/1000000000)
    if row[0] == 'wave.cos':
        cosTs.append(ts)
        cosSeries.append(row[2])
    else:
        sinTs.append(ts)
        sinSeries.append(row[2])

plt.plot(sinTs, sinSeries, label="sin")
plt.plot(cosTs, cosSeries, label="cos")
plt.title("チュートリアルの波形")
plt.legend()
plt.show()
```

{{< figure src="/images/python-chart.jpg" width="500px" >}}

## 例 - pandas {#예시---pandas}

### テーブルからDataFrameの読み込み {#테이블에서-데이터프레임-로드}

- machbase-neoのHTTP APIを使って、pandasのDataFrameを読み込みます。

```python
from urllib import parse
import pandas as pd

query_param = parse.urlencode({
    "q": "select * from example order by time limit 500",
    "format": "csv",
    "timeformat": "s",
})
df = pd.read_csv(f"http://127.0.0.1:5654/db/query?{query_param}")
df
```

{{< figure src="/images/python_http_csv.jpg" width="500px">}}

### DataFrameのテーブルへの書き込み {#데이터프레임을-테이블에-쓰기}

- machbase-neoのHTTP APIで、pandasのDataFrameをタグテーブルに保存します。


```python {{hl_lines=[4]}}
import io, requests

stream = io.StringIO()
df.to_csv(stream, encoding='utf-8', header=False, index=False)
stream.seek(0)

file_upload_resp = requests.post(
    "http://127.0.0.1:5654/db/write/example?timeformat=s&method=append",
    headers={'Content-type':'text/csv'},
    data=stream )

print(file_upload_resp.json())
```

```python
{'success': True, 'reason': 'success, 500 record(s) appended', 'elapse': '2.288791ms'}
```

### CSVの読み込み {#csv-로드}

- pandasとurllibをインポートします。

```py
from urllib import parse
import pandas as pd
```

`"format": "csv"`オプションでクエリURLを作成し、`read_csv`を呼び出します。
時刻データの精度は`timeformat`で指定します。`s`、`ms`、`us`、`ns`（既定値）を使用できます。

```py
query_param = parse.urlencode({
    "q":"select * from example order by time limit 500",
    "format": "csv",
    "timeformat": "s",
})
df = pd.read_csv(f"http://127.0.0.1:5654/db/query?{query_param}")
df
```

### 圧縮CSVの読み込み {#압축-csv-로드}

- HTTP APIからgzip圧縮されたCSVを読み込みます。

```py
from urllib import parse
import pandas as pd
import requests
import io
```

```py
query_param = parse.urlencode({
    "q":"select * from example order by time desc limit 1000",
    "format": "csv",
    "timeformat": "s",
    "compress": "gzip",
})
response = requests.get(f"http://127.0.0.1:5654/db/query?{query_param}", timeout=30, stream=True)
df = pd.read_csv(io.BytesIO(response.content))
df
```

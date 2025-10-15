---
title: 가져오기 & 내보내기
type: docs
weight: 600
---

## CSV 가져오기

```sh
curl -o - https://docs.machbase.com/assets/example/example.csv.gz | \
machbase-neo shell import   \
    --input -               \
    --compress gzip         \
    --timeformat s          \
    EXAMPLE
```
위 명령은 `curl`을 통해 원격 웹 서버에서 압축된 CSV 파일을 다운로드합니다.  
`-o -` 옵션 덕분에 다운로드된 데이터(압축된 바이너리)는 표준 출력으로 전달되고, 그 출력이 `machbase-neo shell import`에 파이프로 연결됩니다. `import` 명령은 `--input -` 옵션을 사용해 표준 입력에서 데이터를 읽습니다.

두 명령을 파이프(`|`)로 연결하면 임시 파일을 만들지 않아도 되므로 로컬 저장 공간을 절약할 수 있습니다.

결과는 1,000건의 레코드가 성공적으로 import 되었음을 보여 줍니다.

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  5352  100  5352    0     0   547k      0 --:--:-- --:--:-- --:--:-- 5226k
import total 1000 record(s) inserted
```

또는 파일을 먼저 로컬에 저장한 뒤 import할 수도 있습니다.

```sh
curl -o data.csv.gz https://docs.machbase.com/assets/example/example.csv.gz
```

압축 여부와 상관없이 CSV 파일을 import할 수 있습니다.  
로컬에 저장된 파일을 `--input <파일>` 옵션으로 지정하고, gzip으로 압축된 경우 `--compress gzip` 옵션을 추가하십시오.

```sh
machbase-neo shell import \
    --input ./data.csv    \
    --timeformat s        \
    EXAMPLE
```

import가 완료되었는지 확인해 봅니다.

```sh
machbase-neo shell "select * from example order by time desc limit 5"
```
```
 ROWNUM  NAME      TIME(UTC)            VALUE     
──────────────────────────────────────────────────
 1       wave.sin  2023-02-15 03:47:50  0.994540  
 2       wave.cos  2023-02-15 03:47:50  -0.104353 
 3       wave.sin  2023-02-15 03:47:49  0.951002  
 4       wave.cos  2023-02-15 03:47:49  0.309185  
 5       wave.cos  2023-02-15 03:47:48  0.669261  
```

샘플 파일에는 1,000개의 레코드가 있으며 import 이후 테이블에도 동일한 수가 저장됨을 확인할 수 있습니다.

```sh
machbase-neo shell "select count(*) from example"
```
```
 ROWNUM  COUNT(*) 
──────────────────
 1       1000     
```

## CSV 내보내기

테이블을 내보내는 방법은 간단합니다. `--output` 옵션으로 저장할 파일 경로를 지정하고, `--format csv`로 CSV 형식을, `--timeformat ns`로 DATETIME 컬럼을 나노초 단위 Unix 에포크로 출력하도록 설정합니다.

```sh
machbase-neo shell export --output ./example_out.csv --format csv --timeformat ns EXAMPLE
```

## Export와 Import를 결합해 테이블 복사

export와 import를 파이프로 연결하면 로컬 임시 파일 없이도 데이터를 “복사”할 수 있습니다.

먼저 데이터를 저장할 새로운 테이블을 생성합니다.

```sh
machbase-neo shell \
    "create tag table EXAMPLE_COPY (name varchar(100) primary key, time datetime basetime, value double)"
```

이제 export 명령과 import 명령을 파이프로 연결해 실행합니다.

```sh
machbase-neo shell export       \
    --output -                  \
    --no-heading --no-footer    \
    --format csv                \
    --timeformat ns             \
    EXAMPLE  |  \
machbase-neo shell import       \
    --input -                   \
    --format csv                \
    --timeformat ns             \
    EXAMPLE_COPY
```

복사된 테이블의 레코드 수를 확인합니다.

```sh
 machbase-neo shell "select count(*) from EXAMPLE_COPY"
```
```
 ROWNUM  COUNT(*) 
──────────────────
 1       1000     
```

이 방식은 A 데이터베이스에서 B 데이터베이스로 테이블을 복사할 때도 활용할 수 있습니다.  
`--server <주소>` 옵션을 사용하면 import 또는 export를 원격 machbase-neo 인스턴스에서 실행하도록 지정할 수 있으며, 두 명령을 서로 다른 서버로 설정하는 것도 가능합니다.

## 쿼리 결과를 import로 활용하기

SELECT 쿼리 결과를 직접 import 명령으로 전달할 수도 있습니다.

```sh
machbase-neo shell sql \
    --output -         \
    --format csv       \
    --no-rownum        \
    --no-heading       \
    --no-footer        \
    --timeformat ns    \
    "select * from example where name = 'wave.sin' order by time" | \
machbase-neo shell import \
    --input -             \
    --format csv          \
    EXAMPLE_COPY
```

위 예제에서는 태그 이름이 `wave.sin`인 데이터를 선택해 `EXAMPLE_COPY` 테이블로 import했습니다.  
`import` 명령은 입력되는 CSV의 필드 개수와 타입을 검증해야 하므로 `sql` 명령에 `--no-rownum`, `--no-heading`, `--no-footer` 옵션을 지정해야 합니다.

## HTTP API로 쿼리 결과 가져오기

machbase-neo HTTP API를 사용하면 쿼리 결과를 가져와 다른 테이블에 적재할 수 있습니다.

```sh
curl -o - http://127.0.0.1:5654/db/query        \
    --data-urlencode "q=select * from EXAMPLE order by time desc limit 100" \
    --data-urlencode "format=csv"                \
    --data-urlencode "heading=false" |           \
curl http://127.0.0.1:5654/db/write/EXAMPLE_COPY \
    -H "Content-Type: text/csv"                  \
    -X POST --data-binary @- 
```

## Import 방식: insert vs. append

기본적으로 import 명령은 `INSERT INTO ...` 문을 사용(`--method insert`)합니다.  
적은 양의 데이터를 처리할 때는 append 방식과 큰 차이가 없지만, 수십만 건 이상의 대량 데이터를 처리할 때는 `--method append`를 사용해 append 방식을 적용하는 것이 효율적입니다.

## 예제

import 기능을 사용해 데이터 파일을 테이블에 적재할 수 있습니다.

{{< callout emoji="📌" >}}
실습을 위해 아래 쿼리를 먼저 실행해 테이블을 준비합니다.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

### CSV 가져오기

`data.csv` 파일을 다음과 같이 생성합니다.

```
name-0,1687405320000000000,123.456
name-1,1687405320000000000,234.567000
name-2,1687405320000000000,345.678000
```

데이터를 가져옵니다.

```sh
machbase-neo shell import \
    --input ./data.csv    \
    --timeformat ns        \
    EXAMPLE
```

Select data

```sh
machbase-neo shell "SELECT * FROM EXAMPLE";

 ROWNUM  NAME    TIME(LOCAL)          VALUE   
──────────────────────────────────────────────
      1  name-0  2023-06-22 12:42:00  123.456 
      2  name-1  2023-06-22 12:42:00  234.567 
      3  name-2  2023-06-22 12:42:00  345.678 
3 rows fetched.
```

### TQL을 이용한 import

**텍스트 import**

`import-data.csv` 파일을 다음과 같이 준비합니다.

```
1,100,value,10
2,200,value,11
3,140,value,12
```

아래 코드를 TQL 에디터에 붙여 넣고 `import-tql-csv.tql`로 저장합니다.

```js
STRING(payload() ?? `1,100,value,10
2,200,value,11
3,140,value,12`, separator('\n'))

SCRIPT({
    str =  $.values[0].trim().split(',');
    $.yield(
        "tag-" + str[0],
        (new Date().getTime()*1000000),
        parseInt(str[1])+parseInt(str[3])
    )
})
APPEND(table("example"))
```

작성한 TQL에 CSV를 전송합니다.

```sh
curl -o - --data-binary @import-data.csv http://127.0.0.1:5654/db/tql/import-tql-csv.tql

append 3 rows (success 3, fail 0).
```

데이터를 조회합니다.

```sh
machbase-neo shell "select * from example";

 ROWNUM  NAME   TIME(LOCAL)          VALUE 
───────────────────────────────────────────
      1  tag-1  1970-01-01 09:00:00  10    
      2  tag-2  1970-01-01 09:00:00  11    
      3  tag-3  1970-01-01 09:00:00  12    
3 rows fetched.
```

**JSON import**

`import-data.json` 파일을 준비합니다.

```json
{
  "tag": "pump",
  "data": {
    "string": "Hello TQL?",
    "number": "123.456",
    "time": 1687405320,
    "boolean": true
  },
  "array": ["elements", 234.567, 345.678, false]
}
```

아래 코드를 TQL 에디터에 붙여 넣고 `import-tql-json.tql`로 저장합니다.

```js
BYTES( payload() ?? {
    {
        "tag": "pump",
        "data": {
            "string": "Hello TQL?",
            "number": "123.456",
            "time": 1687405320,
            "boolean": true
        },
        "array": ["elements", 234.567, 345.678, false]
    }
})
SCRIPT({
    obj = JSON.parse($.values[0]);
    $.yield(obj.tag+"_0", obj.data.time*1000000000, obj.data.number)
    $.yield(obj.tag+"_1", obj.data.time*1000000000, obj.data.array[1])
    $.yield(obj.tag+"_2", obj.data.time*1000000000, obj.data.array[2])
    for (i = 0; i < obj.array.length; i++) {
    }
})
APPEND(table("example"))
```

작성한 TQL에 JSON을 전송합니다.

```sh
curl -o - --data-binary @import-data.json http://127.0.0.1:5654/db/tql/import-tql-json.tql

append 2 rows (success 2, fail 0).
```

데이터를 조회합니다.

```sh
machbase-neo shell "select * from example";

 ROWNUM  NAME    TIME(LOCAL)          VALUE   
──────────────────────────────────────────────
      1  tag-1   1970-01-01 09:00:00  10      
      2  pump_2  2023-06-22 12:42:00  345.678 
      3  tag-2   1970-01-01 09:00:00  11      
      4  tag-3   1970-01-01 09:00:00  12      
      5  pump_1  2023-06-22 12:42:00  234.567 
5 rows fetched.
```


### 브리지에서 import

**사전 준비**

```sh
bridge add -t sqlite mem file::memory:?cache=shared;

bridge exec mem create table if not exists mem_example(name varchar(20), time datetime, value double);

bridge exec mem insert into mem_example values('tag0', '2021-08-12', 10);
bridge exec mem insert into mem_example values('tag0', '2021-08-13', 11);
```

**브리지 데이터 import**

아래 코드를 TQL 에디터에 입력해 실행합니다.

```js
SQL(bridge('mem'), "select * from mem_example")
APPEND(table('example'))
```

데이터를 조회합니다.

```sh
machbase-neo shell "select * from example";

 ROWNUM  NAME  TIME(LOCAL)          VALUE 
──────────────────────────────────────────
      1  tag0  2021-08-12 09:00:00  10    
      2  tag0  2021-08-13 09:00:00  11    
2 rows fetched.
```

### CSV 내보내기

데이터를 내보냅니다.

```sh
machbase-neo shell export      \
    --output ./data_out.csv    \
    --format csv               \
    --timeformat ns            \
    EXAMPLE
```

내보낸 파일을 확인합니다.

```sh
cat data_out.csv 

TAG0,1628694000000000000,100
TAG0,1628780400000000000,110
```

### JSON 내보내기

데이터를 내보냅니다.

```sh
machbase-neo shell export      \
    --output ./data_out.json   \
    --format json              \
    --timeformat ns            \
    EXAMPLE
```

내보낸 파일을 확인합니다.

```sh
cat data_out.json

{
  "data": {
    "columns": [
      "NAME",
      "TIME",
      "VALUE"
    ],
    "types": [
      "string",
      "datetime",
      "double"
    ],
    "rows": [
      [
        "TAG0",
        1628694000000000000,
        100
      ],
      [
        "TAG0",
        1628780400000000000,
        110
      ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.847207ms"
}
```

### Export via TQL

**Export CSV**

```js
SQL(`select * from example`)
CSV()
```

**Export JSON**

```js
SQL(`select * from example`)
JSON()
```

**Export CSV with TQL script**

Copy the code below into TQL editor and save `export-tql-csv.tql`.

```js
SQL( 'select * from example limit 30' )
SCRIPT({
    if  ($.values[2] % 2 == 0) {
        r_value = "even"
    } else {
        r_value = "odd"
    }

    $.yield($.key + "-tql", $.values[2],  r_value)
})
CSV()
```

Open it with web browser at [http://127.0.0.1:5654/db/tql/export-tql-csv.tql](http://127.0.0.1:5654/db/tql/export-tql-csv.tql), or use *curl* command on the terminal.

```sh
TAG1-tql,11,odd
TAG0-tql,10,even
```

### Export into Bridge

**Prepare**

```sh
bridge add -t sqlite mem file::memory:?cache=shared;

bridge exec mem create table if not exists mem_example(name varchar(20), time datetime, value double);
```

**Export data from Bridge**

Copy the code below into TQL editor and run

```js
SQL("select * from example")
INSERT(bridge('mem'), table('mem_example'), 'name', 'time', 'value')
```

Select bridge table data

```sh
machbase-neo shell bridge query mem "select * from mem_example";

┌──────┬───────────────────────────────┬───────┐
│ NAME │ TIME                          │ VALUE │
├──────┼───────────────────────────────┼───────┤
│ TAG0 │ 2021-08-12 00:00:00 +0900 KST │    10 │
│ TAG1 │ 2021-08-13 00:00:00 +0900 KST │    11 │
└──────┴───────────────────────────────┴───────┘
```

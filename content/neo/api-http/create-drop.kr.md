---
title: 테이블 생성과 삭제
type: docs
weight: 30
---

HTTP `query` API는 `SELECT` 구문뿐 아니라 DDL도 실행할 수 있으므로 HTTP API로 테이블을 생성하거나 삭제할 수 있습니다.

## Create table

자세한 내용은 [태그 테이블](/dbms/feature-table/tag/) 문서를 참고해 주십시오.

**요청**

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```
{{< /tab >}}
{{< /tabs >}}

**응답**

```json
{"success":true,"reason":"Created successfully.","elapse":"92.489922ms"}
```

### IF NOT EXISTS

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```
{{< /tab >}}
{{< /tabs >}}

### TAG STATISTICS(태그 통계)

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double summarized)
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double summarized)"
```
{{< /tab >}}
{{< /tabs >}}

{{< callout emoji="📢" >}}
**참고** `summarized` 키워드는 해당 태그 테이블에 데이터가 적재될 때 내부 태그 데이터 구조의 통계를 자동으로 생성한다는 의미입니다. 자세한 내용은 [태그 통계](/dbms/feature-table/tag/manipulate/extract/#display-statistical-information-by-specific-tag-id) 문서를 참고해 주십시오.
{{< /callout >}}

## Drop table

**요청**

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=drop table EXAMPLE
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=drop table EXAMPLE"
```
{{< /tab >}}
{{< /tabs >}}

**응답**

```json
{"success":true,"reason":"Dropped successfully.","elapse":"185.37292ms"}
```

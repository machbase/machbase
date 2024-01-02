---
title: Create, Drop table
type: docs
weight: 10
---

The HTTP "Query" API doesn't accept only "SELECT" SQL but also DDL. So it is possible to create and drop tables via HTTP API

## Create table

{{< tabs items="Linux/macOS,Windows">}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query ^
    --data-urlencode ^
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```
{{< /tab >}}
{{< /tabs >}}

- response

    ```json
    {"success":true,"reason":"Created successfully.","elapse":"92.489922ms"}
    ```

## Drop table

{{< tabs items="Linux/macOS,Windows">}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=drop table EXAMPLE"
```
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query ^
    --data-urlencode "q=drop table EXAMPLE"
```
{{< /tab >}}
{{< /tabs >}}

- response

    ```json
    {"success":true,"reason":"Dropped successfully.","elapse":"185.37292ms"}
    ```

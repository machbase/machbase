---
title: HTTP API
type: docs
weight: 110
---

The machbase-neo provides two main functions via HTTP API.
One is `query` that can execuate any type of SQL statements, the other is `write` that is equivalent `INSERT INTO...` SQL statement.

General purpose of HTTP API is exposing functionalities that access the data stored in machbase database for the user's service applications and data analytics tools,
while sensors and things are storing data into machbase via MQTT and HTTP.

{{< figure src="/images/interfaces.jpg" width="500" >}}


## Endpoints

Applications and sensors can read/write data via HTTP API.

| Method  | Path             | Description                           |
| :-----: | :--------------- | :-------------------------------------|
| GET     | `/db/query`      | execute query with `q` param          |
| POST    | `/db/query`      | execute query with JSON and form data |
| POST    | `/db/write`      | write data from JSON and CSV formats  |
| POST    | `/metrics/write` | write data in ILP (influx line protocol) |

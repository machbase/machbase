---
title: "@jsh/db"
type: docs
weight: 10
---

{{< neo_since ver="8.0.52" />}}


## Client

The database client.

<h6>Usage example</h6>

```js {linenos=table,linenostart=1}
const db = require("@jsh/db");
const client = new db.Client();
try {    
    conn = client.connect();
    rows = conn.query("select * from example limit 10")
    cols = rows.columns()
    console.log("cols.names:", JSON.stringify(cols.columns));
    console.log("cols.types:", JSON.stringify(cols.types));
    
    count = 0;
    for (const rec of rows) {
        console.log(...rec);
        count++;
    }
    console.log("rows:", count, "selected" );
} catch(e) {
    console.log("Error:", e);
} finally {
    if (rows) rows.close();
    if (conn) conn.close();
}
```

### Creation

| Constructor             | Description                          |
|:------------------------|:----------------------------------------------|
| new Client(*options*)     | Instantiates a database client object with an options |

If neither `bridge` nor `driver` is specified, the client defaults to connecting to the internal Machbase DBMS.

<h6>Options</h6>

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| lowerCaseColumns    | Boolean      | `false`        | map the lower-cased column names to the result object |

- Options for Drivers

`driver` and `dataSource` options support `sqlite`, `mysql`, `mssql`, `postgresql` and `machbase` without pre-defined bridge.

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| driver              | String       |                | driver name         |
| dataSource          | String       |                | database connection string |

- Options for Bridge

It is also possible to create Client with predefined bridge.

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| bridge              | String       |                | bridge name         |


### Methods

#### connect()

connect to the database.

<h6>Return value</h6>

[Conn](#Conn)


## Conn

### Methods

#### close()

disconnect to the database and release

<h6>Syntax</h6>

```js
close()
```

#### query()

<h6>Syntax</h6>

```js
query(String *sqlText*, any ...*args*)
```

<h6>Return value</h6>

[Rows](#rows)

#### queryRow()

<h6>Syntax</h6>

```js
queryRow(String *sqlText*, any ...*args*)
```

<h6>Return value</h6>

[Row](#Row)


#### exec()

<h6>Syntax</h6>

```js
exec(String *sqlText*, any ...*args*)
```

<h6>Return value</h6>

[Result](#result)

## Rows

Rows encapsulates the result set obtained from executing a query.

It implements `Symbol.iterable`, enabling support for both patterns:

```js
for(rec := rows.next(); rec != null; rec = rows.next()) {
    console.log(...rec);
}

for (rec of rows) {
    console.log(...rec);
}
```

### Methods

#### close()

Release database statement

<h6>Syntax</h6>

```js
close()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

None.

#### next()

fetch a record, returns null if no more records

<h6>Syntax</h6>

```js
next()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

any[]

#### columns()

<h6>Syntax</h6>

```js
columns()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

[Columns](#columns)

#### columnNames()

<h6>Syntax</h6>

```js
columnNames()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

String[]

#### columnTypes()

<h6>Syntax</h6>

```js
columnTypes()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

String[]


## Row
Row encapsulates the result of queryRow which retrieve a single record.

### Methods

#### columns()

<h6>Syntax</h6>

```js
columns()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

[Columns](#columns)


#### columnNames()

names of the result

<h6>Syntax</h6>

```js
columnNames()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

String[]

#### columnTypes()

types of the result

<h6>Syntax</h6>

```js
columnTypes()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

String[]


#### values()

result columns

<h6>Syntax</h6>

```js
values()
```

<h6>Parameters</h6>

None.

<h6>Return value</h6>

Object

## Result

Result represents the outcome of the `exec()` method, providing details about the execution.

<h6>Properties</h6>

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| message            | String     | result message     |
| rowsAffected       | Number     |                    |

## Columns

<h6>Properties</h6>

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| columns            | []String   | names of the result |
| types              | []String   | types of the result |



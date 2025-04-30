---
title: "@jsh/db"
type: docs
weight: 10
---

{{< neo_since ver="8.0.52" />}}


## Client

The database client.

**Usage example**

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

If `bridge` and `driver` are not sepcified, it create a client that connects to the internal machbase dbms.

### Options

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| lowerCaseColumns    | Boolean      | `false`        | map the lower-cased column names to the result object |

- Options for Bridge
| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| bridge              | String       | `""`           | bridge name         |

- Options for DataSource

| Option              | Type         | Default        | Description         |
|:--------------------|:-------------|:---------------|:--------------------|
| driver              | String       |                | driver name         |
| dataSource          | String       |                | database connection string |

### Methods

| Method                                 | Returns           | Description        |
|:---------------------------------------|:------------------|:-------------------|
| connect()                              | [Conn](#Conn)     | connect to the database |


## Conn

### Methods

| Method                                 | Returns           | Description        |
|:---------------------------------------|:------------------|:-------------------|
| close()                                |                   | disconnect to the database and release |
| query(String *sqlText*, any ...*args*) | [Rows](#rows)     |                    |
| exec(String *sqlText*, any ...*args*)  | [Result](#result) |                    |

## Rows

### Methods

| Method                                 | Returns             | Description        |
|:---------------------------------------|:--------------------|:-------------------|
| close()                                |                     | release database statement |
| next()                                 | any[]               | fetch a record, returns null if no more records |
| columns()                              | [Columns](#columns) |                    |
| columnNames()                          | String[]            | names of the result |
| columnTypes()                          | String[]            | types of the result |

It implements Symbol.iterable, so that it supports two patterns...:

```js
for(rec := rows.next(); rec != null; rec = rows.next()) {
    console.log(...rec);
}

for (rec of rows) {
    console.log(...rec);
}
```

## Result

### Properties

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| message            | String     | result message     |
| rowsAffected       | Number     |                    |

## Columns

### Properties

| Property           | Type       | Description        |
|:-------------------|:-----------|:-------------------|
| columns            | []String   | names of the result |
| types              | []String   | types of the result |


## External Database Drivers

`@jsh/db` module supports `sqlite`, `mysql`, `mssql`, `postgresql` and `machbase` without pre-defined bridge.


### Machbase

This example demonstrates how to connect to another Machbase instance via port 5656 and execute a query.

Set `lowerCaseColumns: true` at line 5 to ensure that the query results use lower-cased property names in the record object, as demonstrated at line 17.

```js {linenos=table,linenostart=1,hl_lines=[4]}
db = require("@jsh/db");
client = db.Client({
    driver: "machbase",
    dataSource: "host=192.168.0.207 port=5656 user=sys password=manager",
    lowerCaseColumns: true
})

try {
    sqlText = "select * from example where name = ? limit ?,?";
    tag = "my-car";
    off = 10;
    limit = 5;

    conn = client.connect()
    rows = conn.query(sqlText, tag, off, limit)
    for( rec of rows) {
        console.log(rec.name, rec.time, rec.value)
    }
} catch(e) {
    console.error(e.message)
} finally {
    rows.close()
    conn.close()
}
```

### Sqlite

```js {linenos=table,linenostart=1,hl_lines=[4]}
const db = require("@jsh/db");
client = new db.Client({
    driver:"sqlite",
    dataSource:"file::memory:?cache=shared"
});

try{
    conn = client.connect()
    conn.exec(`
        CREATE TABLE IF NOT EXISTS mem_example(
            id         INTEGER NOT NULL PRIMARY KEY,
            company    TEXT,
            employee   INTEGER
        )
    `);

    conn.exec(`INSERT INTO mem_example(company, employee) values(?, ?);`, 
        'Fedel-Gaylord', 12);

    rows = conn.query(`select * from mem_example`);
    for( rec of rows ) {
        console.log(...rec)
    }
}catch(e){
    console.error(e.message);
}finally{
    rows.close();
    conn.close();
}

```


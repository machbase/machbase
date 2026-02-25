---
title: JSH - JavaScript
type: docs
weight: 75
---

{{< neo_since ver="8.0.52" />}}

{{< callout type="warning" >}}
**BETA Notice**<br/>
JSH is currently in beta. Its API and commands are subject to change in future releases.
{{< /callout >}}


JSH allows you to write JavaScript applications for Machbase Neo.
Files with the `.js` extension are recognized by Machbase Neo as executable scripts.

## Hello World Example

Copy the following code and save it as `hello.js`.

```js
console.print("Hello World?\n")
```

Select "JSH" from the "New..." page.

{{< figure src="./img/fish.jpg" width="86">}}

It works as a simple command-line interpreter for running `.js` files.

To run the saved script, enter the following command:

```
/work > ./hello.js
Hello World? 
```

{{< figure src="./img/fish-hello.jpg" width="486">}}

## Database Example

You can easily write applications that query and insert Machbase data.

```js
'use strict';
// Load machbase client module.
const machcli = require('machcli');
// Create database client instance.
const db = new machcli.Client({
    host: '127.0.0.1',
    port: 5656, // machbase native port
    username:'sys',
    password: 'manager'
})

var conn, rows;
try {
    // Create a database connection.
    conn = db.connect();
    // Execute query.
    rows = conn.query('SELECT NAME, TYPE, COLCOUNT FROM m$sys_tables LIMIT 5');
    // Iterates result set.
    for (const row of rows) {
        console.println(row.NAME, row.TYPE, row.COLCOUNT);
    }
} finally {
    // Release resources
    rows && rows.close();
    conn && conn.close();
}
```

## External Execution

You can run a JavaScript application you wrote outside the machbase-neo server process,
as long as the machbase-neo executable is available.
When you run `machbase-neo jsh`, the JSH interpreter executes the given script.
With this approach, you can build database query/insert applications using only the machbase-neo executable,
without additional tools.

```sh
$ /path/to/the/machbase-neo jsh ./hello.js
Hello World?
```

## Commands

- `exit` ends the current JSH session.
- `ls` shows the file list in the current working directory.
- `cd` changes the working directory or moves to `/work`.

While functionality is basic, it is sufficient for validating scripts.

## Modules
JSH includes various JavaScript modules that can be used in `SCRIPT()` within TQL and in `*.js` applications.
However, the TQL context object `$`, which provides utility methods such as `$.yield()`, is TQL-only and is not accessible from `*.js` applications.

For detailed information, refer to the documentation for each module.

{{< children_toc />}}

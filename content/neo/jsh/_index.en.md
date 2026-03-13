---
title: JSH
type: docs
weight: 75
tags: JavaScript
---

{{< neo_since ver="8.0.52" />}}

{{< callout type="warning" >}}
**BETA Notice**<br/>
JSH is currently in beta. Its API and commands are subject to change in future releases.
{{< /callout >}}


JSH allows you to write JavaScript applications for Machbase Neo.
Files with the `.js` extension are recognized by Machbase Neo as executable scripts.

## Commands

- `exit` ends the current JSH session.
- `ls` shows the file list in the current working directory.
- `cd` changes the working directory or moves to `/work`.

While functionality is basic, it is sufficient for validating scripts.

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


## Directory Mounting

The JSH runtime environment uses a virtual file system that is isolated from the host OS file system.
If you run JSH and execute `ls -l /` inside it, you can see that JSH has its own directory tree,
which is different from the directory structure of the host operating system.

{{< figure src="./img/fish-ls.jpg" width="513">}}

Among these default directories, `/sbin` and `/lib` contain read-only files built into JSH.
The `/work` directory is automatically mounted to the current OS directory, or to the directory shown in the file explorer in the web environment, unless another directory is specified when JSH starts.

To mount an arbitrary directory, use the `-v <mount_point>=<os_dir>` option.
For example, to mount the OS directory `/var/tmp` as `/tmp` in JSH, run the following command.

```sh
$ machbase-neo jsh -v /tmp=/var/tmp
```

{{< figure src="./img/fish-ls-mount.jpg" width="513">}}

## External Execution

You can run a JavaScript application you wrote outside the machbase-neo server process,
as long as the machbase-neo executable is available.
When you run `machbase-neo jsh`, the JSH interpreter executes the given script.
With this approach, you can build database query/insert applications using only the machbase-neo executable,
without additional tools.

Use the `-C <code>` option when you want to run a short JavaScript snippet directly from the command line,
without creating a separate script file.

```sh
$ /path/to/the/machbase-neo jsh -C 'console.println("Hello World?")'
Hello World?
```

To run a saved script without mounting a local directory, pass the script path with the
`-C @<script_path>` form.

```sh
# If hello.js is located at ./src/hello.js
$ /path/to/the/machbase-neo jsh -C @./src/hello.js
Hello World?
```

If you want to run a script stored in a local directory, use the `-v <mount_point>=<src_dir>` option.
This mounts the host directory into the JSH runtime, allowing you to run the script by its mounted path.
It is especially useful when the script depends on other files in the same directory.

```sh
# If hello.js is at ./src/hello.js, mount the src directory to /script
$ /path/to/the/machbase-neo jsh -v /script=./src /script/hello.js
Hello World?
```

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

## Modules
JSH includes various JavaScript modules that can be used in `SCRIPT()` within TQL and in `*.js` applications.
However, the TQL context object `$`, which provides utility methods such as `$.yield()`, is TQL-only and is not accessible from `*.js` applications.

For detailed information, refer to the documentation for each module.

{{< children_toc />}}

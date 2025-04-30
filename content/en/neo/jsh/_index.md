---
title: JSH
type: docs
weight: 75
---

{{< callout type="warning" >}}
**BETA Notice**<br/>
JSH is currently in beta. Its API and commands are subject to change in future releases.
{{< /callout >}}

{{< neo_since ver="8.0.52" />}}

JSH allows developers to create applications using JavaScript that execute directly within the machbase-neo process.
Files with the `.js` extension are recognized by machbase-neo as executable scripts.

## Hello World?

Copy the below code and save as `hello.js`.

```js
p = require("@jsh/process");
p.print("Hello", "World?", "\n")
```

JSH can be accessed from the "New..." page.
It serves as a straightforward command-line interpreter for executing `.js` files.

To run the saved script, use the following command:

```
jsh / > ./hello.js
Hello World? 
```

## Commands

- `exit` ends the current JSH session.
- `ls` list files of the current working directory.
- `cd` change workding directory.
- `ps` list all processes and its pid.
- `kill <pid>` terminates the specified process.

While its functionality is basic, it is sufficient for testing your scripts.

## Daemon

For creating applications that run in the background, consider implementing them as daemon processes.

```js {linenos=table,hl_lines=[4,"18-22"],linenostart=1}
p = require("@jsh/process")

if( p.ppid() != 1) {
    p.daemonize()
    console.log("svc daemonized")
} else {
    doService()
}

function doService() {
    console.log("svc start - "+p.pid())
    p.addCleanup(()=>{
        // this code be executed when the process is terminated
        console.log("svc stop - "+p.pid())
    })

    sum = 0
    for( i = 0; i < 60; i++) {
        p.sleep(1000)
        sum += i
        console.log("svc pid =", p.pid(), "i =", i)
    }
    console.log("svc sum =", sum)
}
```

- Line 4: `daemonize()` makes the current application to run as backgound process.
- Line 18-22 : it runs every 1 second for a minute.

Save the above code and run, the output messages are printed on the stdout which is the default log writer.

```
2025/04/28 15:44:25.295 INFO  /sbin/svc.js     svc start - 1035
2025/04/28 15:44:26.296 INFO  /sbin/svc.js     svc pid = 1035 i = 0
2025/04/28 15:44:27.296 INFO  /sbin/svc.js     svc pid = 1035 i = 1
2025/04/28 15:44:28.298 INFO  /sbin/svc.js     svc pid = 1035 i = 2
                ... omit ...
2025/04/28 15:45:24.358 INFO  /sbin/svc.js     svc pid = 1035 i = 58
2025/04/28 15:45:25.360 INFO  /sbin/svc.js     svc pid = 1035 i = 59
2025/04/28 15:45:25.360 INFO  /sbin/svc.js     svc sum = 1770
2025/04/28 15:45:25.360 INFO  /sbin/svc.js     svc stop - 1035

```

## Services

To start background process automatically when machbase-neo starts,
Create a JSON file that directs how to start your application.

Create a directory `/etc/services` and create a JSON file in the directory.

- `/etc/services/svc.json`

```json
{
    "enable": true,
    "start_cmd": "/sbin/svc.js",
    "start_args": []
}
```

When machbase-neo starts, it scans the `/etc/services` directory for JSON files.
Each JSON file is treated as a service instruction to launch the specified application.


### Service Control Commands

**`servicectl status`** Display status of services.

**`servicectl start <service>`** Start the service of the given name.

**`servicectl stop <service>`** Stop the service of the given name.

**`servicectl reread`** Re-read the configurations from `/etc/services/*.json` and shows the changes.

**`servicectl update`** Re-read configurations and apply the changes.

## Modules
JSH includes various JavaScript modules that can be used in `SCRIPT()` within TQL and in `*.js` applications.
The exception is the `@jsh/process` module, which is only available in `*.js` applications and cannot be used in TQL.
Conversely, the TQL context object `$`, which provides useful methods such as `$.yield()`, is exclusive to TQL and is not accessible from `*.js` applications.

For detailed information, refer to the documentation for each module.

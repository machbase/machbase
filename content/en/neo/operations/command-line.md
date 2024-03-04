---
title: Command line
type: docs
weight: 10
---

## machbase-neo serve

Start machbase-neo server process.

**Flags**
             
| flag             | desc                                                                             |
|:-----------------|:-------------------------------------------------------------------------------- |
| `--host`         | listening network addr (default `127.0.0.1`) <br/> ex) `--host 0.0.0.0`          |
| `-c`, `--config` | config file location  <br/> ex) `--config /data/machbase-neo.conf`               |
| `--pid`          | file path to save pid <br/> ex) `--pid /data/machbase-neo.pid`                   |
| `--data`         | path to database (default `./machbase_home`) <br/> ex) `--data /data/machbase`   |
| `--file`         | path to files (default `.`)<br/> ex) `--file /data/files`                        |
| `--log-filename`        | log file path (default `-` stdout)<br/> ex) `--log-filename /data/logs/machbase-neo.log` |
| `--log-level`           | log level. TRACE, DEBUG, INFO, WARN, ERROR (default `INFO`)<br/> ex) `--log-level INFO`  |
| `--log-append`          | append existing log file. (default true)               {{< neo_since ver="8.0.13" />}}   |
| `--log-rotate-schedule` | time scheduled log file rotation (default `@midnight`) {{< neo_since ver="8.0.13" />}}   |
| `--log-max-size`        | file max size in MB (default 10)                       {{< neo_since ver="8.0.13" />}}   |
| `--log-max-backups`     | maximum log file backups (default 1)                   {{< neo_since ver="8.0.13" />}}   |
| `--log-max-age`         | maximum days in backup files (default 7)               {{< neo_since ver="8.0.13" />}}   | 
| `--log-compress`        | gzip compress the backup files (default false)         {{< neo_since ver="8.0.13" />}}   |
| `--log-time-utc`        | use UTC time for logging (default false)               {{< neo_since ver="8.0.13" />}}   |
| `--preset`              | database preset `auto`, `fog`, `edge` (default `auto`)<br/> ex) `--preset edge`  |

{{< callout type="info" emoji="📌">}}
**IMPORTANT**<br/>
Since the default of `--host` is the loopback address, it is not allowed to access machbase-neo from the remote hosts.
<br/>
Set `--host <host-address>` or `--host 0.0.0.0` for accepting the network connections from remote clients.
{{< /callout >}}

If execute `machbase-neo serve` with no flags,

```sh
$ machbase-neo serve
```

it is equivalent with

```sh
$ machbase-neo serve --host 127.0.0.1 --data ./machbase_home --file . --preset auto
```

## machbase-neo shell

Start machbase-neo shell. It will start interactive mode shell if there are no other arguments.

**Flags**

| flag (long)       | desc                                                      |      |
|:------------------|:----------------------------------------------------------|------|
| `-s`, `--server`  | machbase-neo's gRPC address. <br/> default: `--server tcp://127.0.0.1:5655` <br/> e.g. `-s unix://./mach-grpc.sock` |
| `--user`          | user name.<br/>default: `sys` <br/>env: `NEOSHELL_USER`            | {{< neo_since ver="8.0.4" />}} |
| `--password`      | password.<br/>default: `manager` <br/>env: `NEOSHELL_PASSWORD`     | {{< neo_since ver="8.0.4" />}} |

When machbase-neo shell starts, it is looking for the user name and password from OS's environment variables `NEOSHELL_USER` and `NEOSHELL_PASSWORD`. Then if the flags `--user` and `--password` are provided, it will override the provided values instead of the environment variables.

###  Precedence of username and password

{{% steps %}}

### Command line flags

If `--user`, `--password` is provided? Use the given values

### Environment variables

If `$NEOSHELL_USER` (on windows `%NEOSHELL_USER%`) is set? Use the value as the user name.

If `$NEOSHELL_PASSWORD` (on windows `%NEOSHELL_PASSWORD%`) is set? Use the value as the password.

### Default

None of those are provided? Use default value `sys` and `manager`.

{{% /steps %}}

### Practical usage

For the security, use instant environment variables as below example.

```sh
$ NEOSHELL_PASSWORD='my-secret' machbase-neo shell --user sys
```

Be aware when you use `--password` flag, the secret can be exposed by simple `ps` command as like an example below.

```sh
$ machbase-neo shell --user sys --password manager
```

```sh
$ ps -aef |grep machbase-neo
  501 13551  3598   0  9:33AM ttys000    0:00.07 machbase-neo shell --user sys --password manager
```

**Run Query**
  
```sh
machbase-neo» select binary_signature from v$version;
┌────────┬─────────────────────────────────────────────┐
│ ROWNUM │ BINARY_SIGNATURE                            │
├────────┼─────────────────────────────────────────────┤
│      1 │ 8.0.2.develop-LINUX-X86-64-release-standard │
└────────┴─────────────────────────────────────────────┘
a row fetched.
```

**Create Table**

```sh
machbase-neo» create tag table if not exists example (name varchar(20) primary key, time datetime basetime, value double summarized);
executed.
```

**Schema Table**

```sh
machbase-neo» desc example;
┌────────┬───────┬──────────┬────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │
├────────┼───────┼──────────┼────────┤
│      1 │ NAME  │ varchar  │     20 │
│      2 │ TIME  │ datetime │      8 │
│      3 │ VALUE │ double   │      8 │
└────────┴───────┴──────────┴────────┘
```

**Insert Table**

```sh
machbase-neo» insert into example values('tag0', to_date('2021-08-12'), 100);
a row inserted.
```

**Select Table**

```sh
machbase-neo» select * from example;
┌────────┬──────┬─────────────────────┬───────┐
│ ROWNUM │ NAME │ TIME(LOCAL)         │ VALUE │
├────────┼──────┼─────────────────────┼───────┤
│      1 │ tag0 │ 2021-08-12 00:00:00 │ 100   │
└────────┴──────┴─────────────────────┴───────┘
a row fetched.
```

**Drop Table**

```sh
machbase-neo» drop table example;
executed.
```

### Show

Display information.

```sh
show [options] <object>
        objects:
          info                   show server info
          license                show license info
          ports                  show service ports
          users                  list users
          tables [-a]            list tables
          table [-a] <table>     describe the table
          meta-tables            list meta tables
...
        options:
          -a,--all               includes all hidden tables/columns
```

#### show info

```sh
machbase-neo» show info;
┌────────────────────┬─────────────────────────────┐
│ NAME               │ VALUE                       │
├────────────────────┼─────────────────────────────┤
│ build.version      │ v2.0.0                      │
│ build.hash         │ #c953293f                   │
│ build.timestamp    │ 2023-08-29T08:08:00         │
│ build.engine       │ static_standard_linux_amd64 │
│ runtime.os         │ linux                       │
│ runtime.arch       │ amd64                       │
│ runtime.pid        │ 57814                       │
│ runtime.uptime     │ 2h 30m 57s                  │
│ runtime.goroutines │ 45                          │
│ mem.sys            │ 32.6 MB                     │
│ mem.heap.sys       │ 19.0 MB                     │
│ mem.heap.alloc     │ 9.7 MB                      │
│ mem.heap.in-use    │ 13.0 MB                     │
│ mem.stack.sys      │ 1,024.0 KB                  │
│ mem.stack.in-use   │ 1,024.0 KB                  │
└────────────────────┴─────────────────────────────┘
```

### Desc

Describe table structure.

```sh
machbase-neo» desc example;
┌────────┬───────┬──────────┬────────┐
│ ROWNUM │ NAME  │ TYPE     │ LENGTH │
├────────┼───────┼──────────┼────────┤
│      1 │ NAME  │ varchar  │     20 │
│      2 │ TIME  │ datetime │      8 │
│      3 │ VALUE │ double   │      8 │
└────────┴───────┴──────────┴────────┘
```

## machbase-neo version

Show version and engine info.

![machbase-neo_version](../img/machbase-neo-version.png)

## machbase-neo gen-config

Prints out default config template.

```
$ machbase-neo gen-config ↵

define DEF {
    LISTEN_HOST       = flag("--host", "127.0.0.1")
    SHELL_PORT        = flag("--shell-port", "5652")
    MQTT_PORT         = flag("--mqtt-port", "5653")
    HTTP_PORT         = flag("--http-port", "5654")
    GRPC_PORT         = flag("--grpc-port", "5655")
......
```

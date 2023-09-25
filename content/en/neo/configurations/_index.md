---
title: Configurations
type: docs
weight: 400
---

## Create a new config file

Execute machbase-neo with `gen-config` and save its output as default config file

```sh
machbase-neo gen-config > ./machbase-neo.conf
```

Edit generated config so that customize settings, then start machbase-neo with `--config <path>` or `-c <path>` option to direct where machbase-neo read config.

```sh
machbase-neo serve --config ./machbase-neo.conf
```

## Database directory

The default value of `DataDir` is `${execDir()}/machbase_home` which is a sub-directory of where `machbase-neo` executable file is.

Change it to new path where you want to store the database files. If the folder is new and has no database files, machbase-neo will create a new database automatically.

## Preference directory

The default value of `PrefDir` is `prefDir("machbase")` which is `$HOME/.config/machbase`.

## Listeners

| Listener                  | Config                    | default                 |
|:--------------------------|:--------------------------|:------------------------|
| SSH Shell                 | Shell.Listeners           | `tcp://127.0.0.1:5652`  |
| MQTT                      | Mqtt.Listeners            | `tcp://127.0.0.1:5653`  |
| HTTP                      | Http.Listeners            | `tcp://127.0.0.1:5654`  |
| gRPC                      | Grpc.Listeners            | `tcp://127.0.0.1:5655` <br/> `unix://${execDir()}/mach-grpc.sock` |
| Machbase native           | Machbase.PORT_NO          | `5656`                  |
|                           | Machbase.BIND_IP_ADDRESS  | `127.0.0.1`             |


{{< callout type="info" >}}
Machbase native port `5656` is used for native clients such as JDBC and ODBC.
JDBC, ODBC drivers can be found from Machbase home page.
{{< /callout >}}

## Config References

Syntax of config file adopts the HCL syntax.

### functions

Serveral functions are supproted for the value of config item.

- `flag(A, B)` : Get value of command line flag 'A'. if not specified, apply B as default value.
- `env(A, B)` : get value of Envrionment variable 'A'. if not specified, appy B as default value
- `execDir()` : Get directory path where executable file is.
- `userDir()` : Get user's home directory, On Linux and macOS, it returns the $HOME environment variable.
- `prefDir(subdir)` : Ger user's preference directory, On Linux and macOS, it returns the real path of $HOME/.config/{subdir}

{{< callout type="info">}}
**Combine env() and flag()**<br/>
It is general practice for seeking user's setting 
that check command line flag first then find Environment variable and finally apply default value if both are not sepcified.
We can write value `flag("--my-var", env("MY_VAR", "myvalue"))` for this use case
{{< /callout >}}

### define DEF

This section is for the default values. the variables in this section are refered in other section.
Users can define their own variables and even change the command line flags.
As example below, `LISTEN_HOST` is taken value from `--host` flag of command line, but take `"127.0.0.1"` as default if `--host` flag is not provided.

If change `"127.0.0.1"` to `"192.168.1.10"`, the default value will be changed.

If change `"--host"` to `"--bind"` for example, command line flag will be changed. From then you can use `machbase-neo serve --bind <ip_addr>` instead of `machbase-neo serve --host <ip_addr>`.

```hcl
define DEF {
    LISTEN_HOST       = flag("--host", "127.0.0.1")
    SHELL_PORT        = flag("--shell-port", "5652")
    MQTT_PORT         = flag("--mqtt-port", "5653")
    HTTP_PORT         = flag("--http-port", "5654")
    GRPC_PORT         = flag("--grpc-port", "5655")
}
```

### define VARS

This section defines commonly used variables. 

```hcl
define VARS {
    DATA_DIR          = flag("--data", "${execDir()}/machbase_home")
    SHELL_LISTEN_HOST = flag("--shell-listen-host", DEF_LISTEN_HOST)
    SHELL_LISTEN_PORT = flag("--shell-listen-port", DEF_SHELL_PORT)
    GRPC_LISTEN_HOST  = flag("--grpc-listen-host", DEF_LISTEN_HOST)
    GRPC_LISTEN_PORT  = flag("--grpc-listen-port", DEF_GRPC_PORT)
    HTTP_LISTEN_HOST  = flag("--http-listen-host", DEF_LISTEN_HOST)
    HTTP_LISTEN_PORT  = flag("--http-listen-port", DEF_HTTP_PORT)
    MQTT_LISTEN_HOST  = flag("--mqtt-listen-host", DEF_LISTEN_HOST)
    MQTT_LISTEN_PORT  = flag("--mqtt-listen-port", DEF_MQTT_PORT)
    MQTT_MAXMESSAGE   = flag("--mqtt-max-message", 1048576)
}
```

### logging config

| Key                         | Type      | Desc                                                     |
|:----------------------------|:----------|----------------------------------------------------------|
| Console                     | bool      | print out log message on console                         |
| Filename                    | string    | log file path `-` for stdout, ex) /logs/machbase-neo.log |
| DefaultPrefixWidth          | int       | alignment width of log prefix                            |
| DefaultEnableSourceLocation | bool      | enable logging source filename and line number           |
| DefaultLevel                | string    | `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`                |
| Levels                      | array     | array of Level object                                    |

- Level object

| Key                         | Type      | Desc                                                     |
|:----------------------------|:----------|----------------------------------------------------------|
| Pattern                     | string    | glob pattern form logger's name                          |
| Level                       | string    | log level for the logger                                 |

```hcl
module "machbase.com/neo-logging" {
    name = "neolog"
    config {
        Console                     = false
        Filename                    = flag("--log-filename", "-")
        DefaultPrefixWidth          = 16
        DefaultEnableSourceLocation = flag("--log-source-location", false)
        DefaultLevel                = flag("--log-level", "INFO")
        Levels = [
            { Pattern="neo*", Level="TRACE" },
            { Pattern="http-log", Level="DEBUG" },
        ]
    }
}
```

### server config

This section is for the database server consists of multiple parts those will be explained in section by section.

#### MachbaseHome

| Key                         | Type      | Desc                                                     |
|:----------------------------|:----------|----------------------------------------------------------|
| MachbaseHome                | string    | directory path where database files are stored           |

#### Machbase

Machbase core properties are here,
please refer [Property section of Machbase Manual](/dbms/config-monitor/property/) for details. And full manual for [Machbase is here](/dbms)


#### Shell

This allows remote access machbase-neo shell via ssh. Since default `LISTEN_HOST` is `"127.0.0.1"` the ssh access only available from same host machine. Set `"0.0.0.0"` or exact IP adress of host machine to allow remote access.

{{< callout type="warning" >}}
**Security**<br/>
Before allow remote access, it is strongly recommended to change `SYS`'s default password from `manager` to your own.
{{< /callout >}}

| Key                         | Type               | Desc                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | listening adresses (ex: `tcp://127.0.0.1:5652`, `tcp://0.0.0.0:5652`)|
| IdleTimeout                 | duration           | server will close the ssh connection if there is no activity for the specified time |


#### Grpc

machbase-neo's gRPC listening address and size limit of messages are configured.

| Key                         | Type               | Desc                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | listening adresses                                       |
| MaxRecvMsgSize              | int                | maximum message size in MB that server can receive       |
| MaxSendMsgSize              | int                | maximum message size in MB                               |

#### Http

server's HTTP listener config.

| Key                         | Type               | Desc                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | listening adresses                                       |
| Handlers                    | array of handler object |                                                     |
| EnableTokenAuth             | bool               | enable token based authentication (default `false`)      |

- handler object

| Key                         | Type               | Desc                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Prefix                      | string             | prefix of http path, must start with `/`                 |
| Handler                     | string             | handler implementation: `machbase`, `influx`             |

`machbase` handler is for standard HTTP API, `influx` handler is for ingesting line protocol.
More handlers will be added along with future releases.

#### Mqtt

| Key                         | Type               | Desc                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Listeners                   | array of string    | listening adresses                                       |
| Handlers                    | array of handler object |                                                     |
| MaxMessageSizeLimit         | int                | maximum size limit of payload in a PUBLISH <br/> (default 1048576 = 1MB) |
| EnableTokenAuth             | bool               | enable token based authentication (default `false`)      |
| EnableTls                   | bool               | enable TLS for the TCP listeners (default `false`)       |

- handler object

| Key                         | Type               | Desc                                                     |
|:----------------------------|:-------------------|----------------------------------------------------------|
| Prefix                      | string             | prefix of mqtt topic, must compatible MQTT specification |
| Handler                     | string             | handler implementation: `machbase`, `influx`             |

`machbase` handler is for standard MQTT API, `influx` handler is for ingesting payload that encoded in line protocol.
More handlers will be added along with future releases.

### neo-server config

```hcl
module "machbase.com/neo-server" {
    name = "neosvr"
    config {
        MachbaseHome     = VARS_DATA_DIR
        Machbase         = {
            HANDLE_LIMIT     = 2048
        }
        Shell = {
            Listeners        = [ "tcp://${VARS_SHELL_LISTEN_HOST}:${VARS_SHELL_LISTEN_PORT}" ]
            IdleTimeout      = "5m"
        }
        Grpc = {
            Listeners        = [ 
                "unix://${execDir()}/mach-grpc.sock",
                "tcp://${VARS_GRPC_LISTEN_HOST}:${VARS_GRPC_LISTEN_PORT}",
            ]
            MaxRecvMsgSize   = 4
            MaxSendMsgSize   = 4
        }
        Http = {
            Listeners        = [ "tcp://${VARS_HTTP_LISTEN_HOST}:${VARS_HTTP_LISTEN_PORT}" ]
            Handlers         = [
                { Prefix: "/db",      Handler: "machbase" },
                { Prefix: "/metrics", Handler: "influx" },
            ]
            EnableTokenAuth  = VARS_HTTP_ENABLE_TOKENAUTH
        }
        Mqtt = {
            Listeners        = [ "tcp://${VARS_MQTT_LISTEN_HOST}:${VARS_MQTT_LISTEN_PORT}"]
            Handlers         = [
                { Prefix: "db",       Handler: "machbase" },
                { Prefix: "metrics",  Handler: "influx" },
            ]
            EnableTokenAuth     = VARS_MQTT_ENABLE_TOKENAUTH
            EnableTls           = VARS_MQTT_ENABLE_TLS
            MaxMessageSizeLimit = VARS_MQTT_MAXMESSAGE
        }
    }
}
```
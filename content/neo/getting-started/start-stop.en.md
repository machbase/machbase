---
title: Start and Stop
type: docs
weight: 12
---

## Linux & macOS

Run machbase-neo with `serve` command on Linux and macOS.

```sh
machbase-neo serve
```

{{< figure src="../img/server-serve.gif" width="600" >}}

### Expose ports

machbase-neo runs and listens to only localhost by default for the security reason. If clients that runs remotely need to access machbase-neo through network, it requires to start with listen address as `--host <bind address>` option.

To allow listening to all available addresses, use `0.0.0.0`

```sh
machbase-neo serve --host 0.0.0.0
```

To allow a specific address, set the IP address of the host.

```sh
machbase-neo serve --host 192.168.1.10
```

### Stop

If the server is running in foreground mode, simply press `Ctrl+C`.

Or use `shutdown` command. It works only if it is executed in the same host.

```sh
machbase-neo shell shutdown
```

## Linux Service

Refer to the document at [Operations/Linux service](../../operations/service-linux/) that shows how to register machbase-neo as a background process.

## Windows

On Windows, double click "neow.exe" and "machbase-neo serve" button of the top left on the window.

{{< figure src="/images/neow-win.png" width="600" >}}

### Windows Service

machbase-neo can be registered as a service on Windows.<br/>
The commands below should be executed in Administrator mode.

- Install

Register a service. The following arguments after `machbase-neo service install` are same as `machbase-neo serve`, but all paths should *absolute path*.

```
C:\neo-server>.\machbase-neo service install --host 127.0.0.1 --data C:\neo-server\database --file C:\neo-server\files --log-filename C:\neo-server\machbase-neo.log --log-level INFO

```

- Start and Stop

It is possible to start and stop the service with service management that is provided by Windows,
or use the commands below manually.

```
C:\neo-server>.\machbase-neo service start
success to start machbase-neo service.

C:\neo-server>.\machbase-neo service stop
success to stop machbase-neo service.
```

- Uninstall

Removing machbase-neo from the Windows service.

```
C:\neo-server>.\machbase-neo service remove
success to remove machbase-neo service.
```

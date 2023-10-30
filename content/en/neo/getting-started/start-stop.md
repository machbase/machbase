---
title: Start and Stop
type: docs
weith: 12
---

## Start

### foreground

```sh
machbase-neo serve
```

![](../img/server-serve.gif)

### background

If pid file path is given, the process id of machbase-neo will be written on it.
It could be helpful later to stop the process running in background mode with `--daemon` option.

```sh
machbase-neo serve --daemon --pid ./machbase-neo.pid
```

### expose ports

machbase-neo runs and listens to only localhost by default for the security reason. If clients that runs remotely need to access machbase-neo through network, it requires to start with listen address as `--host <bind address>` option.

To allow listening to all available addresses, use `0.0.0.0`

```sh
machbase-neo serve --host 0.0.0.0
```

To allow a specific address, set the IP address of the host.

```sh
machbase-neo serve --host 192.168.1.10
```

## Stop

### foreground

If the server is running in foreground mode, simply press `Ctrl+C`.

###  background

If a pid file was generated, signal `SIGTERM` to process as like the command below.

```sh
kill `cat ./machbase-neo.pid`
```

Or use `shutdown` command. It works only if it is executed in the same host.

```sh
machbase-neo shell shutdown
```

## Windows

On Windows, double click "neow.exe" and "machbase-neo serve" button of the top left on the window.

![interfaces](/images/neow-win.png)

### Windows Service

machbase-neo can be registered as a service on Windows.<br/>
The commands below should be executed in Administrator mode.

- Install

Register a service. The following arguments after `machbase-neo service install` are same as `machbase-neo serve`, but all paths should *abolute path*.

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

---
type: docs
title: '16.4.1 machadmin'
weight: 10
toc: true
---

`machadmin` starts and stops the Machbase server, creates and deletes databases, and checks server status.

## Options

```bash
machadmin -h
```

| Option | Description |
|------|------|
| `-u`, `--startup` | Start the Machbase server |
| `--recovery[=simple,complex,reset]` | Set the startup recovery mode (default: simple) |
| `-s`, `--shutdown` | Shut down the Machbase server gracefully |
| `-k`, `--kill` | Force the Machbase server to stop |
| `-c`, `--createdb` | Create the Machbase database |
| `-d`, `--destroydb` | Delete the Machbase database |
| `-e`, `--check` | Check whether the server is running |
| `-i`, `--silent` | Run without a banner |
| `-r`, `--restore` | Restore the database from a backup |
| `-x`, `--extract` | Convert a backup file to a backup directory |
| `-w`, `--viewimage` | Display backup image file information |
| `-t`, `--licinstall` | Install a license file |
| `-f`, `--licinfo` | Display installed license information |
| `--home-path=path` | Set the Machbase home path |

## Starting the Server

```bash
machadmin -u
```

### Specifying a Recovery Mode

```bash
machadmin -u --recovery=simple    # Default recovery after a clean shutdown
machadmin -u --recovery=complex   # Applied automatically after power loss
machadmin -u --recovery=reset     # Full scan if simple/complex recovery fails
```

| Recovery Mode | Description |
|----------|------|
| `simple` | Default recovery after a clean shutdown. Takes less time |
| `complex` | Applied automatically after an abnormal shutdown such as power loss. Takes longer than `simple` |
| `reset` | Scans all table data for recovery. Some data may be lost |

## Stopping the Server

Graceful shutdown (waits for in-progress work to complete):

```bash
machadmin -s
```

Forced shutdown (terminates the process immediately):

```bash
machadmin -k
```

## Creating and Deleting the Database

```bash
# Create the database
machadmin -c

# Delete the database (displays a confirmation prompt)
machadmin -d
```

## Checking Server Status

```bash
machadmin -e
```

Displays the PID if the server is running.

```
Machbase server is already running with PID (14098).
```

Displays an error if the server is not running.

```
[ERR] Server is not running.
```

## Restoring the Database

Restore the database from a backup directory.

```bash
machadmin -r /path/to/backup
```

Example:

```bash
machadmin -r /home/mach/backup/machbase_backup_20240101
```

## License Management

Install a license file:

```bash
machadmin -t /path/to/license.dat
```

Check the installed license:

```bash
machadmin -f
```

## Silent Mode

Runs without a banner or status messages. Useful in scripts.

```bash
machadmin -i -u    # Start the server without a banner
machadmin -i -s    # Stop the server without a banner
machadmin -i -e    # Check status without a banner
```

## Examples

```bash
# Initialize the database and start the server
machadmin -c
machadmin -u

# Check server status, then stop it
machadmin -e
machadmin -s

# Renew the license
machadmin -s
machadmin -t new_license.dat
machadmin -u
```

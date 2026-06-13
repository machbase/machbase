---
title : machadmin
type : docs
weight: 20
---

machadmin is used to start up or shut down the Machbase server and to check the creation, deletion, and execution status.

## Option and Features

The options for machadmin are as follows. The functions described in the previous installation section are omitted.

```bash
mach@localhost:~$ machadmin -h
```

| Options| Describe |
|--|--|
|-u, --startup|Starts the Machbase server |
|--recovery[=simple,complex,reset]|Recovery mode used with startup (default: simple) |
|-s, --shutdown |Machbase server shuts down normally |
|-c, --createdb |Creates Machbase database |
| -d, --destroydb| Deletes Machbase database |
| -k, --kill| Force quits Machbase server |
| -i, --silent| Runs with less output |
| -r, --restore |Restores database from backup |
| -x, --extract| Converts backup files to backup directory |
| -w, --viewimage| Displays information of a backup image file |
|-e, --check| Checks Machbase server run status |
|-t, --licinstall| Installs license file |
|-f, --licinfo| Outputs installed license information|
|--home-path=path|Specifies the Machbase home path |

## Recovery Mode

Syntax

```
machadmin -u --recovery=[simple | complex | reset]
```

The recovery mode is as follows:

* simple: If there is no power loss when the server is running, simple recovery mode is run by default. 
* complex: The complex recovery mode takes longer to execute than the simple mode. It is executed by default when restarting after the power is turned off.
* reset: When recovery is not performed in simple or complex mode, all data in all tables are checked to recover the database. In this case, some loss of data may occur.

## Server Normal Shutdown

Example:

```
mach@localhost:~$ machadmin -s
 
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for the server shut down...
Server shut down successfully.
```

## Create Database

Example:

```
mach@localhost:~$ machadmin -c
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Database created successfully.
```

## Delete Database

Example:

```
mach@localhost:~$ machadmin -d
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Destroy Machbase database- Are you sure?(y/N) y
Database destroyed successfully.
```

## Force to abort Server

Syntax:

```
machadmin -k
```

Example:

```
mach@localhost:~$ machadmin -k
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for Machbase terminated...
Server terminated successfully.
```

## Run Silent Mode

Removes the message that is output when 'machadmin'  runs.

Syntax:

```
machadmin -i
```

## Database Recovery

Syntax:

```
machadmin -r backup_database_path
```

Example:

```
mach@localhost:~$ machadmin -r 'backup'
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Backed up database restored successfully.
```

## Check server is running

Syntax:

```
machadmin -e
```


Example when server is not running:

```
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
[ERR] Server is not running.
```


Example when server is running:

```
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Machbase server is already running with PID (14098).
```

## Install License File

Syntax:

```
machadmin -t license_file
```


Example:

```
mach@localhost:~$ machadmin -t license.dat
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
License installed successfully.
```

## Check License

Example:

```
mach@localhost:~$ machadmin -f
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
	                   INFORMATION
ID                                : 00000001
Issue Date                        : 2099-12-31
License Type(Version 3)           : FOGUNLIMITED
Company                           : MACHBASE
Project(Product)                  : NONE
Country Code                      : KR
Install Date                      : 2026-06-13 15:08:00
-----------------------------------------------------------------
License information displayed successfully.
-----------------------------------------------------------------
License information displayed successfully.
```

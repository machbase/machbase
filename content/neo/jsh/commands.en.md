---
title: Core Commands
type: docs
weight: 10
---

JSH includes a small set of built-in shell-style commands for navigating directories,
reading files, printing text, creating and removing paths, and waiting for a period of time.

## Overview

Most commands are implemented as JavaScript files under `/sbin` and are resolved through the JSH command path.
The `cd` command is different: it is an internal shell command because it must change the current shell working directory.

**Notes**

- These commands operate inside the JSH virtual filesystem, not directly on the host OS filesystem.
- Relative paths are resolved from the current JSH working directory.
- `cd` affects the active shell session, while commands such as `pwd`, `ls`, and `rm` run as normal commands.
- Some commands intentionally provide a smaller feature set than their Unix counterparts.

## cat

Concatenates files to standard output.
It also supports line formatting options and optional syntax highlighting for selected file types.

<h6>Syntax</h6>

```sh
cat [OPTION]... [FILE]...
```

<h6>Options</h6>

- `-n, --number` number all output lines
- `-E, --showEnds` display `$` at the end of each line
- `-T, --showTabs` display tab characters as `^I`
- `-s, --squeeze` suppress repeated empty lines
- `-c, --color` enable syntax highlighting
- `-h, --help` show help

With `-c`, syntax highlighting is supported for these extensions:

- `.js`
- `.json`
- `.ndjson`
- `.sql`
- `.csv`
- `.yaml`
- `.yml`
- `.toml`

<h6>Usage example</h6>

```sh
/work > cat -n notes.txt
/work > cat -c script.js
/work > cat -sE log.txt
```

## cd

Changes the current working directory of the active JSH shell session.
Unlike most other commands, `cd` is an internal command and is not implemented as a separate `/sbin/*.js` file.

<h6>Syntax</h6>

```sh
cd <directory>
```

If the target directory does not exist, `cd` prints an error and returns a non-zero status.

<h6>Usage example</h6>

```sh
/work > cd subdir
/work/subdir >
```

## echo

Prints its arguments separated by spaces and terminates with a newline.

<h6>Syntax</h6>

```sh
echo [ARG]...
```

`echo` does not currently implement shell-style flags such as `-n` or escape interpretation.
It simply prints the arguments exactly as they are passed.

<h6>Usage example</h6>

```sh
/work > echo hello world
hello world
```

## ls

Lists directory contents.
By default it prints entries in columns with colorized names.

<h6>Syntax</h6>

```sh
ls [OPTION]... [PATH]...
```

<h6>Options</h6>

- `-l, --long` use a detailed listing view
- `-a, --all` include hidden entries
- `-t, --time` sort by modification time, newest first
- `-R, --recursive` list subdirectories recursively

If no path is given, `ls` uses the current working directory.
It also accepts simple wildcard patterns such as `*` and `?` in path arguments.

<h6>Usage example</h6>

```sh
/work > ls
/work > ls -la
/work > ls -t /lib
/work > ls -R src
/work > ls *.js
```

## mkdir

Creates one or more directories.

<h6>Syntax</h6>

```sh
mkdir [OPTION]... DIRECTORY...
```

<h6>Options</h6>

- `-p, --parents` create parent directories as needed
- `-v, --verbose` print a message for each created directory
- `-h, --help` show help

Without `-p`, creating an existing directory reports an error.
With `-p`, existing directories are accepted.

<h6>Usage example</h6>

```sh
/work > mkdir data
/work > mkdir -p logs/app/2026
/work > mkdir -pv build/output
```

## pwd

Prints the current working directory.

<h6>Syntax</h6>

```sh
pwd
```

<h6>Usage example</h6>

```sh
/work > pwd
/work
```

## rm

Removes files or directories.

<h6>Syntax</h6>

```sh
rm [OPTION]... FILE...
```

<h6>Options</h6>

- `-r, -R, --recursive` remove directories and their contents recursively
- `-d, --dir, --directory` remove empty directories
- `-f, --force` ignore nonexistent paths and suppress missing operand errors
- `-v, --verbose` print a message for each removed path
- `-h, --help` show help

Important behavior:

- Removing a directory without `-r` or `-d` reports `Is a directory`
- `-d` only removes empty directories
- `-R` is treated the same as `-r`
- `--directory` is treated the same as `--dir`

<h6>Usage example</h6>

```sh
/work > rm old.txt
/work > rm -rf cache
/work > rm -d empty-dir
/work > rm -fv temp.txt missing.txt
```

## sleep

Waits for the specified number of seconds before returning.

<h6>Syntax</h6>

```sh
sleep [options] <sec>
```

<h6>Options</h6>

- `-h, --help` show help

The value is interpreted as seconds.

<h6>Usage example</h6>

```sh
/work > sleep 5
```

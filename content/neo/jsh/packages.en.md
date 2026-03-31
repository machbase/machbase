---
title: Package Manager
type: docs
weight: 200
---

The `pkg` command manages `package.json`, installs JSH packages, and runs package scripts.
It is intended for JSH applications that keep their dependencies in a project directory such as `/work`.

## Overview

The `pkg` command supports these tasks:

- Create a new `package.json`
- Install dependencies into `node_modules`
- Maintain `package-lock.json`
- Run commands defined in `package.json` `scripts`
- Generate executable wrappers from installed package `bin` entries
- Remove dependencies together with generated wrappers

## package.json

`pkg` treats `package.json` as the manifest of the selected package root.
For a normal project install, that root is the current directory or the directory selected by `--dir`.
For `pkg install -g` and `pkg uninstall -g`, the root is always `/work`.

A minimal project manifest looks like this.

```json
{
  "name": "demo-app",
  "version": "1.0.0",
  "scripts": {
    "start": "./main.js"
  },
  "dependencies": {
    "generic-pkg": "^1.2.0",
    "github.com/acme/demo": "#tag=v1.1.0"
  }
}
```

Common fields used by `pkg` are:

| Field | Type | Description |
| --- | --- | --- |
| `name` | `String` | Project package name |
| `version` | `String` | Project version |
| `scripts` | `Object` | Named command lines for `pkg run` |
| `dependencies` | `Object` | Package name to version specifier map |

Notes:

- `scripts` belongs to the current project manifest and is used only by `pkg run`.
- `dependencies` is updated by `pkg install` and `pkg uninstall` for the selected package root.
- `pkg` also writes `package-lock.json` beside `package.json` for reproducible installs.
- `bin` is read from each installed package's own `package.json` inside `node_modules`, and `pkg` uses it to generate wrappers in `node_modules/.bin`.

For example, after `pkg install -g github.com/acme/demo`, the project manifest that is updated is `/work/package.json`, while the installed package manifest is `/work/node_modules/github.com/acme/demo/package.json`.

## pkg init

Creates a new `package.json` in the current project directory.

<h6>Syntax</h6>

```sh
pkg init [options] <name>
```

<h6>Options</h6>

- `-C, --dir <dir>` use the given project directory instead of the current working directory
- `-g, --global` install into `/work` and `/work/node_modules`, ignoring `--dir`
- `-h, --help` show help

<h6>Usage example</h6>

```sh
/work > pkg init demo-app
Created /work/package.json
```

The generated file includes empty `scripts` and `dependencies` objects.

```json
{
  "name": "demo-app",
  "version": "1.0.0",
  "scripts": {},
  "dependencies": {}
}
```

## pkg install

Installs dependencies from `package.json`, or installs a single package request and updates both
`package.json` and `package-lock.json`.

<h6>Syntax</h6>

```sh
pkg install [options] [name]
```

<h6>Options</h6>

- `-C, --dir <dir>` use the given project directory instead of the current working directory
- `-g, --global` remove the package from `/work` and ignore `--dir`
- `-h, --help` show help

If `name` is omitted, `pkg install` installs the dependencies already declared in `package.json`.

### Global install

`pkg install -g <name>` uses `/work` as the package root and `/work/node_modules` as the installation target.
When `-g` is present, `pkg` ignores `--dir`.

This makes two common cases possible:

- install a global executable package whose `bin` wrapper can be run directly from the shell `PATH`
- install a shared library package into the global package directory

Example:

```sh
/work > pkg install -g github.com/acme/demo
Installed github.com/acme/demo#tag=v1.1.0
```

### npm packages

If the package name is not a GitHub repository path, `pkg` installs it from the npm registry.

```sh
/work > pkg install generic-pkg
Installed generic-pkg@1.2.0
```

This adds the dependency to `package.json` with the resolved npm version range.

```json
{
  "dependencies": {
    "generic-pkg": "^1.2.0"
  }
}
```

### GitHub repository packages

If the package name matches `github.com/<org>/<repo>`, `pkg` installs the repository contents directly
from GitHub.

Supported forms are:

- `github.com/<org>/<repo>`
- `github.com/<org>/<repo>@<tag>`
- `github.com/<org>/<repo>#tag=<tag>`
- `github.com/<org>/<repo>#branch=<branch>`

Behavior:

- If `@<tag>` or `#tag=<tag>` is specified, that tag is used.
- If `#branch=<branch>` is specified, that branch is used even if the repository also has tags.
- If no tag is specified and the repository has tags, the latest tag returned by the GitHub tags API is used.
- If no tag is specified and the repository has no tags, the repository `default_branch` is used.

<h6>Usage example: latest tag</h6>

```sh
/work > pkg install github.com/acme/demo
Installed github.com/acme/demo#tag=v1.1.0
```

<h6>Usage example: explicit tag</h6>

```sh
/work > pkg install github.com/acme/demo@v1.0.0
Installed github.com/acme/demo#tag=v1.0.0
```

You can also use the explicit ref form.

```sh
/work > pkg install github.com/acme/demo#tag=v1.0.0
Installed github.com/acme/demo#tag=v1.0.0
```

<h6>Usage example: explicit branch</h6>

```sh
/work > pkg install github.com/acme/demo#branch=develop
Installed github.com/acme/demo#branch=develop
```

<h6>Usage example: default branch fallback</h6>

If the repository has no tags, the default branch is used.

```sh
/work > pkg install github.com/acme/notags
Installed github.com/acme/notags#branch=main
```

### Installation target

Installed packages are copied into the selected `node_modules` directory.
For example:

- `generic-pkg` -> `node_modules/generic-pkg`
- `github.com/acme/demo` -> `node_modules/github.com/acme/demo`

GitHub repository packages now always install under `node_modules`.
With `pkg install -g`, that directory is `/work/node_modules`.

If an installed package defines `package.json` `bin`, `pkg` creates wrappers in `node_modules/.bin`.
The wrapper name comes from the installed package manifest.

Supported `bin` forms are:

- a string, such as `"bin": "./main.js"`
- an object, such as `"bin": { "demo": "./bin/demo.js" }`

If `bin` is a string, `pkg` derives the wrapper name from the package name.
For example, `github.com/acme/demo` produces `demo.js`.
If `bin` is an object, each key becomes a wrapper name.
Wrapper names must contain only letters, digits, `.`, `_`, or `-`.

For example, this installed package manifest:

```json
{
  "name": "github.com/acme/demo",
  "bin": {
    "demo": "./bin/demo.js"
  }
}
```

creates `node_modules/.bin/demo.js`. The generated wrapper changes the working directory to the installed package directory and executes the configured `bin` target.

The `bin` target should therefore be a path that is valid from the installed package root.
Any extra arguments given to the wrapper are passed to that target unchanged.

### Running generated `.bin` wrappers

`pkg run` does not execute installed package `bin` wrappers.
`pkg run` is only for the current project's `package.json` `scripts`.

The shell environment includes `/work/node_modules/.bin` and `./node_modules/.bin` in `PATH`.
This means installed package executables can normally be invoked by name.

To use an installed package executable, run the generated wrapper from the shell environment.
Examples:

```sh
/work > demo.js --help
/work > demo.js import sample.csv
```

You can still run the wrapper by path when needed.

```sh
/work > ./node_modules/.bin/demo.js --help
```

If the same wrapper name already exists, installation keeps going, prints a warning, and skips only that conflicting wrapper.
This means the package itself is still installed, but that specific executable name is not generated.

If the conflicting file was created by another installed package, the warning includes the owner package name.
If the conflicting file already existed without `pkg` ownership metadata, the warning reports it as an existing wrapper.

### Lock file behavior

`pkg` writes `package-lock.json` and stores the resolved source for reproducible installs.
For GitHub packages, the resolved source includes whether the install used a tag or a branch.

Examples:

- `github.com/acme/demo#tag=v1.1.0`
- `github.com/acme/notags#branch=main`

When a lock file is present, `pkg install` reuses the locked GitHub ref instead of resolving a new one.

### Error reporting

If `pkg` cannot determine a GitHub ref, it reports both resolution steps.
For example, it can report a tags lookup failure together with a default branch lookup failure.

## pkg run

Runs a named entry from `package.json` `scripts`.

<h6>Syntax</h6>

```sh
pkg run [options] <key> [...args]
```

<h6>Options</h6>

- `-C, --dir <dir>` use the given project directory instead of the current working directory
- `-h, --help` show help

`pkg run` changes the current working directory to the selected project directory before executing the script.
This means relative command paths such as `./main.js` are resolved from the package directory.

<h6>Usage example</h6>

Given this manifest:

```json
{
  "scripts": {
    "start": "./main.js --mode prod"
  }
}
```

Run it with:

```sh
/work > pkg run start
```

Extra arguments are appended after the script command line.

```sh
/work > pkg run start --verbose
```

The effective command line becomes:

```sh
./main.js --mode prod --verbose
```

## pkg uninstall

Removes a dependency together with its generated wrappers.

<h6>Syntax</h6>

```sh
pkg uninstall [options] <name>
```

<h6>Options</h6>

- `-C, --dir <dir>` use the given project directory instead of the current working directory
- `-h, --help` show help

`pkg uninstall` removes these items when they are managed by `pkg`:

- the dependency entry in `package.json`
- wrappers in `node_modules/.bin` that belong to the installed package
- the installed package directory
- `package-lock.json` when no dependencies remain

To remove a package that was installed with `pkg install -g`, use `pkg uninstall -g`.

```sh
/work > pkg uninstall -g github.com/acme/demo
Removed github.com/acme/demo
```

If a wrapper was skipped during install because of a collision, there may be no wrapper to remove.
Likewise, `pkg uninstall` does not remove user-created files in `node_modules/.bin` that are not managed by `pkg`.

<h6>Usage example</h6>

```sh
/work > pkg uninstall github.com/acme/demo
Removed github.com/acme/demo
```

## Typical workflow

```sh
/work > pkg init demo-app
/work > pkg install github.com/acme/demo
/work > pkg install generic-pkg
/work > pkg run start
```

## Notes

- `pkg` expects a valid `package.json` for `install` without an explicit package name and for `run`.
- `pkg run` executes the script line through JSH command resolution, not through a POSIX shell.
- Relative script commands such as `./tool.js` are recommended for project-local executables.
- For package authors, prefer relative `bin` targets such as `./bin/demo.js` so the generated wrapper can execute them from the installed package directory.
- For package authors, use object-form `bin` when you need explicit executable names, and string-form `bin` when the package name itself should become the executable name.
- GitHub repository installs require the downloaded repository contents to include a valid `package.json`.

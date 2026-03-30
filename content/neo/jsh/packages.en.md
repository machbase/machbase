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

## package.json

A minimal package manifest looks like this.

```json
{
  "name": "demo-app",
  "version": "1.0.0",
  "scripts": {
    "start": "./main.js"
  },
  "dependencies": {
    "generic-pkg": "^1.2.0",
    "github.com/acme/demo": "v1.1.0"
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
| `neo.installType` | `String` | Optional install behavior hint for GitHub repository packages |

`pkg` recognizes this custom metadata for GitHub repository installs:

```json
{
  "neo": {
    "installType": "application"
  }
}
```

If `neo.installType` is set to `application`, `pkg install github.com/<org>/<repo>` treats the downloaded repository as an application project instead of a library dependency.

## pkg init

Creates a new `package.json` in the current project directory.

<h6>Syntax</h6>

```sh
pkg init [options] <name>
```

<h6>Options</h6>

- `-C, --dir <dir>` use the given project directory instead of the current working directory
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
- `-h, --help` show help

If `name` is omitted, `pkg install` installs the dependencies already declared in `package.json`.

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

Behavior:

- If `@<tag>` is specified, that tag is used.
- If no tag is specified and the repository has tags, the latest tag returned by the GitHub tags API is used.
- If no tag is specified and the repository has no tags, the repository `default_branch` is used.

<h6>Usage example: latest tag</h6>

```sh
/work > pkg install github.com/acme/demo
Installed github.com/acme/demo@v1.1.0
```

<h6>Usage example: explicit tag</h6>

```sh
/work > pkg install github.com/acme/demo@v1.0.0
Installed github.com/acme/demo@v1.0.0
```

<h6>Usage example: default branch fallback</h6>

If the repository has no tags, the default branch is used.

```sh
/work > pkg install github.com/acme/notags
Installed github.com/acme/notags@main
```

### Installation target

Installed packages are copied into the project `node_modules` directory.
For example:

- `generic-pkg` -> `node_modules/generic-pkg`
- `github.com/acme/demo` -> `node_modules/github.com/acme/demo`

GitHub repository packages can override this behavior with manifest metadata.
If the downloaded `package.json` contains `neo.installType: "application"`, `pkg` installs the repository into the selected target directory itself instead of `node_modules`.

In that case:

- the repository files become the target project files
- the downloaded `package.json` becomes the target project's `package.json`
- only the application's dependencies are installed into the target project's `node_modules`

This is useful for application templates or starter projects that should become the working project directory after installation.

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
- GitHub repository installs require the downloaded repository contents to include a valid `package.json`.

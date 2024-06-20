---
title: Custom shell in web-ui
type: docs
weight: 22
---

User can customize command line shell and open it in the web ui.

Open a *SHELL* on the web ui or run `machbase-neo shell` on the terminal, and use `shell` command to add/remove custom shell.

In this example, we are going to show how to add a user-defined shell that invokes `/bin/bash` (or `/bin/zsh`) for *nix users and `cmd.exe` for Windows users. You may add any programming language's REPL, other database's command line interface and ssh command that connects to your servers for example.

## Add a custom shell

### Register a custom shell

1. Select the <img src="../img/shell_icon.jpg" width=47 style="display:inline"> menu icon from the left most side.

2. And Click `+` icon <img src="../img/shell_add_icon.jpg" width=265 style="display:inline"> from the top left pane.

3. Set a preferred "Display name" and provide the absolute path and flags for the "Command" field.
For example, to set 'zsh' as the command line on macOS, use the absolute path of your program and click "Save".

{{< figure src="../img/shell_add_form.jpg" width="684px">}}

- Name: display name. (Any valid text is possible except some reserved words that machbase-neo reserves for the future use)
- Command: any executable command in full path with arguments
- Theme : terminal color theme

Any terminal program can be the custome "Command", for example...
- Windows Cmd.exe: `C:\Windows\System32\cmd.exe`
- Linux bash: `/bin/bash`
- PostgreSQL Client on macOS: `/opt/homebrew/bin/psql postgres`

### Use the custom shell

- Open the custom shell on the main editor area.

{{< figure src="/images/web-custom-shell.jpeg" width="600px">}}

- Open the custom shell on the console area.

{{< figure src="../img/web-custom-shell-console.jpg" width="700px">}}

## Command line

The custom shells are manageably with machbase-neo shell command line interface.

### Add new custom shell

Use `shell add <name> <command and args>`. You can give a any name and any executable command with arguments, but the default shell name `SHELL` is reserved.

```sh
machbase-neo» shell add bashterm /bin/bash;
added
```

```sh
machbase-neo» shell add terminal /bin/zsh -il;
added
```

```sh
machbase-neo» shell add console C:\Windows\System32\cmd.exe;
added
```

### Show registered shell list

```sh
machbase-neo» shell list;
┌────────┬────────────────────────────┬────────────┬──────────────┐
│ ROWNUM │ ID                         │ NAME       │ COMMAND      │
├────────┼────────────────────────────┼────────────┼──────────────┤
│      1 │ 11F4AFFD-2A9B-4FC5-BB20-637│ BASHTERM   │ /bin/bash    │
│      2 │ 11F4AFFD-2A9B-4FC5-BB20-638│ TERMINAL   │ /bin/zsh -il │
└────────┴────────────────────────────┴────────────┴──────────────┘
```


### Delete a custom shell

```sh
machbase-neo» shell del 11F4AFFD-2A9B-4FC5-BB20-637;
deleted
```



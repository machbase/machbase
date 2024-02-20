---
title: Custom shell in web-ui
type: docs
weight: 22
---

User can customize command line shell and open it in the web ui.

Open a *SHELL* on the web ui or run `machbase-neo shell` on the terminal, and use `shell` command to add/remove custom shell.

In this example, we are going to show how to add a user-defined shell that invokes `/bin/bash` (or `/bin/zsh`) for *nix users and `cmd.exe` for Windows users. You may add any programming language's REPL, other database's command line interface and ssh command that connects to your servers for example.

## Add a user-defined shell

On web ui the "SHELL" menu has a special small icon on its top right corner. Click it and it shows "Make a copy" menu.

{{< figure src="/images/shell-make-copy.jpg" width="204px" >}}

Then it makes a new copy in name of "CUSTOM SHELL". Any copy of "SHELL" has "Edit..." and "Remove" menu.

{{< figure src="/images/shell-custom.jpg" width="204px" >}}

Click "Edit..." and make some changes.

- Name: display name. (Any valid text is possible except some reserved words that machbase-neo reserves for the future use)
- Command: any executable command in full path with arguments
- Theme : terminal color theme

{{< tabs items="cmd.exe,bash,PostgreSQL" >}}
{{< tab >}}
{{< figure src="../img/shell-custom-cmd.jpg" width="400px">}}
{{< /tab >}}
{{< tab >}}
{{< figure src="/images/shell-edit.jpg" width="400px">}}
{{< /tab >}}
{{< tab >}}
{{< figure src="../img/shell-custom-psql.jpg" width="400px">}}
{{< /tab >}}
{{< /tabs >}}

### CLI

The custom shells are managable with machbase-neo shell command line interface.

#### Add new custom shell

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

{{< figure src="/images/web-custom-shell.jpeg" width="600px">}}

#### Show registered shell list

```sh
machbase-neo» shell list;
┌────────┬────────────────────────────┬────────────┬──────────────┐
│ ROWNUM │ ID                         │ NAME       │ COMMAND      │
├────────┼────────────────────────────┼────────────┼──────────────┤
│      1 │ 11F4AFFD-2A9B-4FC5-BB20-637│ BASHTERM   │ /bin/bash    │
│      2 │ 11F4AFFD-2A9B-4FC5-BB20-638│ TERMINAL   │ /bin/zsh -il │
└────────┴────────────────────────────┴────────────┴──────────────┘
```


#### Delete a custom shell

```sh
machbase-neo» shell del 11F4AFFD-2A9B-4FC5-BB20-637;
deleted
```



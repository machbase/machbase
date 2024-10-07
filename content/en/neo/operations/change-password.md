---
title: Change password
type: docs
weight: 12
---

Change default password for the security before allowing remote access.

### Web UI

1. Select "Change password" menu from the left bottom menu. {{< neo_since ver="8.0.20" />}}

{{< figure src="../img/change_passwd_ui.jpg" width="203px" >}}

2. Enter the new password and re-type for confirmation on the dialog.

{{< figure src="../img/change_passwd_ui2.jpg" width="342px" >}}

### SQL

{{< figure src="../img/change_passwd.jpg" width="800px" >}}

```sql
ALTER USER sys IDENTIFIED BY new_password;
```

### Command line

```sh
machbase-neo shell "ALTER USER SYS IDENTIFIED BY new_password"
```

{{< callout type="info" emoji="❗️">}}
**Escape from OS shell**<br/>
When execute SQL statement in non-interactive mode on command line like above example,
OS shell's special characters should be escaped.
For example, if we execute `machbase-neo shell select * from table` without quotation rks.
'*' will be interpreted by bash (or zsh) as 'all files'.
`\`, `!`, `$` and quotation marks should be carefully used for the same reason.
<br/>
Or we can execute command in neo-shell interactive mode.
Execute `machbase-neo shell` then it will show prompt `machbase-neo >>`.
In interactive mode with machbase-neo prompt, no more shell escaping is required.
{{< /callout >}}

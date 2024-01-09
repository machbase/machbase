---
title: Change password
type: docs
weight: 11
---

Change default password for the security before allowing remote access.

```sh
machbase-neo shell "ALTER USER SYS IDENTIFIED BY my_password"
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
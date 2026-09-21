---
title: SHELL
type: docs
weight: 21
---

## Remote Access via Web

1. Select <img src="/neo/shell/img/shell_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> `SHELL` on the new tab screen.

{{< figure src="/images/web-shell-pick.png" width="600px" >}}

2. The shell opens in the main editor area. Run SQL statements and machbase-neo shell commands at the `sys machbase-neo` prompt.

{{< figure src="/images/web-shell-ui.png" width="700px" >}}

## Remote Access via SSH

SSH (Secure Shell) is a protocol used to securely log onto remote systems.
It can use a password for authentication, but it also supports a more secure method called public key authentication.

machbase-neo provides an SSH interface for remote operation and administration.
Users can access the SQL interpreter by using the SSH command as shown below.

- User: SYS
- Default password: manager
- Default port: 5652

```sh
$ ssh -p 5652 sys@127.0.0.1
sys@127.0.0.1's password: manager↵
```

Then after `machbase-neo» ` prompt, users can query with SQL statements.

```
machbase-neo» select * from example;
┌─────────┬──────────┬─────────────────────────┬───────────┐
│ ROWNUM  │ NAME     │ TIME(UTC)               │ VALUE     │
├─────────┼──────────┼─────────────────────────┼───────────┤
│       1 │ wave.sin │ 2023-01-31 03:58:02.751 │ 0.913716  │
│       2 │ wave.cos │ 2023-01-31 03:58:02.751 │ 0.406354  │
                        ...omit...
│      13 │ wave.sin │ 2023-01-31 03:58:05.751 │ 0.668819  │
│      14 │ wave.cos │ 2023-01-31 03:58:05.751 │ -0.743425 │
└─────────┴──────────┴─────────────────────────┴───────────┘
```

### SSH without password

1. **Generate a key pair**: The first step is to generate a new key pair on the local machine (the machine you will log in from). 
   This is done using the `ssh-keygen` command.

    > You can skep this step, if you have already a key pair.


    ```bash
    ssh-keygen -t rsa
    ```

    This command will create two files in the .ssh directory in your home directory: `id_rsa` (private key) and `id_rsa.pub` (public key).

2. **Copy the public key to the remote machine**: The next step is to copy the public key to the remote machine.

    To register the public key into the machbase server, follow the steps below.

3. **Log in with the key pair**: Now you can log in to the machbase server using your key pair.
The SSH client will automatically use your private key to decrypt a challenge sent by the server, proving your identity.

    ```bash
    ssh -p 5652 sys@127.0.0.1
    ```

    If everything is set up correctly, you should be logged in to the machbase-neo without being asked for a password.

#### Register ssh key from Web UI

1. Click the <img src="/neo/shell/img/settings_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px"> icon at the bottom of the left menu and select `SSH Keys`. {{< neo_since ver="8.0.20" />}}

{{< figure src="/neo/shell/img/ssh_keys.jpg" width="200px" >}}

2. Click `New SSH key`, give the key a name in `Title`, paste the whole public key into `Public Key`, then click `Add SSH key`.

{{< figure src="/neo/shell/img/ssh_keys2.jpg" width="590px" >}}

3. The registered key appears in the `Authentication Keys` list. Use `Delete` to remove a key you no longer use.

{{< figure src="/neo/shell/img/ssh_keys3.jpg" width="600px" >}}

#### Register ssh key from shell command

Adding the public key to the machbase-neo server enables the execution of any `machbase-neo shell` command without the need for a prompt or password entry.

1. Add your public key to server

```sh
machbase-neo shell ssh-key add `cat ~/.ssh/id_rsa.pub`
```

2. Get list of registered public keys

```sh
machbase-neo shell ssh-key list
```

or

```
$ machbase-neo shell ↵

machbase-neo» ssh-key list
┌────────┬───────────────────────────────────────────┬─────────────────────┬────────────────────────────────────────────────────┐
│ ROWNUM │ NAME                                      │ KEY TYPE            │ FINGERPRINT                                        │
├────────┼───────────────────────────────────────────┼─────────────────────┼────────────────────────────────────────────────────┤
│      1 │ **DO NOT DELETE** machbase-neo server key │ ecdsa-sha2-nistp521 │ SHA256:osfeJKNiUV+a2bIdZPA92maMDI23xA/40gAFwqAfpyQ │
│      2 │ myid@laptop.local                         │ ecdsa-sha2-nistp256 │ SHA256:0IFv6KPDuNJe2s9PoqUBimreYAYih3sDKcxpCYpZCmE │
└────────┴───────────────────────────────────────────┴─────────────────────┴────────────────────────────────────────────────────┘
```

3. Remove registered public key

```sh
machbase-neo» ssh-key del <fingerprint>
SSH key deleted successfully.
```

#### Connect without password

```sh
$ ssh -p 5652 sys@127.0.0.1 ↵

Greetings, SYS
machbase-neo v8.7.1-snapshot (b55f8170 2026-09-10T05:43:13) standard
sys machbase-neo 2026-09-17 17:45:13
> 
```

### Execute commands via SSH

We can execute any machbase-neo shell command remotely only with `ssh`.

```sh
$ ssh -p 5652 sys@127.0.0.1 'select * from example order by time desc limit 5'↵

┌────────┬────────┬─────────────────────────┬───────────┐
│ ROWNUM │ NAME   │ TIME                    │     VALUE │
├────────┼────────┼─────────────────────────┼───────────┤
│      1 │ signal │ 2026-09-17 17:09:26.712 │ -0.033411 │
│      2 │ signal │ 2026-09-17 17:09:26.711 │ -0.185026 │
│      3 │ signal │ 2026-09-17 17:09:26.71  │ -0.344666 │
│      4 │ signal │ 2026-09-17 17:09:26.709 │ -0.508032 │
│      5 │ signal │ 2026-09-17 17:09:26.708 │ -0.670817 │
└────────┴────────┴─────────────────────────┴───────────┘
5 rows selected.
```

### Security Considerations

While public key authentication is more secure than password authentication,
it is important to keep your private key safe. Anyone who gains access to 
your private key can log in to any system that has your public key.


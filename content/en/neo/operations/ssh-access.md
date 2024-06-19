---
title: Remote access with SSH
type: docs
weight: 13
---

machbase-neo supports ssh interface for the remote operation and administration.
Users can access the sql interpreter via ssh command like below.

## SSH from remote hosts

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

## SSH without password

### Register ssh key from Web UI

1. Select "SSH Keys" menu from the left bottom menu. {{< neo_since ver="8.0.20" />}}

{{< figure src="../img/ssh_keys.jpg" width="207px" >}}

2. Click "New SSH Key" button. Paste your public key and write any title. The press "Add SSH Key"

{{< figure src="../img/ssh_keys2.jpg" width="630px" >}}

3. Your SSH key has been registered in the list.

{{< figure src="../img/ssh_keys3.jpg" width="630px" >}}


### Register ssh key from shell command
Adding the public key to machbase-neo server makes it possible to execute any `machbase-neo shell` command without prompt and entering password.

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
┌────────┬────────────────────────────┬─────────────────────┬──────────────────────────────────┐
│ ROWNUM │ NAME                       │ KEY TYPE            │ FINGERPRINT                      │
├────────┼────────────────────────────┼─────────────────────┼──────────────────────────────────┤
│      1 │ myid@laptop.local          │ ssh-rsa             │ 80bdaba07591276d065ca915a6037fde │
│      2 │ myid@desktop.local         │ ecdsa-sha2-nistp256 │ e300ee460b890ad4c22cd4c1eae03477 │
└────────┴────────────────────────────┴─────────────────────┴──────────────────────────────────┘
```

3. Remove registered public key

```sh
machbase-neo» ssh-key del <fingerprint>
```

## Connect without password

```sh
$ ssh -p 5652 sys@127.0.0.1 ↵

Greetings, SYS
machbase-neo v8.0.20-snapshot (8f10fa95 2024-06-19T16:32:09) standard
sys machbase-neo»
```

## Execute commands via SSH

We can execute any machbase-neo shell command remotely only with `ssh`.

```sh
$ ssh -p 5652 sys@127.0.0.1 'select * from example order by time desc limit 5'↵

 ROWNUM  NAME      TIME(UTC)            VALUE     
──────────────────────────────────────────────────
 1       wave.sin  2023-02-09 11:46:46  0.406479  
 2       wave.cos  2023-02-09 11:46:46  0.913660  
 3       wave.sin  2023-02-09 11:46:45  -0.000281 
 4       wave.cos  2023-02-09 11:46:45  1.000000  
 5       wave.cos  2023-02-09 11:46:44  0.913431  
```

---
type: docs
title: '17.1.1.20 USER/AUTH syntax'
weight: 200
toc: true
---

## DROP USER and active sessions

Dropping a user from another administrator session does not immediately disconnect an existing
session. New connections fail, while the existing session retains the user name and ID captured at
login. See [Account management](../../../../security-access-control/account/) and
[User context functions](../../dictionary/functions-full/#current-session-user).

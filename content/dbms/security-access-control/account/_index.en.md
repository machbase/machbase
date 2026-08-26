---
type: docs
title: '14.2 계정 관리'
weight: 20
toc: true
---



<a id="create-delete-user"></a>

## 사용자 생성과 삭제

<a id="drop-user-active-session"></a>

### Dropping a user with an active session

Dropping a user from another administrator session does not immediately disconnect sessions that
already authenticated as that user. Existing sessions retain the user name and internal ID captured
at login, but new connections fail and the user disappears from `M$SYS_USERS`. Check and close active
application sessions before dropping the account.

Starting with Machbase 8.7.0, use
[CURRENT_USER and SESSION_USER](../../reference/sql/dictionary/functions-full/#current-session-user)
to inspect the context retained by an existing session.

<a id="policy-password"></a>

## 비밀번호 정책

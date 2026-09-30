---
title : 'Insufficient Memory'
type: docs
weight: 100
---

This section describes how to change properties when an insufficient memory error occurs while executing a query.

## An error occurred due to insufficient memory when executing the query

The memory available for executing a query is limited for the following reason.

If a specific query uses too much memory, other queries running at the same time may fail to execute due to insufficient memory.

You can resolve the insufficient memory error by increasing the property value for the maximum memory that one query can use.

The `MAX_QPX_MEM` property manages the maximum memory that one SQL statement can use.

For how to set it at runtime, and for the error messages and TRC messages caused by insufficient memory, see [SET MAX_QPX_MEM](../../sql-reference/sys-session-manage/#set-max_qpx_mem).

A value set with the `SET` command is not kept after Machbase restarts, so modify the `machbase.conf` file as well, as follows.

**Standard Edition**

Change `MAX_QPX_MEM` in `machbase.conf` to a larger value.

**Cluster Edition**

Same as Standard Edition. However, `machbase.conf` must be modified on all cluster nodes.

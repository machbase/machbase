---
type: docs
title: '16.8.10 operations-checklist'
weight: 100
toc: true
---

Base operational responses on the procedures in
[Operations, Configuration, and Recovery](/dbms/operations-configuration-recovery/)
and apply the following safety sequence.

1. Identify symptoms, occurrence time, complete errors, and target databases/nodes/tables.
2. Inspect current state read-only with `machadmin -e`, relevant `V$` views, and logs.
3. Distinguish normal operation from failure and provide evidence that a change is needed.
4. Specify change targets, impact, downtime, rollback, and success criteria.
5. Check the user's authorization scope, execute one step at a time, and verify results.

Do not automatically suggest server restarts, session termination, data deletion, configuration
changes, backup restoration, or cluster node changes as diagnostic commands. Verify commands and SQL
in the relevant [operations chapter](/dbms/operations-configuration-recovery/).

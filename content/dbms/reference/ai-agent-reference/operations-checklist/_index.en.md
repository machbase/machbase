---
type: docs
title: '17.8.10 operations-checklist'
weight: 100
toc: true
---

Use the [Operations checklist](/dbms/operations-configuration-recovery/checklist/) as
the canonical source and apply this safety order:

1. Identify the symptom, time, complete error, and target database, node, or table.
2. Inspect current state with read-only status, catalog, and log checks.
3. Distinguish normal activity from failure and state why a change is required.
4. Document target, impact, downtime, rollback, and success conditions.
5. Confirm authorization, execute one step, and verify the result.

Do not treat restart, session termination, deletion, configuration mutation, recovery,
or cluster node changes as diagnostic commands. Verify procedures in
[Operations, configuration, and recovery](/dbms/operations-configuration-recovery/).

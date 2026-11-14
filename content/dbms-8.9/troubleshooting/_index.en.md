---
type: docs
title: '15. Troubleshooting'
weight: 150
toc: true
---

This chapter addresses operational problems in Machbase through symptom identification,
diagnosis, resolution, and prevention.

{{< callout type="info" >}}
Before classifying a problem, check server status with `machadmin -e`. Record recent errors
from `$MACHBASE_HOME/trc/machbase.trc` and the client's `ERR-XXXXX` code.
{{< /callout >}}

## Chapter contents

| Order | Section | Content |
|-----:|------|------|
| 15.1 | [Troubleshooting Approach](./troubleshooting/) | Symptom collection, diagnostic commands, log and error code analysis |
| 15.2 | [Server and Connection Problems](./server-connection/) | Server startup, remote access, authentication errors |
| 15.3 | [Ingestion and Loading Problems](./item/) | Append and CSV import errors |
| 15.4 | [Query and Performance Problems](./performance/) | Slow queries, empty results, memory, transaction conflicts |
| 15.5 | [Backup and Recovery Problems](./recovery-backup/) | BACKUP, RESTORE, MOUNT, and UMOUNT errors |
| 15.6 | [Cluster Problems](./cluster/) | Node state and Cluster Edition errors |
| 15.7 | [ROLLUP Problems](./rollup/) | Aggregation lag, result differences, and rebuild decisions |

For TAG and LOOKUP UPDATE/DELETE predicate errors, see the constraints and troubleshooting
page in the relevant table chapter.

After resolving a problem, record the cause, corrective action, verification queries, and
prevention measures in the operations log.

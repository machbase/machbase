---
type: docs
title: '11.5.5 Append API'
weight: 50
toc: true
---

JDBC Append is a separate high-volume input lifecycle, not a batch of ordinary SQL INSERT calls.

1. Open the target table with the supported `MachStatement` Append method.
2. Match every value to the target column order and type.
3. Send rows and consume per-row or callback errors.
4. Flush when the application requires an acknowledgement boundary.
5. Close the Append handle and verify success and failure counts.

Keep Append and query connections separate. Do not assume Append participates in a TRANSACTION-table
rollback. Use the exact method signatures in the deployed JDBC driver and test reconnect and duplicate
handling with representative data.

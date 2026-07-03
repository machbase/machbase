---
type: docs
title: '10-Minute Quick Start'
weight: 20
toc: true
---

The quick start is a short test run. Just as you power on new equipment and check the
controls before using it in production, this page verifies create, insert, query, and
cleanup in one `machsql` run. Machbase's focus on industrial IoT and financial tick
data also starts from this same basic SQL workflow. Start with a LOG table to confirm
the SQL workflow, then preview TAG table behavior from the next-document page.

In production, this flow repeats very quickly: a collector receives data, writes it to
the DBMS, and users query recent values or aggregate them by time interval. The quick
start reduces that entire loop to the smallest useful example.

## Prerequisites

- Machbase DBMS server: `127.0.0.1:5656`
- User: `SYS`
- Password: `MANAGER`
- Client: `machsql`

## Quick Start Sample

This sample records one event saying that a service has started. A LOG table is the
basic container for events that keep arriving over time, such as equipment events,
collector status records, or tick receive histories.

```sql
CREATE TABLE DBMS_GS_QUICK (
  EVENT_ID INTEGER,
  MESSAGE VARCHAR(40)
);

INSERT INTO DBMS_GS_QUICK VALUES (1, 'service started');

SELECT EVENT_ID, MESSAGE FROM DBMS_GS_QUICK;

DROP TABLE DBMS_GS_QUICK;
```

Assuming the SQL above is saved as `/tmp/dbms_gs_quick.sql`, run the following command.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_quick.sql
```

If `service started` is printed, the basic SQL workflow is working.
If a rerun fails because `DBMS_GS_QUICK` already exists, run
`DROP TABLE DBMS_GS_QUICK;` and start again.

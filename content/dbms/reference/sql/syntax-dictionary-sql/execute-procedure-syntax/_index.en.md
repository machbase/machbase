---
type: docs
title: '17.1.1.24 EXEC Procedures and ROLLUPGAP'
weight: 240
toc: true
---

Reference for public table and ROLLUP procedures.

<a id="table-flush"></a>
<a id="index-flush"></a>
<a id="table-refresh"></a>
<a id="freeze-tag-index"></a>
<a id="rollup-start-stop"></a>
<a id="rollup-force"></a>
<a id="rollup-rebuild"></a>
<a id="show-rollupgap"></a>

| Procedure | Forms | Scope |
|---|---|---|
| `TABLE_FLUSH` | `EXEC TABLE_FLUSH(table)` | Flush pending table input |
| `INDEX_FLUSH` | `EXEC INDEX_FLUSH(table [, index])` | Wait for index build completion |
| `TABLE_REFRESH` | `EXEC TABLE_REFRESH(lookup)` | Reload a LOOKUP runtime table |
| `FREEZE_TAG_INDEX` | `EXEC FREEZE_TAG_INDEX(tag_table)` | Freeze a TAG index |
| `UNFREEZE_TAG_INDEX` | `EXEC UNFREEZE_TAG_INDEX(tag_table)` | Unfreeze a TAG index |
| `ROLLUP_START` | 0 or 1 rollup-name argument | Start current-user or named ROLLUP work |
| `ROLLUP_STOP` | 0 or 1 rollup-name argument | Stop current-user or named ROLLUP work |
| `ROLLUP_FORCE` | 0 or 1 rollup-name argument | Process a default chain or wait for a named ROLLUP |
| `ROLLUP_REBUILD` | 4 arguments | Rebuild a Standard Edition TAG range |

`SHOW ROLLUPGAP` is a machsql client command, not server SQL. It reports source and ROLLUP END_RID,
their gap, state, and timing; Cluster output also includes `HOSTNAME`.

See [ROLLUP_REBUILD](../rollup-rebuild-syntax/) and
[V$ROLLUP](/dbms/reference/log-logs-system-catalog/dictionary-vrollup/) for detailed contracts.

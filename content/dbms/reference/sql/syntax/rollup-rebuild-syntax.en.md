---
type: docs
title: 'ROLLUP_REBUILD'
weight: 190
toc: true
---

ROLLUP_REBUILD is a Standard Edition procedure that recalculates historical buckets for supported
TAG aggregates. It is unavailable in Cluster Edition.

## Syntax and Arguments

```text
EXEC ROLLUP_REBUILD(source_tag, tag_name, begin_time, end_time);
```

| Argument | Current Input |
|---|---|
| source_tag | Source TAG identifier, owner-qualified if needed |
| tag_name | String naming one tag to rebuild |
| begin_time | Time string or TO_DATE with constant string arguments |
| end_time | End timestamp in the same form; must be at least begin_time |

Current time argument handling does not evaluate general DATETIME expressions. Do not use NOW,
NOW-1h, columns, or bind parameters in examples. For relative ranges, resolve timestamps in an
operational tool and pass supported constants. Specify date strings, formats, and timezones clearly.

## Time Range

Includes the buckets containing both endpoints and recalculates entire buckets. At one-minute
resolution, 00:00:30–00:01:00 covers [00:00:00, 00:02:00).
Equal start/end rebuilds the containing bucket; start greater than end is an error.
The HOUR level can expand the range further to whole hour buckets.

Passing the upper bound of a half-open source WHERE range directly may include the next bucket.
Determine impact from the actual corrected timestamps and each aggregate's bucket boundaries.

## Targets and Constraints

- Use a complete automatic SEC→MIN→HOUR hierarchy as the basic exercise target.
- Do not assume the same path handles manually named ordinary ROLLUPs or automatic hierarchies
  missing SEC.
- Custom trees use a separate path. Current time-boundary generation supports 1 SEC, 1 MIN, and
  1 HOUR. Other creatable intervals, such as 10 MIN, do not imply rebuild support.
- Custom SELECT buckets and origin must match rebuild boundaries.
- A nonexistent tag may be a no-op when a valid target exists.
- If source data has been removed, statistics from before deletion cannot be restored.

## Example

The following call assumes the ch6_rebuild exercise objects are prepared.

```sql
EXEC ROLLUP_REBUILD(ch6_rebuild, 'S1',
    TO_DATE('2026-01-01 00:00:30', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'));
```

Setup SQL, source corrections, ordinary/Custom result comparison, and cleanup are provided in
[6.10 Complete Exercise](/dbms/tag-rollup-usage/rollup-rebuild/).

## Job State and Failures

Related jobs pass through stop, recalculate, and restart stages. Normal aggregation is not
 guaranteed to continue unchanged during rebuilding. Test source-read stabilization and data
regeneration impact in an isolated environment.

A failure may leave some results changed. Do not assume complete rollback or automatic restoration
of an originally stopped state. Check source data, target buckets, V$ROLLUP, gaps, and the first error.
Do not repeat the command before excluding unsupported jobs or correcting the procedure.

Also check [Creation/Query Syntax](../rollup-syntax/),
[Support Scope](/dbms/reference/support-scope-constraints/rollup/),
and [Troubleshooting](/dbms/troubleshooting/rollup/).

---
type: docs
title: '16.2.4 Timezone Configuration Dictionary'
weight: 50
toc: true
---

Machbase supports a timezone option for client connections. Internally, datetime values are
processed as nanosecond values; the timezone option affects conversion to and from strings.

## Supported Timezone Format

| Format | Example | Description |
|------|------|------|
| UTC offset | `+0900`, `-0530` | Hour and minute offset from UTC |

The format documented in the original 8.5 manual and current `machsql` and `machloader` help is
an offset in `+-HHMM` format. IANA region names such as `Asia/Seoul` and the
`DEFAULT_TIMEZONE` server property have not been verified in the current distribution samples,
so this chapter does not list them as supported formats.

## Client Timezone Settings

### machsql

Use `-z` to set the session timezone.

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -z +0900
```

### machloader

Use `-z` to set the timezone for datetime conversion during import and export.

```bash
machloader -i -d data.csv -t table_name -z +0900
machloader -o -d data.csv -t table_name -z +0900
```

### JDBC

For JDBC timezone settings, check the connection options in the driver documentation.
This page describes the `+-HHMM` offset format used by `machsql` and `machloader`.

## Timezone Precedence

An explicit client timezone, such as `-z +0900`, applies to input and output conversion in that session.

## Timezone Conversion Example

Connect as follows to use the `+0900` timezone.

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -z +0900
```

---
type: docs
title: '16.1.3 Function Dictionary'
weight: 30
toc: true
---

Built-in functions organized by category.

| Category | Description |
|----------|------|
| [Aggregate Functions](aggregation/) | Group aggregates such as COUNT, SUM, AVG, MIN, MAX, STDDEV, FIRST, and LAST |
| [Window/Series Functions](series/) | Window and series analysis functions such as ROWNUM and SERIESNUM |
| [Date/Time Functions](datetime/) | Date/time processing with TO_DATE, TO_CHAR, DATE_TRUNC, ADD_TIME, and others |
| [JSON Functions and Dot Notation](operators-json/) | JSON extraction, modification, and member access |
| [Regular Expression Functions](regex/) | Regex search and transformation with REGEXP_LIKE, REGEXP_SUBSTR, and others |
| [NEXTVAL](nextval/) | Automatic sequence values for Lookup table sequence columns |
| [User Context Functions](functions-full/#current-session-user) | CURRENT_USER, SESSION_USER, and internal user IDs |
| [Complete Function Reference](functions-full/) | Complete reference, including existing functions and CAST |

## Common Rules

- NULL input produces NULL output unless otherwise stated.
- Argument type mismatches produce `ERR-02036` or `ERR-02037`.

---
title: '5.1 Overview and Use Criteria'
weight: 10
toc: true
---

Consider TAG when recording repeated observations of subjects such as sensors or equipment.
Distinguish one tag from one observation row: many timestamps can share a tag name, and sharing
a name alone does not cause duplicate removal.

<a id="overview-tag-characteristics"></a>

## TAG Characteristics

`PRIMARY KEY` identifies the tag rather than requiring every measurement row to have a distinct
name. Select one time or distance axis.

```sql
CREATE TAG TABLE ch5_overview (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

The name is the first column and the axis is the second. If used, `SUMMARIZED` belongs on the
third column. It identifies a representative statistics/aggregation column; it does not by itself
create ROLLUP objects. See [Schema](../table-structure-schema/) for supported types and order.

| Area | Meaning |
|---|---|
| Tag name | Sensor or recurring observation subject |
| DATA | One observation: an axis value and data columns |
| METADATA | Current per-tag attributes such as location, unit, and settings |
| STAT | Statistics about input data, distinct from the DATA rows themselves |

<a id="overview-tag-use-criteria"></a>

## Usage Criteria

- Many subjects continuously add observations with the same schema.
- Queries commonly restrict a tag and a time/distance interval.
- Current metadata attributes select tags whose histories are analyzed.
- Time-axis data can use supported ROLLUPs for recurring interval statistics.

A single-value model uses tags for measurement channels. A multi-value model groups temperature,
pressure, and other values from the same observation. Do not combine readings with different
timestamps without defining missing-data and quality handling. Repeated timestamps can also result
from retries; define duplicate handling for names, axis values, and data.

<a id="overview-tag-not-use"></a>

## When to Consider Other Tables

| Requirement | Alternative to consider |
|---|---|
| Event-centric searches rather than recurring observation subjects | LOG |
| Persistent reference data with general predicate queries and changes | LOOKUP |
| Explicit transactions across DML and relational mutation | TRANSACTION in Standard Edition |
| Shared state that can be rebuilt from authoritative data | VOLATILE |

TAG supports JOIN and constrained value corrections. Neither “JOIN rules out TAG” nor “every
measurement must use TAG” is an appropriate selection rule.

<a id="overview-tag-design-flow"></a>

## Design Sequence

1. Decide whether a tag identifies a sensor, device, or inspection run.
2. Define the meaning and units of its measurement time or distance/position.
3. Choose value types, NULL and quality handling, and observation frequency.
4. Separate attributes retained with each observation from current METADATA.
5. Check query, aggregation, correction, and retention requirements against Edition support.

Inspect and remove the example table when finished:

```sql
DESC ch5_overview;
DROP TABLE ch5_overview;
```

Continue with [Schema Design](../table-structure-schema/) and
[Input Exercises](../data-input-mutation/).

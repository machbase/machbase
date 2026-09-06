---
type: docs
title: '2. Core Concepts'
weight: 20
toc: true
---

Chapter 1 introduced the SQL workflow for storing and reading data. This chapter explains that
workflow from a design and operations perspective. The appropriate table and storage strategy
depend on the meaning of time, how data changes, and which ranges you query.

For example, keeping a device's current temperature requires a different number of records
from keeping its temperature history for the past month. Calculating a monthly average and
detecting brief anomalies require different levels of detail. Understanding these differences
helps you choose tables, indexes, ROLLUP, and retention policies for their intended purposes.

## Contents

| Section | Questions it addresses |
|---|---|
| [Data Model Concepts](concepts/) | What does one row represent, and how should time, NULL, duplicates, and changes be interpreted? |
| [Storage and Execution Architecture](storage-execution-architecture/) | How is relevant data found, and which costs do storage, indexes, and caches reduce? |
| [Feature Concepts and Distinctions](features-concepts/) | What are the separate purposes of raw data, aggregates, retention, and backups? |
| [Edition Concepts](concepts-edition/) | When should you choose a single server or a distributed deployment, and which feature differences matter? |

The examples use small data sets to explain concepts. Follow the links in each section for
feature-specific SQL, support limits, and operational procedures. Then apply the concepts to your
own data in [Table Type Selection and Schema Design](../data-modeling-table-design/).

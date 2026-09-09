---
type: docs
title: '7. LOG Table Usage'
weight: 70
toc: true
---

Storing logs and finding the logs you need are different tasks. During incident analysis, questions
often arise that were overlooked during ingestion: does this timestamp represent occurrence or
collection, and why does a word in a message not appear in search results?

This chapter connects LOG table selection and design with ingestion, search, and retention
management. It explains both how to run commands and how to check their results. LOG uses a model
that continuously appends source events, so its usage differs from business tables whose stored rows
are repeatedly updated.

<a id="필요한-작업부터-찾아보세요"></a>

## Chapter Contents

If you are new to LOG tables, read the overview and schema sections, then follow creation,
ingestion, and querying in order. Start with 7.10 for time predicates or 7.11 for message search.

| Section | What you will learn |
|---|---|
| [7.1 Overview and Use Criteria](./overview-use-criteria/) | Distinguish LOG use cases from other table types |
| [7.2 Table Structure and Schema](./table-structure-schema/) | Separate event time, search fields, and raw messages |
| [7.3 Create, Alter, and Drop](./create-alter-drop/) | Change schemas while checking existing data |
| [7.4 Data Ingestion](./data-input-mutation/) | Choose INSERT, Append, or file loading |
| [7.5 Queries and Analysis](./query-analysis/) | Query time ranges and join reference data |
| [7.6 Indexes and Performance](./index-performance/) | Choose indexes and inspect execution plans |
| [7.7 Operations and Data Lifecycle](./operations-lifecycle/) | Check deletion boundaries and apply retention policies |
| [7.8 Constraints, Errors, and Troubleshooting](./constraints-errors-troubleshooting/) | Identify causes and remedies from symptoms |
| [7.9 Usage Patterns and Scenarios](./patterns-scenarios/) | Ingest, search, and aggregate application logs |
| [7.10 _arrival_time Time Model](./arrival-time-model/) | Distinguish automatic, explicit, and out-of-order timestamps |
| [7.11 Text Search and KEYWORD Indexes](./text-search-keyword-index/) | Understand how search methods affect results |
| [7.12 Network Type Queries](./regex-network-query/) | Query IPV4/IPV6 addresses and ranges |

<a id="실습-환경을-먼저-구분하세요"></a>

## Example Environment

The examples follow the DBMS 8.7 documentation. Unless stated otherwise, SQL exercises target a
Standard Edition validation environment. Use an account that can create tables and indexes. For
Cluster environments, also review
[Edition Differences](/dbms/reference/support-scope-constraints/edition/) and the relevant
operational procedures.

Example objects start with `ch7_`. Each section creates its own tables and can be followed
independently. Before rerunning a section, confirm that its final cleanup SQL was executed.
Intentionally failing SQL is separated from the normal exercise.

Caution: `DELETE`, `TRUNCATE`, and `DROP` remove data. Do not substitute production table names for
the example names.

If your results differ, compare the SQL you ran with its actual results. Identifying the first step
that differs helps narrow down the cause.

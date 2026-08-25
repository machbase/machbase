---
title: '8.4 Data Input and Mutation'
weight: 40
toc: true
aliases:
  - /dbms/rdb-table-usage/sdk-append-scope/
---
English structure placeholder. Korean content is authoritative for this restructuring pass.


<a id="modeling-rdb-update-delete"></a>

## RDB UPDATE/DELETE 중심 모델링

<a id="reference-self-rdb-insert-select"></a>

## RDB INSERT SELECT와 자기 참조 일관성 제약

<a id="unsupported-rejected-rdb-append-api"></a>
<a id="support-scope-rdb-sdk"></a>

## Bulk input and Append

TRANSACTION tables support Append, but the path follows relational constraints and transaction
behavior rather than the TAG/LOG ingestion model. Compare prepared batch, Append, and machloader with
representative data. See [SDK feature support](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-append).

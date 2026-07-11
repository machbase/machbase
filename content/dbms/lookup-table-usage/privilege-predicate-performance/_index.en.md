---
title: '9.15 LOOKUP Privileges and DML Performance'
weight: 150
toc: true
---

This page mirrors the Korean chapter structure. Detailed English content will be aligned after the Korean
manual is finalized.

<a id="privileges-lookup-update-delete-target-select"></a>

## LOOKUP UPDATE and DELETE Privileges

<a id="performance-considerations-lookup-predicate-dml"></a>

## DML Performance Considerations

LOOKUP UPDATE and DELETE support both primary-key and general predicates. A primary-key equality predicate
uses the fast path; general predicates collect matching primary keys before applying the DML. UPDATE and
DELETE do not require an additional SELECT privilege for this internal lookup. A DELETE statement without a
WHERE clause removes all rows.

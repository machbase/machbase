---
title: '9.14 LOOKUP Privileges and DML Performance'
weight: 140
toc: true
---

This page mirrors the Korean chapter structure. Detailed English content will be aligned after the Korean
manual is finalized.

<a id="privileges-lookup-update-delete-target-select"></a>

## LOOKUP UPDATE and DELETE Privileges

<a id="performance-considerations-lookup-predicate-dml"></a>

## DML Performance Considerations

LOOKUP UPDATE and conditional DELETE use a primary-key equality predicate. A DELETE statement without a
WHERE clause removes all rows.

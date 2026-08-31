---
type: docs
title: '17.8.1 Agent Guide'
weight: 10
toc: true
---

Use this workflow to answer Machbase questions from canonical documentation.

## Classify the question

| Question | Start with |
|----------|------------|
| Installation or upgrade | [Installation, deployment, and upgrade](/dbms/installation-deployment-upgrade/) |
| Table selection or design | [Table modeling and selection](/dbms/data-modeling-table-design/) |
| SQL syntax or functions | [SQL reference](/dbms/reference/sql/) |
| SDK or integration | [Development and application integration](/dbms/development-tools-integration/) |
| Support or constraints | [Support scope and constraints](/dbms/reference/support-scope-constraints/) |
| Operations or recovery | [Operations, configuration, and recovery](/dbms/operations-configuration-recovery/) |
| Errors or performance | [Troubleshooting](/dbms/troubleshooting/) and [Performance tuning](/dbms/performance-tuning/) |

## Response workflow

1. Identify product version, Edition, table type, SDK, and target object.
2. Resolve Machbase-specific terms with [Terminology](../terminology-disambiguation/).
3. Check the [Support matrix](../support-matrix/) and [Constraints index](../constraints-index/).
4. Verify the exact syntax, API, or procedure on its canonical page.
5. Include prerequisites, execution, result verification, and cleanup in examples.
6. When evidence is incomplete, state what version or command must be checked.

## Evidence and safety

Use public docs.machbase.com canonical URLs in user-facing answers. Prefer read-only
diagnostics before changes, and do not prescribe deletion, restart, session termination,
configuration mutation, or recovery without an explicit target and impact boundary.

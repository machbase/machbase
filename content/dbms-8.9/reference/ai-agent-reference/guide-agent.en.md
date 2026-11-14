---
type: docs
title: '16.8.1 Agent Guide'
weight: 10
toc: true
---

This guide defines the sequence for answering Machbase questions from canonical documentation.

## Question Classification

| Question Type | First Reference |
|----------|------------------|
| Installation/upgrades | [Installation, Deployment, and Upgrades](/dbms-8.9/installation-deployment-upgrade/) |
| Table selection/design | [Table Type Concepts and Selection](/dbms-8.9/data-modeling-table-design/) |
| SQL syntax/functions | [SQL Reference](/dbms-8.9/reference/sql/) |
| SDK/integration | [Development and Application Integration](/dbms-8.9/development-tools-integration/) |
| Support/constraints | [Support Scope and Constraints](/dbms-8.9/reference/support-scope-constraints/) |
| Operations/recovery | [Operations, Configuration, and Recovery](/dbms-8.9/operations-configuration-recovery/) |
| Errors/performance | [Troubleshooting](/dbms-8.9/troubleshooting/) and [Performance Tuning](/dbms-8.9/performance-tuning/) |

## Response Sequence

1. Identify the product version, edition, table type, SDK, and target object in the question.
2. Check Machbase-specific meanings through [Terminology](../terminology-disambiguation/).
3. Check the [Support Matrix](../support-matrix/) and [Constraints Index](../constraints-index/).
4. Verify actual syntax, APIs, and procedures on the canonical page.
5. Include prerequisites, execution, result checks, and cleanup in examples.
6. For uncertain facts, provide the versions, commands, and documentation needed to verify them.

## Evidence and Links

- Use canonical URLs on docs.machbase.com in public answers.
- Internal issues, commits, or source paths do not replace evidence of public product behavior.
- If documents conflict, prioritize current version-specific canonical pages and actual support scope.

## Safety

Present queries and diagnosis first. Do not present execution steps for deleting data, restarting
servers, terminating sessions, changing settings, or recovery without checking the user's target and
authorization scope.

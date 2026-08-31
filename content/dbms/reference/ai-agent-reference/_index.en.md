---
type: docs
title: '17.8 AI Agent Reference'
weight: 100
toc: true
description: 'Navigation and evidence guidance for AI agents and RAG systems using the Machbase DBMS manual'
---

AI Agent Reference is a navigation layer for AI agents and RAG systems using the
Machbase DBMS 8.7 manual. It points to canonical syntax, SDK, operations, and support
pages instead of redefining product facts.

## Contents

| Page | Purpose |
|------|---------|
| [Agent guide](./guide-agent/) | Question classification, verification, and response rules |
| [canonical-url-map](./canonical-url-map/) | Canonical URLs by subject |
| [task-map](./task-map/) | Reading and verification sequence by user task |
| [support-matrix](./support-matrix/) | Canonical Edition, table, and SDK support matrices |
| [constraints-index](./constraints-index/) | Canonical constraints and rejection conditions |
| [evidence-map](./evidence-map/) | Evidence source by claim type |
| [terminology-disambiguation](./terminology-disambiguation/) | Machbase-specific terminology |
| [sql-generation-rules](./sql-generation-rules/) | Checks required before generating SQL |
| [sdk-api-selection-rules](./sdk-api-selection-rules/) | SDK and API selection workflow |
| [operations-checklist](./operations-checklist/) | Safety rules for operational answers |
| [error-resolution-map](./error-resolution-map/) | Canonical troubleshooting routes |
| [llms.txt](./llms-txt/) | Compact machine-readable manual map |
| [Full text and RAG index](./llms-full-txt-chunk-index/) | Full Markdown and JSON document index |

## Machine-readable outputs

- [llms.txt](/llms.txt)
- [llms-full.txt](/llms-full.txt)
- [llms-chunks.json](/llms-chunks.json)

These outputs contain only the current English DBMS manual. Machbase Neo and the
archived DBMS 8.5 manual are excluded.

## Rules

1. Identify server version, Edition, table type, and SDK first.
2. Read the feature reference together with its support matrix.
3. Do not invent syntax, defaults, limits, or error codes.
4. State the target, impact, recovery path, and completion check for operational changes.
5. Link public canonical documentation in user-facing answers.

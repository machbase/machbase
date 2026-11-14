---
type: docs
title: '16.8 AI Agent Reference'
weight: 100
toc: true
description: 'Navigation and evidence guide for AI agents and RAG systems using Machbase DBMS documentation'
---

AI Agent Reference helps AI agents and RAG systems find the correct canonical pages in the
Machbase DBMS 8.7 documentation. It links to the authoritative feature documentation rather than
redefining SQL syntax, SDK support, or operating procedures.

## Contents

| Page | Purpose |
|--------|------|
| [Agent Guide](./guide-agent/) | Question classification, verification order, and response principles |
| [canonical-url-map](./canonical-url-map/) | Canonical documentation URLs by topic |
| [task-map](./task-map/) | Reading and verification order by user task |
| [support-matrix](./support-matrix/) | Canonical edition, table, and SDK support matrices |
| [constraints-index](./constraints-index/) | Canonical constraints and error conditions |
| [evidence-map](./evidence-map/) | Evidence selection by claim type |
| [terminology-disambiguation](./terminology-disambiguation/) | Clarify easily confused terms |
| [sql-generation-rules](./sql-generation-rules/) | Verification rules before generating SQL |
| [sdk-api-selection-rules](./sdk-api-selection-rules/) | SDK and API selection order |
| [operations-checklist](./operations-checklist/) | Sequence for safe operational responses |
| [error-resolution-map](./error-resolution-map/) | Canonical error diagnosis references |
| [llms.txt](./llms-txt/) | Concise machine-readable documentation map |
| [Full Text and RAG Index](./llms-full-txt-chunk-index/) | Full Markdown and JSON documentation index |

## Machine-readable Outputs

- [llms.txt](/kr/llms.txt)
- [llms-full.txt](/kr/llms-full.txt)
- [llms-chunks.json](/kr/llms-chunks.json)

The outputs linked above include only current Korean DBMS documentation. Machbase Neo and
archived DBMS 8.5 documentation are excluded.

## Principles

1. Check the server version, edition, table type, and SDK first.
2. Read the canonical feature page together with its support scope.
3. Do not invent unverified syntax, defaults, limits, or error codes.
4. For operational changes, specify the target, impact, recovery method, and completion criteria.
5. Use public canonical URLs in responses.

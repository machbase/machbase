---
type: docs
title: '17.8.12 llms.txt'
weight: 120
toc: true
---

`llms.txt` is a UTF-8 plain-text index that helps an LLM find the current Machbase
DBMS manual structure and canonical references.

## URLs

| Language | URL |
|----------|-----|
| English | [https://docs.machbase.com/llms.txt](/llms.txt) |
| Korean | [https://docs.machbase.com/kr/llms.txt](/kr/llms.txt) |

The output contains only current `/dbms/` pages. Machbase Neo, archived DBMS 8.5,
drafts, and aliases are excluded.

## Contents

- Product and manual version
- Top-level DBMS chapters and canonical URLs
- SQL, SDK, operations, support, and error references
- AI Agent Reference
- Full-text and JSON-index URLs

Use `llms.txt` to select a canonical section, an individual `index.md` for one page,
`llms-full.txt` for the complete corpus, and `llms-chunks.json` for page-level metadata.
The index is a navigation aid; linked current pages remain authoritative.

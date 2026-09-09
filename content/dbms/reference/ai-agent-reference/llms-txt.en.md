---
type: docs
title: '16.8.12 llms.txt'
weight: 120
toc: true
---

`llms.txt` is a UTF-8 plain-text contents map that helps LLMs quickly find the structure and
main canonical pages of the current Machbase DBMS manual.

## URL

| Language | URL |
|------|-----|
| English | [https://docs.machbase.com/llms.txt](/llms.txt) |
| Korean | [https://docs.machbase.com/kr/llms.txt](/kr/llms.txt) |

The output includes only current `/dbms/` documentation. Machbase Neo, archived DBMS 8.5,
drafts, and alias pages are excluded.

## Contents

- Product and manual version
- Top-level DBMS chapters and canonical URLs
- Canonical SQL, SDK, operations, support scope, and error code references
- AI Agent Reference
- Full-text and JSON index URLs

## Usage

1. Find the question's canonical section in `llms.txt`.
2. For individual Markdown, read `index.md` under that document's URL.
3. For the complete corpus, use [llms-full.txt](../llms-full-txt-chunk-index/).
4. Use `llms-chunks.json` when a crawler needs document-level metadata.

`llms.txt` is a navigation index. Verify product facts in the linked current documentation
before composing a response.

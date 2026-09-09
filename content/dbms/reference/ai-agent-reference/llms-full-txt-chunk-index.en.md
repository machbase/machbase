---
type: docs
title: '16.8.13 Full Text and RAG Document Index'
weight: 130
toc: true
---

The current DBMS manual provides full Markdown text and a page-level JSON index.

## Full Text

| Language | URL |
|------|-----|
| English | [llms-full.txt](/llms-full.txt) |
| Korean | [llms-full.txt](/kr/llms-full.txt) |

Full text concatenates published DBMS pages in navigation weight order. Each page boundary includes
the title, language, and canonical URL. The body preserves source Markdown.

## JSON Index

| Language | URL |
|------|-----|
| English | [llms-chunks.json](/llms-chunks.json) |
| Korean | [llms-chunks.json](/kr/llms-chunks.json) |

Schema version 1 has the following top-level fields.

| Field | Description |
|------|------|
| `schema_version` | JSON contract version; currently `1` |
| `product` | `Machbase DBMS` |
| `manual_version` | Product version covered by the manual |
| `language` | `en` or `kr` |
| `document_count` | Size of the `documents` array |
| `documents` | Document metadata array |

Each document provides `id`, `title`, `url`, `markdown_url`, `kind`, `parent_url`, `weight`, and
`last_modified`. JSON does not duplicate the body. Fetch each page's Markdown from `markdown_url`
or use `llms-full.txt` as the corpus.

## Chunk Boundaries

The current index treats one published page as one document chunk. SQL syntax, SDK tasks, and
operating procedures remain on separate pages where possible, so URLs and titles can serve as
stable chunk identifiers. Preserve the page `id` when subdividing large dictionary pages.

Nondeterministic values such as build time are omitted. Neo, DBMS 8.5, drafts, and alias pages
are excluded from both the index and full text.

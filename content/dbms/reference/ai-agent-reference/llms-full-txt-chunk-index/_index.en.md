---
type: docs
title: '17.8.13 Full Text and RAG Document Index'
weight: 130
toc: true
---

The current DBMS manual provides a concatenated Markdown corpus and a page-level JSON index.

## Full text

| Language | URL |
|----------|-----|
| English | [llms-full.txt](/llms-full.txt) |
| Korean | [llms-full.txt](/kr/llms-full.txt) |

The full text walks published DBMS pages in navigation-weight order. Each boundary
includes title, language, and canonical URL followed by source Markdown.

## JSON index

| Language | URL |
|----------|-----|
| English | [llms-chunks.json](/llms-chunks.json) |
| Korean | [llms-chunks.json](/kr/llms-chunks.json) |

Schema version 1 contains `schema_version`, `product`, `manual_version`, `language`,
`document_count`, and `documents`. Each document provides `id`, `title`, `url`,
`markdown_url`, `kind`, `parent_url`, `weight`, and `last_modified`.

The JSON file does not duplicate content. Fetch `markdown_url` for an individual page
or use `llms-full.txt` as the corpus. One published page is one stable document chunk.
Neo, archived DBMS 8.5, drafts, aliases, and non-deterministic build timestamps are excluded.

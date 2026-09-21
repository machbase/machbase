---
title: Japanese handoff
weight: 1000
toc: false
build:
  render: never
  list: never
  publishResources: false
---

# Tag Analyzer — Japanese handoff

- `content/neo/tag-analyzer/_index.ja.md`: Japanese documentation, using the existing Hugo structure and anchors.
- `static/images/web-ui/tag-analyzer/*-ja.gif`: nine GIFs with Japanese step labels. Animation timing and final pauses are preserved.
- Other referenced PNGs are unchanged copies of the current documentation screenshots, including the Board outline.

This package is not integrated into the site. No existing pages, language settings, or navigation were changed.
The integration owner can copy the `content` and `static` files into the target repository and configure the Japanese locale (`ja`).
Image references retain the existing site-relative `/images/web-ui/tag-analyzer/` paths. UI button and tab names remain in English to match the recordings.

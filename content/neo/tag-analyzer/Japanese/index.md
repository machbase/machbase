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

## Current guide

The current Japanese translation is now at `content/neo/tag-analyzer/_index.ja.md`
in the repository root, alongside the English and Korean guides. It follows the current
section structure and includes Japanese descriptions for the shared numbered screenshots.
Videos and screenshots without Japanese versions use the current English media.

Japanese is registered in `hugo.yaml` with `languages.ja.disabled: true`.
Normal builds do not publish Japanese pages or show Japanese in the language selector.
To launch Japanese later, set this flag to `false`; the guide will be available at
`/ja/neo/tag-analyzer/`. The language selector is site-wide, so coordinate this change
with the site's Japanese launch. Pages without a Japanese translation link to the
Japanese home page instead of a translated counterpart.

For a local preview without changing the launch flag, create a temporary YAML file:

```yaml
languages:
  ja:
    disabled: false
```

Then run `hugo server --config hugo.yaml,path/to/ja-preview.yaml --port 1315`
and open `http://localhost:1315/ja/neo/tag-analyzer/`.

## Archived handoff package

The nested `content/` and `static/` folders below this directory are the older handoff.
Keep them as reference; do not copy them over the current guide.

- `content/neo/tag-analyzer/_index.ja.md`: Japanese documentation, using the existing Hugo structure and anchors.
- `static/images/web-ui/tag-analyzer/*-ja.gif`: nine GIFs with Japanese step labels. Animation timing and final pauses are preserved.
- Other referenced PNGs are unchanged copies of the current documentation screenshots, including the Board outline.

This older package is not integrated into the site. Its section structure and GIFs
precede the current guide and video-based demonstrations.
Image references retain the existing site-relative `/images/web-ui/tag-analyzer/` paths. UI button and tab names remain in English to match the recordings.

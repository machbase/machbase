# Japanese manual maintenance

Japanese product pages use the same content paths as Korean and English, with a `.ja.md`
suffix. Scope includes DBMS 8.7, DBMS 8.5, Neo, Apps, Fluid, and developer documentation.
For DBMS 8.7, Korean is the primary source; the English-only cache page is also translated.
For other sections, compare both languages and retain information unique to either source.
Record source selection and justified corrections in `scripts/japanese_manual_sources.json`;
consult verified product sources to resolve source errors. SQL/API identifiers,
values, options, explicit anchors, shortcodes, table rows, and examples must be preserved.
Translate prose, explanations, and comments without summarizing away constraints.

Use データベース, テーブル, テーブルタイプ, 行, 列, クエリ, 取り込み, インデックス,
述語, 永続, トランザクション, and 保持ポリシー consistently. Keep names such as TAG,
ROLLUP, BASETIME, and SQL commands unchanged.

## Site behavior

- Japanese product pages use `/ja/neo/`, `/ja/dbms/`, `/ja/dbms-8.5/`, and `/ja/apps/`.
  `/ja/` and the Japanese logo lead to `/ja/neo/`. Navigation includes these products, site
  home, search, and GitHub. The language switcher sends untranslated pages to the Japanese homepage.
- Preserve publication state: Fluid remains excluded by `ignoreFiles`; draft Neo pages remain
  drafts. Translation alone does not authorize publishing hidden or draft content.
- Hextra v0.12.3 supplies Japanese UI strings; project overrides are in `i18n/ja.yaml`.
- All three locales use translated labels in the DBMS `llms` outputs. Japanese Markdown output
  localizes root-relative product page links outside fenced examples, while shared assets retain
  their original paths. Relative links retain the source
  page's canonical URL as their base.
- The local FlexSearch override is based on Hextra v0.12.3. It supports input/paste and IME
  composition, waits for index loading, and ignores stale requests. Heading display names are
  plain text while their original HTML remains available for fragment extraction. Recheck these
  customizations when upgrading the theme.
- The reference generator supports `en`, `kr`, and `ja` at the current flat Markdown paths.
  Its raw inventory retains registered error definitions, but the published 8.7 catalog excludes
  the 24 removed-feature entries already omitted in the source manuals. Error messages remain
  in their original server language.

## Verification

```bash
python3 -B -m unittest discover -s scripts/tests -v
hugo --gc --minify --printUnusedTemplates --printI18nWarnings \
  --destination /tmp/machbase-ja-all-preview
python3 -B scripts/check_japanese_manual.py --all-documents \
  --public-dir /tmp/machbase-ja-all-preview --expected-rendered-pages 564 --landing /ja/neo/ \
  --source-policy scripts/japanese_manual_sources.json \
  --review-file scripts/japanese_manual_reviews.json --json
```

The document checker reports structural errors separately from changes needing human review.
Do not treat zero structural errors as semantic approval. Review all numeric/code differences,
then independently read high-risk SQL/API, data-loss, backup, and authentication procedures.
A review file can approve exact findings using source, companion-source, and target hashes; edits
invalidate those approvals. The current scope is 588 canonical translations: 583 product documents
and 5 developer documents. Of these, 564 product pages are published by the normal build;
8 Fluid documents and 11 Neo drafts remain unpublished. Recompute these counts when scope changes. See `python3 scripts/check_japanese_manual.py --help` for the review-file interface.

The browser regression checks landing pages, same-article language switching, Japanese search,
IME composition, delayed index loading, no results, clipboard, themes, mobile menus, and TOC
navigation. Install browser test dependencies outside the source checkout if desired:

```bash
npm install --prefix /tmp/machbase-ja-browser --no-save --package-lock=false playwright@1.58.2
/tmp/machbase-ja-browser/node_modules/.bin/playwright install chromium
python3 -m http.server 14313 --bind 127.0.0.1 --directory /tmp/machbase-ja-all-preview
```

With that server running, use a separate terminal:

```bash
NODE_PATH=/tmp/machbase-ja-browser/node_modules \
  node scripts/tests/japanese_browser.cjs http://127.0.0.1:14313 /tmp/machbase-ja-browser
```

`PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` optionally selects an installed Chromium binary. Inspect
both desktop and mobile screenshots from the output directory; passing interaction checks alone
does not establish visual quality. The tests do not execute SQL against a live DBMS.

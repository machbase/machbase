# Japanese manuals — independent review

**Status: APPROVED for translated content.** All 588 canonical documents have Japanese counterparts:
242 DBMS 8.7 documents, 119 DBMS 8.5 documents, 213 Neo documents, 1 Apps document,
8 Fluid documents, and 5 developer documents. This report supersedes the earlier DBMS-only signoff.

Translation and independent review ran in parallel. Reviewers checked other authors' work;
the TQL author did not approve their own TQL translations. Korean and English product sources
remain unchanged. Where the sources differ, the Japanese version retains the additional material
and records the primary source, companion sources, and justified corrections.

## Evidence and reproducible checks

- `scripts/japanese_manual_sources.json` records bilingual source choices and documented corrections.
- `scripts/japanese_manual_reviews.json` binds each approved finding to the exact source, translation,
  companion-source hashes, and finding fingerprint. Structural and rendered errors remain actionable.
- `scripts/japanese_manual_coverage.json` records every document's source and Japanese hashes and
  independent reviewers, including pages with no automatic findings.
- [Japanese manual maintenance](JAPANESE_MANUAL.md) contains the commands for repeating source,
  rendered-site, unit, and browser checks.

The final normal Hugo build succeeded with `--gc --minify --printUnusedTemplates --printI18nWarnings`.
The rendered audit checked 564 canonical Japanese product pages and 414,299 internal links,
assets, and fragments, with no errors. All published page-level Markdown bodies and the 242-document
DBMS `llms` corpus match their current Japanese source, allowing the documented link localization.
Alias redirects are checked separately and are not counted as canonical documents.

All 51 Python tests passed. All 19 browser checks passed without recorded page or search errors:
Japanese landing and navigation for Neo, DBMS 8.7, DBMS 8.5, and Apps; same-page language switching;
Japanese search and IME confirmation; delayed-index query replacement, Escape, and blur; no results;
clipboard, themes, mobile navigation, viewport fit, and table-of-contents links. Desktop and mobile
search screenshots were also inspected.

The 11 Neo drafts remain unpublished in a normal build and are available in a draft build.
The 8 Fluid documents remain excluded by `ignoreFiles`. Translation does not change publication state.

## Content verification

Review covered complete prose, table fields and units, SQL/API identifiers, options, defaults,
constraints, examples, expected results, headings, anchors, shortcodes, and links. Original server
messages and meaningful sample data remain in their original language. The DBMS 8.5 error dictionary
includes Japanese explanations for all 857 entries; the DBMS 8.7 public error catalog retains all
1,062 entries after the existing 24 exclusions from its 1,086-entry source manifest.

Source-backed corrections include backup restoration preconditions, retention units and cutoff
meaning, metadata operations, numeric examples, UTF-8 field capacity, command flags, connector
units, JavaScript support, and legacy Tengo examples. Corrections and evidence are recorded in the
review dispositions; they are not blanket changes to another product version's contract.

Isolated Neo tests verified selected SQL, metadata, TQL transformations, MQTT messages, and UTF-8
behavior. The TQL compile audit covered 337 examples: 325 compiled; 9 source-only fragments require
a sink, and 3 explicitly versioned 8.7 examples are unavailable in the older local Neo checkout.
This does not claim that every installation procedure or external database connector was executed.
Existing production databases and cluster installations were not modified by validation.

## State binding

This approval applies to the hashes in the coverage and review manifests. Any source or translation
change requires the affected review and generated output to be checked again. Existing Korean i18n
and unused-theme-template warnings were distinguished from Japanese content and UI validation.
Commit, push, and deployment are separate from this review.

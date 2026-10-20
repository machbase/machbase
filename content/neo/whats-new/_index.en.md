---
title: "What's New?"
type: docs
weight: 5
toc: false
---

Read the latest Machbase Neo news and release highlights, with the newest entries first.

## 2026-10-20 — Machbase Neo v8.7.2 release

This release makes ARRAY data easier to explore and introduces an experimental feature for
turning the start page into your own workspace. It also improves chart and file workflows,
strengthens authentication defaults, and enhances server and database stability.

- **Start page customization (experimental)**: This feature is enabled only when the server
  is started with `--experiment true`. It supports user settings, groups, and view modes.
  Issues with layout, saving, groups, and dialogs in the New tab have also been fixed.
- **ARRAY data exploration**: Select elements of numeric ARRAYs in Data Viewer and inspect
  them in detailed charts and tables. Send selected elements to Tag Analyzer for analysis
  and saving.
- **Chart and analysis improvements**: ECharts 6 support with v5 compatibility has been added,
  and the chart runtime has been unified. Fixes also address lost edits and popover behavior
  in Tag Analyzer, as well as dashboard issues.
- **File operations and error handling**: File overwrite warnings, encoding, and error
  reporting have been improved. The save shortcut is `Cmd+S` on macOS and `Ctrl+S` on other
  platforms. Deeply nested JSON is displayed as text instead of causing a rendering error,
  and error handling has been strengthened to prevent a failure in one part of the UI
  from affecting the entire app.
- **Authentication and server stability**: JWT signing keys are now generated and stored
  more securely. Improvements also cover concurrent TQL requests and cancellation,
  shell output and error handling, and concurrent access to and batch storage of
  server operational metrics.
- **Database engine improvements**: DBMS 8.7.2 fixes `SQLColumns` compatibility with older
  servers and reduces CPU costs for some queries. It also fixes a bitmap index memory
  visibility issue on ARM64.

**Before upgrading:** HTTP and MQTT token authentication are now enabled by default.
If you previously used HTTP APIs or MQTT without tokens, check your clients' authentication
settings before upgrading. To disable authentication through command-line options, explicitly
set `--http-enable-token-auth false` and `--mqtt-enable-token-auth false`.

[v8.7.2 release notes](https://github.com/machbase/neo-server/releases/tag/v8.7.2)
· [Full changelog](https://github.com/machbase/neo-server/compare/v8.7.1...v8.7.2)

---

## 2026-10-05 — Showcases menu added

The **Showcases** link is now available to the right of **Apps** in the top navigation.
Its blue background and small play icon make it easy to find demonstrations and examples
of how to use Machbase Neo. The link opens the showcase page in your current document language.

[Explore Showcases]({{< relref "/neo/showcases" >}})

---

## 2026-09-23 — Machbase Neo v8.7.1 release

This release adds API token authentication for SSH and the TQL API, and improves signal
handling and service termination. It also improves nested file-system mounts and conflict
resolution, file-handling endpoints, and JSH and Neo-shell help, and fixes the TQL buffer limit.

[v8.7.1 release notes](https://github.com/machbase/neo-server/releases/tag/v8.7.1)
· [Full changelog](https://github.com/machbase/neo-server/compare/v8.7.0...v8.7.1)

---

## 2026-09-17 — Machbase Neo v8.5.12 release

Machbase Neo v8.5.12 has been released. Its release page does not include detailed notes;
see the full changelog for the changes between v8.5.11 and v8.5.12.

[v8.5.12 release page](https://github.com/machbase/neo-server/releases/tag/v8.5.12)
· [Full changelog](https://github.com/machbase/neo-server/compare/v8.5.11...v8.5.12)

---

## 2026-09-09 — Machbase Neo v8.7.0 release

This release introduces engine v8.7 and client v2, multi-database support, and named query
parameters. It improves CSV import performance, SQL compatibility and transaction handling,
authentication and session management, and database backup requests and validation.

[v8.7.0 release notes](https://github.com/machbase/neo-server/releases/tag/v8.7.0)
· [Full changelog](https://github.com/machbase/neo-server/compare/v8.5.10...v8.7.0)

---
type: docs
title: '11.11 External Tools'
weight: 110
toc: true
aliases:
  - /dbms/application-integration/external-tools/
---

Connect collection and visualization tools through Machbase SQLCLI, JDBC, ODBC, or a verified
plugin. Confirm availability and compatibility for the deployed tool version before production use.

## Common checks

1. Test TCP connectivity to port 5656 from the tool host.
2. Use a minimum-privilege account for the intended read or write path.
3. Do not store a password or AUTH KEY private key in plaintext configuration.
4. Round-trip representative timestamps, NULLs, strings, and numeric values.
5. Define timeout, batch, retry, and failed-row behavior.
6. Record an identifier that correlates the external-tool and Machbase logs.

<a id="fluentd-plugin"></a>

## Fluentd

For a Fluentd output plugin or file pipeline, verify Ruby and Fluentd compatibility, LOG-table
column mapping, buffer flush and overflow policy, restart duplicate handling, and a dead-letter path.
Use [Fluentd pipeline](fluentd/) as the canonical DBMS workflow and
the installed plugin's documentation for version-specific options.

<a id="grafana-plugin"></a>

## Grafana

Configure the server address, database, read-only account, and timeout. Test a fixed short time
range first, then verify time-filter conversion, series mapping, row count, timezone, and alert
queries. Apply time and tag filters before increasing dashboard range or cardinality.

<a id="tableau-connector"></a>

## Tableau

Tableau can connect through Machbase JDBC or ODBC where the deployment supports those interfaces.
Install the same driver on every desktop or server node that executes the workbook. See
[JDBC](../jdbc/) and [SQLCLI and ODBC](../cli-odbc/) for driver and connection configuration.

Validate custom SQL in `machsql` before using it in Tableau. For extracts, define an explicit time
range and incremental key, then document duplicate and refresh-failure recovery.

## Production validation

- Execute the real query or input path instead of stopping at a connection test.
- Confirm credential storage and file permissions.
- Test schema and timestamp round trips in staging after plugin or driver upgrades.
- Bound timeout and retry behavior so an outage cannot remain hidden indefinitely.
- Do not standardize an unverified plugin name or fixed version.

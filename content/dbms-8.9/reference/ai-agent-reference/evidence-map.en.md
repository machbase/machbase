---
type: docs
title: '16.8.6 evidence-map'
weight: 60
toc: true
---

Select public evidence appropriate to each claim in the response.

| Claim Type | Preferred Evidence |
|----------|-----------|
| SQL syntax/functions/types | [SQL Reference](/dbms-8.9/reference/sql/) |
| Edition/table/SDK support | [Support Scope and Constraints](/dbms-8.9/reference/support-scope-constraints/) and [SDK Support](/dbms-8.9/development-tools-integration/sdk-support-scope/) |
| Configuration keys/defaults | [Configuration Reference](/dbms-8.9/reference/configuration/) and distribution configuration files |
| System status columns | [System Catalog](/dbms-8.9/reference/system-catalog/) |
| CLI options | [Command-line Tools](/dbms-8.9/reference/command-line-tools/) and distribution `--help` |
| Error meaning/actions | [Error Codes](/dbms-8.9/reference/error-codes/) and [Troubleshooting](/dbms-8.9/troubleshooting/) |
| Operating procedures | [Operations, Configuration, and Recovery](/dbms-8.9/operations-configuration-recovery/) |

## Verification Rules

- Preserve version and edition conditions with the evidence.
- Do not generalize example results into guarantees or performance claims.
- Mark facts absent from public canonical documentation as requiring verification.
- Internal development history does not replace public manual links.

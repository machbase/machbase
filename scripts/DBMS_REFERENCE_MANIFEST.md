# DBMS reference source manifests

The JSON files in `data/dbms-reference/` are generated audit inputs for the DBMS manual. They capture
the registered function descriptors, fixed-table schemas, and errors found in the authoritative NFX
source checkout. Registration is not, by itself, a promise that an item is a public API. The error
generator additionally owns the marked complete-catalog blocks in the Korean and English error
dictionary pages. Surrounding explanations, examples, compatibility notes, causes, and remedies
remain hand-authored.

Regenerate the snapshots and localized error catalog blocks after changing the NFX revision or the
corresponding reference pages:

```bash
python3 scripts/generate_dbms_reference_manifest.py \
  --nfx-root /path/to/nfx
```

CI or review can detect stale JSON or manual catalog blocks without modifying files:

```bash
python3 scripts/generate_dbms_reference_manifest.py \
  --nfx-root /path/to/nfx \
  --check
```

The `has_korean_reference_heading` field is a narrow coverage signal based on reference headings. A
`false` value is a review queue entry, not proof that the whole manual never mentions the item. The
complete generated Korean error catalog makes `listed_in_korean_reference` true for every parsed
`ERR_ID`. Edition-specific descriptors and
preprocessor conditions remain visible in each manifest so reviewers do not accidentally turn one
build variant into a universal contract.

Function return types and sizes are descriptor declarations. A validator can select the actual SQL
return type, and the size expression is an internal buffer size rather than a user-facing length
limit. The function inventory is a source-level heuristic over `gRootOfFunctions` and `mNext`-shaped
initializers; it must not be used as an Edition support contract without a compiled descriptor dump
from both builds. Static fixed-table manifests synthesize `_ARRIVAL_TIME`, conditional `HOSTNAME`, and
`_RID` exactly as the metadata builder does; runtime `V$<TAG_TABLE_NAME>_STAT` views are recorded
separately as a dynamic name pattern. Error messages preserve C format tokens but do not infer cause,
remedy, retryability, Edition, or version support.

The `.msg` lexer treats `#`, `//`, and `/* ... */` as comments only outside quoted strings. The
`format_tokens` array preserves literal `%%`; `conversion_tokens` contains conversion tokens but is
not an argument list because width and precision `*` can consume additional arguments.

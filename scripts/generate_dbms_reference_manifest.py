#!/usr/bin/env python3
"""Generate DBMS reference inventories and error catalogs from the NFX source tree.

The generated JSON records what the server registers. The complete error catalog
blocks in the Korean and English manuals are generated from the same parsed error
definitions while surrounding user-facing guidance remains hand-authored.
"""

from __future__ import annotations

import argparse
import ast
import html
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable


SCHEMA_VERSION = 1
FUNCTION_MANUAL = Path("content/dbms/reference/sql/functions/functions-full/_index.kr.md")
TABLE_MANUAL = Path("content/dbms/reference/system-catalog/virtual-table-full/_index.kr.md")
ERROR_MANUAL = Path("content/dbms/reference/error-codes/_index.kr.md")
ERROR_MANUAL_EN = Path("content/dbms/reference/error-codes/_index.en.md")
ERROR_CATALOG_BEGIN = "<!-- BEGIN GENERATED NFX ERROR CATALOG -->"
ERROR_CATALOG_END = "<!-- END GENERATED NFX ERROR CATALOG -->"


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def git_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def strip_comments(text: str) -> str:
    """Remove C comments while preserving newlines and quoted strings."""
    out: list[str] = []
    i = 0
    quote = ""
    while i < len(text):
        if quote:
            out.append(text[i])
            if text[i] == "\\" and i + 1 < len(text):
                out.append(text[i + 1])
                i += 2
                continue
            if text[i] == quote:
                quote = ""
            i += 1
            continue
        if text[i] in ('"', "'"):
            quote = text[i]
            out.append(text[i])
            i += 1
        elif text.startswith("//", i):
            end = text.find("\n", i)
            if end < 0:
                out.extend(" " * (len(text) - i))
                break
            out.extend(" " * (end - i))
            i = end
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end < 0:
                raise ValueError("unterminated C comment")
            chunk = text[i : end + 2]
            out.extend("\n" if char == "\n" else " " for char in chunk)
            i = end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def strip_msg_comments(text: str) -> str:
    """Remove .msg comments, including genmsg's # line comments, preserving offsets."""
    without_c_comments = strip_comments(text)
    out: list[str] = []
    quote = ""
    i = 0
    while i < len(without_c_comments):
        char = without_c_comments[i]
        if quote:
            out.append(char)
            if char == "\\" and i + 1 < len(without_c_comments):
                out.append(without_c_comments[i + 1])
                i += 2
                continue
            if char == quote:
                quote = ""
            i += 1
        elif char == '"':
            quote = char
            out.append(char)
            i += 1
        elif char == "#":
            end = without_c_comments.find("\n", i)
            if end < 0:
                out.extend(" " * (len(without_c_comments) - i))
                break
            out.extend(" " * (end - i))
            i = end
        else:
            out.append(char)
            i += 1
    return "".join(out)


def balanced_block(text: str, open_at: int) -> tuple[str, int]:
    """Return the contents and end offset of a brace-delimited C initializer."""
    if text[open_at] != "{":
        raise ValueError("initializer does not start with an opening brace")
    depth = 0
    quote = ""
    i = open_at
    while i < len(text):
        char = text[i]
        if quote:
            if char == "\\":
                i += 2
                continue
            if char == quote:
                quote = ""
        elif char in ('"', "'"):
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[open_at + 1 : i], i + 1
        i += 1
    raise ValueError("unterminated C initializer")


def split_top_level(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depths = {"(": 0, "[": 0, "{": 0}
    closing = {")": "(", "]": "[", "}": "{"}
    quote = ""
    i = 0
    while i < len(text):
        char = text[i]
        if quote:
            if char == "\\":
                i += 2
                continue
            if char == quote:
                quote = ""
        elif char in ('"', "'"):
            quote = char
        elif char in depths:
            depths[char] += 1
        elif char in closing:
            depths[closing[char]] -= 1
        elif char == "," and not any(depths.values()):
            parts.append(text[start:i].strip())
            start = i + 1
        i += 1
    tail = text[start:].strip()
    if tail:
        parts.append(tail)
    return parts


def find_initializers(text: str, declaration: re.Pattern[str]) -> Iterable[tuple[re.Match[str], str]]:
    for match in declaration.finditer(text):
        open_at = text.find("{", match.end())
        if open_at < 0:
            raise ValueError(f"missing initializer after {match.group(0)!r}")
        body, _ = balanced_block(text, open_at)
        yield match, body


def edition_hint(path: Path) -> list[str]:
    if path.name.endswith("_std.c"):
        return ["standard"]
    if path.name.endswith("_ent.c"):
        return ["cluster"]
    return ["standard", "cluster"]


def preprocess_fragment(text: str, edition: str) -> str:
    """Evaluate the small EDITION_* preprocessor subset used by NFX registries."""
    defined = {"EDITION_STANDARD"} if edition == "standard" else {"EDITION_CLUSTER"}
    active = True
    stack: list[tuple[bool, bool]] = []
    output: list[str] = []

    def condition_value(directive: str, expression: str) -> bool:
        if directive == "ifdef":
            return expression in defined
        if directive == "ifndef":
            return expression not in defined
        value = expression
        value = re.sub(
            r"defined\s*\(\s*(\w+)\s*\)",
            lambda match: "True" if match.group(1) in defined else "False",
            value,
        )
        value = re.sub(r"defined\s+(\w+)", lambda match: "True" if match.group(1) in defined else "False", value)
        value = value.replace("&&", " and ").replace("||", " or ")
        value = re.sub(r"!\s*(?!=)", " not ", value)
        if re.search(r"[^\s()TrueFalsandornt]", value):
            raise ValueError(f"unsupported preprocessor expression: {expression}")
        return bool(eval(value, {"__builtins__": {}}, {}))  # noqa: S307 - validated boolean grammar

    for line in text.splitlines(keepends=True):
        match = re.match(r"\s*#\s*(ifdef|ifndef|if|elif|else|endif)\b\s*(.*?)\s*$", line)
        if not match:
            output.append(line if active else "\n" if line.endswith("\n") else "")
            continue
        directive, expression = match.groups()
        if directive in {"ifdef", "ifndef", "if"}:
            parent = active
            branch = condition_value(directive, expression)
            stack.append((parent, branch))
            active = parent and branch
        elif directive == "elif":
            if not stack:
                raise ValueError("orphan #elif")
            parent, prior_branch = stack[-1]
            branch = (not prior_branch) and condition_value("if", expression)
            stack[-1] = (parent, prior_branch or branch)
            active = parent and branch
        elif directive == "else":
            if not stack:
                raise ValueError("orphan #else")
            parent, prior_branch = stack[-1]
            stack[-1] = (parent, True)
            active = parent and not prior_branch
        else:
            if not stack:
                raise ValueError("orphan #endif")
            parent, _ = stack.pop()
            active = parent
        output.append("\n" if line.endswith("\n") else "")
    if stack:
        raise ValueError("unterminated preprocessor condition")
    return "".join(output)


def markdown_headings(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [
        match.group(1).strip().upper()
        for line in path.read_text(encoding="utf-8").splitlines()
        if (match := re.match(r"^#{2,6}\s+(.+?)\s*$", line))
    ]


def named_in_headings(name: str, headings: list[str]) -> bool:
    pattern = re.compile(rf"(?<![A-Z0-9_]){re.escape(name.upper())}(?![A-Z0-9_])")
    return any(pattern.search(heading) for heading in headings)


def string_macros(nfx_root: Path) -> dict[str, set[str]]:
    macros: dict[str, set[str]] = defaultdict(set)
    pattern = re.compile(r'^\s*#\s*define\s+(\w+)\s+("(?:\\.|[^"\\])*")\s*$', re.MULTILINE)
    for path in sorted(nfx_root.glob("*/src/**/*.[ch]")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in pattern.finditer(text):
            macros[match.group(1)].add(match.group(2))
    return dict(macros)


def integer_macros(paths: Iterable[Path]) -> dict[str, set[int]]:
    macros: dict[str, set[int]] = defaultdict(set)
    pattern = re.compile(r"^\s*#\s*define\s+(\w+)\s+([0-9]+)\s*$", re.MULTILINE)
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in pattern.finditer(text):
            value = int(match.group(2))
            macros[match.group(1)].add(value)
    return dict(macros)


def generate_functions(nfx_root: Path, manual_root: Path) -> dict:
    qpf_dir = nfx_root / "qp/src/qpf"
    registry_path = qpf_dir / "qpf.c"
    registry_text = strip_comments(registry_path.read_text(encoding="utf-8"))
    registry_match = re.search(
        r"static\s+qpfFuncDesc\s*\*\s*gRootOfFunctions\s*\[\s*\]\s*=\s*\{",
        registry_text,
    )
    if not registry_match:
        raise ValueError("gRootOfFunctions registry was not found")
    registry_body, _ = balanced_block(registry_text, registry_text.find("{", registry_match.start()))
    roots = re.findall(r"&\s*(g[A-Za-z0-9_]+Desc)\b", registry_body)

    definitions: dict[str, list[dict]] = defaultdict(list)
    declaration = re.compile(r"\bqpfFuncDesc\s+(g[A-Za-z0-9_]+Desc)\s*=\s*")
    qpf_sources = sorted(qpf_dir.glob("*.c"))
    arg_macros = integer_macros(
        [*qpf_sources, *sorted((nfx_root / "qp/src/include").glob("*.h"))]
    )
    for path in qpf_sources:
        raw = path.read_text(encoding="utf-8")
        text = strip_comments(raw)
        for match, body in find_initializers(text, declaration):
            fields = split_top_level(body)
            if len(fields) < 5 or not re.fullmatch(r'"[^"\\]*"', fields[0]):
                continue
            links = re.findall(r"&\s*(g[A-Za-z0-9_]+Desc)\b", body)
            arg_count_text = fields[3].strip()
            if re.fullmatch(r"-?\d+", arg_count_text):
                arg_count = int(arg_count_text)
            elif arg_count_text in arg_macros and len(arg_macros[arg_count_text]) == 1:
                arg_count = next(iter(arg_macros[arg_count_text]))
            else:
                raise ValueError(f"unresolved function argument count: {arg_count_text}")
            definitions[match.group(1)].append(
                {
                    "name": ast.literal_eval(fields[0]),
                    "declared_return_type": fields[1],
                    "internal_return_size_expression": fields[2],
                    "argument_count": arg_count,
                    "aggregate": fields[4].split()[0] == "NBP_TRUE",
                    "next_symbol": links[-1] if links else None,
                    "editions": edition_hint(path),
                    "source": f"{relative(path, nfx_root)}:{line_number(raw, match.start())}",
                }
            )

    missing = sorted(symbol for symbol in roots if symbol not in definitions)
    if missing:
        raise ValueError(f"registered function descriptors are missing definitions: {missing}")

    headings = markdown_headings(manual_root / FUNCTION_MANUAL)
    functions: list[dict] = []
    seen_roots: set[str] = set()
    seen_names: set[str] = set()
    for root_symbol in roots:
        if root_symbol in seen_roots:
            continue
        seen_roots.add(root_symbol)
        queue = [root_symbol]
        seen_symbols: set[str] = set()
        overloads: list[dict] = []
        while queue:
            symbol = queue.pop(0)
            if symbol in seen_symbols:
                raise ValueError(f"function descriptor cycle at {symbol}")
            seen_symbols.add(symbol)
            variants = definitions.get(symbol)
            if not variants:
                raise ValueError(f"overload descriptor {symbol} is missing")
            overloads.append({"symbol": symbol, "variants": variants})
            next_symbols = {item["next_symbol"] for item in variants if item["next_symbol"]}
            queue.extend(sorted(next_symbols - seen_symbols))
        names = sorted({variant["name"] for item in overloads for variant in item["variants"]})
        if len(names) != 1:
            raise ValueError(f"descriptor chain {root_symbol} has inconsistent names: {names}")
        name = names[0]
        if name != name.upper() or not re.fullmatch(r"[A-Z][A-Z0-9_]*", name):
            raise ValueError(f"registered function name is not canonical uppercase: {name}")
        if name in seen_names:
            raise ValueError(f"duplicate registered function name: {name}")
        seen_names.add(name)
        aggregate_flags = {
            variant["aggregate"] for item in overloads for variant in item["variants"]
        }
        if len(aggregate_flags) != 1:
            raise ValueError(f"descriptor chain {name} has inconsistent aggregate flags")
        for edition in ("standard", "cluster"):
            arities = [
                variant["argument_count"]
                for item in overloads
                for variant in item["variants"]
                if edition in variant["editions"]
            ]
            if len(arities) != len(set(arities)):
                raise ValueError(f"descriptor chain {name} repeats an arity in {edition}: {arities}")
        functions.append(
            {
                "name": name,
                "registered_symbol": root_symbol,
                "has_korean_reference_heading": named_in_headings(name, headings),
                "overloads": overloads,
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "repository": "nfx",
            "revision": git_revision(nfx_root),
            "registry": relative(registry_path, nfx_root),
            "extraction_mode": "source_heuristic",
            "limitations": [
                "Use as a drift and review signal, not as proof of public API or Edition support.",
                "Declared return type can be replaced by a validator at runtime.",
                "A compiled Standard/Cluster descriptor visitor is required for an Edition contract.",
            ],
        },
        "manual_reference": FUNCTION_MANUAL.as_posix(),
        "counts": {
            "registered_functions": len(functions),
            "functions_with_korean_reference_heading": sum(
                item["has_korean_reference_heading"] for item in functions
            ),
            "descriptor_symbols": sum(len(item["overloads"]) for item in functions),
        },
        "functions": functions,
    }


def generate_system_tables(nfx_root: Path, manual_root: Path) -> dict:
    source_files = sorted(path for path in nfx_root.glob("*/src/**/*.c") if path.is_file())
    table_decl = re.compile(r"\bpmsTableSpec\s+(g[A-Za-z0-9_]+)\s*=\s*")
    field_decl = re.compile(r"\b(?:static\s+)?pmsFieldDesc\s+(\w+)\s*\[\s*\]\s*=\s*")
    registry_decl = re.compile(r"\bpmsTableSpec\s*\*\s*(g[A-Za-z0-9_]*TableSpecs)\s*\[\s*\]\s*=\s*")

    fields: dict[str, dict] = {}
    definitions: dict[str, list[dict]] = defaultdict(list)
    registrations: dict[str, list[dict]] = defaultdict(list)
    macros = string_macros(nfx_root)

    def parse_field_body(body: str, label: str) -> list[dict]:
        columns: list[dict] = []
        items = [item for item in split_top_level(body) if item]
        sentinel_seen = False
        for item_index, item in enumerate(items):
            item = item.strip()
            if not item.startswith("{") or not item.endswith("}"):
                raise ValueError(f"unsupported field initializer in {label}")
            parts = split_top_level(item[1:-1])
            if len(parts) < 4:
                raise ValueError(f"short field initializer in {label}")
            if parts[0] == "NULL":
                if item_index != len(items) - 1 or "0xFFFFFFFF" not in parts[1]:
                    raise ValueError(f"invalid field sentinel in {label}")
                sentinel_seen = True
                continue
            if re.fullmatch(r'"(?:\\.|[^"\\])*"', parts[0]):
                field_name = ast.literal_eval(parts[0])
            elif (
                re.fullmatch(r"[A-Za-z_]\w*", parts[0])
                and parts[0] in macros
                and len(macros[parts[0]]) == 1
            ):
                field_name = ast.literal_eval(next(iter(macros[parts[0]])))
            else:
                raise ValueError(f"unresolved field name in {label}")
            type_match = re.search(r"PMS_FIELD_TYPE_([A-Z0-9_]+)", parts[2])
            if not type_match:
                raise ValueError(f"unknown field type in {label}")
            columns.append(
                {
                    "name": field_name,
                    "type": type_match.group(1),
                    "pointer": "PMS_FIELD_FLAG_PTR" in parts[2],
                    "declared_size": parts[3],
                }
            )
        if not sentinel_seen:
            raise ValueError(f"field descriptor has no final sentinel: {label}")
        return columns

    for path in source_files:
        raw = path.read_text(encoding="utf-8", errors="replace")
        text = strip_comments(raw)
        for match, body in find_initializers(text, field_decl):
            label = f"{path}:{match.group(1)}"
            fields[match.group(1)] = {
                "columns_by_edition": {
                    edition: parse_field_body(preprocess_fragment(body, edition), label)
                    for edition in ("standard", "cluster")
                },
                "source": f"{relative(path, nfx_root)}:{line_number(raw, match.start())}",
            }

        for match, body in find_initializers(text, table_decl):
            parts = split_top_level(body)
            if len(parts) < 4 or not re.fullmatch(r'"[^"\\]*"', parts[0]):
                continue
            definitions[match.group(1)].append(
                {
                    "name": ast.literal_eval(parts[0]),
                    "field_descriptor": parts[1],
                    "columns_by_edition": fields.get(parts[1], {}).get("columns_by_edition"),
                    "need_hostname_expression": parts[3],
                    "source": f"{relative(path, nfx_root)}:{line_number(raw, match.start())}",
                }
            )

    registry_config = [
        ("pm", "pm/src/pmi/pmiFixedTableList.c", {"standard", "cluster"}),
        ("mm", "mm/src/mmi/mmiFixedTableList.c", {"standard", "cluster"}),
        ("qp", "qp/src/qpi/qpiFixedTableList.c", {"standard", "cluster"}),
        ("sm", "sm/src/smi/smiFixedTableList.c", {"standard", "cluster"}),
        ("cc", "cc/src/cci/cciFixedTableList.c", {"cluster"}),
        ("xm", "xm/src/xmi/xmiFixedTableList.c", {"cluster"}),
        ("rp", "rp/src/rpi/rpiFT.c", {"cluster"}),
    ]
    for component, source_name, startup_editions in registry_config:
        path = nfx_root / source_name
        raw = path.read_text(encoding="utf-8")
        text = strip_comments(raw)
        found_registry = False
        for match, body in find_initializers(text, registry_decl):
            found_registry = True
            for edition in sorted(startup_editions):
                active_body = preprocess_fragment(body, edition)
                for symbol in re.findall(r"&\s*(g[A-Za-z0-9_]+(?:Desc|FTblDesc))\b", active_body):
                    registrations[symbol].append(
                        {
                            "component": component,
                            "edition": edition,
                            "registry": match.group(1),
                            "startup_scope": "normal service startup",
                            "source": f"{source_name}:{line_number(raw, match.start())}",
                        }
                    )
        if not found_registry:
            raise ValueError(f"fixed-table registry was not found in {source_name}")

    unresolved = sorted(symbol for symbol in registrations if symbol not in definitions)
    if unresolved:
        raise ValueError(f"registered table descriptors are missing definitions: {unresolved}")

    headings = markdown_headings(manual_root / TABLE_MANUAL)
    by_name: dict[str, list[dict]] = defaultdict(list)
    for symbol in sorted(registrations):
        for variant in definitions[symbol]:
            if variant["columns_by_edition"] is None:
                raise ValueError(
                    f"registered table {symbol} references an unparsed field descriptor "
                    f"{variant['field_descriptor']}"
                )
            editions = sorted({item["edition"] for item in registrations[symbol]})
            if any(not variant["columns_by_edition"].get(edition) for edition in editions):
                raise ValueError(f"registered table {symbol} has no declared fields")
            need_hostname = {
                edition: "NBP_TRUE" in preprocess_fragment(variant["need_hostname_expression"], edition)
                for edition in editions
            }
            declared_columns = {
                edition: variant["columns_by_edition"][edition] for edition in editions
            }
            runtime_columns = {}
            for edition in editions:
                columns = [
                    {"name": "_ARRIVAL_TIME", "type": "DATE", "hidden": True, "builtin": "arrival_time"}
                ]
                if edition == "cluster" and need_hostname[edition]:
                    columns.append({"name": "HOSTNAME", "type": "VARCHAR", "hidden": False, "builtin": "hostname"})
                columns.extend(
                    {**column, "hidden": False, "builtin": None}
                    for column in declared_columns[edition]
                )
                columns.append({"name": "_RID", "type": "LONG", "hidden": True, "builtin": "rid"})
                runtime_columns[edition] = columns
            by_name[variant["name"]].append(
                {
                    "symbol": symbol,
                    "availability": editions,
                    "declared_columns": declared_columns,
                    "runtime_columns": runtime_columns,
                    "field_descriptor": variant["field_descriptor"],
                    "need_hostname": need_hostname,
                    "source": variant["source"],
                    "registrations": registrations[symbol],
                }
            )

    tables = [
        {
            "name": name,
            "has_korean_reference_heading": named_in_headings(name, headings),
            "variants": variants,
        }
        for name, variants in sorted(by_name.items())
    ]
    for edition in ("standard", "cluster"):
        names = [
            table["name"]
            for table in tables
            if any(edition in variant["availability"] for variant in table["variants"])
        ]
        if len(names) != len({name.upper() for name in names}):
            raise ValueError(f"duplicate fixed-table name in {edition} registry")
    for table in tables:
        if not re.fullmatch(r"[MV]\$[A-Z0-9_]+", table["name"]):
            raise ValueError(f"registered fixed-table name has an unexpected form: {table['name']}")
        for variant in table["variants"]:
            for edition, columns in variant["runtime_columns"].items():
                names = [column["name"].upper() for column in columns]
                if len(names) != len(set(names)):
                    raise ValueError(f"duplicate column in {table['name']} ({edition})")
    edition_counts = {
        edition: sum(
            any(edition in variant["availability"] for variant in table["variants"])
            for table in tables
        )
        for edition in ("standard", "cluster")
    }
    revision = git_revision(nfx_root)
    known_counts = {
        "144a63e39d65b1e276b901e4dbe17ae665b2ed3e": {"standard": 67, "cluster": 76}
    }
    if revision in known_counts and edition_counts != known_counts[revision]:
        raise ValueError(
            f"fixed-table count differs from the audited NFX baseline: {edition_counts}"
        )

    dynamic_fields = fields.get("gQpmTagStatFiledDescArray")
    if not dynamic_fields or not dynamic_fields["columns_by_edition"]:
        raise ValueError("dynamic TAG-stat field descriptor was not parsed")
    dynamic_runtime_columns = {}
    for edition in ("standard", "cluster"):
        columns = [{"name": "_ARRIVAL_TIME", "type": "DATE", "hidden": True, "builtin": "arrival_time"}]
        if edition == "cluster":
            columns.append({"name": "HOSTNAME", "type": "VARCHAR", "hidden": False, "builtin": "hostname"})
        columns.extend(
            {**column, "hidden": False, "builtin": None}
            for column in dynamic_fields["columns_by_edition"][edition]
        )
        columns.append({"name": "_RID", "type": "LONG", "hidden": True, "builtin": "rid"})
        dynamic_runtime_columns[edition] = columns
    return {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "repository": "nfx",
            "revision": revision,
            "registries": [item[1] for item in registry_config],
            "scope": "static fixed tables registered during normal service startup",
        },
        "manual_reference": TABLE_MANUAL.as_posix(),
        "counts": {
            "registered_tables_union": len(tables),
            "registered_tables_standard": edition_counts["standard"],
            "registered_tables_cluster": edition_counts["cluster"],
            "tables_with_korean_reference_heading": sum(
                item["has_korean_reference_heading"] for item in tables
            ),
            "table_variants": sum(len(item["variants"]) for item in tables),
        },
        "tables": tables,
        "dynamic_patterns": [
            {
                "name_pattern": "V$<TAG_TABLE_NAME>_STAT",
                "availability": ["standard", "cluster"],
                "dynamic": True,
                "owner_scope": "tag table owner",
                "source": "qp/src/qpm/qpmTagStat.c:qpmCreateTagStatView",
                "field_descriptor_source": dynamic_fields["source"],
                "declared_columns": dynamic_fields["columns_by_edition"],
                "runtime_columns": dynamic_runtime_columns,
                "note": "Created at runtime and intentionally absent from static registry counts.",
            }
        ],
    }


def decode_c_string(value: str) -> str:
    try:
        tokens = re.findall(r'"(?:\\.|[^"\\])*"', value)
        return "".join(ast.literal_eval(token) for token in tokens)
    except (SyntaxError, ValueError) as exc:
        raise ValueError(f"cannot decode C message string {value!r}") from exc


def error_catalog_cell(value: str) -> str:
    escaped = html.escape(value, quote=True)
    escaped = (
        escaped.replace("|", "&#124;")
        .replace("*", "&#42;")
        .replace("`", "&#96;")
        .replace("[", "&#91;")
        .replace("]", "&#93;")
    )
    escaped = escaped.replace("\r", "&#13;").replace("\n", "&#10;")
    return f"<code>{escaped}</code>"


def render_error_catalog(errors: list[dict], language: str) -> str:
    if language not in {"en", "kr"}:
        raise ValueError(f"unsupported error catalog language: {language}")

    grouped: dict[int, list[dict]] = defaultdict(list)
    for error in errors:
        grouped[(error["id"] // 1000) * 1000].append(error)

    if language == "kr":
        title = "전체 오류 메시지"
        intro = (
            f"다음 {len(errors):,}개 항목은 Machbase 8.7.0 NFX 오류 카탈로그의 "
            "`ERR_ID`, `KEY`, `MSG_EN`을 생성한 결과입니다."
        )
        columns = ("코드", "심볼", "메시지 원문")
    else:
        title = "Complete error message catalog"
        intro = (
            f"The following {len(errors):,} entries are generated from the `ERR_ID`, "
            "`KEY`, and `MSG_EN` fields in the Machbase 8.7.0 NFX error catalog."
        )
        columns = ("Code", "Symbol", "Message")

    lines = [
        '<a id="full-error-catalog"></a>',
        "",
        f"## {title}",
        "",
        intro,
        "",
    ]
    for range_start, entries in sorted(grouped.items()):
        range_end = range_start + 999
        lines.extend(
            [
                f"### `ERR-{range_start:05d}`–`ERR-{range_end:05d}` ({len(entries):,})",
                "",
                f"| {columns[0]} | {columns[1]} | {columns[2]} |",
                "|------|------|------|",
            ]
        )
        for error in entries:
            lines.append(
                "| "
                + " | ".join(
                    (
                        error_catalog_cell(error["code"]),
                        error_catalog_cell(error["key"]),
                        error_catalog_cell(error["message_en"].rstrip()),
                    )
                )
                + " |"
            )
        lines.append("")
    return "\n".join(lines).rstrip()


def replace_generated_error_catalog(text: str, catalog: str) -> str:
    if text.count(ERROR_CATALOG_BEGIN) != 1 or text.count(ERROR_CATALOG_END) != 1:
        raise ValueError("error manual must contain exactly one generated catalog marker pair")
    start = text.index(ERROR_CATALOG_BEGIN) + len(ERROR_CATALOG_BEGIN)
    end = text.index(ERROR_CATALOG_END)
    if end < start:
        raise ValueError("generated error catalog markers are out of order")
    return text[:start] + "\n\n" + catalog.rstrip() + "\n\n" + text[end:]


def generate_errors(nfx_root: Path) -> dict:
    message_path = nfx_root / "pm/src/msg/machbaseErrNLogMsg.msg"
    raw_text = message_path.read_text(encoding="utf-8")
    text = strip_msg_comments(raw_text)
    errors: list[dict] = []
    for id_match in re.finditer(r"\bERR_ID\s*=\s*(\d+)\s*;", text):
        open_at = text.rfind("{", 0, id_match.start())
        body, _ = balanced_block(text, open_at)
        key_match = re.search(r"\bKEY\s*=\s*([A-Z][A-Z0-9_]+)\s*;", body)
        message_matches = re.findall(r'\bMSG_EN\s*=\s*((?:"(?:\\.|[^"\\])*"\s*)+)\s*;', body)
        if not key_match or len(message_matches) != 1:
            raise ValueError(f"incomplete error definition at line {line_number(text, id_match.start())}")
        error_id = int(id_match.group(1))
        code = f"ERR-{error_id:05d}"
        message = decode_c_string(message_matches[0])
        format_tokens = re.findall(
            r"%(?:\d+\$)?[-+#0 ']*(?:\*|\d+)?(?:\.(?:\*|\d+))?"
            r"(?:hh|h|ll|l|j|z|t|L)?[diuoxXfFeEgGaAcspnS%]",
            message,
        )
        unmatched_format = re.sub(
            r"%(?:\d+\$)?[-+#0 ']*(?:\*|\d+)?(?:\.(?:\*|\d+))?"
            r"(?:hh|h|ll|l|j|z|t|L)?[diuoxXfFeEgGaAcspnS%]",
            "",
            message,
        )
        if "%" in unmatched_format:
            raise ValueError(f"unrecognized format token in {code}: {message!r}")
        conversions = [token for token in format_tokens if token != "%%"]
        errors.append(
            {
                "code": code,
                "id": error_id,
                "key": key_match.group(1),
                "message_en": message,
                "format_tokens": format_tokens,
                "conversion_tokens": conversions,
                "listed_in_korean_reference": True,
                "source": f"{relative(message_path, nfx_root)}:{line_number(text, id_match.start())}",
            }
        )
    if len({item["id"] for item in errors}) != len(errors):
        raise ValueError("duplicate ERR_ID values were found")
    if len({item["key"] for item in errors}) != len(errors):
        raise ValueError("duplicate error keys were found")
    if any(item["id"] < 1 or item["id"] > 0xFFFFF for item in errors):
        raise ValueError("ERR_ID is outside the public code range")
    errors.sort(key=lambda item: item["id"])
    return {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "repository": "nfx",
            "revision": git_revision(nfx_root),
            "message_catalog": relative(message_path, nfx_root),
        },
        "manual_reference": ERROR_MANUAL.as_posix(),
        "counts": {
            "error_codes": len(errors),
            "error_codes_listed_in_korean_reference": sum(
                item["listed_in_korean_reference"] for item in errors
            ),
        },
        "errors": errors,
    }


def serialize(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nfx-root", type=Path, required=True, help="path to the NFX source checkout")
    parser.add_argument(
        "--manual-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="path to this manual checkout",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/dbms-reference"),
        help=(
            "generated JSON directory, relative to the manual root by default; "
            "error catalog blocks remain under the manual root"
        ),
    )
    parser.add_argument("--check", action="store_true", help="fail if any generated output is stale")
    args = parser.parse_args()

    nfx_root = args.nfx_root.resolve()
    manual_root = args.manual_root.resolve()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = manual_root / output_dir

    required = [
        nfx_root / "qp/src/qpf/qpf.c",
        nfx_root / "pm/src/msg/machbaseErrNLogMsg.msg",
        manual_root / FUNCTION_MANUAL,
        manual_root / TABLE_MANUAL,
        manual_root / ERROR_MANUAL,
        manual_root / ERROR_MANUAL_EN,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        parser.error(f"required inputs are missing: {', '.join(missing)}")

    error_manifest = generate_errors(nfx_root)
    generated = {
        "functions.json": generate_functions(nfx_root, manual_root),
        "system-tables.json": generate_system_tables(nfx_root, manual_root),
        "errors.json": error_manifest,
    }
    rendered = {name: serialize(value) for name, value in generated.items()}
    error_manuals = {
        ERROR_MANUAL: replace_generated_error_catalog(
            (manual_root / ERROR_MANUAL).read_text(encoding="utf-8"),
            render_error_catalog(error_manifest["errors"], "kr"),
        ),
        ERROR_MANUAL_EN: replace_generated_error_catalog(
            (manual_root / ERROR_MANUAL_EN).read_text(encoding="utf-8"),
            render_error_catalog(error_manifest["errors"], "en"),
        ),
    }

    if args.check:
        stale: list[str] = []
        for name, expected in rendered.items():
            path = output_dir / name
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                stale.append(path.as_posix())
        for relative_path, expected in error_manuals.items():
            path = manual_root / relative_path
            if path.read_text(encoding="utf-8") != expected:
                stale.append(path.as_posix())
        if stale:
            print("stale DBMS reference outputs:", file=sys.stderr)
            for path in stale:
                print(f"  {path}", file=sys.stderr)
            return 1
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        for name, value in rendered.items():
            (output_dir / name).write_text(value, encoding="utf-8")
        for relative_path, value in error_manuals.items():
            (manual_root / relative_path).write_text(value, encoding="utf-8")

    summary = {
        "revision": next(iter(generated.values()))["source"]["revision"],
        "functions": generated["functions.json"]["counts"],
        "system_tables": generated["system-tables.json"]["counts"],
        "errors": generated["errors.json"]["counts"],
        "mode": "check" if args.check else "write",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

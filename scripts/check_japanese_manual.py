#!/usr/bin/env python3
"""Compare Japanese manuals with Korean sources (English for EN-only pages).

Structural failures are errors. Numeric, example and inline-code differences are
review findings: translations may legitimately change comments or anchor links,
but a human must assess them. A clean report is evidence, not semantic signoff.
No source files are modified. Use --json for a machine-readable audit artifact.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit

HANGUL = re.compile(r"[가-힣]")
JAPANESE = re.compile(r"[ぁ-ゖァ-ヺ]")


def split_document(text):
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not match:
        return {}, text
    fields = {}
    for line in match[1].splitlines():
        pair = re.match(r"^([\w-]+)\s*:\s*(.*?)\s*$", line)
        if pair:
            fields[pair[1]] = pair[2]
    return fields, text[match.end():]


def extract_fences(body):
    """Support backticks/tildes, indentation and closing fences longer than open."""
    fences, prose = [], []
    marker = None
    for line in body.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if marker is None:
            if match:
                marker = match[1]
                language = match[2].strip()
                code = []
            else:
                prose.append(line)
        elif match and match[1][0] == marker[0] and len(match[1]) >= len(marker) and not match[2].strip():
            fences.append((language, '\n'.join(code)))
            marker = None
        else:
            code.append(line)
    return fences, '\n'.join(prose), marker is not None


def link_targets(prose):
    # Inline links/images and reference-style definitions; retain fragments.
    return Counter(re.findall(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", prose)
                   + re.findall(r"(?m)^\s*\[[^\]]+\]:\s*(\S+)", prose))


def shortcode_signature(text):
    # Only display attributes may be translated; links, versions and all other
    # technical attributes remain part of the strict structural signature.
    def normalize(match):
        value = match.group(0)
        attributes = 'title|subtitle|caption|alt' + ('|name' if re.match(r'{{[<%]\s*tab\s', value) else '')
        value = re.sub(r'\b(' + attributes + r')\s*=\s*("[^"\n]*"|\'[^\'\n]*\')',
                       lambda attr: attr[1] + '="<localized>"', value)
        # Whitespace between attributes is insignificant; quoted values stay exact.
        tokens = re.findall(r'"[^"\n]*"|\'[^\'\n]*\'|[^\s"\']+', value)
        return ' '.join(tokens)
    return [normalize(match) for match in re.finditer(r'{{[<%].*?[>%]}}', text, re.S)]


def compare_documents(source, target, require_frontmatter=True):
    issues = []
    def add(level, check, detail):
        issues.append(dict(level=level, check=check, detail=detail))
    sf, sb = split_document(source)
    tf, tb = split_document(target)
    for key in (('title', 'weight', 'toc') if require_frontmatter else ()):
        if key not in tf:
            add('error', 'frontmatter', f'missing {key}')
    for key, value in sf.items():
        if key not in ('title', 'description', 'keywords') and tf.get(key) != value:
            add('error', 'frontmatter', f'{key} differs: {value!r} -> {tf.get(key)!r}')
    sc, sp, su = extract_fences(sb)
    tc, tp, tu = extract_fences(tb)
    if tu:
        add('error', 'fences', 'unclosed code fence')
    if [x[0] for x in sc] != [x[0] for x in tc]:
        add('error', 'fences', 'code fence count/languages differ')
    elif sc != tc:
        changed = [i + 1 for i, (a, b) in enumerate(zip(sc, tc)) if a != b]
        add('review', 'code', f'code block contents differ at blocks {changed}')
    signatures = {
        'headings': lambda s: re.findall(r'(?m)^\s{0,3}(#{1,6})\s+', s),
        'anchors': lambda s: re.findall(r'<(?:a|span)\b[^>]*\bid=[\"\']([^\"\']+)[\"\']|\{#([^}]+)\}', s),
        'shortcodes': shortcode_signature,
    }
    for name, signature in signatures.items():
        source_signature, target_signature = signature(sp), signature(tp)
        if name == 'anchors':
            source_signature = [next(part for part in anchor if part) for anchor in source_signature]
            target_signature = [next(part for part in anchor if part) for anchor in target_signature]
            duplicates = {anchor: count for anchor, count in Counter(target_signature).items() if count > 1}
            if duplicates:
                add('error', 'duplicate-anchors', f'duplicate explicit anchors: {duplicates}')
            remaining = iter(target_signature)
            if not all(any(candidate == anchor for candidate in remaining) for anchor in source_signature):
                if not (Counter(source_signature) - Counter(target_signature)):
                    add('review', name, 'source anchors reordered (verify localized deep links)')
                else:
                    add('error', name, 'source anchors missing or reordered')
            elif source_signature != target_signature:
                add('review', name, 'additional explicit anchors (verify localized deep links)')
        elif source_signature != target_signature:
            add('error', name, f'{name} signature differs')
    if link_targets(sp) != link_targets(tp):
        add('review', 'links', 'link destinations differ (verify localized anchors/routes)')
    inline = lambda s: Counter(re.findall(r'(?<!`)`([^`\n]+)`(?!`)', s))
    if inline(sp) != inline(tp):
        add('review', 'inline-code', 'inline code differs (verify identifiers and syntax)')
    html_code = lambda s: Counter(re.findall(r'<code\b[^>]*>(.*?)</code>', s, re.S))
    if html_code(sp) != html_code(tp):
        add('review', 'html-code', 'HTML code contents differ (verify server error messages and identifiers)')
    for line in tp.splitlines():
        # Quoting each dash destroys Markdown table delimiters after localization.
        stripped = line.strip()
        if '`' in stripped and re.fullmatch(r'[|:`\-\s]+', stripped):
            cells = stripped.strip('|').split('|')
            if len(cells) >= 2 and all(re.fullmatch(r'\s*:?-{3,}:?\s*', cell.replace('`', '')) for cell in cells):
                add('error', 'table-delimiter', 'table delimiter contains inline-code backticks')
    table_rows = lambda s: len(re.findall(r'(?m)^\s*\|.*\|\s*$', s))
    if table_rows(sp) != table_rows(tp):
        add('review', 'table-rows', f'table row count differs: {table_rows(sp)} -> {table_rows(tp)}')
    def technical_table_cells(text):
        cells = []
        types = {'int', 'bool', 'boolean', 'string', 'string array', 'obj', 'obj array',
                 'float', 'double', 'long', 'integer', 'int64', 'uint64', 'number'}
        for line in text.splitlines():
            if not line.strip().startswith('|'):
                continue
            row = [part.strip() for part in line.strip().strip('|').split('|')]
            # References commonly format API field names and types as inline code.
            row = [cell[1:-1] if re.fullmatch(r'`[^`]+`', cell) else cell for cell in row]
            if len(row) >= 3 and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', row[0]) and row[1].lower() in types:
                required = row[2] if row[2] in ('', 'O', 'X', '✓', '-', 'true', 'false') else '<description>'
                cells.append((row[0], row[1], required))
        return Counter(cells)
    if technical_table_cells(sp) != technical_table_cells(tp):
        add('review', 'table-types', 'configuration/API table key, type or required marker differs: '
            + f'removed={list((technical_table_cells(sp) - technical_table_cells(tp)).elements())}, '
            + f'added={list((technical_table_cells(tp) - technical_table_cells(sp)).elements())}')
    numbers = lambda s: Counter(re.findall(r'(?<![\w])\d+(?:[.,]\d+)*(?![\w])', s, re.ASCII))
    if numbers(sp) != numbers(tp):
        removed = numbers(sp) - numbers(tp)
        added = numbers(tp) - numbers(sp)
        add('review', 'numbers', f'numeric tokens differ: removed={dict(removed)}, added={dict(added)}')
    # Preserved Korean anchor IDs are markup, not untranslated visible prose.
    visible = re.sub(r'<!--.*?-->|<[^>]*>|\{#[^}]+\}', '', tp, flags=re.S)
    # Korean data in code blocks is valid; Korean prose must be investigated.
    if HANGUL.search(visible) or HANGUL.search(tf.get('title', '')):
        lines = [i for i, line in enumerate(visible.splitlines(), 1) if HANGUL.search(line)]
        add('review', 'korean-prose', f'Korean text remains outside code at prose lines {lines[:20]}')
    if not JAPANESE.search(tp + tf.get('title', '')):
        add('review', 'japanese-prose', 'no Japanese kana found; check untranslated content')
    if sp.strip() == tp.strip() and sp.strip():
        add('review', 'untranslated', 'prose identical to source')
    return issues


def inventory(root):
    sources = {p.relative_to(root).as_posix().replace('.kr.md', ''): p for p in root.rglob('*.kr.md')}
    for path in root.rglob('*.en.md'):
        sources.setdefault(path.relative_to(root).as_posix().replace('.en.md', ''), path)
    for path in root.rglob('*.md'):
        if not path.name.endswith(('.kr.md', '.en.md', '.ja.md')):
            sources.setdefault(path.relative_to(root).as_posix()[:-3], path)
    return sources


DEVELOPER_DOCUMENTS = ('README.md', 'vhs/README.md', 'scripts/DBMS_REFERENCE_MANIFEST.md',
                       'scripts/JAPANESE_MANUAL.md', 'scripts/JAPANESE_MANUAL_REVIEW.md')


def audit(root, repository_root=None, source_policy=None):
    sources = inventory(root)
    policies = (source_policy or {}).get('sources', {})
    files, translated = [], 0
    for key, source in sorted(sources.items()):
        target = root / (key + '.ja.md')
        policy = policies.get(str(target), {})
        if policy.get('primary'):
            source = Path(policy['primary'])
        compared_sources = [source] + [Path(p) for p in policy.get('companions', [])]
        if not source.is_file():
            files.append(dict(source=str(source), target=str(target), findings=[dict(
                level='error', check='missing-source', detail='Selected primary source missing')]))
            continue
        if not target.exists():
            findings = [dict(level='error', check='missing', detail='Japanese page missing')]
        else:
            translated += 1
            findings = compare_documents(source.read_text(), target.read_text(),
                                         require_frontmatter=bool(split_document(source.read_text())[0]))
        if policy.get('integration'):
            for finding in findings:
                if finding['check'] in ('headings', 'fences') and finding['detail'] != 'unclosed code fence':
                    finding['level'] = 'review'
                    finding['detail'] += ' (declared bilingual integration; compare both sources)'
        for finding in findings:
            reason = policy.get('structural_review', {}).get(finding['check'])
            if reason and finding['level'] == 'error' and finding['detail'] != 'unclosed code fence':
                finding['level'] = 'review'
                finding['detail'] += ' (declared source correction: ' + reason + ')'
        for companion in compared_sources[1:]:
            if not companion.is_file():
                findings.append(dict(level='error', check='missing-source', detail=f'Companion source missing: {companion}'))
        if findings:
            page = dict(source=str(source), target=str(target), findings=findings)
            if policy:
                page['compared_sources'] = [str(p) for p in compared_sources]
                page['source_policy'] = policy
            files.append(page)
    if repository_root is not None:
        for relative in DEVELOPER_DOCUMENTS:
            source = repository_root / relative
            target = source.with_name(source.stem + '.ja.md')
            if not source.is_file():
                files.append(dict(source=str(source), target=str(target), findings=[dict(
                    level='error', check='missing-source', detail='Expected developer document missing')]))
                continue
            sources['developer:' + relative] = source
            if target.is_file():
                translated += 1
                findings = compare_documents(source.read_text(), target.read_text(), require_frontmatter=False)
            else:
                findings = [dict(level='error', check='missing', detail='Japanese developer document missing')]
            if findings:
                files.append(dict(source=str(source), target=str(target), findings=findings))
    for target in root.rglob('*.ja.md'):

        key = target.relative_to(root).as_posix().replace('.ja.md', '')
        if key not in sources:
            files.append(dict(target=str(target), findings=[dict(level='review', check='extra', detail='no source counterpart')]))
    counts = Counter(f['level'] for page in files for f in page['findings'])
    return dict(source_pages=len(sources), translated_pages=translated, errors=counts['error'],
                review_findings=counts['review'], files=files)


def finding_fingerprint(finding):
    return hashlib.sha256(json.dumps(finding, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def apply_reviews(report, review_file):
    """Accept only a human review bound to the exact source, target and finding."""
    data = json.loads(review_file.read_text())
    if data.get('schema_version') != 1 or not isinstance(data.get('reviews'), list):
        raise ValueError('review file must have schema_version 1 and a reviews list')
    accepted = 0
    used = set()
    for page in report['files']:
        source, target = Path(page.get('source', '')), Path(page['target'])
        if not source.is_file() or not target.is_file():
            continue
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        target_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        for finding in page['findings']:
            if finding['level'] != 'review':
                continue
            fingerprint = finding_fingerprint(finding)
            companion_hashes = {str(p): hashlib.sha256(Path(p).read_bytes()).hexdigest()
                                for p in page.get('compared_sources', []) if Path(p).is_file()}
            for number, entry in enumerate(data['reviews']):
                if (entry.get('target') == page['target']
                    and entry.get('source_sha256') == source_hash
                    and entry.get('target_sha256') == target_hash
                    and entry.get('finding_sha256') == fingerprint
                    and entry.get('check') == finding['check']
                    and (not companion_hashes or entry.get('compared_source_sha256') == companion_hashes)
                    and isinstance(entry.get('reason'), str) and entry['reason'].strip()
                    and isinstance(entry.get('reviewer'), str) and entry['reviewer'].strip()):
                    finding['disposition'] = 'approved'
                    finding['review_reason'] = entry['reason']
                    accepted += 1
                    used.add(number)
                    break
    report['approved_review_findings'] = accepted
    report['pending_review_findings'] = report['review_findings'] - accepted
    report['unused_review_entries'] = len(data['reviews']) - len(used)
    return report


class PageHTML(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.main_links = []
        self.main_depth = 0
        self.redirects = []
        self.lang = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'main':
            self.main_depth += 1
        if tag == 'a' and self.main_depth and 'href' in attrs:
            self.main_links.append(attrs['href'])
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a' and 'name' in attrs:
            self.ids.add(attrs['name'])
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag in ('a', 'link') and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag in ('img', 'script') and 'src' in attrs:
            self.links.append(attrs['src'])
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            match = re.search(r'url\s*=\s*(.*)', attrs.get('content', ''), re.I)
            if match:
                self.redirects.append(match[1].strip())

    def handle_endtag(self, tag):
        if tag == 'main':
            self.main_depth = max(0, self.main_depth - 1)


def localized_markdown_body(text):
    """Expected JA export: preserve code; localize site-relative DBMS links."""
    _, body = split_document(text)
    lines, fence = [], None
    for line in body.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not match[2].strip():
                fence = None
        elif fence is None:
            def localize(match):
                target = match[1]
                tail = re.sub(r'^/(?:dbms-8\.5|dbms|neo|apps|fluid)', '', urlsplit(target).path)
                if Path(tail.rstrip('/')).suffix:
                    return match[0]
                return '](/ja' + target
            line = re.sub(r'\]\((/(?:dbms-8\.5|dbms|neo|apps|fluid)(?=/|#|\?|\))[^\s)]*)', localize, line)
        lines.append(line)
    return '\n'.join(lines).strip()


def source_for_url(source_root, url):
    prefix = '/ja/' if source_root.name == 'content' else '/ja/dbms/'
    path = unquote(urlsplit(url).path).removeprefix(prefix).strip('/')
    candidates = [source_root / (path + '.ja.md'), source_root / path / '_index.ja.md', source_root / path / 'index.ja.md'] if path else [source_root / '_index.ja.md']
    exact = next((path for path in candidates if path.is_file()), None)
    if exact is not None:
        return exact
    # Hugo lowercases canonical paths even when source filenames use camelCase.
    folded = {str(path).casefold() for path in candidates}
    return next((path for path in source_root.rglob('*.ja.md') if str(path).casefold() in folded), None)


def audit_rendered(public_dir, expected_pages, source_root=None, sections=('dbms',), landing='/ja/dbms/'):
    findings = []
    def add(check, target, detail):
        findings.append(dict(level='error', check=check, target=str(target), detail=detail))
    japanese_root = public_dir / 'ja'
    if not japanese_root.is_dir():
        return dict(pages=0, links_checked=0, findings=[dict(level='error', check='rendered-root', target=str(japanese_root), detail='Japanese output directory missing')])
    parsed = {}
    def read_page(path):
        if path not in parsed:
            parsed[path] = PageHTML(path.read_text())
        return parsed[path]
    # Hugo emits alias redirect pages alongside canonical documents.
    pages = [p for section in sections for p in sorted((japanese_root / section).rglob('index.html')) if not read_page(p).redirects]
    if len(pages) != expected_pages:
        add('rendered-inventory', japanese_root, f'expected {expected_pages} document pages, found {len(pages)}')
    checked = 0
    for page in sorted(japanese_root.rglob('*.html')):
        html = read_page(page)
        if html.lang not in ('ja', 'ja-JP'):
            add('html-language', page, f'HTML lang is {html.lang!r}')
        relative = '/' + page.relative_to(public_dir).as_posix()
        for href in html.links + html.redirects:
            url = urlsplit(urljoin('https://docs.machbase.com' + relative, href))
            if url.scheme not in ('http', 'https') or url.netloc != 'docs.machbase.com':
                continue
            checked += 1
            target = public_dir / unquote(url.path).lstrip('/')
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                add('broken-link', page, href)
            elif url.fragment and target.suffix == '.html' and unquote(url.fragment) not in read_page(target).ids:
                add('broken-fragment', page, href)
        for href in html.main_links:
            url = urlsplit(urljoin('https://docs.machbase.com' + relative, href))
            if url.scheme not in ('http', 'https') or url.netloc != 'docs.machbase.com':
                continue
            path = unquote(url.path)
            match = re.match(r'^/(?:kr/)?(dbms-8\.5|dbms|neo|apps)(/.*|$)', path)
            if match is None or Path(match[2].rstrip('/')).suffix:
                continue
            counterpart = japanese_root / match[1] / match[2].strip('/') / 'index.html'
            if counterpart.is_file() and not read_page(counterpart).redirects:
                add('unlocalized-page-link', page, href)
    home = japanese_root / 'index.html'
    if not home.is_file() or landing not in read_page(home).redirects:
        add('landing', home, f'Japanese home must redirect to {landing}')
    # Root AI corpus remains the explicit DBMS product contract. Other products
    # still require fresh page-level Markdown exports and localized search.
    ai_pages = [p for p in pages if p.is_relative_to(japanese_root / 'dbms')]
    if len(sections) > 1 and source_root is not None:
        for page in pages:
            url = '/' + page.parent.relative_to(public_dir).as_posix() + '/'
            source = source_for_url(source_root, url)
            exported_path = (page.with_name('index.md') if source is None or source.name == '_index.ja.md'
                             else page.parent.parent / (page.parent.name + '.md'))
            if not exported_path.is_file():
                add('markdown-export', page, 'missing Japanese page-level Markdown export')
            elif source is None:
                add('markdown-source', page, 'no Japanese source for page-level export')
            elif exported_path.read_text().partition('\n')[2].strip() != localized_markdown_body(source.read_text()):
                add('stale-markdown', source, 'exported body differs from current Japanese source')
    chunks = japanese_root / 'llms-chunks.json'
    if not chunks.is_file():
        add('llms-index', chunks, 'missing Japanese document index')
    else:
        try:
            index = json.loads(chunks.read_text())
            docs = index.get('documents', [])
            if index.get('language') != 'ja' or index.get('document_count') != len(ai_pages) or len(docs) != len(ai_pages):
                add('llms-inventory', chunks, 'language/document count mismatch')
            urls = [urlsplit(doc.get('url', '')).path for doc in docs]
            rendered_urls = ['/' + p.parent.relative_to(public_dir).as_posix() + '/' for p in ai_pages]
            if Counter(urls) != Counter(rendered_urls):
                add('llms-urls', chunks, 'document URLs differ from rendered Japanese pages')
            for doc in docs:
                markdown_path = urlsplit(doc.get('markdown_url', '')).path
                if not any(markdown_path.startswith('/ja/' + section + '/') for section in sections) or not (public_dir / unquote(markdown_path).lstrip('/')).is_file():
                    add('markdown-export', chunks, f"missing Japanese Markdown export: {doc.get('markdown_url', '')}")
                elif source_root is not None:
                    source = source_for_url(source_root, doc.get('url', ''))
                    if source is None:
                        add('markdown-source', chunks, f"no Japanese source for {doc.get('url', '')}")
                    else:
                        exported = (public_dir / unquote(markdown_path).lstrip('/')).read_text().partition('\n')[2].strip()
                        if exported != localized_markdown_body(source.read_text()):
                            add('stale-markdown', source, 'exported body differs from current Japanese source')
        except (ValueError, TypeError) as exc:
            add('llms-index', chunks, str(exc))
    for name in ('llms.txt', 'llms-full.txt'):
        path = japanese_root / name
        if not path.is_file():
            add('llms-text', path, 'missing Japanese AI output')
            continue
        text = path.read_text()
        if not JAPANESE.search(text[:1500]):
            add('llms-language', path, 'Japanese introduction missing')
        if name == 'llms-full.txt':
            markers = re.findall(r'<!-- document: ([^ ]+) -->', text)
            expected_urls = ['/' + p.parent.relative_to(public_dir).as_posix() + '/' for p in ai_pages]
            if Counter(markers) != Counter(expected_urls):
                add('llms-full-inventory', path, 'full text document markers differ from Japanese pages')
            if source_root is not None:
                for match in re.finditer(r'<!-- document: ([^ ]+) -->(.*?)(?=<!-- document: |\Z)', text, re.S):
                    source = source_for_url(source_root, match[1])
                    document = re.split(r'(?m)^# [^\n]*\n', match[2], maxsplit=1)
                    if source is None or len(document) != 2 or document[1].strip() != localized_markdown_body(source.read_text()):
                        add('stale-llms-full', path, f'full text body differs from current Japanese source: {match[1]}')
    return dict(pages=len(pages), links_checked=checked, findings=findings)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('content/dbms'))
    parser.add_argument('--all-documents', action='store_true', help='audit all content plus developer documentation')
    parser.add_argument('--landing', default='/ja/neo/', help='expected landing for all-document mode')
    parser.add_argument('--expected-rendered-pages', type=int, help='published source count after Hugo draft/ignore rules')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--public-dir', type=Path, help='also audit built Japanese pages and AI outputs')
    parser.add_argument('--source-policy', type=Path, help='primary/companion sources for bilingual integration')
    parser.add_argument('--review-file', type=Path, help='human dispositions bound to exact source/target hashes')
    args = parser.parse_args()
    if args.all_documents:
        args.root = Path('content')
    policy = json.loads(args.source_policy.read_text()) if args.source_policy else None
    report = audit(args.root, Path('.') if args.all_documents else None, policy)
    if args.review_file:
        try:
            apply_reviews(report, args.review_file)
        except (OSError, ValueError, TypeError) as exc:
            parser.error(str(exc))
    if args.public_dir:
        report['rendered'] = audit_rendered(args.public_dir, args.expected_rendered_pages if args.expected_rendered_pages is not None else report['source_pages'], args.root,
            sections=('dbms', 'dbms-8.5', 'neo', 'apps') if args.all_documents else ('dbms',),
            landing=args.landing if args.all_documents else '/ja/dbms/')
        report['errors'] += len(report['rendered']['findings'])
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Japanese pages: {report['translated_pages']}/{report['source_pages']}; errors: {report['errors']}; review findings: {report['review_findings']}")
        if args.review_file:
            print(f"Approved: {report['approved_review_findings']}; pending: {report['pending_review_findings']}; unused/stale entries: {report['unused_review_entries']}")
        for page in report['files']:
            for finding in page['findings']:
                print(f"{page['target']}: {finding['level']} {finding['check']}: {finding['detail']}")
        if 'rendered' in report:
            print(f"Rendered pages: {report['rendered']['pages']}; links checked: {report['rendered']['links_checked']}")
            for finding in report['rendered']['findings']:
                print(f"{finding['target']}: {finding['check']}: {finding['detail']}")
    return 1 if report['errors'] or report.get('pending_review_findings', report['review_findings']) else 0


if __name__ == '__main__':
    raise SystemExit(main())

import importlib.util
import json
import hashlib
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('check_japanese_manual', Path(__file__).resolve().parents[1] / 'check_japanese_manual.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

SOURCE = '''---
title: 시작
weight: 10
toc: true
---
## 연결 {#connect}
포트 5656으로 `machsql`을 사용합니다. [참고](../reference/)
{{< callout type="info" >}}
확인합니다.
{{< /callout >}}
```sql
SELECT * FROM sensor;
```
'''
TARGET = SOURCE.replace('시작', '開始').replace('연결', '接続').replace('포트 5656으로 `machsql`을 사용합니다.', 'ポート5656で`machsql`を使用します。').replace('참고', '参照').replace('확인합니다.', '確認します。')

class TranslationAuditTest(unittest.TestCase):
    def checks(self, text):
        return {f['check'] for f in MODULE.compare_documents(SOURCE, text)}

    def test_preserved_markdown_korean_anchor_is_not_visible_prose(self):
        findings = MODULE.compare_documents(SOURCE, TARGET + "\n## 追加 {#한국어-앵커}")
        self.assertNotIn("korean-prose", {f["check"] for f in findings})

    def test_duplicate_explicit_anchor_is_an_error(self):
        findings = MODULE.compare_documents(SOURCE, TARGET + '\n<a id="connect"></a>')
        self.assertTrue(any(f["check"] == "duplicate-anchors" and f["level"] == "error" for f in findings))

    def test_configuration_type_change_is_detected(self):
        findings = MODULE.compare_documents(SOURCE + "\n| AccessPolicy | obj array | O | 원문 |", TARGET + "\n| AccessPolicy | string | O | 設定 |")
        self.assertIn("table-types", {f["check"] for f in findings})

    def test_inline_formatted_api_keys_and_types_are_checked(self):
        for key in ('name', '`name`'):
            source = SOURCE + f"\n| {key} | `string` | 원문 |"
            valid = TARGET + f"\n| {key} | `string` | 説明 |"
            self.assertNotIn('table-types', {f['check'] for f in MODULE.compare_documents(source, valid)})
            invalid = TARGET + "\n| 名前 | `string` | 説明 |"
            self.assertIn('table-types', {f['check'] for f in MODULE.compare_documents(source, invalid)})
            wrong_type = TARGET + f"\n| {key} | `number` | 説明 |"
            self.assertIn('table-types', {f['check'] for f in MODULE.compare_documents(source, wrong_type)})

    def test_yaml_space_before_colon_is_valid(self):
        self.assertEqual(MODULE.compare_documents(SOURCE.replace("title:", "title :"), TARGET.replace("title:", "title :")), [])

    def test_quoted_dashes_do_not_count_as_valid_table_delimiters(self):
        table = "\n| 項目 | 説明 |\n|---|---|\n| x | y |\n"
        broken = table.replace("|---|---|", "|`-``-``-`|`-``-``-`|")
        self.assertIn('table-delimiter', {f['check'] for f in MODULE.compare_documents(SOURCE + table, TARGET + broken)})
        self.assertNotIn('table-delimiter', {f['check'] for f in MODULE.compare_documents(SOURCE + table, TARGET + table)})
        literal = "\n| `-` | `-` |\n"
        self.assertNotIn('table-delimiter', {f['check'] for f in MODULE.compare_documents(SOURCE + literal, TARGET + literal)})

    def test_equivalent_translation_is_clean(self):
        self.assertEqual(MODULE.compare_documents(SOURCE, TARGET), [])

    def test_numeric_change_requires_review(self):
        self.assertIn('numbers', self.checks(TARGET.replace('5656', '5657')))

    def test_sql_identifier_change_requires_review(self):
        self.assertIn('code', self.checks(TARGET.replace('sensor;', 'sensors;')))

    def test_broken_fence_is_error(self):
        findings = MODULE.compare_documents(SOURCE, TARGET.rsplit('```', 1)[0])
        self.assertTrue(any(f['check'] == 'fences' and f['level'] == 'error' for f in findings))

    def test_heading_and_explicit_anchor_loss_is_error(self):
        self.assertTrue({'headings', 'anchors'} <= self.checks(TARGET.replace('## 接続 {#connect}', '# 接続')))

    def test_new_anchor_is_reviewable_but_original_must_remain(self):
        findings = MODULE.compare_documents(SOURCE, TARGET + '<a id="追加"></a>')
        self.assertEqual([f['level'] for f in findings if f['check'] == 'anchors'], ['review'])
        findings = MODULE.compare_documents(SOURCE, TARGET.replace('{#connect}', '{#new}'))
        self.assertEqual([f['level'] for f in findings if f['check'] == 'anchors'], ['error'])

    def test_link_change_and_untranslated_text_require_review(self):
        self.assertIn('links', self.checks(TARGET.replace('../reference/', '../wrong/')))
        self.assertIn('korean-prose', self.checks(SOURCE))
        self.assertIn('untranslated', self.checks(SOURCE))

    def test_frontmatter_and_shortcode_changes_are_errors(self):
        self.assertIn('frontmatter', self.checks(TARGET.replace('weight: 10', 'weight: 20')))
        self.assertIn('shortcodes', self.checks(TARGET.replace('type="info"', 'type="warning"')))

    def test_html_error_message_change_requires_review(self):
        source = SOURCE + '<code>ERR-00001: invalid value %s</code>'
        target = TARGET + '<code>ERR-00001: invalid value %d</code>'
        findings = MODULE.compare_documents(source, target)
        self.assertIn('html-code', {f['check'] for f in findings})

    def test_missing_table_row_requires_review(self):
        source = SOURCE + '\n| A | B |\n| C | D |\n'
        target = TARGET + '\n| A | B |\n'
        findings = MODULE.compare_documents(source, target)
        self.assertIn('table-rows', {f['check'] for f in findings})

    def test_inventory_includes_english_only_and_prefers_korean(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'one.kr.md').write_text(SOURCE)
            (root / 'one.en.md').write_text(SOURCE)
            (root / 'two.en.md').write_text(SOURCE)
            (root / 'one.ja.md').write_text(TARGET)
            result = MODULE.audit(root)
            self.assertEqual(result['source_pages'], 2)
            self.assertEqual(result['translated_pages'], 1)
            self.assertEqual(result['errors'], 1)
            self.assertEqual(MODULE.inventory(root)['one'].suffixes, ['.kr', '.md'])

    def test_preserved_korean_anchor_is_not_untranslated_prose(self):
        source = SOURCE + '<a id="접속-방법"></a>'
        target = TARGET + '<a id="접속-방법"></a>'
        self.assertEqual(MODULE.compare_documents(source, target), [])

    def test_korean_sample_data_in_fence_is_allowed(self):
        source = SOURCE.replace('SELECT * FROM sensor;', "SELECT '한국어';")
        target = TARGET.replace('SELECT * FROM sensor;', "SELECT '한국어';")
        self.assertEqual(MODULE.compare_documents(source, target), [])

class ExtendedSourceAuditTest(unittest.TestCase):
    def test_shortcode_display_translation_preserves_technical_attributes(self):
        source = SOURCE + '{{< card title="안내" link="/neo/" >}}\n{{< tab name="연결" >}}'
        target = TARGET + '{{< card title="ガイド" link="/neo/" >}}\n{{< tab name="接続" >}}'
        self.assertNotIn('shortcodes', {f['check'] for f in MODULE.compare_documents(source, target)})
        self.assertIn('shortcodes', {f['check'] for f in MODULE.compare_documents(source, target.replace('/neo/', '/apps/'))})
        self.assertNotEqual(MODULE.shortcode_signature('{{< param name="one" >}}'),
                            MODULE.shortcode_signature('{{< param name="two" >}}'))

    def test_assets_are_not_localized_in_markdown_exports(self):
        for target in ('/neo/tql/img/map.jpg', '/neo/img/a.svg#part', '/neo/file.csv?raw=1'):
            text = f'[画像]({target})'
            self.assertEqual(MODULE.localized_markdown_body(text), text)

    def test_bilingual_review_binds_both_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'one.kr.md'
            companion = root / 'one.en.md'
            target = root / 'one.ja.md'
            source.write_text(SOURCE)
            companion.write_text(SOURCE + '\n## Extra\nMore.')
            target.write_text(TARGET + '\n## 追加\n説明です。')
            policy = {'sources': {str(target): {'primary': str(source), 'companions': [str(companion)], 'integration': True}}}
            result = MODULE.audit(root, source_policy=policy)
            self.assertEqual(result['errors'], 0)
            finding = result['files'][0]['findings'][0]
            entry = dict(target=str(target), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                         target_sha256=hashlib.sha256(target.read_bytes()).hexdigest(), check=finding['check'],
                         finding_sha256=MODULE.finding_fingerprint(finding), reviewer='fixture', reason='Compared both.',
                         compared_source_sha256={str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (source, companion)})
            reviews = root / 'reviews.json'
            reviews.write_text(json.dumps({'schema_version': 1, 'reviews': [entry]}))
            self.assertEqual(MODULE.apply_reviews(result, reviews)['pending_review_findings'], 0)
            companion.write_text(companion.read_text() + '\nChanged source.')
            self.assertEqual(MODULE.apply_reviews(MODULE.audit(root, source_policy=policy), reviews)['approved_review_findings'], 0)


class WholeRepositoryAuditTest(unittest.TestCase):
    def test_plain_document_is_required_and_needs_no_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'guide-en.md').write_text('## Connect\nUse the server.')
            (root / 'guide-ko.md').write_text('## 연결\n서버를 사용합니다.')
            (root / 'guide-en.ja.md').write_text('## 接続\nサーバーを使用します。')
            result = MODULE.audit(root)
            self.assertEqual(result['source_pages'], 2)
            self.assertEqual(result['translated_pages'], 1)
            self.assertEqual(result['errors'], 1)
            (root / 'guide-ko.ja.md').write_text('## 接続\nサーバーを使用します。')
            self.assertEqual(MODULE.audit(root)['errors'], 0)

    def test_developer_documents_cannot_silently_disappear(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / 'content'
            content.mkdir()
            result = MODULE.audit(content, root)
            self.assertEqual(result['errors'], len(MODULE.DEVELOPER_DOCUMENTS))
            for name in MODULE.DEVELOPER_DOCUMENTS:
                source = root / name
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text('## Setup\nRun the command.')
                source.with_name(source.stem + '.ja.md').write_text('## 設定\nコマンドを実行します。')
            result = MODULE.audit(content, root)
            self.assertEqual(result['source_pages'], len(MODULE.DEVELOPER_DOCUMENTS))
            self.assertEqual(result['errors'], 0)

    def test_all_section_export_localization(self):
        for section in ('neo', 'apps', 'dbms', 'dbms-8.5', 'fluid'):
            for suffix in ('/guide/', '/', '/#setup', '?view=all'):
                self.assertEqual(MODULE.localized_markdown_body(f'[参照](/{section}{suffix})'),
                                 f'[参照](/ja/{section}{suffix})')

    def test_content_root_resolves_each_product_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'content'
            for section in ('neo', 'apps', 'dbms', 'dbms-8.5'):
                source = root / section / '_index.ja.md'
                source.parent.mkdir(parents=True)
                source.write_text('日本語です。')
                self.assertEqual(MODULE.source_for_url(root, '/ja/' + section + '/'), source)


class ReviewDispositionTest(unittest.TestCase):
    def fixture(self, root):
        source = root / 'one.kr.md'
        target = root / 'one.ja.md'
        source.write_text(SOURCE)
        target.write_text(TARGET.replace('5656', '5657'))
        report = MODULE.audit(root)
        finding = report['files'][0]['findings'][0]
        review = dict(target=str(target), check=finding['check'], source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), target_sha256=hashlib.sha256(target.read_bytes()).hexdigest(), finding_sha256=MODULE.finding_fingerprint(finding), reason='Fixture: approved documented port correction.', reviewer='test reviewer')
        path = root / 'reviews.json'
        path.write_text(json.dumps(dict(schema_version=1, reviews=[review])))
        return source, target, path

    def test_exact_review_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, _, path = self.fixture(root)
            result = MODULE.apply_reviews(MODULE.audit(root), path)
            self.assertEqual(result['approved_review_findings'], 1)
            self.assertEqual(result['pending_review_findings'], 0)

    def test_target_or_source_edit_invalidates_approval(self):
        for source_edit in (False, True):
            with self.subTest(source_edit=source_edit), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                source, target, path = self.fixture(root)
                changed = source if source_edit else target
                changed.write_text(changed.read_text() + '\n')
                result = MODULE.apply_reviews(MODULE.audit(root), path)
                self.assertEqual(result['approved_review_findings'], 0)
                self.assertEqual(result['pending_review_findings'], 1)

    def test_new_finding_cannot_reuse_existing_fingerprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, target, path = self.fixture(root)
            target.write_text(target.read_text().replace('machsql', 'wrongsql'))
            data = json.loads(path.read_text())
            # Even updating the document hash cannot approve a new finding.
            data['reviews'][0]['target_sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
            path.write_text(json.dumps(data))
            result = MODULE.apply_reviews(MODULE.audit(root), path)
            self.assertEqual(result['approved_review_findings'], 1)
            self.assertEqual(result['pending_review_findings'], 1)

class RenderedAuditTest(unittest.TestCase):
    def build_fixture(self, root):
        ja = root / 'ja'
        dbms = ja / 'dbms'
        dbms.mkdir(parents=True)
        (ja / 'index.html').write_text('<html lang="ja-JP"><meta http-equiv="Refresh" content="0; url=/ja/dbms/"></html>')
        (dbms / 'index.html').write_text('<html lang="ja"><a href="#接続">接続</a><h2 id="接続">接続</h2></html>')
        (ja / 'llms-chunks.json').write_text(json.dumps(dict(language='ja', document_count=1, documents=[dict(url='https://docs.machbase.com/ja/dbms/', markdown_url='https://docs.machbase.com/ja/dbms/index.md')]), ensure_ascii=False))
        (dbms / 'index.md').write_text('日本語のマニュアル')
        (ja / 'llms.txt').write_text('日本語のマニュアル')
        (ja / 'llms-full.txt').write_text('日本語のマニュアル\n<!-- document: /ja/dbms/ -->')
        return dbms / 'index.html'

    def test_complete_rendered_site_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_fixture(root)
            self.assertEqual(MODULE.audit_rendered(root, 1)['findings'], [])

    def test_flat_product_markdown_export_is_checked_at_hugo_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_fixture(root)
            source = root / 'content/neo'
            source.mkdir(parents=True)
            (source / 'topic.ja.md').write_text(TARGET)
            page = root / 'ja/neo/topic'
            page.mkdir(parents=True)
            (page / 'index.html').write_text('<html lang="ja"></html>')
            exported = page.parent / 'topic.md'
            exported.write_text('# 開始\n' + MODULE.localized_markdown_body(TARGET))
            result = MODULE.audit_rendered(root, 2, root / 'content', sections=('dbms', 'neo'))
            self.assertFalse(any(f['check'] in ('markdown-export', 'stale-markdown') and 'neo' in f['target'] for f in result['findings']))
            exported.write_text('# 開始\n古い本文')
            result = MODULE.audit_rendered(root, 2, root / 'content', sections=('dbms', 'neo'))
            self.assertTrue(any(f['check'] == 'stale-markdown' and 'neo' in f['target'] for f in result['findings']))
            exported.unlink()
            result = MODULE.audit_rendered(root, 2, root / 'content', sections=('dbms', 'neo'))
            self.assertTrue(any(f['check'] == 'markdown-export' and 'neo' in f['target'] for f in result['findings']))

    def test_leaf_bundle_and_camelcase_markdown_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_fixture(root)
            source = root / 'content/neo'
            (source / 'bundle').mkdir(parents=True)
            (source / 'bundle/index.ja.md').write_text(TARGET)
            (source / 'parseArgs.ja.md').write_text(TARGET)
            for name in ('bundle', 'parseargs'):
                page = root / 'ja/neo' / name
                page.mkdir(parents=True)
                (page / 'index.html').write_text('<html lang="ja"></html>')
                (page.parent / (name + '.md')).write_text('# 開始\n' + MODULE.localized_markdown_body(TARGET))
            result = MODULE.audit_rendered(root, 3, root / 'content', sections=('dbms', 'neo'))
            self.assertFalse(any(f['check'] in ('markdown-export', 'markdown-source', 'stale-markdown') and 'neo' in f['target'] for f in result['findings']))
            self.assertEqual(MODULE.source_for_url(root / 'content', '/ja/neo/parseargs/'), source / 'parseArgs.ja.md')

    def test_main_links_keep_japanese_locale_but_language_switches_are_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = self.build_fixture(root)
            original = root / 'dbms'
            original.mkdir()
            (original / 'index.html').write_text('<html lang="en"></html>')
            page.write_text('<html lang="ja"><nav><a href="/dbms/">English</a></nav><main><a href="/dbms/">記事</a></main></html>')
            result = MODULE.audit_rendered(root, 1)
            self.assertEqual(len([f for f in result['findings'] if f['check'] == 'unlocalized-page-link']), 1)
            page.write_text('<html lang="ja"><nav><a href="/dbms/">English</a></nav><main><a href="/ja/dbms/">記事</a></main></html>')
            result = MODULE.audit_rendered(root, 1)
            self.assertFalse(any(f['check'] == 'unlocalized-page-link' for f in result['findings']))

    def test_alias_redirect_is_valid_but_not_counted_as_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_fixture(root)
            alias = root / 'ja/dbms/old'
            alias.mkdir()
            (alias / 'index.html').write_text('<html lang="ja"><meta http-equiv="refresh" content="0; url=/ja/dbms/"></html>')
            result = MODULE.audit_rendered(root, 1)
            self.assertEqual(result['pages'], 1)
            self.assertEqual(result['findings'], [])

    def test_missing_markdown_export_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_fixture(root)
            (root / 'ja/dbms/index.md').unlink()
            result = MODULE.audit_rendered(root, 1)
            self.assertIn('markdown-export', {f['check'] for f in result['findings']})

    def test_stale_export_and_full_text_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_fixture(root)
            sources = root / 'source'
            sources.mkdir()
            (sources / '_index.ja.md').write_text('---\ntitle: マニュアル\nweight: 1\ntoc: true\n---\n最新版です。')
            result = MODULE.audit_rendered(root, 1, sources)
            self.assertTrue({'stale-markdown', 'stale-llms-full'} <= {f['check'] for f in result['findings']})
            (root / 'ja/dbms/index.md').write_text('# マニュアル\n最新版です。')
            (root / 'ja/llms-full.txt').write_text('日本語のマニュアル\n<!-- document: /ja/dbms/ -->\n---\nlanguage: ja\n---\n# マニュアル\n最新版です。')
            self.assertEqual(MODULE.audit_rendered(root, 1, sources)['findings'], [])

    def test_export_localization_preserves_code_literals(self):
        text = '---\ntitle: テスト\n---\n[参照](/dbms/reference/)\n```text\n[サンプル](/dbms/reference/)\n```'
        expected = '[参照](/ja/dbms/reference/)\n```text\n[サンプル](/dbms/reference/)\n```'
        self.assertEqual(MODULE.localized_markdown_body(text), expected)

    def test_missing_fragment_file_and_bad_language_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = self.build_fixture(root)
            page.write_text('<html lang="en"><a href="#missing">anchor</a><a href="gone/">missing page</a></html>')
            findings = MODULE.audit_rendered(root, 1)['findings']
            self.assertTrue({'broken-fragment', 'broken-link', 'html-language'} <= {f['check'] for f in findings})

    def test_wrong_llm_language_and_incomplete_corpus_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_fixture(root)
            (root / 'ja/llms-chunks.json').write_text(json.dumps(dict(language='en', document_count=0, documents=[])))
            (root / 'ja/llms-full.txt').write_text('English manual')
            findings = MODULE.audit_rendered(root, 1)['findings']
            self.assertTrue({'llms-inventory', 'llms-urls', 'llms-language', 'llms-full-inventory'} <= {f['check'] for f in findings})

if __name__ == '__main__':
    unittest.main()

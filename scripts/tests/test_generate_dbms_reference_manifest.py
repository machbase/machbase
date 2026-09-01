import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "generate_dbms_reference_manifest.py"
SPEC = importlib.util.spec_from_file_location("dbms_reference_manifest", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class MessageLexerTest(unittest.TestCase):
    def test_hash_comment_does_not_override_active_message(self):
        source = '''
{
    ERR_ID = 2282;
    KEY = ERR_QP_DELETE_ALREADY_DOING;
#   MSG_EN = "old %s";
    MSG_EN = "active %s";
}
'''
        cleaned = MODULE.strip_msg_comments(source)
        self.assertNotIn("old %s", cleaned)
        self.assertIn('MSG_EN = "active %s";', cleaned)
        self.assertEqual(source.count("\n"), cleaned.count("\n"))

    def test_adjacent_literals_are_concatenated(self):
        self.assertEqual(MODULE.decode_c_string('"line 1\\n" "line 2"'), "line 1\nline 2")


class ErrorCatalogRenderTest(unittest.TestCase):
    def test_html_cell_preserves_markdown_special_characters(self):
        self.assertEqual(
            MODULE.error_catalog_cell("value<%s>|`next`\nline"),
            "<code>value&lt;%s&gt;&#124;&#96;next&#96;&#10;line</code>",
        )

    def test_html_cell_prevents_typographic_quote_replacement(self):
        self.assertEqual(
            MODULE.error_catalog_cell("file's \"name\""),
            "<code>file&#x27;s &quot;name&quot;</code>",
        )

    def test_html_cell_preserves_markdown_emphasis(self):
        self.assertEqual(
            MODULE.error_catalog_cell("(*NOT USED*)"),
            "<code>(&#42;NOT USED&#42;)</code>",
        )

    def test_catalog_is_grouped_and_sorted_by_range(self):
        errors = [
            {"id": 1001, "code": "ERR-01001", "key": "ERR_B", "message_en": "second"},
            {"id": 1, "code": "ERR-00001", "key": "ERR_A", "message_en": "first"},
        ]
        catalog = MODULE.render_error_catalog(errors, "en")
        self.assertIn("### `ERR-00000`–`ERR-00999` (1)", catalog)
        self.assertIn("### `ERR-01000`–`ERR-01999` (1)", catalog)
        self.assertLess(catalog.index("ERR-00001"), catalog.index("ERR-01001"))

    def test_generated_marker_replacement_is_stable(self):
        source = (
            "before\n"
            + MODULE.ERROR_CATALOG_BEGIN
            + "\nold\n"
            + MODULE.ERROR_CATALOG_END
            + "\nafter\n"
        )
        expected = (
            "before\n"
            + MODULE.ERROR_CATALOG_BEGIN
            + "\n\nnew\n\n"
            + MODULE.ERROR_CATALOG_END
            + "\nafter\n"
        )
        self.assertEqual(MODULE.replace_generated_error_catalog(source, "new"), expected)

    def test_generated_marker_pair_is_required(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            MODULE.replace_generated_error_catalog("no markers", "catalog")


if __name__ == "__main__":
    unittest.main()

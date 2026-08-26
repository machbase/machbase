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


if __name__ == "__main__":
    unittest.main()

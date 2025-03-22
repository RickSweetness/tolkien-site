import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_header(self):
        md = "# header"
        self.assertEqual(extract_title(md), "header")

    def test_extract_header_error(self):
        with self.assertRaises(Exception):
            md = "## header\nheader"
            extract_title(md)

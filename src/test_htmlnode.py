import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("a", "click here", None, {"href": "https://www.google.com"})
        with self.assertRaises(NotImplementedError):
            node.to_html()


    def test_initialization(self):
        node = HTMLNode("a", "click here", None, {"href": "https://www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "click here")
        self.assertIsNone(node.children)  # Children is None
        self.assertEqual(node.props, {"href": "https://www.google.com"})  # props dictionary

    def test_props_to_html(self):
        node = HTMLNode("a", "click here", None, {
            "href": "https://www.google.com",
            "target": "_blank"
        })
        # Expected result should match the HTML format
        props_html = node.props_to_html()
        self.assertEqual(props_html, ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()

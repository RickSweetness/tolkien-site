import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This is a link node", TextType.LINK, "website.com")
        node2 = TextNode("This is a link node", TextType.LINK, "website.com")
        self.assertEqual(node, node2)
    
    def test_eq_url_none(self):
        node = TextNode("This is a link node", TextType.LINK, None)
        node2 = TextNode("This is a link node", TextType.LINK)
        self.assertEqual(node, node2)

 



if __name__ == "__main__":
    unittest.main() 
import unittest

from leafnode import LeafNode

from textnode import TextNode, TextType, text_node_to_html_node

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_w_dict(self):
        node = LeafNode("p", "click here", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com">click here</p>')


#BELOW HERE IS TEXTNODE TO LEAFNODE TESTS

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_node(self):
        text_node = TextNode(text_type=TextType.BOLD, text="Bold Text", url=None)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold Text")
        self.assertIsNone(html_node.props)

    def test_italic_node(self):
        text_node = TextNode(text_type=TextType.ITALIC, text="Italic Text", url=None)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic Text")
        self.assertIsNone(html_node.props)

    def test_code_node(self):
        text_node = TextNode(text_type=TextType.CODE, text="Code Example", url=None)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code Example")
        self.assertIsNone(html_node.props)    

    def test_link_node(self):
        text_node = TextNode(text_type=TextType.LINK, text="Google", url="https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image_node(self):
        text_node = TextNode(text_type=TextType.IMAGE, text="Image Alt Text", url="https://www.example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.example.com/image.png", "alt": "Image Alt Text"})

    def test_empty_text(self):
        text_node = TextNode(text_type=TextType.TEXT, text="", url=None)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "")
        self.assertIsNone(html_node.props)

    def test_empty_url_for_link(self):
        text_node = TextNode(text_type=TextType.LINK, text="No URL", url="")
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "No URL")
        self.assertEqual(html_node.props, {"href": ""})

    def test_invalid_text_type(self):
        with self.assertRaises(Exception):  # Assuming a ValueError is raised for invalid TextType
            text_node = TextNode(text_type=None, text="Invalid Type", url=None)
            text_node_to_html_node(text_node)


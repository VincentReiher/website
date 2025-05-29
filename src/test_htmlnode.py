import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        test_props = {
            "key1": "val1"
        }
        node = HTMLNode("tag", "value", "children", test_props)
        self.assertEqual(str(node), str(node))

    def test_eq_empty(self):
        node = HTMLNode()
        self.assertEqual(str(node), str(node))

    def test_props_to_html(self):
        test_props = {
                        "href": "https://www.google.com",
                        "target": "_blank",
                    }
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html()," href=\"https://www.google.com\" target=\"_blank\"") 

    def test_empty_props_to_html(self):
        test_props = {}
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), "")

    def test_none_props_to_html(self):
        test_props = None
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_url_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

class TestTextNodeConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node in bold", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node in bold")
        
    def test_italics(self):
        node = TextNode("This is a text node in italics", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node in italics")
        
    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
        
    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.google.com")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {'href':node.url})
        
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src':node.url, 'alt':node.text})


if __name__ == "__main__":
    unittest.main()
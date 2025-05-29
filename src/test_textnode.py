import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)

class TestTextNodeSplitter(unittest.TestCase):

    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes_target = [TextNode("This is text with a ", TextType.NORMAL),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.NORMAL)]
        self.assertEqual(new_nodes, new_nodes_target)

    def test_split_bold(self):
        node = TextNode("This is text with a **bold text** block", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes_target = [TextNode("This is text with a ", TextType.NORMAL),
                            TextNode("bold text", TextType.BOLD),
                            TextNode(" block", TextType.NORMAL)]
        self.assertEqual(new_nodes, new_nodes_target)

    def test_split_italics(self):
        node = TextNode("This is text with an _italics block_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes_target = [TextNode("This is text with an ", TextType.NORMAL),
                            TextNode("italics block", TextType.ITALIC)]
        self.assertEqual(new_nodes, new_nodes_target)

    def test_split_leading_delim(self):
        node = TextNode("`Here` a code block leads and ends the `old node`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes_target = [TextNode("Here", TextType.CODE),
                            TextNode(" a code block leads and ends the ", TextType.NORMAL),
                            TextNode("old node", TextType.CODE)]
        self.assertEqual(new_nodes, new_nodes_target)

    def test_split_adjacent_delims(self):
        node = TextNode("Here two `code blocks` `are immediately` adjacent", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes_target = [TextNode("Here two ", TextType.NORMAL),
                            TextNode("code blocks", TextType.CODE),
                            TextNode(" ", TextType.NORMAL),
                            TextNode("are immediately", TextType.CODE),
                            TextNode(" adjacent", TextType.NORMAL)]
        self.assertEqual(new_nodes, new_nodes_target)

    def test_split_multiple_nodes(self):
        node1 = TextNode("Here is the **first** node", TextType.NORMAL)
        node2 = TextNode("Here is the **second** node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        new_nodes_target = [TextNode("Here is the ", TextType.NORMAL),
                            TextNode("first", TextType.BOLD),
                            TextNode(" node", TextType.NORMAL),
                            TextNode("Here is the ", TextType.NORMAL),
                            TextNode("second", TextType.BOLD),
                            TextNode(" node", TextType.NORMAL)]
        self.assertEqual(new_nodes, new_nodes_target)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_identical_nodes(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [Google link](https://www.google.com) and a [boot.dev link](https://www.boot.dev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("Google link", TextType.LINK, "https://www.google.com"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("boot.dev link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_same_link(self):
        node = TextNode(
            "This is text with a [Google link](https://www.google.com) and again a [Google link](https://www.google.com)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("Google link", TextType.LINK, "https://www.google.com"),
                TextNode(" and again a ", TextType.NORMAL),
                TextNode("Google link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

class TestTextToTextnodes(unittest.TestCase):
    def splitAllTypes(self):
        text="This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

if __name__ == "__main__":
    unittest.main()
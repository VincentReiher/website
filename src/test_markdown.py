import unittest

from markdown import BlockType, extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type, extract_title
from markdown_interpreter import markdown_to_html_node

class TestMarkdown(unittest.TestCase):

    def test_image_finder(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_block_paragraph(self):
        block = "This is just a block of normal\ntext that should be detected as paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_markdown_block_heading(self):
        block = "### This is a block of heading text that should be detected as a heading."
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_markdown_block_code(self):
        block = "```This is just a block of code\ntext that should be detected as code.```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_markdown_block_quote(self):
        block = "> This is just a block of quoted\n> text that should be detected as a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_markdown_block_unordered(self):
        block = "- This is a bit\n- of text that\n- should be detected as\n- an unordered list."
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_markdown_block_ordered(self):
        block = "1. This bit of text\n2. and this bit\n3. and also this bit\n4. form an ordered list"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_markdown_block_heading_too_many(self):
        block = "####### This is a block of heading text that should not be detected as a heading because it has too many pound symbols."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_markdown_block_wrong_quote(self):
        block = "> This is just a block of quoted\n> text that should not be detected as a quote\nbecause the last line doesn't have the marker."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_markdown_block_wrong_order(self):
        block = "1. This bit of text\n2. and this bit\n4. and also this bit\n3. form an ordered list but in\n5. the wrong order."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownInterpreter(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headerblock(self):
        md = "#### IMPORTANT DOCUMENT"
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h4>IMPORTANT DOCUMENT</h4></div>"
        )

    def test_quoteblock(self):
        md = """
> Once upon a time
> one particular person
> said this one thing
> that was extremely profound.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>Once upon a time one particular person said this one thing that was extremely profound.</blockquote></div>"
        )

    def test_ullistblock(self):
        md = """
- One listed item
- another listed item
- yet another listed item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ul><li>One listed item</li><li>another listed item</li><li>yet another listed item</li></ul></div>"
        )

    def test_ollistblock(self):
        md = """
1. First listed item
2. second listed item
3. third listed item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ol><li>First listed item</li><li>second listed item</li><li>third listed item</li></ol></div>"
        )

    def test_title_extraction(self):
        md = """
## NOT QUITE HEADER
# HEADER   
"""
        title = extract_title(md)

        self.assertEqual(
            title,
            "HEADER"
        )

    def test_no_title_extraction(self):
        md = """
## NOT QUITE HEADER
### ACTUALLY NO HEADER AT ALL
"""

        with self.assertRaises(Exception):
            title = extract_title(md)

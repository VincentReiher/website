from enum import Enum
from htmlnode import LeafNode
from markdown import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text, text_type, url=None):

        if text_type == TextType.CODE:
            self.text = text
        else:
            self.text = text.replace("\n", " ")
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):

        return  self.text == other.text and \
                self.text_type == other.text_type and \
                self.url == other.url
    
    def __repr__(self):

        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def to_html_node(self):
        match self.text_type:
            case TextType.NORMAL:
                return LeafNode(None, self.text, None)
            case TextType.BOLD:
                return LeafNode("b", self.text, None)
            case TextType.ITALIC:
                return LeafNode("i", self.text, None)
            case TextType.CODE:
                return LeafNode("code", self.text, None)
            case TextType.LINK:
                return LeafNode("a", self.text, {'href':self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {'src':self.url, 'alt':self.text})
            case _:
                raise Exception("invalid text type")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            new_node_text = node.text.split(delimiter)
            new_node_idx = 0
            for text in new_node_text:
                if text == "":
                    new_node_idx += 1
                    continue
                else:
                    if new_node_idx % 2 == 0:
                        new_node_type = node.text_type
                    else:
                        new_node_type = text_type

                    new_nodes.append(TextNode(text, new_node_type, node.url))
                    new_node_idx += 1
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_image(old_nodes):

    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            image_data_list = extract_markdown_images(node.text)
            remaining_node_str = node.text

            for image_data in image_data_list:
                image_str = f"![{image_data[0]}]({image_data[1]})"
                pre_str, remaining_node_str = remaining_node_str.split(image_str, maxsplit=1)
                new_nodes.append(TextNode(pre_str, text_type=TextType.NORMAL, url=node.url))
                new_nodes.append(TextNode(image_data[0], TextType.IMAGE, image_data[1]))

            if remaining_node_str != "":
                new_nodes.append(TextNode(remaining_node_str, node.text_type))
        else:
            new_nodes.append(node)


    return new_nodes

def split_nodes_link(old_nodes):
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.NORMAL:

            link_data_list = extract_markdown_links(node.text)
            remaining_node_str = node.text

            for link_data in link_data_list:
                link_str = f"[{link_data[0]}]({link_data[1]})"
                pre_str, remaining_node_str = remaining_node_str.split(link_str, maxsplit=1)
                new_nodes.append(TextNode(pre_str, text_type=TextType.NORMAL))
                new_nodes.append(TextNode(link_data[0], TextType.LINK, link_data[1]))

            if remaining_node_str != "":
                new_nodes.append(TextNode(remaining_node_str, node.text_type))
        else:
            new_nodes.append(node)


    return new_nodes

def text_to_textnodes(text):

    initial_node = [TextNode(text, TextType.NORMAL)]
    nodes_split_images = split_nodes_image(initial_node)
    nodes_split_links = split_nodes_link(nodes_split_images)
    nodes_split_bold = split_nodes_delimiter(nodes_split_links, "**", TextType.BOLD)
    nodes_split_italics = split_nodes_delimiter(nodes_split_bold, "_", TextType.ITALIC)
    nodes_split_code = split_nodes_delimiter(nodes_split_italics, "`", TextType.CODE)
    
    return nodes_split_code
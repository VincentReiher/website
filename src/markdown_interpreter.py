from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_to_textnodes
from markdown import BlockType, markdown_to_blocks, block_to_block_type



def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)
    document_HTML_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                text_nodes = text_to_textnodes(block)
                html_nodes = [text_node.to_html_node() for text_node in text_nodes]

                paragraph_HTML_node = ParentNode("p", html_nodes, props=None)
                document_HTML_nodes.append(paragraph_HTML_node)

            case BlockType.HEADING:
                # find heading size
                header_size, header_text = block.split(" ", 1)
                header_size_tag = f"h{len(header_size)}"

                header_text_node = text_to_textnodes(header_text)
                html_nodes = [text_node.to_html_node() for text_node in header_text_node]

                header_html_node = ParentNode(header_size_tag, html_nodes, props=None)

                document_HTML_nodes.append(header_html_node)

            case BlockType.CODE:

                # remove leading and ending backticks from the code
                code = "\n".join(block.split("\n")[1:-1]) + "\n"

                # create TextNode containing the code, without markdown backticks
                code_text_node = TextNode(code, TextType.CODE)

                # code TextNode is converted to an HTML code node and nested into a parent <pre> HTML node
                preformatted_code_node = ParentNode("pre", [code_text_node.to_html_node()], props=None)

                document_HTML_nodes.append(preformatted_code_node)

            case BlockType.QUOTE:
                quote_text = extract_text_from_quote_block(block)
                quote_text_nodes = text_to_textnodes(quote_text)
                html_nodes = [text_node.to_html_node() for text_node in quote_text_nodes]

                quote_html_node = ParentNode("blockquote", html_nodes, props=None)

                document_HTML_nodes.append(quote_html_node)

            case BlockType.UNORDERED_LIST:
                list_items = extract_items_from_list(block, block_type)
                list_HTML_nodes = []

                for item in list_items:
                    item_text_nodes = text_to_textnodes(item)
                    item_html_subnodes = [text_node.to_html_node() for text_node in item_text_nodes]
                    item_html_node = ParentNode("li", item_html_subnodes, props=None)

                    list_HTML_nodes.append(item_html_node)

                list_master_node = ParentNode("ul", list_HTML_nodes, props=None)

                document_HTML_nodes.append(list_master_node)

            case BlockType.ORDERED_LIST:
                list_items = extract_items_from_list(block, block_type)
                list_HTML_nodes = []

                for item in list_items:
                    item_text_nodes = text_to_textnodes(item)
                    item_html_subnodes = [text_node.to_html_node() for text_node in item_text_nodes]
                    item_html_node = ParentNode("li", item_html_subnodes, props=None)

                    list_HTML_nodes.append(item_html_node)

                list_master_node = ParentNode("ol", list_HTML_nodes, props=None)

                document_HTML_nodes.append(list_master_node)

            case _:
                raise TypeError("Invalid block type")
            
    return ParentNode("div", document_HTML_nodes, props=None)

def extract_text_from_quote_block(block):

    block_lines = block.split("\n")

    # remove leading "> " from each quote line
    block_text_lines = [line[2:] for line in block_lines]
    return "\n".join(block_text_lines)

def extract_items_from_list(block, block_type):
    if block_type == BlockType.UNORDERED_LIST:
        line_buffer_size = 2
    elif block_type == BlockType.ORDERED_LIST:
        line_buffer_size = 3
    else:
        raise TypeError("Unexpected list type")
    
    list_lines = block.split("\n")
    list_items = [line[line_buffer_size:] for line in list_lines]

    return list_items
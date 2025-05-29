import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def extract_markdown_images(text):    
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def markdown_to_blocks(markdown):
    
    blocks = []
    split_strings = markdown.split("\n\n")

    for block_string in split_strings:
        if block_string == "":
            continue

        blocks.append(block_string.strip())

    return blocks

def block_to_block_type(block):
    
    if block[0] == "#":
        heading_markers, _ = block.split(" ", 1)

        if all(character == "#" for character in list(heading_markers)) and len(heading_markers) <= 6:
            return BlockType.HEADING

    if block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    block_lines = block.split("\n")
    
    if all(line[0] == ">" for line in block_lines):
        return BlockType.QUOTE
    
    if all(line[0:2] == "- " for line in block_lines):
        return BlockType.UNORDERED_LIST
    
    if all(block_lines[idx][0:3] == f"{idx+1}. " for idx in range(len(block_lines))):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
        

def extract_title(markdown):

    text_lines = markdown.split("\n")

    for line in text_lines:
        if line == "":
            continue

        stripped_line = line.strip()
        if stripped_line[0] == "#" and stripped_line[1] == " ":
            return line[2:].strip()
        
    raise Exception("no h1 header found")
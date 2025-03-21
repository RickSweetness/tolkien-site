from enum import Enum
import re
from block_markdown import markdown_to_blocks
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"

def block_to_block_type(text):
    lines = text.split("\n")
    quote_counter = 0
    unordered_counter = 0
    ordered_counter = 0
    #heading
    if re.match(r"^#{1,6} ", text):
        return BlockType.HEADING
    #code
    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    #quote
    for line in lines:
        if line != "":
            if line[0] == ">":
                quote_counter +=1
    if quote_counter == len(lines):
        return BlockType.QUOTE
    #unordered list
    for line in lines:
        if line != "":
            if line[0:2] == "- ":
                unordered_counter += 1
    if unordered_counter ==  len(lines):
        return BlockType.ULIST
    #ordered list
    if text.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    #paragraph
    return BlockType.PARAGRAPH

def markdown_to_html_node(text):
    super_children = []
    text = markdown_to_blocks(text)
    for block in text:
        block_type = block_to_block_type(block)
        #HEADING
        if block_type == BlockType.HEADING:
            block = block.replace("\n", " ")
            if len(text_to_children(block)) ==  1:
                super_children.append(LeafNode(heading_node_number(block), block))
                continue
            super_children.append(ParentNode(heading_node_number(block), text_to_children(block)))
        #PARAGRAPH
        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            if len(text_to_children(block)) ==  1:
                super_children.append(LeafNode("p", block))
                continue
            super_children.append(ParentNode("p", text_to_children(block)))
        #QUOTE
        if block_type == BlockType.QUOTE:
            block = block.replace("\n", " ")
            if len(text_to_children(block)) == 1:
                super_children.append(LeafNode("blockquote", block))
                continue
            super_children.append(ParentNode("blockquote", text_to_children(block)))
        #CODE
        if block_type == BlockType.CODE:
            code_text = block[3:-3]
            if code_text.startswith("\n"):
                code_text = code_text[1:]
            raw_text_node = TextNode(code_text, TextType.TEXT)
            child = text_node_to_html_node(raw_text_node)
            code = ParentNode("code", [child])
            super_children.append(ParentNode("pre", [code]))
        #ULIST
        if block_type == BlockType.ULIST:
            line_list = []
            for line in block.split("\n"):
                if len(text_to_children(line)) ==  1:
                    line_list.append(LeafNode("li", line))
                    continue
                line_list.append(ParentNode("li", text_to_children(line)))
            super_children.append(ParentNode("ul", line_list))
        #OLIST
        if block_type == BlockType.OLIST:
            line_list = []
            for line in block.split("\n"):
                if len(text_to_children(line)) ==  1:
                    line_list.append(LeafNode("li", line))
                    continue
                line_list.append(ParentNode("li", text_to_children(line)))
            super_children.append(ParentNode("ol", line_list))
    return ParentNode("div", super_children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes





def heading_node_number(block):
    if block.startswith("######"):
        return "h6"
    if block.startswith("#####"):
        return "h5"
    if block.startswith("####"):
        return "h4"
    if block.startswith("###"):
        return "h3"
    if block.startswith("##"):
        return "h2"
    if block.startswith("#"):
        return "h1"




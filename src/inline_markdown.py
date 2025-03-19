import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = [] #make new nodes list
    for node in old_nodes:
        if node.text_type != TextType.TEXT: #we only alter Text Nodes, this skips non-text nodes
            new_nodes.append(node)
            continue
        split_nodes = [] #make the list we'll later extend ontoo new_nodes
        sections = node.text.split(delimiter) #split the current nodes text into sections
        if len(sections) % 2 == 0: #this checks to see there's an uneven amount of segments, to make sure the formatted section is closed
            raise ValueError("invalid markdown, formatted section not closed") 
        for i in range(len(sections)):
            if sections[i] == "": #skip blank sections
                continue
            if i % 2 == 0: #if the section we're in is even we're not in a markdown formmated section
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
        
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches  

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        elif not re.search(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text):
            new_nodes.append(node)
        else:
            original_text = node.text
            extract_list = []
            extracted_images = extract_markdown_images(original_text)
            for extracted_image in extracted_images:
                alt_text = extracted_image[0]
                link = extracted_image[1]
                sections = original_text.split(f"![{alt_text}]({link})", 1)
                if len(sections) != 2:
                    raise ValueError("invalid markdown, image section not closed")
                if sections[0] != "":
                    extract_list.append(TextNode(sections[0], TextType.TEXT, None))
                extract_list.append(TextNode(alt_text, TextType.IMAGE, link))
                original_text = sections[1]
            if original_text != "":
                extract_list.append(TextNode(original_text, TextType.TEXT))
            new_nodes.extend(extract_list)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue        
        if node.text == "":
            continue
        elif not re.search(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text):
            new_nodes.append(node)
        else:
            original_text = node.text
            extract_list = []
            extracted_links = extract_markdown_links(original_text)
            if len(extracted_links) == 0:
                new_nodes.append(node)
                continue            
            for extracted_link in extracted_links:
                alt_text = extracted_link[0]
                link = extracted_link[1]
                sections = original_text.split(f"[{alt_text}]({link})", 1)
                if len(sections) != 2:
                    raise ValueError("invalid markdown, link section not closed")
                if sections[0] != "":
                    extract_list.append(TextNode(sections[0], TextType.TEXT, None))
                extract_list.append(TextNode(alt_text, TextType.LINK, link))
                original_text = sections[1]
            if original_text != "":
                extract_list.append(TextNode(original_text, TextType.TEXT))
            new_nodes.extend(extract_list)
    return new_nodes


def text_to_textnodes(text):
    conv_text = [TextNode(text, TextType.TEXT)]
    delimiter_splits = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(conv_text, "_", TextType.ITALIC), "**", TextType.BOLD), "`", TextType.CODE)
    image_link_split = split_nodes_link(split_nodes_image(delimiter_splits))
    return image_link_split

        
        
        
        
        
        
        

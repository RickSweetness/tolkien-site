from textnode import TextNode, TextType
from blocktype import markdown_to_html_node
from htmlnode import *
import os, shutil, sys

def find_basepath():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    return basepath


def copy_and_paste_directory(source, destination):
    if os.path.exists(source) == False:
        raise ValueError("Path does not exist, or need admin privilege")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    source_dir = os.listdir(source)
    for item in source_dir:
        if "." in item:
            shutil.copy(f"{source}/{item}", destination)
        else:
            copy_and_paste_directory(f"{source}/{item}", f"{destination}/{item}")

def extract_title(markdown):
    markdown_lines = markdown.split("\n")
    for line in markdown_lines:
        if line.startswith("#") and not line.startswith("##"):
            return line.lstrip("#").strip(" ")
    raise Exception("No header")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    print(from_path)
    with open(from_path, "r") as f:
        md_content = f.read()
    with open(template_path, "r") as f:
        template_content =  f.read()
    md_to_html = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    new_file = template_content.replace("{{ Title }}", title).replace("{{ Content }}", md_to_html)
    new_file = new_file.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    os.makedirs(dest_path, exist_ok=True)
    new_file_path = f"{dest_path}/index.html"
    with open(new_file_path, "w") as f:
        f.write(new_file)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    if not os.path.exists(dir_path_content):
        raise ValueError("Path to content directory does not exist, or need admin privilege")
    source_dir_list = os.listdir(dir_path_content)
    for item in source_dir_list:
        if ".md" in item:
            generate_page(f"{dir_path_content}/{item}", template_path, dest_dir_path, basepath)
        elif "." not in item:
            generate_pages_recursive(f"{dir_path_content}/{item}", template_path, f"{dest_dir_path}/{item}", basepath)
        else:
            continue

def main():
    print(find_basepath())
    copy_and_paste_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", find_basepath())





if __name__ == "__main__":
    main()
from textnode import TextNode, TextType
import os, shutil

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
















def main():
    copy_and_paste_directory("/home/rrheu/workspace/tolkien-site/static", "/home/rrheu/workspace/tolkien-site/public")




















if __name__ == "__main__":
    main()
from textnode import *

def main():
    text_node = TextNode("this is some anchor text", TextType.LINK, "website.com")
    print(text_node)

if __name__ == "__main__":
    main()
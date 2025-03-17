from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent Node requires tag value")
        if self.children == None:
            raise ValueError("Parent Node requires children value")
        current_text = ""
        for child in self.children:
            current_text += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{current_text}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


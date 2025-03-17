from htmlnode import HTMLNode
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All Leaf nodes must have a value")
        if self.tag == None:
            return self.value
        props_to_html_output = self.props_to_html()
        return f"<{self.tag}{props_to_html_output}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
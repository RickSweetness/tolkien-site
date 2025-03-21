class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag 
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_string = ""
        if self.props == None:
            return props_string
        for attribute in self.props:
            props_string += f' {attribute}="{self.props[attribute]}"'
        return props_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All Leaf nodes must have a value")
        if self.tag is None:
            return self.value
        props_to_html_output = self.props_to_html()
        return f"<{self.tag}{props_to_html_output}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Node requires tag value")
        if self.children is None:
            raise ValueError("Parent Node requires children value")
        current_text = ""
        for child in self.children:
            current_text += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{current_text}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
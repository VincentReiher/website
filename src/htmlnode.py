class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        
        if self.props is None:
            return ""

        item_strings = []
        for item in self.props:
            item_strings.append(f" {item}=\"{self.props[item]}\"")

        return "".join(item_strings)
    
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required")
        if self.children is None:
            raise ValueError("children is undefined")
        
        html_string_entries = []
        for child in self.children:
            html_string_entries.append(child.to_html())

        children_html_string = "".join(html_string_entries)

        return f"<{self.tag}>{children_html_string}</{self.tag}>"
    

class LeafNode(HTMLNode):

    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("all Leaf nodes must have a value")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("all Leaf nodes must have a value")
        
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
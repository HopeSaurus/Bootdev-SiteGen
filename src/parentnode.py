from htmlnode import HTMLNode

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.children == None:
      raise ValueError("Cannot create parent node without a children")
    if self.tag == None:
      raise ValueError("A tag is needed to create a node")
    
    def recursive_list(node_list):
      if not node_list:
        return ""
      else:
        return node_list[0].to_html() + recursive_list(node_list[1:])
      

    return (f"<{self.tag}>{recursive_list(self.children)
    }</{self.tag}>")

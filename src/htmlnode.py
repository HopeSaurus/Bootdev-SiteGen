type HTMLNode = HTMLNode

class HTMLNode:
  def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict = {}):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError()
  
  def props_to_html(self):
    result = ""
    if self.props == {} or self.props == None:
      return result
    for i,(key,value) in enumerate(self.props.items()):
      result += f" {key}=\"{value}\""
    return result
    
  def __repr__(self) -> str:
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

      
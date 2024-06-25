class TextNode:
  def __init__(self, text, text_type, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, x):
    return self.text == x.text and self.text_type == x.text_type and self.url == x.url
  
  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type}, {self.url})"
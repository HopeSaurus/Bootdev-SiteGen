from leafnode import LeafNode
from textnode import TextNode
from parentnode import ParentNode
from htmlnode import HTMLNode
import re

def text_node_to_html_node(text_node):
  tag = ""
  text = text_node.text
  props = {}
  match(text_node.text_type):
    case "text":
      tag = None
    case "bold":
      tag = "b"
    case "italic":
      tag = "i"
    case "code":
      tag = "code"
    case "link":
      tag = "a"
      props = {
        "href": text_node.url,
      }
    case "image":
      tag = "img"
      text = ""
      props = {
        "src": text_node.url,
        "alt": text_node.text,
      }
    case _:
      raise Exception("Incorrect text type")
  return LeafNode(tag,text,props)

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str) -> list:
  new_nodes = []
  for item in old_nodes:
    if item.text_type != "text":
      new_nodes.append(item)
    else:
      tmp_list = item.text.split(delimiter)
      if len(tmp_list) == 0:
        new_nodes.append(item)
      else:
        for idx, item in enumerate(tmp_list):
          if idx % 2 == 0:
            new_nodes.append(TextNode(item,"text"))
          else:
            new_nodes.append(TextNode(item, text_type))
  return new_nodes

def extract_markdown_images(text):
  return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
  return re.findall(r"\[(.*?)\]\((.*?)\)",text)

def split_nodes_image(old_nodes):
  def recursive_split(text, delimiter_image_urls):
    result = []
    if delimiter_image_urls == []:
      if text == "":
        result = []
      else:
        result = [TextNode(text,"text")]
    else:
      text_splitted = text.split(f"![{delimiter_image_urls[0][0]}]({delimiter_image_urls[0][1]})")
      loop_return = [TextNode(delimiter_image_urls[0][0],"image",delimiter_image_urls[0][1])]
      if len(text_splitted) == 1:
        return loop_return
      result.extend(loop_return + recursive_split(text_splitted[1],delimiter_image_urls[1:]))
    return result

  new_nodes = []
  for item in old_nodes:
    image_markdown = extract_markdown_images(item.text)
    new_nodes.extend(recursive_split(item.text,image_markdown))
  return new_nodes

def split_nodes_link(old_nodes):
  def recursive_split(text, delimiter_image_urls):
    result = []
    if delimiter_image_urls == []:
      if text == "":
        result = []
      else:
        result = [TextNode(text,"text")]
    else:
      text_splitted = text.split(f"![{delimiter_image_urls[0][0]}]({delimiter_image_urls[0][1]})")
      loop_return = [TextNode(delimiter_image_urls[0][0],"link",delimiter_image_urls[0][1])]
      if len(text_splitted) == 1:
        return loop_return
      result.extend(loop_return + recursive_split(text_splitted[1],delimiter_image_urls[1:]))
    return result

  new_nodes = []
  for item in old_nodes:
    image_markdown = extract_markdown_links(item.text)
    new_nodes.extend(recursive_split(item.text,image_markdown))
  return new_nodes


def text_to_textnodes(text):
  nodes = [TextNode(text, "text")]
  nodes = split_nodes_delimiter(nodes, "**", "bold")
  nodes = split_nodes_delimiter(nodes, "*", "italic")
  nodes = split_nodes_delimiter(nodes, "`", "code")
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)
  return nodes

# Block 

def markdown_to_blocks(markdown: str) -> list[list]:
  lines = markdown.split('\n')
  result = []
  block = []
  for line in lines:
    line = line.strip()
    if len(line)>0:
      block.append(line)
    else:
      result.append(block)
      block = []
  result.append(block)
  return result
  
def block_to_block_type(block: list):
  first_block_char = block[0][0]
  ordered_list_idx = 1
  block_type = "paragraph"
  for line in block:
    ordered_list_idx_char = str(ordered_list_idx)
    first_char = line[0]
    if first_char != first_block_char and first_char != ordered_list_idx_char and first_block_char!='`':
      return "paragraph"
    match first_char:
      case '#':
        tmp = line.lstrip(first_char)
        n_hashes = len(line) - len(tmp)
        if n_hashes > 6 or tmp[0]!= " ":
          return "paragraph"
        else:
          return "heading"
      case '>':
        block_type = "quote"
      case '*' | '-':
        tmp = line.lstrip(first_char)
        if len(line) - len(tmp) > 1 or tmp[0]!= " ":
          return "paragraph"
        else: 
          block_type = 'unordered_list'
      case '`':
        tmp = line.lstrip(first_char)
        if len(line) - len(tmp) != 3:
          return "paragraph"
        if len(block[len(block)-1]) - len(block[len(block)-1].rstrip(first_char)) == 3:
          return "code"
      case _:
        if line[0] == ordered_list_idx_char and line[1] == "." and line[2] == " ":
          ordered_list_idx += 1
          block_type = "ordered_list"
        else:
          return "paragraph"
  return block_type

def text_to_children(text):
  text_nodes = text_to_textnodes(text)
  children = []
  for text_node in text_nodes:
    children.append(text_node_to_html_node(text_node))
  return children

def block_to_HTMLNode(block: list) -> object:
  block_type = block_to_block_type(block)
  match block_type:
    case "paragraph":
      return ParentNode("p",text_to_children(" ".join(block)))
    case "quote":
      return ParentNode("blockquote",text_to_children(" ".join(list(map(lambda x: x.lstrip("> "),block)))))
    case "heading":
      n_hashes = len(block[0]) - len(block[0].strip("#"))
      return ParentNode(f"h{n_hashes}",text_to_children(" ".join(list(map(lambda x: x.lstrip("# "),block)))))
    case "ordered_list":
      children = []
      for idx, line in enumerate(block):
        children.append(ParentNode("li",text_to_children(line.lstrip(f"{idx+1}. "))))
      return ParentNode("ol", children)
    case "unordered_list":
      children = []
      for line in block:
        children.append(ParentNode("li",text_to_children(line.lstrip("* ").lstrip("- "))))
      return ParentNode("ul", children=children)
    case "code":
      return ParentNode("pre",[ParentNode("code",
                                         text_to_children("\n".join(block).strip("` ")))])
    case _:
      raise Exception("What the fuck did you do")
    
def markdown_to_html_node(markdown: str):
  blocks = markdown_to_blocks(markdown)
  children = []
  for block in blocks:
    children.append(block_to_HTMLNode(block))
  return ParentNode("div", children=children)
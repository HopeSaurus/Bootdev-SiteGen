import unittest
import helpers
from textnode import TextNode

class TestHelpers(unittest.TestCase):
  def test_split_nodes_delimiters(self):
    node = TextNode("This is text with a `code block` word", "text")
    new_nodes = helpers.split_nodes_delimiter([node], "`", "code")

    self.assertEqual(new_nodes,[
    TextNode("This is text with a ", "text"),
    TextNode("code block", "code"),
    TextNode(" word", "text"),
    ]
                     )

    node_complex = TextNode("This *text* has many *italic* words, or are they *bold?*","text")
    new_nodes = helpers.split_nodes_delimiter([node_complex], "*", "bold")

    self.assertEqual(new_nodes,[
      TextNode("This ","text"),
      TextNode("text","bold"),
      TextNode(" has many ", "text"),
      TextNode("italic","bold"),
      TextNode(" words, or are they ", "text"),
      TextNode("bold?","bold"),
      TextNode("", "text")
    ]

    )

    node = TextNode("This is text with a *code block* word", "text")
    new_nodes = helpers.split_nodes_delimiter([node,node_complex], "*", "bold")

    self.assertEqual(new_nodes,[
      TextNode("This is text with a ", "text"),
      TextNode("code block", "bold"),
      TextNode(" word", "text"),
      TextNode("This ","text"),
      TextNode("text","bold"),
      TextNode(" has many ", "text"),
      TextNode("italic","bold"),
      TextNode(" words, or are they ", "text"),
      TextNode("bold?","bold"),
      TextNode("", "text")
      ]
    )

    node = TextNode("italic","italic")
    node2 = TextNode("bold", "bold")
    node3 = TextNode("code","code")

    new_nodes = helpers.split_nodes_delimiter([node,node2,node3], "*", "bold")

    self.assertEqual(new_nodes,[
      TextNode("italic", "italic"),
      TextNode("bold","bold"),
      TextNode("code","code"),
    ])
  
  def test_extract_markdown_images(self):
    text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
    self.assertEqual(helpers.extract_markdown_images(text),[
      ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
    ])

    text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    self.assertEqual(helpers.extract_markdown_links(text),[("link", "https://www.example.com"), ("another", "https://www.example.com/another")])


  def test_split_nodes_image(self):
    node = TextNode(
        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
        "text",
    )
    new_nodes = helpers.split_nodes_image([node])

    self.assertEqual(new_nodes, [
                                  TextNode("This is text with an ", "text"),
                                  TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                                  TextNode(" and another ", "text"),
                                  TextNode(
                                      "second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                                  ),
                                ])
    

    node = TextNode(
        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) Help, pls help",
        "text",
    )
    new_nodes = helpers.split_nodes_image([node])

    self.assertEqual(new_nodes, [
                                  TextNode("This is text with an ", "text"),
                                  TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                                  TextNode(" and another ", "text"),
                                  TextNode(
                                      "second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                                  ),
                                  TextNode(
                                    " Help, pls help", "text"
                                  )
                                ])
    
    def test_text_to_text_nodes(self):
      pass

  def test_markdown_to_blocks(self):
    markdown = """This is **bolded** paragraph
    This is another paragraph with *italic* text and `code` here
    This is the same paragraph on a new line
    
    * This is a list
    * with items"""

    self.assertEqual([["This is **bolded** paragraph","This is another paragraph with *italic* text and `code` here","This is the same paragraph on a new line"],
                      ["* This is a list", "* with items"]], helpers.markdown_to_blocks(markdown))


  def test_block_to_block_type(self):
    block = ["######## This a false heading, should return paragraph"]

    result = helpers.block_to_block_type(block)

    self.assertEqual(result,"paragraph")

    block = ["###### This is a correct heading"]

    result = helpers.block_to_block_type(block)

    self.assertEqual(result, "heading")

    block = ["```This is a block of code", "I havent test it yet", "But this should return a code block```"]

    result = helpers.block_to_block_type(block)

    self.assertEqual(result, "code")

    block = ["* This is an unordered", "* list containing nonsense"]

    result = helpers.block_to_block_type(block)

    self.assertEqual(result, "unordered_list")

    block = ["> quote block should work", "> Extra nonsense", "> more nonsense"]

    result = helpers.block_to_block_type(block)

    self.assertEqual(result, "quote")

    block = ["> quote block shouldnt work cause of missing more than sign", " Extra nonsense", " more nonsense"]

    result = helpers.block_to_block_type(block)

    self.assertEqual(result, "paragraph")

    block = ["1. ordered list block should work", "2. Extra nonsense", "3. more nonsense"]

    result = helpers.block_to_block_type(block)

    self.assertEqual(result, "ordered_list")

    block = ["1. ordered list block shouldnt work", "2. Extra nonsense", "3 more nonsense"]

    result = helpers.block_to_block_type(block)

    self.assertEqual(result, "paragraph")
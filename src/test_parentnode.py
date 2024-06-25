import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
  def test_to_html(self):
    simple_parent_node = ParentNode("p",
                                    [
                                      LeafNode("b", "Bold text"),
                                      LeafNode(None, "Normal text"),
                                      LeafNode("i", "italic text"),
                                      LeafNode(None, "Normal text"),
                                    ],{})
    self.assertEqual(simple_parent_node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    parent_node_1 = ParentNode("section",
                               [
                                 simple_parent_node,
                                 ParentNode("article",[
                                   ParentNode("p",[
                                     LeafNode("b","Hello World")
                                   ],
                                     
                                   )
                                 ],
                                   {}
                                 )
                               ]
    )

    self.assertEqual(parent_node_1.to_html(),"<section><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
                     "<article><p><b>Hello World</b></p></article>"
                     "</section>"
                     )

    
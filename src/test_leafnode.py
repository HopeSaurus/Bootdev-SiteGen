import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
  def test_to_html(self):
    leaf_node = LeafNode("p","This is a paragraph")
    self.assertEqual(leaf_node.to_html(),f"<p>This is a paragraph</p>")

    leaf_node_with_props = LeafNode("a","Click me!", {"href": "https://www.google.com"})
    self.assertEqual(leaf_node_with_props.to_html(), f"<a href=\"https://www.google.com\">Click me!</a>")

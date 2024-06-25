import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def test_props_to_html(self):
    html_node = HTMLNode(props={"href": "https://google.com",
                                "target": "_blank",
                                "data": "Not_important",
                                "response": "200",
                                })
    self.assertEqual(html_node.props_to_html(), (" href=\"https://google.com\" target=\"_blank\" "
                                                 "data=\"Not_important\" response=\"200\""
                                                 ))
if __name__ == "__main__":
    unittest.main()
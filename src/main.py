from textnode import TextNode
from generate_page import copy_static, generate_page, generate_pages_recursively

def main():

  working_dir = "/Users/admin/BootDev/SiteGen"
  public_dir = working_dir + '/public'
  static_dir = working_dir + '/static'

  copy_static(static_dir,public_dir)

  generate_pages_recursively( working_dir + '/content', working_dir + '/template.html', public_dir)

  
if __name__ == "__main__":
  main()

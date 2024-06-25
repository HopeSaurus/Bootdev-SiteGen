from textnode import TextNode
from helpers import markdown_to_html_node
import os
import shutil

def main():

  working_dir = "/Users/admin/BootDev/SiteGen"
  public_dir = working_dir + '/public'
  static_dir = working_dir + '/static'

  def copy_static(origin, destination):

    if os.path.exists(destination):
      shutil.rmtree(destination)
    os.mkdir(destination)
  
    if not os.path.exists(origin):
      raise Exception("Origin folder does not exist")
    
    def recursive_copy_paste(dir):
      x = os.listdir(dir)
      for item in x : 
        path = os.path.join(dir,item)
        if os.path.isfile(path):
          new_dir = path.replace(origin,destination)
          shutil.copyfile(path, new_dir)
          print(f"copying {item} to: {new_dir}")
        else:
          new_dir = path.replace(origin,destination)
          print(f"making directory in: {new_dir}")
          os.mkdir(new_dir)
          recursive_copy_paste(path)

    recursive_copy_paste(origin)

  def extract_title(markdown: str) -> str:
    tmp = markdown.split("\n")
    for line in tmp:
      if line.startswith("# "):
        return line
    raise Exception("Document should contain a h1 title")
  
  def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template = open(template_path).read()

    main_title = extract_title(markdown)

    html = markdown_to_html_node(markdown).to_html()

    template.replace("{{ Title }}", main_title).replace("{{ Content }}", html)

    if not os.path.exists(dest_path):
      os.makedirs(dest_path)
    dest_file = os.open(dest_path+'index.html',"w").write(html)
    dest_file.close()

  generate_page(working_dir + '/content/index.md', working_dir + '/template.html','/public')


  # copy_static(static_dir,public_dir)


  
if __name__ == "__main__":
  main()

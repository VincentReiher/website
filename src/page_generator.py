import os

from markdown import extract_title
from markdown_interpreter import markdown_to_html_node

def generate_page(src_file, template_path, dest_folder, basepath):

    filename = src_file.rsplit("/", 1)[1].rsplit(".", 1)[0]
    ext = ".html"
    target_file = dest_folder + filename + ext
    print(f"Generating page from {src_file} to {target_file} using {template_path}...")

    try:
        with open(src_file, 'r') as file:
            markdown = file.read()
    except FileNotFoundError:
        print("Markdown file not found")
        return 1
    
    try:
        with open(template_path, 'r') as file:
            template = file.read()
    except FileNotFoundError:
        print("HTML Template file not found")
        return 2
    
    print(basepath)

    page_title = extract_title(markdown)
    page_content_html_node = markdown_to_html_node(markdown)
    page_content_html = page_content_html_node.to_html()
    file_html = template.replace("{{ Title }}", page_title).replace("{{ Content }}", page_content_html)
    file_html = file_html.replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")


    with open(target_file, 'w') as target_file:
        target_file.write(file_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    content_files = os.listdir(dir_path_content)

    for item_name in content_files:
        if os.path.isfile(dir_path_content + item_name):

            generate_page(dir_path_content + item_name, template_path, dest_dir_path, basepath)
        else:
            new_source_dir = f"{dir_path_content}{item_name}/"
            new_target_dir = f"{dest_dir_path}{item_name}/"

            if not os.path.exists(new_target_dir):
                os.mkdir(new_target_dir)

            generate_pages_recursive(new_source_dir, template_path, new_target_dir, basepath)


import sys

from file_manager import initialize_public_directory
from page_generator import generate_pages_recursive

def main():

    print(sys.argv)

    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    target_dir = "docs/"

    initialize_public_directory(target_dir)
    generate_pages_recursive("content/", "template.html", target_dir, basepath)

if __name__ == "__main__":
    main()
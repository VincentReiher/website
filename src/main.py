from file_manager import initialize_public_directory
from page_generator import generate_pages_recursive

def main():
    initialize_public_directory()
    generate_pages_recursive("content/", "template.html", "public/")

if __name__ == "__main__":
    main()
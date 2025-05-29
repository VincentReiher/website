import os, shutil

def initialize_public_directory():
    if os.path.exists("public/"):
        shutil.rmtree("public/")

    copy_directory("static/", "public/")

def copy_directory(source_dir, target_dir):
    
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    # list contents of source dir
    contents = os.listdir(source_dir)

    for item_name in contents:
        if os.path.isfile(source_dir + item_name):
            shutil.copy(source_dir + item_name, target_dir)
        else:
            new_source_dir = f"{source_dir}{item_name}/"
            new_target_dir = f"{target_dir}{item_name}/"
            copy_directory(new_source_dir, new_target_dir)

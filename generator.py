import json
import os
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader(""),
    autoescape=select_autoescape()
)

def load_variables_from_json(filename):
    f = open(filename)     
    data = json.load(f)
    f.close()
    return data

def save_page(path, data, filename = "index"):
    page = open(path + "/" + filename + ".html", "w")
    page.write(data)
    page.close()

def save_sitemap(path, data):
    page = open(path + "sitemap.xml", "w")
    page.write(data)
    page.close

def create_dir(working_directory, foldername):
    newpath = working_directory + foldername
    print ("Creating " + newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

def generate_website(template, data):
    page = template.render(
            title=data["title"], 
            description=data["description"]
        )
    path = create_dir(data["working_directory"], data["name"])
    save_page(path, page)
    copy_assets(path)

def copy_assets(target):
    src = "assets"
    shutil.copytree(src, target + "/assets")

def generate_sitemap(sitemap_data):
    template = env.get_template("template/sitemap.v1.j2")
    page = template.render(
            website = "www.superlanding.page",
            sitemap_data = sitemap_data,
            page_name = "index",
            gen_date = "2024-09-19"
        )
    path = "/Users/alizardo/Documents/superlanding-generator/output/"
    save_sitemap(path, page)

def main():
    data = load_variables_from_json("data/blog.json")
    template = env.get_template("templates/core/index.jinja2")
    generate_website(template, data)
    
if __name__ == "__main__":
    main()
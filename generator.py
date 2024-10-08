import json
import os
import shutil
from datetime import datetime
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader(""),
    autoescape=select_autoescape()
)

class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if info:
            lexer = get_lexer_by_name(info, stripall=True)
            formatter = html.HtmlFormatter(noclasses=True)
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'

def render_markdown(text):
    markdown = mistune.create_markdown(renderer=HighlightRenderer())
    return markdown(text)

def load_variables_from_json(filename):
    f = open(filename)     
    data = json.load(f)
    f.close()
    return data

def load_markdown(filename):
    f = open(filename)     
    data = render_markdown(f.read())
    f.close()
    return data

def save_page(path, data, filename = "index"):
    page = open(path + "/" + filename + ".html", "w")
    page.write(data)
    page.close()

def save_sitemap(path, data):
    page = open(path + "/" + "sitemap.xml", "w")
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
            description=data["description"],
            about_page=data["about_page"],
            blog=True,
            website=data["website"],
            posts=[data["blog"][i:i+2] for i in range(0, len(data["blog"]), 2)],
            gtag=data["gtag"]
        )
    path = create_dir(data["working_directory"], data["name"])
    save_page(path, page)
    copy_assets(path)

def copy_assets(target):
    try:
        src = "assets"
        shutil.copytree(src, target + "/assets")
    except:
        print("Assets might have been copied already.")

def get_posts():
    basepath = "data/posts"
    get_posts = []
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            get_posts.append({
                "path": basepath + "/" + entry,
                "name": entry.replace(".md", "")
            })
    return get_posts

def generate_sitemap(template, data):
    if data["blog"] is not None:
        print("Adding blog posts to sitemap")
        for page in data["blog"]:
            data["sitemap"].append({
                    "name": page["document"],
                    "type": "blog"
                })
    render = template.render(
            website = data["name"],
            pages = data["sitemap"],
            gen_date = datetime.today().strftime('%Y-%m-%d')
        )
    path = create_dir(data["working_directory"], data["name"])
    save_sitemap(path, render)

def generate_posts(template, posts, data):
    for post in posts:
        content = load_markdown(post["path"])
        page = template.render(
                title=data["title"], 
                description=data["description"],
                about_page=data["about_page"],
                blog=data["blog"],
                website=data["website"],
                post=content,
                gtag=data["gtag"]
            )
        path = create_dir(data["working_directory"], data["name"] + "/blog")
        save_page(path, page, post["name"])

def generate_about(template, data):
    page = template.render(
            title=data["title"], 
            description=data["description"],
            about_page=data["about_page"],
            website=data["website"],
            about=load_markdown("data/about.md"),
            gtag=data["gtag"]
        )
    path = create_dir(data["working_directory"], data["name"])
    save_page(path, page, filename = "about")

def main():
    data = load_variables_from_json("data/blog.json")
    if data["blog"] is not None:
        print("Generating blog entries")
        posts = get_posts()
        template = env.get_template("templates/" + data["template"] + "/posts.jinja2")
        generate_posts(template, posts, data)

    print("Generating index.html")    
    template = env.get_template("templates/" + data["template"] + "/index.jinja2")
    generate_website(template, data)

    print("Generating about.html")
    template = env.get_template("templates/" + data["template"] + "/about.jinja2")
    generate_about(template, data)

    print("Generating sitemap.xml")
    template = env.get_template("templates/" + data["template"] + "/sitemap.jinja2")
    generate_sitemap(template, data)

    
if __name__ == "__main__":
    main()
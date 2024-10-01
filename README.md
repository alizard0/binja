# Blog + Jinja2 = BINJA
> Binja is a static blog generator made with Jinja2 & Python.

## Install

### Python3, Virtualenv
```bash
$ python3 -m venv /path/to/binja/website
$ source /path/to/binja/website/activate
```

### Dependencies
```bash
$ pip3 install -r requirements.txt
```

## How to use
1. Update your blog configuration file at `data/blog.json`. 
	1. Name, update title and description
	1. List the blog entries that you want to publish, if you create markdown files inside `blog/` they wont be published automatically, it considers them drafts if you dont register them here.
	1. Pick one template. Currently there are two templates: core and minimal.
```json
{
	"working_directory": "/Users/alizardo/Documents/binja/output/",
	"name":"andrelizardo.com",
	"website":"https://www.andrelizardo.com",
	"title":"André Lizardo",
	"description":"Notes on software development and software architecture.",
	// publish about page?
	"about_page": true,
	// list of published blog posts
	"blog": [
		{
			"title": "Lorem Ipsum",
			"description": "Coniugis pariter oraque mea reddat Pervenit legebat, subiecta vulgusque. His avertitur si vela volucris dabat",
			"document": "hello-world",
			"tags": ["Amazon", "Google"],
			"created-at":"1 September 2024"
		},
		{
			"title": "Lorem Ipsum Espanol",
			"description": "Coniugis pariter oraque mea reddat Pervenit legebat, subiecta vulgusque. His avertitur si vela volucris dabat",
			"document": "hola-mundo",
			"tags": ["Amazon", "Google"],
			"created-at":"1 September 2024"
		}
	],
	// there are two templates available atm, core and minimal
	// you can create your own templates by creating a new directory under templates and extend the core template
	"template": "minimal",
	"sitemap": [
		{
			"name": "index",
			"type": "base"
		},
		{
			"name": "about",
			"type": "base"
		}
	]
}
```
1. Create posts using markdown and saving them inside `posts/`
1. Update your `about.md` too
1. Run `python3 generator.py`
1. Your website will be available inside of `output`
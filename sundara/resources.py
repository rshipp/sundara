"""File resources used by Sundara."""

README = """# Welcome to Sundara!

To get started, create an `index.md` inside the `md/` folder for your
site's homepage. Then run:

    git add -A
    git commit -am "Initial commit."
    sundara g

This will add `index.md` to the git index, commit it, and generate an
`index.html` in the `www/` inside your project. You can run `sundara s`
to preview the generated HTML.

Remember that Sundara uses the git index to find new markdown files, not
file globbing, so if you don't `git add` them, new files will not be
included in the generation.
"""

GITIGNORE = """# Ignore Sundara's generated HTML files.
www/
"""

CONFIG = """# Sundara configuration file.
[meta]
    # Site name (used for homepage <title>) and domain.
    name = 
    # Domain name (used for robots.txt and sitemap generation).
    domain = 
    # Available variables: {name}, {h1}
    title = {h1}
    description = 
    # Change these if you use a different language or encoding.
    lang = en-US
    encoding = utf-8
[style]
    # Bootstrap/jQuery (uses CDN): on, off
    bootstrap = on
    jquery = on
    # Where generated stylesheet/js documents will go inside the
    # generate folder. This is how HTML documents will refer to them as
    # well, so make sure to include a preceding slah if these will be in
    # the root of your site.
    css = /css/
    js = /js/
[content]
    # Div ids and classes; check the HTML for a better idea of how these
    # work.
    main = main
    header = navbar navbar-fixed navbar-top navbar-inverse
    header_role = navigation
    header_content = container-fluid col-xs-10 col-xs-offset-1 col-md-8 col-md-offset-2
    nav = 
    nav_role = navigation
    container = container-fluid
    row = row
    content = col-xs-10 col-xs-offset-1 col-md-8 col-md-offset-2
    footer = footer
    footer_content = container-fluid col-xs-10 col-xs-offset-1 col-md-8 col-md-offset-2
[sundara]
    # Directories: use a trailing slash!
    md = md/
    generate = www/
    css = css/
    js = js/
[server]
    ip = 127.0.0.1
    port = 8080
"""

# SITEMAP % (domain)
SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset
      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
      http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
<url>
  <loc>http://%s/</loc>
  <priority>1.00</priority>
  <changefreq>weekly</changefreq>
</url>
</urlset>
"""

# SITEMAP_URL % (domain, page)
SITEMAP_URL = """<url>
  <loc>http://%s/%s</loc>
  <priority>0.8</priority>
  <changefreq>weekly</changefreq>
</url>
"""

# ROBOTS % (domain, domain)
ROBOTS = """User-agent: *
Disallow: 
Sitemap: http://%s/sitemap.gz
Sitemap: http://%s/sitemap.xml
"""

INIT_FILES = {
        'README.md': README,
        '.gitignore': GITIGNORE,
}

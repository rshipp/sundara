# Sundara jāla

### For a beautiful web.

## What is it?

Sundara jāla is (yet another) static website generator. It may not be
better than any other generator, and it may not do what you want it to.
It does, however, do exactly what I need.

## So what does it do?

At its most basic level, Sundara is a markdown to HTML5 converter. It
was designed to allow easy and extremely customizable creation of
standards-compliant HTML5 websites, beautiful both to the end user and
under the hood.

The stated goals of this project are as follows:

* To output perfectly formed HTML5 web pages.
* To integrate with Bootstrap and jQuery to provide end-user eye candy.
* To maintain seperation of code, style and content.
* To simplify the process of creating and maintaining a website.
* To allow any level of customization without sacrificing simplicity.

## What does the name mean?

Sundara jāla can be translated (more or less literally) from Sanskrit as
"beautiful web." (But I don't know Sanskrit, and am relying solely on
online translators, so don't quote me on that.)

## Installation

First, make sure you have the `libgit2` headers installed. If you're on
Ubuntu <=12, this means you probably want to compile it from source.
Check the `before_install` script in `.travis.yml` if you need help with
that. On Ubuntu >12, you'll want `libgit2-dev`; on other distros, look
for a `libgit2-dev` or `libgit2` package.

Once libgit2 is installed, you should be good to go. Just run:

    git clone https://github.com/george2/sundara.git
    cd sundara
    sudo python setup.py install

## Usage

### Command syntax

Starting development on a new website is easy:

    sundara init mywebsite

Or:

    cd mywebsite
    sundara init

The main purpose of Sundara is to generate websites, so presumably
at some point you will want to do this. To have Sundara read in all
your wonderful content and beautiful style documents and spit out
a shiny new website, run:

    sundara generate

The site files will be placed in the `www\` subdirectory by default.
You should never need to edit these files (if you do, all your
changes will be overwritten the next time you run `sundara generate`).
Just copy them directly on to your web server, and you're ready to go.

If you need to change the default site directory to something else (to
avoid conflicts with a subdirectory in your site, for example), just
tell Sundara where to put the files explicitly:

    sundara generate mywwwwfiles

Sundara comes with a small built-in development server, so you can test
your changes instantly:

    sundara server [[ip_address:]port]

By default, the server binds to 127.0.0.1:8080. Note that the
server's root is set to the `www\` subdirectory, so you should
run `sundara generate` first to create/update those files.

### Creating content

Sundara uses git to find files you have added to your git repository.
Any file that ends with `.md` is assumed to be a webpage, and will be
added to your site.

To start with, you will probably want a homepage; create index.md with
your content, and add it to the git index:

    git add index.md

For other markdown files, sundara will use the filename, minus the
`.md` extension, to decide where to place the file in your website.
For example, if you create a file called `about.md` that contains
content for your About page, then add that file to Sundara and
generate your website:

    git add about.md
    sundara generate

You will be able to access the new page (once you put it on your
server, of course) as [http://yoursite.com/about]().

But what if you want to add subdirectories to your site? Well,
Sundara supports that too:

    git add mysubdir/mynewpage.md
    sundara generate

The new page will be placed on your site as
[http://yoursite.com/mysubdir/mynewpage]().

### Changing the look of your site

Websites generated with Sundara will use the generic bootstrap CSS
files by default. If you want to do some bootstrap subclassing,
or even remove bootstrap altogether and use your own stylesheets,
you can do that too.

    # TODO


## Hacking

The source is Python 3, and is freely available under a "New BSD" or
"BSD 3-clause" license. You are encouraged, but not required, to
contribute any changes you make back to the project.

### Have fun!

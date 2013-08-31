# Sundara jāla
## For a beautiful web.

### What is it?
Sundara jāla is (yet another) static website generator. It may not be
better than any other generator, and it may not do what you want it to.
It does, however, do exactly what I need.

### So what does it do?
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

### What does the name mean?
Sundara jāla can be translated (more or less literally) from Sanskrit as
"beautiful web." (But I don't know Sanskrit, and am relying solely on
online translators, so don't quote me on that.)

### Installation


### Usage
#### Command syntax
Sundara's command-line syntax is heavily influenced by git and django.

Starting development on a new website is easy:

    $ # Create a new project, git style
    $ mkdir mywebsite
    $ cd mywebsite
    $ sundara init
    $ # Or if you prefer, django-style
    $ sundara startproject mywebsite
    $ cd mywebsite

Since Sundara makes use of git behind the scenes, you can (and are
encouraged to) take advantage of all of git's features:

    $ sundara remote add origin https://github.com/myusername/mywebsite.git
    $ sundara push -u origin master
    $ sundara checkout -b development
    $ # Edit your website
    $ sundara add -A
    $ sundara commit -m "Made it all better." -m "Changed this, that and the other."
    $ sundara push -u origin development
    $ sundara checkout master
    $ sundara merge development
    $ sundara push

The main purpose of Sundara is to generate websites, so presumably
at some point you will want to do this. To have Sundara read in all
your wonderful content and beautiful style documents and spit out
a shiny new website, run:

    $ sundara generate

The site files will be placed in the `www\` subdirectory. You should
never need to edit these files (if you do, all your changes will be
overwritten the next time you run `sundara generate`). Just copy
them directly on to your web server, and you're ready to go.

Just like django, Sundara comes with a small built-in development
server, so you can test your changes instantly:

    $ sundara runserver [[ip_address:]port]

By default, the server binds to 127.0.0.1:8080. Note that the
server's root is set to the `www\` subdirectory, so you should
run `sundara generate` first to create/update those files.

#### Creating content
Sundara uses git to find files you have added to your git repository.
Any file that ends with `.md` is assumed to be a webpage, and will be
added to your site. 

To start with, you will probably want a homepage:

    $ vim index.md
    $ # Write the markdown content for your homepage!
    $ sundara add index.md

For other markdown files, sundara will use the filename, minus the
`.md` extension, to decide where to place the file in your website.
For example, if you create a file called `about.md` that contains
content for your About page, then add that file to Sundara and
generate your website:

    $ sundara add about.md
    $ sundara generate

You will be able to access the new page (once you put it on your
server, of course) as http://yoursite.com/about

But what if you want to add subdirectories to your site? Well,
Sundara supports that too:

    $ sundara add mysubdir/mynewpage.md
    $ sundara generate

The new page will be placed on your site as 
http://yoursite.com/mysubdir/mynewpage.md

If you want to create s subdirectory with the same name as one of
the folders Sundara creates, that's possible too (although a little
more complicated). Say you want to put a page on your site as
http://yoursite.com/www/mywebtips

    $ mkdir www_files  # You can call this folder whatever you want.
    $ vim www_files/mywebtips.md  # Write that amazing content.
    $ sundara add www_files/mywebtips.md --as www/mywebtips

Note: You can use the `--as` flag for any page, but you are
encouraged to avoid it if at all possible.

#### Changing the look of your site
Websites generated with Sundara will use the generic bootstrap CSS
filles by default. If you want to do some bootstrap subclassing,
or even remove bootstrap altogether and use your own stylesheets,
you can do that too. 

    # TODO


### Hacking
The source is Python 3, and is freely available under a "New BSD" or
"BSD 3-clause" license. You are encouraged, but not required, to
contribute any changes you make back to the project. The development
cycle for Sundara most closely resembles git-flow; in other words,
please DO NOT submit pull requests to the `master` branch; new features
are developed in a branch named after them (for example, if you wanted to
add support for embedded videos, you might create a branch called
`video-support`), and bugs are fixed in the `bugfix` branch. New features
will be developed in their own branches and eventually merged into
`development` to be tested, while bugfixes will be commited to the
`bugfix` branch and merged into `development` when they are in a
working state. At arbitrary intervals when the code is determined to
be (mostly) bug-free and contain the planned features for a version,
it will be merged into `master` and tagged as a new release.

Have fun!

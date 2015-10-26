Flask blog
==========

Personal blog written using the Flask microframework.

**This is a personal project and I will not be actively maintaining it, nor accepting any form of requests. Nor merge requests, though that's impossible since this is a personal git install. The source was only made available to be nice, some people might like it.**

With that being said. This software is pretty much [WTFPL](https://en.wikipedia.org/wiki/WTFPL) licenced if anything

If you do something with this code, mention me on [Twitter](http://twitter.com/QuadPiece), I'd love to see :3

Requirements
============

Python 2.7+, because that's just what Flask recommends.  
`tmux` to keep the blog running.

Everything else is listed in the `requirements.txt` file.  
You might also want to make sure that you have `sqlite3` installed on your system so that you can generate the database.

I will not be providing any support for Windows users.

Getting started
===============

Setup is fairly easy for this application due to the nature of how it's built. However, I will inform you ahead of time that this is not designed for high-traffic load. Due to things like SQLite usage.

1. Clone the repository into a folder anywhere you wish
2. (Optional) Create a virtual environment for the project
3. Install everything listed in requirements.txt using `pip install -r requirements.txt` or do it manually
4. Proceed with the relevant procedure fitting your use case below

Development
-----------

1. Generate the sqlite database by running `sqlite3 blog.db < schema.sql` in the directory where you cloned the repo
2. Do `python exec.py`
3. Start working

Production
----------

1. Edit the variables in `exec.py` to fit your needs, **Make sure you remove `debug=True` from `app.run()` for security reasons, you should also make sure that `host="<something>"` is set to `127.0.0.1` for step 3**
2. Generate the sqlite database by running `sqlite3 blog.db < schema.sql` in the directory where you cloned the repo
3. Set up a proper webserver to handle your requests. I recommend nginx. Configure it as a reverse proxy for your desired subdomain or url, pointing to `127.0.0.1` and whatever port you defined in `exec.py`
4. Do `python exec.py`
5. (Optional) It's heavily recommended that you configure your webserver to handle static files for you. This can greatly improve performance and in some cases, security

Migration
---------

Now this is the best part

1. Do exactly the same as above, but instead of creating the database with the `schema.sql` file, just bring along your own `blog.db` file

Backup
------

1. Copy the `blog.db` somewhere

why can't everything be this easy

Usage
=====

This is really simple at the moment.

Posts are written using Markdown. I recommend taking a little time to [learn it](https://guides.github.com/features/mastering-markdown/). It's pretty simple and you'll get the basics in a minute or two

* You can log in using `example.com/login`, you must do this before anything else on this list will work
* A logout link and a link to the post editor will appear at the bottom
* To edit a post, use the link added to the post page. Alternatively, add `/edit` to the post url. To edit `example.com/post/2`, you'd visit `example.com/post/2/edit`
* To delete a post, replace `post` in the URL with `del`. To delete `example.com/post/3`, you'd just visit `exaple.com/del/3` **WARNING: No confimation, your post will be deleted the instant the server recieves the GET request from your browser**

At the moment, that's it.

For images, upload them somewhere else and add them using regular markdown

Goals
=====

This project was started to learn some basic Flask and Python features that could come in handy later. Mainly, these features are:

* Using markdown
* Handling files
* Templating
* Some lazy single-user login just to test the session feature
* ~~Not sure if DB (prolly just SQLite) or static files~~ SQLite apparently
* Getting used to route-based web development

**Warning, most of the Python code will probably end up being written in a single, messy file. Call me old school or stupid, but "ctrl+f"-ing for the route I want to work on is just how I tend to go about these things**
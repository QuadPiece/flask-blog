Flask blog
==========

Personal blog written using the Flask microframework.

Usage
-----

Setup is faily easy for this application due to the nature of how it's built. However, I will inform you ahead of time that this is not designed for high-traffic load. Due to things like SQLite usage.

1. Clone the repository into a folder anywhere you wish
2. (Optional) Created a virtual environment for the project
3. Install everything listed in requirements.txt using `pip install -r requirements.txt` or do it manually
4. Proceed with the relevant procedure fitting your use case below

### Development

1. Generate the sqlite database by running `sqlite3 blog.db < schema.sql` in the directory where you cloned the repo
2. Do `python exec.py`
3. Start working

### Production

1. Edit the variables in `exec.py` to fit your needs, **Make sure you remove `debug=True` from `app.run()` for security reasons, you should also make sure that `host="<something>"` is set to `127.0.0.1` for step 4**
2. Generate the sqlite database by running `sqlite3 blog.db < schema.sql` in the directory where you cloned the repo
3. Set up a proper webserver to handle your requests. I recommend nginx. Configure it as a reverse proxy for your desired subdomain or url, pointing to `127.0.0.1` and whatever port you defined in `exec.py`
4. Do `python exec.py`
5. (Optional) It's heavily recommended that you configure your webserver to handle static files for you. This can greatly improve performance and in some cases, security

### Migration

Now this is the best part

1. Do exactly the same as above, but instead of creating the database with the `schema.sql` file, just bring along your own `blog.db` file

Goals
-----

This project was started to learn some basic Flask and Python features that could come in handy later. Mainly, these features are:

* Using markdown
* Handling files
* Templating
* Some lazy single-user login just to test the session feature
* Not sure if DB (prolly just SQLite) or static files
* Getting used to route-based web development
* Maybe some JSON stuff
* Maybe some Self-written caching in Python

**Warning, most of the Python code will probably end up being written in a single, messy file. Call me old school or stupid, but "ctrl+f"-ing for the route I want to work on is just how I tend to go about these things**

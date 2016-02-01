# Import party
import sqlite3, markdown, time
from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup

# Config variables
# TODO: Move to a separate file
DATABASE = './blog.db'
SECRET_KEY = 'sample key'
USERNAME = 'user'
PASSWORD = 'bananacar'
DEBUG = True

# Create instance
app = Flask(__name__)
app.config.from_object(__name__)


# Debug functions
def calculate_time():
  return (time.time() - g.startTime) * 1000


# Database functions
def db_connect():
  return sqlite3.connect(app.config['DATABASE'])


# TODO: Take the time to only use this function when needed
@app.before_request
def before_request():
  g.db = db_connect()
  if app.config['DEBUG']:
    g.startTime = time.time()


# TODO: Take the time to only use this function when needed
@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()
  if app.config['DEBUG']:
    app.logger.debug('Request processed in %d ms', calculate_time())


def query_db(query, args=(), one=False):
  cur = g.db.execute(query, args)
  rv = cur.fetchall()
  return (rv[0] if rv else None) if one else rv


def time_to_string(unixtime):
  return datetime.fromtimestamp(unixtime).strftime('%B %d, %Y (%H:%M - ' + time.tzname[time.daylight] + ')')


# Actual routes for the basic site
@app.route('/')
def home():
  cur = g.db.execute('select title, id, text, time from entries order by id desc')
  entries = [dict(title=row[0], id=row[1], text=row[2], time=row[3]) for row in cur.fetchall()]

  if len(entries) < 1:
    return render_template('empty.html')

  # Fix post one for display if it exists
  if entries[0]:
    entries[0]["text"] = Markup(markdown.markdown(entries[0]["text"]))
    if entries[0]["time"]:
      entries[0]["time"] = time_to_string(entries[0]["time"])
    else:
      entries[0]["time"] = None

  if len(entries) > 5:
    return render_template('home.html', entries=entries[1:5], post=entries[0], long=True)
  else:
    return render_template('home.html', entries=entries[1:], post=entries[0], long=False)

@app.route('/all')
def post_list():
  cur = g.db.execute('select title, id, time from entries order by id desc')
  entries = [dict(title=row[0], id=row[1], time=row[2]) for row in cur.fetchall()]

  if entries:
    for entry in entries:
      if entry["time"]:
        entry["time"] = time_to_string(entry["time"])
    else:
      entry["time"] = None

  if len(entries) < 1:
    return render_template('empty.html')

  return render_template('list.html', entries=entries, long=False)


@app.route('/post/<int:id>')
def view_post(id):
  response = query_db('select title, text, time, updated from entries where id = ?', [id])
  posts = [dict(title=row[0], text=row[1], time=row[2], updated=row[3]) for row in response]
  posts[0]["text"] = Markup(markdown.markdown(posts[0]["text"]))
  # Unix epoch time -> Human readable
  if posts[0]["time"]:
    posttime = time_to_string(posts[0]["time"])
  else:
    posttime = None
  if posts[0]["updated"]:
    updatetime = time_to_string(posts[0]["updated"])
  else:
    updatetime = None
  return render_template('post.html', post=posts[0], id=id, posttime=posttime, updatetime=updatetime)


# Editor routes
@app.route('/add', methods=['POST'])
def add_post():
  if not session.get('logged_in'):
    abort(401)
  g.db.execute('insert into entries (title, text, time) values (?, ?, ?)',
               [request.form['title'], request.form['text'], time.time()])
  g.db.commit()
  flash('New entry was successfully posted')
  return redirect(url_for('home'))


@app.route('/update/<int:postid>', methods=['POST'])
def update_post(postid):
  if not session.get('logged_in'):
    abort(401)
  g.db.execute('update entries set title = ?, text = ?, updated = ? where id = ?',
               [request.form['title'], request.form['text'], time.time(), postid])
  g.db.commit()
  flash('Post was updated')
  return redirect(url_for('home'))


@app.route('/write')
def write_new():
  if not session.get('logged_in'):
    abort(401)
  else:
    return render_template('newpost.html')


@app.route('/del/<int:id>')
def delete_post(id):
  if not session.get('logged_in'):
    abort(401)
  g.db.execute('delete from entries where id = ?', [id])
  g.db.commit()
  flash('Deleted post ID:' + str(id))
  return redirect(url_for('home'))


@app.route('/post/<int:id>/edit')
def edit_post(id):
  if not session.get('logged_in'):
    abort(401)
  response = query_db('select title, text from entries where id = ?', [id])
  posts = [dict(title=row[0], text=row[1]) for row in response]
  return render_template('edit.html', post=posts[0], id=id)


# Sessions
@app.route('/login', methods=['GET', 'POST'])
def login_page():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('home'))
  return render_template('login.html', error=error)


@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('home'))


app.run(host="0.0.0.0", port=5800)

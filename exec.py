# Import party
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#Config variables
DATABASE = './blog.db'
SECRET_KEY = 'sample key'
USERNAME = 'user'
PASSWORD = 'bananacar'

# Create instance
app = Flask(__name__)
app.config.from_object(__name__)

# Database functions
def db_connect():
  return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = db_connect()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Actual routes
@app.route('/')
def home():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('home.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('home'))

# Sessions
@app.route('/login', methods=['GET', 'POST'])
def login():
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

app.run(debug=True,host="0.0.0.0",port=5800)

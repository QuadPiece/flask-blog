# Import party
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#Config
DATABASE = './blog.db'
DEBUG = True
SECRET_KEY = 'sample key'
USERNAME = 'user'
PASSWORD = 'bananacar'

# Create instance
app = Flask(__name__)
app.config.from_object(__name__)

# Database functions
def db_connect():
  return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def index():
  return 'Hello World!'

app.run(debug=True)

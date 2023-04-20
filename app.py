# native imports
import os
import datetime
# third-party imports 
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
# local imports
from helpers import login_required, dbinit

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///main.db")

# Handle 404 Error - Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

# Handle 403 Error - Forbidden
@app.errorhandler(403)
def page_not_found(e):
    return render_template('errors/403.html'), 403

# Handle 500 Error - Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'), 500

# Handle 503 Error - Service Unavailable
@app.errorhandler(503)
def page_not_found(e):
    return render_template('errors/503.html'), 503

# Handle 504 Error - Gateway Timeout
@app.errorhandler(504)
def page_not_found(e):
    return render_template('errors/504.html'), 504

# Determine where user lands when opening the app
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
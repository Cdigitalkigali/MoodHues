# native imports
import os
from datetime import datetime
import linecache
# third-party imports 
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
# local imports
from helpers import login_required, dbinit

# Configure application
app = Flask(__name__)
dbinit()
 
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "7895s48s9511s85z"

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///main.db")

# Determine where user lands when opening the app
@app.route("/", methods=["GET"])
def index():
    if session.get("user_id") is None:
        return render_template("app/landing.html")
    else:
        return redirect("/app")


# Signup
@app.route("/signup", methods=["POST"])
def signup():
    session.clear()
    # Get form inputs
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    # Check if username already exists
    check = db.execute("SELECT * FROM users WHERE username == :user", user=username)
    if len(check) != 0:
        flash("That username is already taken, please try another.")
        return redirect("/")
    else:
        # Sign user up
        db.execute("INSERT INTO users (username, email, pwd, pfp, premium) VALUES (:username, :email, :pwd, :pfp, :premium)",
            username = username,
            email = email,
            pwd = generate_password_hash(password),
            pfp = "none",
            premium = "1"
        )
        # Sign user in
        current_user = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        session["user_id"] = current_user[0]["id"]
        # Send them to their homepage
        return redirect("/")

# Signin
@app.route("/signin", methods=["POST"])
def singin():
    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = :username",
                        username=request.form.get("username"))
    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["pin"], request.form.get("pin")):
        flash("Username or password incorrect")
        return redirect("/")
    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]
    # Redirect user to home page
    return redirect("/")

# Logout
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

# Main app interface
@app.route("/app")
def app_view():
    # Get all information about the user
    current_user = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
    user_id = current_user[0]["id"]
    user_gratitude = db.execute("SELECT * FROM gratitude WHERE user_id = :id", id = user_id)
    user_moods = db.execute("SELECT * FROM moods WHERE user_id = :id", id = user_id)
    
    # Find first day of this month
    input_dt = datetime.today()
    res = input_dt.replace(day=1)
    first = res.date()
    
    # Find all the moods since the first day of the month
    user_moods_month = db.execute("SELECT * FROM moods WHERE user_id = :id AND created > :first", id = user_id, first=first)
    
    # Define variables for each mood
    happy = 0
    sad = 0
    neutral = 0
    anxious = 0
    angry = 0
    tired = 0
    depressed = 0
    emotional = 0
    sickly = 0
    
    # Populate variables by looping through the list
    for i in range(len(user_moods_month)):
        if user_moods_month[i]["mood"] == "happy":
            happy = happy + 1
        elif user_moods_month[i]["mood"] == "sad":
            sad = sad + 1
        elif user_moods_month[i]["mood"] == "neutral":
            neutral = neutral + 1
        elif user_moods_month[i]["mood"] == "anxious":
            anxious = anxious + 1
        elif user_moods_month[i]["mood"] == "angry":
            angry = angry + 1
        elif user_moods_month[i]["mood"] == "tired":
            tired = tired + 1
        elif user_moods_month[i]["mood"] == "depressed":
            depressed = depressed + 1
        elif user_moods_month[i]["mood"] == "emotional":
            emotional = emotional + 1
        else:
            sickly = sickly + 1
    
    # Find total moods for the month
    total = happy + sad + neutral + anxious + angry + tired + depressed + emotional + sickly
    
    # Calculate percentages of moods for the month
    if len(user_moods_month) != 0:
        phappy = round((happy / total) * 10)
        psad = round((sad / total) * 10)
        pneutral = round((neutral / total) * 10)
        panxious= round((anxious / total) * 10)
        pangry = round((angry / total) * 10)
        ptired = round((tired / total) * 10)
        pdepressed = round((depressed / total) * 10)
        pemotional = round((emotional / total) * 10)
        psickly = round((sickly / total) * 10)

        # Get suggestions from the suggestions.txt
        depressed_suggestion = linecache.getline(r"/resources/suggestions.txt", 1)
        happy_suggestion = linecache.getline(r"/resources/suggestions.txt", 2)
        mixed_suggestion = linecache.getline(r"/resources/suggestions.txt", 3)

        # If you are depressed more than fifty percent of the time:
        if pdepressed >= 50:
            msg = depressed_suggestion
        # If you are happy more than fifty percent of the time:
        elif phappy >= 50:
            msg = happy_suggestion
        # Or else:
        else:
            msg = mixed_suggestion
        
        return render_template("index.html", 
        current_user=current_user, 
        user_moods=user_moods, 
        user_gratitude=user_gratitude, 
        user_moods_month=user_moods_month, 
        last=last, 
        happy=happy, 
        sad=sad, 
        neutral=neutral, 
        anxious=anxious, 
        angry=angry, 
        tired=tired, 
        emotional=emotional, 
        depressed=depressed, 
        sickly=sickly, 
        phappy=phappy, 
        psad=psad, 
        pneutral=pneutral, 
        panxious=panxious, 
        pangry=pangry, 
        ptired=ptired, 
        pemotional=pemotional, 
        pdepressed=pdepressed, 
        psickly=psickly, msg=msg
        )
    return render_template("app/index.html", current_user=current_user)


# Adding moods for the day
@app.route("/add-mood", methods=["POST"])
@login_required
def add_mood():
    # Get form inputs
    mood = request.form.get("mood")
    note = request.form.get("note")
    diet = request.form.get("diet")
    stress = request.form.get("stress")
    exercise = request.form.get("exercise")

    # Write inputs into table
    db.execute("INSERT INTO moods (user_id, mood, note, diet, stress, exercise, created) VALUES (:user_id, :mood, :note, :diet, :stress, :exercise, :created)",
        user_id = session["user_id"],
        mood = mood,
        note = note,
        diet = diet,
        stress = stress,
        exercise = exercise,
        created = datetime.now()
    )
    return redirect("/")




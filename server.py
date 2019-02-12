"""RunBuddy Routes"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Message, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/register")
def get_new_user_info():
    """Show  user registration  page ."""
    
    return render_template("registration.html")

@app.route("/register", methods = ["POST"])
def register_new_user():
    """All new user to complete registration form and save details
    in database.  Save user to session"""



    user_name = request.form.get('name')
    user_email = request.form.get('email')
    password = request.form.get('password')
    street_address = request.form.get('street_address')
    city = request.form.get('city')
    state = request.form.get('state')
    zipcode = request.form.get('zipcode')
    pace = request.form.get('pace')
    run_type = request.form.get('run_type')

    user = User.query.filter_by(email = user_email).first()

    if user != None:
        return redirect("user_login.html")

    else:
        user = User(
            name = user_name,
            email = user_email,
            password =password,
            street_address =street_address,
            city = city,
            state = state,
            zipcode = zipcode,
            pace = pace,
            run_type = run_type,)

        db.session.add(user)
        db.session.commit()
    
    
    return redirect("/user_login")




@app.route("/user_login")
def login_user():
    """Allow existing user to login ."""
    
    return render_template("user_login.html")

@app.route("/user_login", methods = ["POST"])
def verify_user_login():
    """make sure that password is correct."""

    user_email = request.form.get('email')
    password = request.form.get('password')


    user = User.query.filter_by(email = user_email).first()
    print(user)

    if user == None:
        flash("User information not found, redirecting to registration.")
        return redirect('/register')

    elif user.password == password:
        

        session["user_id"] = user.user_id
        print(session["user_id"])
        flash("Logged in!")
        return redirect('/search')

    else:
        flash("Error, please try logging in again.")
        return redirect('/user_login')





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
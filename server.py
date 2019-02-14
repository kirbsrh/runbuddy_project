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
    """All new users need to complete registration form. Commit and save details
    in database. Send registered user to confirmation page once complete.
    If user already exists, redirect to login to avoid duplicates"""

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

    return render_template("/confirmation_page.html")

#@app.route("/confirmation_page")
#def confirm_registered_user():
    """confirm that the new user is registered 
        and provide them with nav options"""


   # return render_template("/confirmation_page.html")

@app.route("/profile")
def show_runner_profile():
    """display the profile of the user saved in the session."""

    user = User.query.get(session['user_id'])
    print(user)

    return render_template("/profile.html", user = user)



@app.route("/user_login")
def login_user():
    """Allow existing user to view login page."""
    
    return render_template("user_login.html")

@app.route("/user_login", methods = ["POST"])
def verify_user_login():
    """Log user in by making sure that password is correct."""

    user_email = request.form.get('email')
    password = request.form.get('password')

    #save user object using email as unique identifier
    user = User.query.filter_by(email = user_email).first()
    
    # if a user tries to login but is not registered, redirect to registration
    if user == None:
        flash("User information not found, redirecting to registration.")
        return redirect('/register')

    #if user exists, make sure password matches database
    elif user.password == password:

        #save user to the session
        session['user_id'] = user.user_id 

        #save the user_name variable and pass this to confirmation page to display
        user_name = user.name
        
        flash("Logged in!")
        return render_template('/options.html', user_name = user_name)

    # if the user is not None but the passwords do not match have them try again 
    else:
        flash("Error, please try logging in again.")
        return redirect('/user_login')


@app.route("/search")
def display_search_page():
    """Show search page form """

    return render_template("search.html")


@app.route("/search", methods = ["POST"])
def process_search_request():
    """Process search form data."""

    #set zipcode to zipcode query
    zipcode = request.form.get('zipcode')

    #set pace to pace query
    pace = request.form.get('pace')

    #search for users/runners who meet criteria in form
    # save query as object list

    user_list = User.query.filter_by(zipcode = zipcode, pace = pace).all()
    
    # if the query has no results let the user know
    if user_list == None:
        flash("No runners found who meet your criteria, please alter your search.")
        return redirect('/search')

    # pass list of results to display in display runner info template
    else:
        
        return render_template("display_runner_info.html",
         user_list = user_list)


@app.route("/user_info/<user_id>")
def show_specific_user_profile(user_id):
    """Allow user to view the profile details of a runner
    who appears in their search results"""

    user = User.query.get(user_id)

    name = user.name
    city = user.city
    pace = user.pace
    run_type =user.run_type
    user_id = user.user_id

    return render_template("/user_info.html", name = name,
     city = city, pace = pace, run_type = run_type, user_id = user_id)

@app.route("/send_message/<user_id>")
def show_message_form(user_id):
    """Display the form to send a message to a user"""

    user = User.query.get(user_id)
    print(user)

    name = user.name
    user_id = user.user_id

    return render_template("/send_message.html", name = name, user_id = user_id)

@app.route("/send_message", methods = ["GET","POST"])
def send_message():
    """Send message from sender to receiver and store message in DB"""

    #data stored in the session is that of the user who is logged in
    #the user who is logged in is the sender

    sender_id = session['user_id']
    print(sender_id)

    #get the user object of the person we are sending the message to
    

    #set the user_id of the user object equal to the variable receiver_id
    receiver_id = request.form.get('receiver_id')
    print(receiver_id)

    #get message from form and save it as message variable
    message = request.form.get('message')

    #check to make sure there is a message before adding to DB
    if message == None:
        flash("Error!  Your message appears to be blank.  Please try again.")
        return redirect("/send_message.html")

    else:

        #create message object
        new_message = Message(
            sender_id = sender_id,
            receiver_id = receiver_id,
            message = message,
           )

        db.session.add(new_message)
        db.session.commit()

                #make sure the user knows that their message was sent
        flash("Message successfully sent!")

        # redirect to search page to see if user wants to do anything else
        return redirect("/search.html")


        #set query equal to a variable
        # sql = """"INSERT INTO messages (sender_id, receiver_id, message")
        # VALUES (:sender_id, :receiver_id, :message)"""

        # #execute query with variables
        # db.session.execute(
        # sql, {
        # "sender_id" : sender_id,
        # "receiver_id" : receiver_id,
        # "message" : message,
        #     }
        # )

        # db.session.execute("""INSERT INTO messages (sender_id, receiver_id, message")
        #     VALUES ('sender_id', 'receiver_id', 'message')""")



@app.route("/logout")
def confirm_logout_intention():
    """confirm whether the user really wants to logout"""

    return render_template("logout.html")

@app.route("/logout", methods = ["POST"])
def take_logout_form_action():

    #check to see which button is pressed
    if request.form['submit_button'] == "Logout":

        #log out user by removing them from session
        session.pop('user_id', None)

        #send them to the homepage
        return redirect("/")

    #user does NOT want to logout    
    elif request.form['submit_button'] == "Cancel":

        #send them back to their profile page
        return redirect("/profile")   




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
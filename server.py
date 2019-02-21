"""RunBuddy Routes"""
import geocoder
from math import cos, pi

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Message, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

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

    #add address components together to allow for conversion to lat/long pair
    address = street_address + ", " + city + ", " + state + " " + zipcode

    #get lat long pair from address
    g = geocoder.osm(address)
    lat_long_pair = g.latlng 
    lat = lat_long_pair[0]
    lng = lat_long_pair[1]

    #user email is unique, use this to check for existing users
    user = User.query.filter_by(email = user_email).first()

    # if the user is already found in the DB reroute to login
    if user != None:
        return redirect("user_login.html")

    #user info is not found, instantiate user and add to DB
    else:
        user = User(
            name = user_name,
            email = user_email,
            password =password,
            lat = lat,
            lng = lng,
            pace = pace,
            run_type = run_type,
            )

        db.session.add(user)
        db.session.commit()

    return render_template("/confirmation_page.html")


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
    user = User.query.filter(User.email == user_email).first()
    
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

@app.route("/profile")
def show_runner_profile():
    """display the profile of the user saved in the session."""
   
    user = User.query.get(session['user_id'])
    print(user)

    return render_template("/profile.html", user = user)



@app.route("/search")
def display_search_page():
    """Show search page form """

    return render_template("search.html")


@app.route("/search", methods = ["POST"])
def process_search_request():
    """Process search form data."""

    #set radius to distance selected in form
    distance = request.form.get('distance')
    radius = int(distance)

    #set pace to pace query
    pace = request.form.get('pace')

    #calculate square grid for search using userid saved in session for lat/long center point
    center_user = User.query.get(session['user_id'])

    my_lat = center_user.lat

    my_long =center_user.lng 

    df = (radius/69)

    dl = ((df)/(cos((my_lat)*(pi/180))))

    southernmost_lat = (my_lat - df) 

    northernmost_lat = (my_lat + df) 

    westernmost_long = (my_long - dl)

    easternmost_long =  (my_long + dl) 

    #search for users/runners who meet criteria in form
    # save query as object list

    user_list = User.query.filter((User.lat > southernmost_lat) & 
                                            (User.lat < northernmost_lat) &
                                            (User.lng > westernmost_long) & 
                                            (User.lng < easternmost_long) &
                                            (User.pace == pace)).all()

    
    
    # if the query has no results let the user know
    if user_list == None:
        flash("No runners found who meet your criteria, please alter your search.")
        return redirect('/search')

    # pass list of results to display in display runner info template
    else:
        
        return render_template("display_runner_info.html",
         user_list = user_list, my_lat = my_lat, my_long = my_long)


@app.route("/user_info/<user_id>")
def show_specific_user_profile(user_id):
    """Allow user to view the profile details of a runner
    who appears in their search results"""

    user = User.query.get(user_id)

    name = user.name
    pace = user.pace
    run_type =user.run_type
    user_id = user.user_id

    return render_template("/user_info.html", name = name,
        pace = pace, run_type = run_type, user_id = user_id)

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
    #print(sender_id)

    #set the receiver id from the hidden form equal to the variable receiver_id
    receiver_id = request.form.get('receiver_id')
    #print(receiver_id)

    #get message from form and save it as message variable
    message = request.form.get('message')

    #check to make sure there is a message before adding to DB
    if message == None:
        flash("Error!  Your message appears to be blank.  Please try again.")
        return redirect("/send_message")

    else:

        #create message object
        new_message = Message(
            sender_id = sender_id,
            receiver_id = receiver_id,
            message = message,
           )

        #Add and Save to DB
        db.session.add(new_message)
        db.session.commit()

        #make sure the user knows that their message was sent
        flash("Message successfully sent!")

        # redirect to search page to see if user wants to do anything else
        return redirect("/search")

@app.route('/messages')
def show_messages():

    
    #check to see is user is logged in
    if 'user_id' in session:

        #get user info from session to check for messages
        user = User.query.get(session['user_id'])

        #query data base to see if user_id matches receiver_id in Msg table
        #save query as a list 
        message_list = Message.query.filter(Message.receiver_id == user.user_id).all()

    

        #check to see if message list is empty or none, redirect to search
        if message_list == []:
            flash("You do not have any messages at this time. Find someone to message!")
            return redirect("/profile")

    # if there are messages then loop over messages to pull out details
        else:
            for message in message_list:
                sender_id = message.sender_id
                sender_info = User.query.get(sender_id)
                sender_name = sender_info.name

            return render_template("messages.html", message_list = message_list,
             sender_name = sender_name, sender_id = sender_id)

    else:

           #if user not logged in, redirect to login
        flash("You must be logged in to view your messages.  Please login.")
        return redirect("/user_login")

@app.route("/change_details")
def change_user_details():
    """display the profile of the user saved in the session and allow them
    to view and make changes."""

    #for the "get" portion of the route:
    
    #check to see make sure user is logged in
    if 'user_id' in session:

        user = User.query.get(session['user_id'])

        #get user latitude and longitude
        user_lat = user.lat
        
        user_lng = user.lng
        

        #use lat lng details to get address info for user
        user_address_info = geocoder.osm([user_lat, user_lng], method = 'reverse')
    
        #get housenumber
        housenumber = user_address_info.housenumber
        #get street
        street = user_address_info.street
        #get city
        city = user_address_info.city
        #get state
        state = user_address_info.state
        #get zipcode
        zipcode = user_address_info.postal
        

        #use string concatenation to recreate and display user address
        user_address = housenumber + " " + street + ", " + city + ", " + state + " " + zipcode

    
        return render_template("/change_details.html", user = user,
            user_address = user_address)
    else:

       #if user not logged in, redirect to login
        flash("You must be logged in to view your profile details.  Please login.")
        return redirect("/user_login")

@app.route("/send_details", methods = ["POST"])
def allow_for_user_edits():
    """take responses from form and allow user to edit existing information and
    save new changes to the DB"""

    
    if 'user_id' in session:
        #user should still be the user in the session
        user = User.query.get(session['user_id'])

        #get details from edits form
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        address = request.form.get('address')
        pace = request.form.get('pace')
        run_type = request.form.get('run_type')

        #take user address and convert to lat long to store in DB for search purposes
        g = geocoder.osm(address)
        lat_long_pair = g.latlng 
        lat = lat_long_pair[0]
        lng = lat_long_pair[1]

        #update user in database with new information

        user.name = user_name
        user.email = user_email
        user.lat = lat
        user.lng = lng
        user.pace = pace
        user.run_type = run_type
            
           

        #add and save user changes to DB
        
        db.session.commit()
        flash("Your profile has been updated!!")
        return render_template("/change_success.html", user = user, address = address)

    else:
        #if user not logged in, redirect to login
        flash("You must be logged in to view your profile details.  Please login.")
        return redirect("/user_login")




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


@app.route("/test_map")
def test_map_functionality():
    """Route purely for testing OSM mapping with Open Layers"""

    #points

    user_list = User.query.all()

    return render_template("test_map.html", user_list = user_list) 

@app.route("/test_map_2")
def test_map_with_popups():
    """Route purely for testing OSM maps with popup functionality"""

    return render_template("test_map_2.html") 

@app.route("/test_map_3")
def test_map_with_functioning_popups():
    """Route purely for testing OSM maps with popup functionality"""

    return render_template("test_map_3.html")




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
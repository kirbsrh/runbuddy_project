"""RunBuddy Routes"""
import geocoder
#import correlation
from math import cos, pi, sqrt

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify, url_for)
from flask_debugtoolbar import DebugToolbarExtension

from hashlib import md5

from model import User, Message, Compatibility, connect_to_db, db
from similarity import euclid, square_rooted, cosine_similarity, corrcoef
from search_functions import get_radius, get_pace, calculate_search_grid



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
        full_name_list = user_name.split()
        first_name=full_name_list[0]
        
        flash("Logged in!")
        return render_template('/options.html', first_name = first_name)

    # if the user is not None but the passwords do not match have them try again 
    else:
        flash("Error, please try logging in again.")
        return redirect('/user_login')


@app.route("/runner_compatibility")
def display_runner_compatibility_form():
    """display the form for runner compatibility"""

    return render_template("/runner_compatibility.html")

@app.route("/runner_compatibility", methods = ["POST"])
def store_runner_compatibility_data():
    """add runner compatibility to database"""

    activity_quest = request.form.get('activity_level')
    talking_quest = request.form.get('talking')
    weather_quest = request.form.get('weather')
    distance_quest = request.form.get('distance')
    track_quest = request.form.get('track')
    dogs_quest = request.form.get('dogs')
    kids_quest = request.form.get('kids')
    music_quest = request.form.get('music')
    current_race_quest = request.form.get('current_race')
    why_quest = request.form.get('why')

    #get user info from session
    user = User.query.get(session['user_id'])

    # user.compatibility = compatibility_list
    compatibility_list = Compatibility.query.all()

    if user.user_id in compatibility_list:
        flash("You have already completed our compatibility form.  Start your search!")
        return redirect("search.html")

    #user info is not found, instantiate user and add to DB
    else:

        new_user_compatibility = Compatibility(
            user_id = int(user.user_id),
            activity_quest = int(activity_quest),
            talking_quest = int(talking_quest),
            weather_quest = int(weather_quest),
            distance_quest = int(distance_quest),
            track_quest = int(track_quest),
            dogs_quest = int(dogs_quest),
            kids_quest = int(kids_quest),
            music_quest = int(music_quest),
            current_race_quest = int(current_race_quest),
            why_quest = int(why_quest)
            )

        db.session.add(new_user_compatibility)
        db.session.commit()

    flash("Your answers have been saved!")
    return redirect('/search')

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

@app.route("/show_results")
def calculate_compatibility_for_user_list():
    """calculate the compatibility for users in the list
    compared with the center user"""
    #call calculate search grid function to get user list
    user_list = calculate_search_grid()

    results_per_page = 10

    total_search_results=len(user_list)
    print(total_search_results)

    total_pages = int(round(total_search_results/results_per_page))

    page = int(request.args.get('page'))

    end = (page*results_per_page)
    beginning = (end)-(results_per_page)
    

    user_list = user_list[beginning:end]

    distance = str(get_radius())
    pace = get_pace()



    # print(user_list)
    
    # if the query has no results let the user know
    if user_list == None:
        flash("No runners found who meet your criteria, please alter your search.")
        return redirect('/search')
    
    else:
    #calculate compatibility scores for users in list
        center_user = User.query.get(session['user_id'])
        center_user_responses = Compatibility.query.get(center_user.user_id)
        my_lat = center_user.lat
        my_long =center_user.lng 
        center_response_list = []

        if center_user_responses == None:
            for user in user_list:
                compatibility_rating = "Not found"
                user.compatibility_rating = (compatibility_rating)
                

        else:
            #query database for answers to questions
            center_activity = center_user_responses.activity_quest
            center_talking = center_user_responses.talking_quest
            center_weather = center_user_responses.weather_quest
            center_distance = center_user_responses.distance_quest
            center_track = center_user_responses.track_quest
            center_dogs = center_user_responses.dogs_quest
            center_kids = center_user_responses.kids_quest
            center_music = center_user_responses.music_quest
            center_current_race = center_user_responses.current_race_quest
            center_why = center_user_responses.why_quest

            #add answers to list
            center_response_list.append(center_activity)
            center_response_list.append(center_talking)
            center_response_list.append(center_weather)
            center_response_list.append(center_distance)
            center_response_list.append(center_track)
            center_response_list.append(center_dogs)
            center_response_list.append(center_kids)
            center_response_list.append(center_music)
            center_response_list.append(center_current_race)
            center_response_list.append(center_why)

            #loop over user list to query DB for answers
            for user in user_list:
                user_responses = Compatibility.query.get(user.user_id)

                if user_responses == None:
                    
                    compatibility_rating = "Not found"
                    user.compatibility_rating = (compatibility_rating)

                else:
                    user_response_list = []

                    user_activity = user_responses.activity_quest
                    user_response_list.append(user_activity)

                    user_talking = user_responses.talking_quest
                    user_response_list.append(user_talking)

                    user_weather = user_responses.weather_quest
                    user_response_list.append(user_weather)

                    user_distance = user_responses.distance_quest
                    user_response_list.append(user_distance)

                    user_track = user_responses.track_quest
                    user_response_list.append(user_track)

                    user_dogs = user_responses.dogs_quest
                    user_response_list.append(user_dogs)

                    user_kids = user_responses.kids_quest
                    user_response_list.append(user_kids)

                    user_music = user_responses.music_quest
                    user_response_list.append(user_music)

                    user_current_race = user_responses.current_race_quest
                    user_response_list.append(user_current_race)

                    user_why =user_responses.why_quest
                    user_response_list.append(user_why)

                    compatibility_rating = euclid(zip(center_response_list, user_response_list))

               
                    user.compatibility_rating = str(compatibility_rating) + "%"
            
        return render_template("/display_runner_info.html", user_list = user_list, my_lat = my_lat, my_long = my_long,
        center_user= center_user, total_search_results=total_search_results, page=page, total_pages=total_pages,
        distance=distance, pace=pace)


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
        pace = pace, run_type = run_type, user_id = user_id, user=user)

@app.route("/send_message/<user_id>", methods = ["GET"])
def show_message_form(user_id):
    """Display the form to send a message to a user"""

    user = User.query.get(user_id)

    name = user.name
    user_id = user.user_id

    print(user)

    return render_template("/send_message.html", name = name, user_id = user_id)


@app.route("/send_message", methods = ["POST"])
def send_message_using_json():
    """using AJAX to send message and display to user"""

       #data stored in the session is that of the user who is logged in
    #the user who is logged in is the sender
    sender_id = session['user_id']
    #print(sender_id)

    user_message = request.form.get('message')
    receiver_id = request.form.get('receiver_id')

    #check to make sure there is a message before adding to DB
    if user_message == None:
        flash("Error!  Your message appears to be blank.  Please try again.")
        return redirect("/send_message")

    else:

        #create message object
        new_message = Message(
            sender_id = sender_id,
            receiver_id = receiver_id,
            message = user_message,
           )

        #Add and Save to DB
        db.session.add(new_message)
        db.session.commit()

        #make sure the user knows that their message was sent
        flash("Message successfully sent!")

        # redirect to search page to see if user wants to do anything else
        print(new_message.message)
        return(new_message.message) 


@app.route('/messages')
def show_messages():
    """let a user view their messages"""
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
                message.sender_name = sender_name


            return render_template("messages.html", message_list = message_list,
             sender_name = sender_name, sender_id = sender_id, sender_info=sender_info)

    else:

           #if user not logged in, redirect to login
        flash("You must be logged in to view your messages.  Please login.")
        return redirect("/user_login")


@app.route("/messages_with_/<user_id>")
def show_messages_with_specific_runner(user_id):
    """show the messages between the logged in user and one other specific user"""

        #check to see is user is logged in
    if 'user_id' in session:

        #get user info from session to check for messages
        logged_in_user = User.query.get(session['user_id'])

        specific_user = User.query.get(user_id)

        #query data base to get messages between logged in user and specific user
        #check sender and receiver for both
        #save query as a list 
        message_list = Message.query.filter(((Message.receiver_id == logged_in_user.user_id) & 
                                            (Message.sender_id == specific_user.user_id))|
                                            ((Message.receiver_id == specific_user.user_id) & 
                                            (Message.sender_id == logged_in_user.user_id))
                                            ).all()

        #query data base to see if user_id matches receiver_id in Msg table
        #save query as a list 
        #message_list = Message.query.filter(Message.receiver_id == user.user_id).all()

        #check to see if message list is empty or none, redirect to search
        if message_list == []:
            flash("You do not have any messages at this time. Find someone to message!")
            return redirect("/profile")

    # if there are messages then loop over messages to pull out details
        else:
            for message in message_list:
                sender_id = message.sender_id
                print (sender_id)
                sender_stuff = User.query.get(sender_id)
                print (sender_stuff)
                sender_name = sender_stuff.name
                message.sender_name = str(sender_name)
                message.sender_stuff=sender_stuff
                
            return render_template("message_history.html", message_list = message_list,
                specific_user = specific_user, sender_stuff=sender_stuff)

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

@app.route("/about_us")
def show_about_us_page():
    """route the user to the about us page"""

    return render_template("/about_us.html")

@app.route("/careers")
def show_career_page():
    """route to the career page"""

    return render_template("/careers.html")

@app.route("/mission")
def show_mission_and_vision():
    """display to page showing vision and mission"""

    return render_template("/mission.html")


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
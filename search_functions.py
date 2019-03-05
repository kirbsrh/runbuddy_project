import geocoder
#import correlation
from math import cos, pi, sqrt
from flask import (Flask, render_template, redirect, request, flash, session, jsonify, url_for)

from model import User, Message, Compatibility, connect_to_db, db


def get_radius():
    """Get distance from search form and calc radius."""

    #set radius to distance selected in form
    distance = request.form.get('distance')
    # print(distance)
    radius = int(distance)

    return radius

def get_pace():
    """Get pace from search form"""

    #set pace to pace query
    pace = request.form.get('pace')
    return pace



def calculate_search_grid():
    """calculate square grid for search using userid saved
     in session for lat/long center point, return user list"""

     #save user in session as center user
    center_user = User.query.get(session['user_id'])
    #get user's name
    center_user_name = center_user.name
    #get lat and longitude for center user
    my_lat = center_user.lat
    my_long =center_user.lng 

    radius = get_radius()
    pace = get_pace()

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
                                            (User.pace == pace)&
                                            (User.user_id != center_user.user_id)).all()
    return user_list

def calculate_compatibility_for_user_list():

    """calculate the compatibility for users in the list
    compared with the center user"""
    #call calculate search grid function to get user list
    user_list = calculate_search_grid()
    
    # if the query has no results let the user know
    if user_list == None:
        flash("No runners found who meet your criteria, please alter your search.")
        return redirect('/search')
    
    else:
    #calculate compatibility scores for users in list
        center_user = User.query.get(session['user_id'])
        center_user_responses = Compatibility.query.get(center_user.user_id)

        center_response_list = []

        if center_user_responses == None:
            pass
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
                    user.compatibility_rating = "Not found"

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


        # pass list of results to display in display runner info template            
        return render_template("/display_runner_info.html",
        user_list = user_list,my_lat = my_lat, my_long = my_long,
         center_user= center_user)
import geocoder
#import correlation
from math import cos, pi, sqrt
from flask import (Flask, render_template, redirect, request, flash, session, jsonify, url_for)

from model import User, Message, Compatibility, connect_to_db, db
from similarity import euclid, square_rooted, cosine_similarity, corrcoef


def get_radius():
    """Get distance from search form and calc radius."""

    #set radius to distance selected in form
    distance = request.args.get('distance')
    # print(distance)
    radius = int(distance)
    print(radius)
    return radius

def get_pace():
    """Get pace from search form"""

    #set pace to pace query
    pace = request.args.get('pace')
    print(pace)
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
    my_long = center_user.lng 

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
    print(user_list)
    return user_list

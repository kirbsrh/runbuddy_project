# RunBuddy

RunBuddy is a full stack web application that allows users to search for runners based on pace and distance.  Open Street Maps and Open Layers are used to display the map and the search results.  Python's geocoder library is used for geocoding addresses and lat/longs.

## Table of Contents
* [Overview](#overview)<br/>
* [Tech Stack](#techstack)<br/>


<a name="overview"/></a>
## Overview

Once a user registers, they will login. The user data is stored in a PostgreSQL database. The user can then complete a compatibility form with 10 simple questions.  The values of the answers are also storied in the database.  When a user executes a search, the database is queried and a grid is formed using lat/long pairs.  For the runners within the grid, euclidian distance is calculated to determine the similarity between the user and the runners. The map that displays the search results with the markers is populated using Open Street Maps and Open Layers.

<a name="techstack"/></a>
## Tech Stack
**Frontend:** Javascript, AJAX, JSON, jQuery, Jinja, HTML, CSS, Bootstrap</br>
**Backend:** Python, Flask, SQLAlchemy, PostgreSQL<br/>

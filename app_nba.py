#############################################################################
##### set up web app

from flask import Flask, render_template, redirect, jsonify
#from pprint import pprint

# Create an instance of Flask
app = Flask(__name__)


##############################################################################
#### connect to mongo to find the draftee

import pymongo


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.draftee


##############################################################################
#### connect to mysql to find the players
   
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine

#####
# Database Setup

MySQL_root_PW = "PASSWORD"
MySQL_db = 'nba'

MySQL_engine = create_engine("mysql://root:"+MySQL_root_PW+"@localhost/"+MySQL_db)
conn = MySQL_engine.connect()


### import sqlachemy 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(MySQL_engine, reflect=True)

# Assign the 'recent_players' class to a variable called `Player`
Player = Base.classes.recent_players

# Create our session (link) from Python to the DB
session = Session(MySQL_engine)


#############################################################################################
######################################## create each pages###################################
###############################################################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"<br/>"
        f"1. input the player's first and last name you like to see his draft info:<br/>"
        f"/api/v1.0/draftee/(firstName)/(lastName)<br/>"
        f"<br/>"
        f"<br/>"
        f"2. input the player name you like to see his current placement in nba:<br/>"
        f"/api/v1.0/player/(firstName)/(lastName)(input the player name you like)<br/>"
        f"<br/>"
        f"<br/>"
        f"3. input the player's first and last name you like to compare his draft and current placement<br/>"
        f"/api/v1.0/compare/(firstName)/(lastName)(input the player name you like)<br/>"
    )


#######################################################################################
############################# create draftee page #####################################

@app.route("/api/v1.0/draftee/<first_name>/<last_name>")
def draftee(first_name,last_name):
    
    draftee_long = {}

    # Return data
    for x in db.collection.find({ "firstName": first_name,"lastName":last_name}):
        draftee_long["1_name"] = f"The draftee you like to know is {x['firstName'], x['lastName']}" 
        draftee_long["2_year"] = f"He was drafted at {x['year']}"
        draftee_long["3_round"] = f"He was drated in the round {x['round']}"
        draftee_long["4_pick"] = f"His draft pick was {x['pick']}"
        draftee_long["5_position"] = f"He was picked for the position: {x['position']}"
        draftee_long["6_school"] = f"BTW, he was graduated from {x['school']}"
        
    
    return jsonify(draftee_long)
              
              

#######################################################################################
############################# create draftee page #####################################

@app.route("/api/v1.0/player/<first_name>/<last_name>")
def player(first_name,last_name):
    
    players = session.query(Player).filter(Player.firstName == first_name).filter(Player.lastName == last_name).all()
    player_long = {}

    # Query the info we need for each data
    for x in players:
        player_long["1_name"] = f"The player you like to know is {x.firstName} {x.lastName}"
        player_long["2_team"] = f"He is now playing for {x.team}"
        player_long["3_number_in_team"] = f"His number in team is {x.number_in_team}"
        player_long["4_headshot_src"] = f"You can find his headshot through the link: {x.headshot_src}"      
    
    return jsonify(player_long)

#######################################################################################
###################### create draftee VS. player compare page #########################

@app.route("/api/v1.0/compare/<first_name>/<last_name>")
def index(first_name,last_name):
    
    # write a statement that finds all the items in the db and sets it to a variable
    draftee_short = {}
    player_short = {}
    
    players = session.query(Player).filter(Player.firstName == first_name).filter(Player.lastName == last_name).all()
    
    # Return data
    for x in db.collection.find({ "firstName": first_name,"lastName":last_name}):
                
        draftee_short["first_name"] = x['firstName']
        draftee_short["last_name"] = x['lastName']
        draftee_short["year"] = x['year']
        draftee_short["round"] = x['round']
        draftee_short["pick"] = x['pick']
        draftee_short["position"] = x['position']
        draftee_short["school"] = x['school']
    
    
    for x in players:
            
        player_short["first_name"] = x.firstName
        player_short["last_name"] = x.lastName
        player_short["team"] = x.team
        player_short["number_in_team"] = x.number_in_team
        player_short["headshot_src"] = x.headshot_src  
    

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", player_short=player_short, draftee_short=draftee_short)



if __name__ == "__main__":
    app.run(debug=True)

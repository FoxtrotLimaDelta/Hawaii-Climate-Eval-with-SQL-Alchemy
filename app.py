from matplotlib import style
#style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

from flask import Flask, jsonify
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Create engine.#Use SQLAlchemy create_engine to connect to your sqlite database. 
hawaii_path = "Resources/hawaii.sqlite"

engine_hawaii = create_engine(f"sqlite:///{hawaii_path}")
#engine_hawaii = create_engine(f"sqlite:///Resources/hawaii.sqlite")

hawaii = pd.read_sql("SELECT * FROM measurement", engine_hawaii)
hawaii.head()

hawaii = pd.read_sql("SELECT * FROM station", engine_hawaii)
hawaii.head()

inspector = inspect(engine_hawaii)
inspector.get_table_names()

Base = automap_base()
Base.prepare(engine_hawaii, reflect=True)

Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

# Get a list of column names and types
columns = inspector.get_columns('measurement')
for c in columns:
    print(c['name'], c["type"])
    
 # Get a list of column names and types
columns = inspector.get_columns('station')
for c in columns:
    print(c['name'], c["type"])
    
    # Flask Setup

app = Flask(__name__)

 # Flask Routes

@app.route("/")
def welcome():
    
    """List all available API routes."""
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/about<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp_start<br/>"
        f"/api/v1.0/temp-start_end<br/>"
        f"/api/v1.0/contact"
    )
    
      
@app.route("/api/v1.0/about")

def about():
   name = "Flynn LLC"
   location = "Arizona"
   
   return f"We are {name} and we are located in sunny {location}."

# /api/v1.0/precf"/api/v1.0/precipitation<br/>"precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation"""
    # Query all measurements
    results = session.query(measurement.date, measurement.prcp).all()

    # Convert list of tuples into normal list
    all_precipitation = list(np.ravel(results))

    return jsonify(all_precipitation)

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Query for the date and precipitation (max, mean, min) 
# for all dates in the year
# Sort the result by date


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs"""
    # Query all observations
    results = session.query(measurement.tobs).filter(measurement.station =="USC00519281").all()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

# /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max
# temperature for a given start or start-end range.
@app.route("/api/v1.0/temp/<start>")
def tobs_start(start=None):
    
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    results = session.query(*sel).filter(measurement.date>=start).all()
    all_tobs = list(np.ravel(results))
    return jsonify(all_tobs)
    
@app.route("/api/v1.0/temp/<start>/<end>")
def tobs_start_end(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all tobs"""
    # Query all observations
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    results = session.query(*sel).filter(measurement.date>=start).filter(measurement.date<=end).all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)
@app.route("/api/v1.0/contact")
def contact():
   email = "Flynnworking@gmail.com"
     
   return f"Questions, Comments, Complaints? Send an email to {email}."

if __name__ == "__main__":
    
 app.run(debug=True)
 
 

 
# Set up the Flask Weather App

# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,inspect, func
from flask import Flask, jsonify
from pathlib import Path
import os

#cwd = os.getcwd()
dir = r"E:\Thins\School\UTAustin Bootcamp\UTA-VIRT-DATA-PT-10-2022-U-LOLC\00-Homework\10-Advanced-Data-Storage-and-Retrieval\Instructions\Resources\\"
# Set up database engine for Flask app
# Create function allows access to SQLite database file
path = Path(dir + "hawaii.sqlite")
engine = create_engine(f"sqlite:///{path}", connect_args={"check_same_thread": False})
# Reflect database into classes
Base = automap_base()
# Reflect tables
Base.prepare(engine, reflect=True)
# Set class variables
measurement = Base.classes.measurement
station = Base.classes.station
# Creates session link from Python to SQLite database
session = Session(engine)


# Create Flask app, all routes go after this code
app = Flask(__name__)


# HOMEPAGE - Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

#PRESIPITATION Route
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= prev_year).all()
   precipitation = {date: prcp for date, prcp in results}
   return jsonify(precipitation)


#STATIONS Route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

#TOBS Route
@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

#STATS Route
@app.route("/app/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]           

    #what to do while not at the end
    if not end: 
        results = session.query(*sel).\
            filter(measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)

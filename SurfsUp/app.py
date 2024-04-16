# Import the dependencies.

import numpy as np
import scipy as sp
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Rescources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
# session = Session(engine)
# in each query


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#homepage, list of all pages
@app.route("/")
def homepage():
        """List all avaliable routes"""
        return(
                f"Avaliable Routes:<br/>"
                f"/api/v1.0/precipitation"
                f"/api/v1.0/stations"
                f"/api/v1.0/tobs"
                f"/api/v1.0/<start>"
                f"/api/v1.0/<start>/<end>"
        )

#precipation, with results of past year of precipation analysis
@app.route("api/v1.0/precipitation")
def precipitation():
        #query results from past year
        session = Session(engine)

        recent_date = dt.date(2017, 8, 23)
        year_ago = recent_date - dt.timedelta(days=365)

        measure_query = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= year_ago).\
            order_by(Measurement.date).all()

        session.close()

        #dictionary and return json
        all_measure = []
        for date, prcp in measure_query:
            measure_dict = {}
            measure_dict["date"] = date
            measure_dict["prcp"] = prcp
            all_measure.append(measure_dict)

        return jsonify(all_measure)

#stations, with list of all stations
@app.route("api/v1.0/stations")
def stations():
        #return list of stations
        session = Session(engine)
        
        station_query = session.query(Station.station).all()

        session.close()

        #tuple to list and jsonify
        all_stations = list(np.ravel(station_query))

        return jsonify(all_stations)

#tobs, temperatures for most active station
@app.route("/api/v1.0/tobs")
def tobs():
        #query dates and temps for most active station
        session = Session(engine)

        recent_date = dt.date(2017, 8, 23)
        year_ago = recent_date - dt.timedelta(days=365)

        active_query = session.query(Measurement.tobs).\
        filter(Measurement.date >= year_ago).\
        filter(Measurement.station == "USC00519281").all()
       
        session.close()

        #tuple to list and jsonify
        active_tobs = list(np.ravel(active_query))

        return jsonify(active_tobs)

#temp data for selected start date
@app.route("/app/v1.0/<start>")
def start(start):
        #query min, avg, max from specficed start date
        session = Session(engine)

        sel = ([Measurement.date,
               func.min(Measurement.tobs), 
               func.avg(Measurement.tobs), 
               func.max(Measurement.tobs)])
        
        select_temps = session.query.\
            filter(Measurement.date >= start).all()
               
        session.close()

        #add to dictionary which can be displayed?
        temp_range = []
        for date, min_tobs, avg_tobs, max_tobs in select_temps:
            date_dict = {}
            date_dict["Date"] = date
            date_dict["TMinimum"] = min_tobs
            date_dict["TAverage"] = avg_tobs
            date_dict["TMaximum"] = max_tobs
            temp_range.append(date_dict)

        return jsonify(temp_range)

#temp data for selected start and end dates
@app.route("/app/v1.0/<start>/<end>")
def startend(start, end):
        #query min, avg, max from specficed start and end date

        session = Session(engine)

        sel = ([Measurement.date,
               func.min(Measurement.tobs), 
               func.avg(Measurement.tobs), 
               func.max(Measurement.tobs)])
        
        select_temps = session.query.\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
               
        session.close()

        #add to dictionary which can be displayed?
        temp_range = []
        for date, min_tobs, avg_tobs, max_tobs in select_temps:
            date_dict = {}
            date_dict["Date"] = date
            date_dict["TMinimum"] = min_tobs
            date_dict["TAverage"] = avg_tobs
            date_dict["TMaximum"] = max_tobs
            temp_range.append(date_dict)

        return jsonify(temp_range)




#
if __name__ =='__main__':
       app.run(debug=True)
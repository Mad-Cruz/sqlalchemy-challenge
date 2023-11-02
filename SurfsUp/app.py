# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind=engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
base_date = datetime.datetime.strptime("2017-08-23", "%Y-%m-%d")
numdays = 365
date_list = [base_date - datetime.timedelta(days=x) for x in range(0, numdays)]



# Converting them to a list of strings
str_dates = []
for date in date_list:
    new_date = date.strftime("%Y-%m-%d")
    str_dates.append(new_date)
    
    
@app.route("/api.v1.0/precipitation")
def precipitation():

    # Query
    results = session.query(Measurement).filter(Measurement.date.in_(str_dates))
    
    prcp_data = []
    for day in results:
        prcp_dict = {}
        prcp_dict[day.date] = day.prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():

    # Query 
    results = session.query(Station)

    station_data = []
    for station in results:
        station_dict = {}
        station_dict["Station"] = station.station
        station_dict["Name"] = station.name
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query 
    results = session.query(Measurement).filter(Measurement.date.in_(str_dates))

    temp_data = []
    for day in results:
        temp_dict = {}
        temp_dict[day.date] = day.tobs
        temp_data.append(temp_dict)

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def temperature_s(start):
    # Set start and end dates for date range
    startDate = datetime.datetime.strptime(start, "%Y-%m-%d")
    endDate = datetime.datetime.strptime("2017-08-23", "%Y-%m-%d")

    # Date range
    # Getting date range
    delta = endDate - startDate
    date_range = []
    for i in range(delta.days + 1):
        date_range.append(startDate + timedelta(days=i))
    
    # Converting to strings to filter
    str_date_range = []
    for date in date_range:
        new_date = date.strftime("%Y-%m-%d")
        str_date_range.append(new_date)

    # Grabbing avg, min & max temps    
    temp_avg = session.query(func.avg(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]
    temp_min = session.query(func.min(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]
    temp_max = session.query(func.max(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]

    # Dictionary of temperatures
    temp_dict = {}
    temp_dict["Average Temperature"] = temp_avg
    temp_dict["Minimum Temperature"] = temp_min
    temp_dict["Maximum Temperature"] = temp_max

    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>")
def temperature(start, end):
    # Set start and end dates for date range
    startDate = datetime.datetime.strptime(start, "%Y-%m-%d")
    endDate = datetime.datetime.strptime(end, "%Y-%m-%d")

    # Date range
    # Getting date range
    delta = endDate - startDate
    date_range = []
    for i in range(delta.days + 1):
        date_range.append(startDate + timedelta(days=i))
    
    # Converting to strings to filter
    str_date_range = []
    for date in date_range:
        new_date = date.strftime("%Y-%m-%d")
        str_date_range.append(new_date)

    # Grabbing avg, min & max temps    
    temp_avg = session.query(func.avg(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]
    temp_min = session.query(func.min(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]
    temp_max = session.query(func.max(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]

    # Dictionary of temperatures
    temp_dict = {}
    temp_dict["Average Temperature"] = temp_avg
    temp_dict["Minimum Temperature"] = temp_min
    temp_dict["Maximum Temperature"] = temp_max

    return jsonify(temp_dict)

if __name__ == '__main__':
    app.run(debug=True)
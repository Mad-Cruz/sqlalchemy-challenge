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

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"//api/v1.0/tobs<br/>"
        f"/api/v1.0/start date/<start><br/>"
        f"/api/v1.0/start date/end date/<start>/<end><br/>"
        "<br/>"
        f"Use the following format when entering a start/end date: yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    prcp_analysis = session.query(Measurement.prcp, Measurement.date).\
        filter(Measurement.date >= '2016-08-23').all()
    
    session.close()
    
    prcp_date_list = []

    for prcp, date in prcp_analysis:
        dict_data = {}
        dict_data['prcp'] = prcp
        dict_data['date'] = date
        prcp_date_list.append(dict_data)

    return jsonify(prcp_date_list)

@app.route("/api/v1.0/stations")
def stations():


    session = Session(engine)

    stations_data = session.query(Station.station, Station.name).all()

    session.close()

    station_data = []

    for station, name in stations_data:
        dict_data = {}
        dict_data['station'] = station
        dict_data['name'] = name
        station_data.append(dict_data)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():


    session = Session(engine)

    stations_count = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    
    most_active_station = stations_count[0][0]

    observations = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == most_active_station).all()

    session.close()

    temp_observations = []
    

    for station, date, tobs in observations:
        dict_data = {}
        dict_data['station'] = station
        dict_data['date'] = date
        dict_data['tobs'] = tobs
        temp_observations.append(dict_data)

    return jsonify(temp_observations)

@app.route("/api/v1.0/start date/<start>")
def start_date(start):

    session = Session(engine)

    min_temp = session.query(Measurement.tobs, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).scalar()
    
    max_temp = session.query(Measurement.tobs, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).scalar()
    
    avg_temp = session.query(Measurement.tobs, func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).scalar()


    session.close()

    dict_data = {"The minimum temperature is": min_temp, "The maximum temperature is": max_temp, "The average temperature is": avg_temp}
    
    return jsonify(dict_data)

@app.route("/api/v1.0/start date/end date/<start>/<end>")
def specified_date(start, end):

    session = Session(engine)

    minimum = session.query(Measurement.tobs, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).scalar()
    
    maximum = session.query(Measurement.tobs, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).scalar()
    
    average= session.query(Measurement.tobs, func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).scalar()
    
    session.close()

    dict_data = {"The minimum temperature is": minimum, "The maximum temperature is": maximum, "The average temperature is": average}
    
    return jsonify(dict_data)


if __name__ == '__main__':
    app.run(debug=True)
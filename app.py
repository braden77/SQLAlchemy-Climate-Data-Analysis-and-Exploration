import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# List all routes that are available
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# List all the precipitation data available
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    results = session.query (Measurement.date, Measurement.prcp).all()
    session.close()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date]=prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

# List all the stations in the database
@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    results = session.query (Station.station).all()
    session.close()

    all_station = []
    for station in results:
        all_station.append(station)

    return jsonify(all_station)

# Query the dates and temperature observations of the most active station 
# for the last year of data
@app.route("/api/v1.0/tobs")
def tobs():
    last_data= dt.datetime(2017,8,22)
    year_ago = dt.datetime(2017,8,22)-dt.timedelta(days=365)
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.station=='USC00519281').\
        filter(Measurement.date>=year_ago).\
        filter(Measurement.date<last_data).all()
    session.close()

    all_tobs = []
    for tobs in results:
        all_tobs.append(tobs)

    return jsonify(all_tobs)

# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature after a given start date.
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    return jsonify(results)

# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature between a given start date and a given end date. 

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
from datetime import datetime   ,date
# import pandas as pd

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")  # 19550 weather measurements measured by 9 stations 
Base = automap_base()
Base.prepare(engine, reflect=True)
# print(Base.classes.keys())   
Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route("/")
def welcome():                                                
    return (
        f"<br/>Welcome to the Hawaii Climate API!  <br/><br/>"
        f"Hawaii Climate API uses the data of 19550 temperature observations and precipitation scores from nine stations measured from 2010-01-01 till 2017-08-23.<br/><br/>"
        
        f"<br/>5 Available Routes:<br/><br/>"

        f"1. /api/v1.0/precipitation <br/>"                      
        f"it returns [multiple] records of precipitation scores measured during the last 12 months.<br/><br/>"
        f"2. /api/v1.0/stations <br/>"                            
        f"it returns [nine] records of temperature observation counts from the nine stations.<br/><br/>"
        f"3. /api/v1.0/tobs <br/>"                               
        f"it returns [multiple] records of temperature observations measured during the last 12 months.<br/><br/>"
        f"4. /api/v1.0/temperature1/startdate <br/>"              
        f"it returns [one] record composed of the minimum, average, and maximum temperatures since the startdate in format 'yyyy-mm-dd'.<br/><br/>"           
        f"5. /api/v1.0/temperature2/startdate/enddate <br/>"      
        f"it returns [one] record composed of the minimum, average, and maximum temperatures between the startdate and enddate in format 'yyyy-mm-dd'.<br/><br/><br/><br/>"    
        f"Thank you!"
        
        # f"1. Precipitation:  precipitation scores measured during the last 12 months.<br/>"
        # f"2. Stations: temperature observation counts from the nine stations.<br/>"
        # f"3. Tobs: temperature observations measured during the last 12 months.<br/>"
        # f"4. Temperature1: the minimum, average, and maximum temperatures since the startdate in format 'yyyy-mm-dd'.<br/>"           
        # f"5. Temperature2: the minimum, average, and maximum temperatures between the startdate and enddate in format 'yyyy-mm-dd'.<br/>"    
    )


#   * 1.Precipitation: the last 12 months precipitation scores
#   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#   * Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")    
def precipitation():  #  precipitation data of last 12 months 
    from datetime import datetime ,date 
    session = Session(engine)
    lastDate_str = session.query(func.max(Measurement.date).label('lastDate')).one().lastDate   
    lastDate_date = datetime.strptime(lastDate_str, '%Y-%m-%d')
    year=lastDate_date.year
    month=lastDate_date.month
    day=lastDate_date.day
    Oneyearago_date = date(year=year-1,month=month,day=day)   
    prcpdata_list = session.query(Measurement.date,Measurement.prcp).filter((Measurement.date>Oneyearago_date)&(Measurement.date<lastDate_str)).all()
    session.close()   

    all_precipitations = []
    for date,precipitation in prcpdata_list:         
        precipitation_dict = {}
        precipitation_dict[date] = precipitation
        all_precipitations.append(precipitation_dict)
    return jsonify(all_precipitations)


#   * 2.Stations: temperature observation counts from the nine stations
#   * weather measurement counts of the nine station
#   * Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations") 
def stations():    # stations and observation counts in descending order
    session = Session(engine)
    stationrowcounts_list = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    return jsonify(stationrowcounts_list)

#   * 3.Tobs: temperature observations of the last year
#   * query for the dates and temperature observations from a year from the last data point.
#   * Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")  
def tobs():    # emperature observation data of last 12 months of the most active station(has the highest number of observations)
    from datetime import datetime ,date 
    session = Session(engine)
    lastDate_str = session.query(func.max(Measurement.date).label('lastDate')).one().lastDate   
    lastDate_date = datetime.strptime(lastDate_str, '%Y-%m-%d')
    year=lastDate_date.year
    month=lastDate_date.month
    day=lastDate_date.day
    Oneyearago_date = date(year=year-1,month=month,day=day)  
    subq = session.query(Measurement.station, func.count(Measurement.id).label('idcount')).group_by(Measurement.station).subquery('t2')
    query = session.query(Measurement.station, func.max(subq.c.idcount)).join(subq,Measurement.station == subq.c.station)
    mostactivestation = query.one()[0]
    tobsdata_list = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == mostactivestation).filter((Measurement.date>Oneyearago_date)&(Measurement.date<lastDate_str)).all()
    return jsonify(tobsdata_list)

#   * 4.Temperature1: the minimum, average, and maximum temperatures since the startdate in format 'yyyy-mm-dd'
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
#   * accept start date and end date in the format '%Y-%m-%d' 
@app.route("/api/v1.0/temperature1/<start>")  
def temperaturewithstart(start):
    session = Session(engine)
    temp_list = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(temp_list)
#   * 5.Temperature2: the minimum, average, and maximum temperatures between the startdate and enddate in format 'yyyy-mm-dd'
@app.route("/api/v1.0/temperature2/<start>/<end>")
def temperaturewithstartandend(start,end):
    session = Session(engine)
    temp_list = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(temp_list)


if __name__ == "__main__":              
    app.run(debug=True)

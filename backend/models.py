from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WeatherStation(Base):
    __tablename__ = 'weather_station'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    max_temp = Column(Float)
    min_temp = Column(Float)
    precipitation = Column(Float)
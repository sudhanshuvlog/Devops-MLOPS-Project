from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL
DATABASE_URL = "postgresql+psycopg2://postgres:mysecretpassword@127.0.0.1:5432/weather_data"

# Database engine setup
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# WeatherStation model defination
class WeatherStation(Base):
    __tablename__ = 'weather_station'
    station_id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)

# WeatherData model defination
class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('weather_station.station_id'))
    date = Column(Date, nullable=False)
    max_temp = Column(Integer)  # Stored in tenths of a degree Celsius
    min_temp = Column(Integer)  # Stored in tenths of a degree Celsius
    precipitation = Column(Integer)  # Stored in tenths of a millimeter
    __table_args__ = (UniqueConstraint('station_id', 'date', name='_station_date_uc'),)

# Create the tables in the database
Base.metadata.create_all(engine)
import os
import datetime
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import WeatherData, WeatherStation, Base

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_weather_data(wx_data_dir):
    # Set up the database connection
    engine = create_engine(os.getenv('DATABASE_URL'))
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create tables if they do not exist
    Base.metadata.create_all(engine)

    # Iterate over files in wx_data directory
    for file_name in os.listdir(wx_data_dir):
        file_path = os.path.join(wx_data_dir, file_name)
        if file_path.endswith('.txt'):
            logger.info(f"Processing file: {file_path}")
            df = pd.read_csv(file_path, delimiter='\t', header=None, 
                             names=['date', 'max_temp', 'min_temp', 'precipitation'])
            
            # Handle missing values
            df.replace(-9999, pd.NA, inplace=True)
            
            # Insert data into the database
            for _, row in df.iterrows():
                weather_data = WeatherData(
                    station_id=1,  # You need to define logic for station_id
                    date=pd.to_datetime(row['date'], format='%Y%m%d'),
                    max_temp=row['max_temp'],
                    min_temp=row['min_temp'],
                    precipitation=row['precipitation']
                )
                try:
                    # Check for duplicates before inserting
                    existing_data = session.query(WeatherData).filter_by(
                        station_id=weather_data.station_id,
                        date=weather_data.date
                    ).first()
                    if not existing_data:
                        session.add(weather_data)
                        session.commit()
                except Exception as e:
                    logger.error(f"Error inserting data: {e}")
                    session.rollback()
    
    logger.info(f"Data ingestion finished at {datetime.datetime.now()}")
    session.close()

if __name__ == "__main__":
    wx_data_dir = '/app/wx_data'
    ingest_weather_data(wx_data_dir)
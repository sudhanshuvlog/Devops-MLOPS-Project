import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://127.0.0.1:mysecretpassword@localhost:5432/weather_data')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import text
# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@127.0.0.1/weather_data'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define model
class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    station_id = db.Column(db.Integer, nullable=False)
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    precipitation = db.Column(db.Float)

class WeatherDataSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherData
        load_instance = True

weather_data_schema = WeatherDataSchema()
weather_data_schemas = WeatherDataSchema(many=True)

# Routes
@app.route('/api/weather', methods=['GET'])
def get_weather_data():
    date = request.args.get('date')
    station_id = request.args.get('station_id')
    query = WeatherData.query
    if date:
        query = query.filter(WeatherData.date == date)
    if station_id:
        query = query.filter(WeatherData.station_id == station_id)
    weather_data = query.all()
    return jsonify(weather_data_schemas.dump(weather_data))

@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    # Example placeholder for stats calculation
    # Implement actual logic for calculating stats
    
    year = request.args.get('year')
    station_id = request.args.get('station_id')

    query = """
    SELECT
        station_id,
        EXTRACT(YEAR FROM date) AS year,
        AVG(max_temp) AS avg_max_temp,
        AVG(min_temp) AS avg_min_temp,
        SUM(precipitation) / 10.0 AS total_precipitation_cm
    FROM
        weather_data
    """

    # Add filtering based on query parameters
    filters = []
    if year:
        filters.append(f"EXTRACT(YEAR FROM date) = {year}")
    if station_id:
        filters.append(f"station_id = {station_id}")
    
    if filters:
        query += " WHERE " + " AND ".join(filters)
    
    query += " GROUP BY station_id, EXTRACT(YEAR FROM date);"
    
    result = db.session.execute(text(query))
    stats = [dict(row) for row in result]

    return jsonify(stats)

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
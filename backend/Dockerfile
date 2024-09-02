FROM python:3.9-slim

# Install git to clone the repository
RUN apt-get update && apt-get install -y git

# Set the working directory
WORKDIR /app

# Clone the GitHub repository
RUN git clone https://github.com/corteva/code-challenge-template.git

RUN cp -r  code-challenge-template/wx_data wx_data

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY create_db_model.py /app/
COPY models.py /app/
COPY ingest_data.py /app/

# Set environment variables
ENV DATABASE_URL="postgresql+psycopg2://postgres:mysecretpassword@127.0.0.1:5432/weather_data"
#Create the db tables
CMD ["python", "create_db_model.py"] 
# Start the data ingestion process
CMD ["python", "ingest_data.py"]
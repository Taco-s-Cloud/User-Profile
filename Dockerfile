# Start with a Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variable for Google credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

# Ensure /app is included in the Python module search path
ENV PYTHONPATH=/app

ENV FLASK_APP=app

# Run the application
CMD ["python", "main.py"]

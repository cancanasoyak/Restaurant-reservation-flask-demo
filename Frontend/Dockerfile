# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /frontend

# Copy the current directory contents into the container at /app
COPY . /frontend

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir Flask requests

# Expose port 5000 to the outside world
EXPOSE 5000

# Define environment variable for the backend API URL
ENV BACKEND_API_URL=http://flaskappback:8000/api

# Command to run the Flask application
CMD ["python", "frontapp.py"]
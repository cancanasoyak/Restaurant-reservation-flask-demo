# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /frontend

# Copy the current directory contents into the container at /app
COPY . /frontend

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir Flask requests

# Expose port 8000 to the outside world
EXPOSE 8000

# Define environment variable for the backend API URL
ENV BACKEND_API_URL=http://localhost:5000/api

# Command to run the Flask application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]
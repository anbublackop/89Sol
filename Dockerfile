# Use a lightweight Python base image
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
# This step is done first to leverage Docker's layer caching
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the application code
COPY . /app

# Expose the port where the FastAPI application will run
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
# The 'main:app' refers to the 'app' object in 'main.py'
# CMD ["fastapi", "dev", "fixed_news_summarizer.py", "--port", "8000"]
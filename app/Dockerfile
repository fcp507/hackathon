# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8080

# Set environment variable for the port
ENV PORT 8080

# Set environment variable
ENV GOOGLE_CLOUD_PROJECT hackathon-448821

# Run chainlit when the container launches
CMD ["python", "main.py"]
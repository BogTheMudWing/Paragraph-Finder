# Python 3.8 is the parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy contents into the container at /app
COPY . /app

# Install packages
RUN pip install --no-cache-dir flask

# Run Python script when the container launches
CMD ["python", "paragraph-finder-web.py"]
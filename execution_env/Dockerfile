# Use an official lightweight Python image
FROM python:3.8-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the rest of your application code (if any)
COPY . /app

# Install any dependencies if needed (uncomment and adjust if you have requirements)
# RUN pip install -r requirements.txt

# Set the entrypoint to allow running arbitrary scripts
ENTRYPOINT ["python"]
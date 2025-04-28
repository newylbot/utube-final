# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (FFmpeg and others)
RUN apt-get update && apt-get install -y ffmpeg gcc libffi-dev libssl-dev && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot code
COPY . .

# Expose port for FastAPI (needed for some platforms like Koyeb)
EXPOSE 8080

# Run the bot directly with FastAPI and subprocess monitoring
CMD ["python3", "run.py"]

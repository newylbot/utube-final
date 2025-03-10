# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment file path
ENV FILE_PATH=add_variables.env

# Run the bot with environment variables loaded
CMD ["sh", "-c", "if [ -f $FILE_PATH ]; then export $(grep -v '^#' $FILE_PATH | xargs); fi && python3 -m bot"]

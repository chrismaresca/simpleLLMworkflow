# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install the required dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the entire application code into the container
COPY ./app /code/app

# Copy the templates directory into the container
COPY ./templates /code/templates

# Expose the port FastAPI will run on
EXPOSE 80

# Command to run the FastAPI app
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "80"]

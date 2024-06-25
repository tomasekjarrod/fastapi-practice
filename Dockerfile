# Use the official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the entire app directory into the container
COPY ./app /code/app

# Command to run the FastAPI server using Uvicorn
CMD ["fastapi", "run", "app/main.py", "--port", "80"]

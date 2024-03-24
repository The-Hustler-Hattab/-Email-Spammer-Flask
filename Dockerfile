FROM python:3.11.3-slim-bullseye

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*


# Set the working directory in the container
WORKDIR /workspace


COPY requirements.txt requirements.txt


RUN pip install --upgrade pip \
    && pip install mysqlclient \
    && pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port on which your Flask app runs
EXPOSE 5000

# Command to run the Flask application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
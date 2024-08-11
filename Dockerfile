# Step 1) Define the container image (depends on the project)
FROM python:3.12-slim-bullseye

# Step 2) Set up the working directory
WORKDIR /

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       default-libmysqlclient-dev \
       build-essential \
       pkg-config \
       gcc \
       python3-dev \
       libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Step 4) Create the virtual environment
RUN python -m venv /opt/venv
# python -m venv <location_of_the_venv>

# Step 5) Set up the path to the venv
ENV PATH="/opt/venv/bin:$PATH"

# Step 6) Copy the project files to the container
COPY . .
# Note: "." means all files

# Step 7) Install Python dependencies
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip freeze > requirements.txt

# Step 8) Run the project
EXPOSE 8000

#CMD ["python", "manage.py", "makemigrations", ";", "python", "manage.py", "migrate", ";", "python", "manage.py", "createsuperuser.py", ";", "python", "manage.py", "runserver", "0.0.0.0:8000"]

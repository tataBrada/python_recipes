# Use a Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the code files into the container
COPY . /app

# Copy the font file into the container
COPY fonts /app/fonts

# Install required packages
RUN apt-get update  \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    && apt-get install -y wget libgl1-mesa-glx


# Download and install libssl1.1
RUN wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb
RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb

# Cleaning up unused files
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false  \
    && rm -rf /var/lib/apt/lists/*

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the streamlit configuration
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Expose the port that Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "--server.port", "8501", "--server.enableCORS", "false", "app.py"]

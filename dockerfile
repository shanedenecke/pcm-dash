# Use an official Ubuntu as a parent image
FROM ubuntu:24.04

# Set environment variables to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

### Install Python
RUN apt-get update -y \
    && apt install python3 -y \
    && apt install python3-pip -y \
    && apt install python3-venv -y 


WORKDIR /app

# Copy the application files into the container
COPY . /app


### Set up Python venv
RUN python3 -m venv venv
RUN /bin/bash -c "source venv/bin/activate"
RUN /bin/bash -c "venv/bin/pip install -r requirements.txt"


# Expose the port Dash uses
EXPOSE 8050


# Run the application. Use python by itself because installing venv
CMD ["venv/bin/python", "main.py"]


#ENV PATH="$PATH:venv/bin"
#CMD ["python", "main.py"]

#Download base image ubuntu 20.04
FROM ubuntu:20.04

# LABEL about the custom image
LABEL maintainer="mauricio.moldes@crg.eu"
LABEL version="0.1"
LABEL description="This is custom Docker Image for the RT_over_96H."


# Update Ubuntu Software repository
RUN apt update

# Install from ubuntu repository
RUN apt install -y python3 python3-pip  && \    
    apt clean

# python requirements

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt 
COPY . /tmp/

#queue music

WORKDIR /tmp/src

CMD [ "python3", "rt_over_96h.py"]

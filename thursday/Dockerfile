# APT
FROM ubuntu:jammy AS prereqs

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=Etc/UTC
ARG GITHUB_TOKEN
# RUN echo "Token is: ${GITHUB_TOKEN}"
RUN apt-get update -y && \
    apt-get install -y \
        build-essential \
        iputils-ping \
        python3-pip \
        python3-pandas \
        netcat \
        curl \
        git \
        swig



RUN pip3 install pip==25.0.1 --retries 30 --default-timeout=60
RUN pip3 install --upgrade pip setuptools wheel
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

# PIP
# FROM prereqs AS pip

# RUN pip3 install -r requirements.txt --upgrade pip --retries 30 --default-timeout=60
COPY ./requirements.txt /
RUN pip3 install -r requirements.txt --retries 30 --default-timeout=60
RUN pip3 install git+https://jaodev-ph:${GITHUB_TOKEN}@github.com/jaodev-ph/python-library@v1.1.0


COPY . /srv/thursday
WORKDIR /srv/thursday
RUN python3 setup.py install
CMD ''






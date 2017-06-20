FROM debian:stretch

RUN apt-get update -qy && apt-get install -qy python-pip
RUN pip install requests

ADD aplus /aplus
ENV PATH "$PATH:/aplus"

RUN mkdir -p /feedback
WORKDIR /submission

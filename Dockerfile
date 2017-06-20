FROM debian:stretch

ADD . /aplus
ENV PATH "$PATH:/aplus"
RUN mkdir -p /feedback

RUN apt-get update && apt-get install python-pip
RUN pip install requests

WORKDIR /submission

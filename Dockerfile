FROM debian:stretch

ADD . /aplus
ENV PATH "$PATH:/aplus"
RUN mkdir -p /feedback

RUN apt-get update -qy && apt-get install -qy python-pip
RUN pip install requests

WORKDIR /submission

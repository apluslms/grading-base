FROM debian:stretch

RUN apt-get update -qy && apt-get install -qy \
  sudo \
  curl \
  python-pip
RUN pip install requests

ADD bin /usr/local/bin

RUN mkdir -p /feedback
WORKDIR /submission

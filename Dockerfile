FROM debian:stretch

RUN apt-get update -qy && apt-get install -qy \
  sudo \
  curl \
  git \
  openssh-client \
  python-pip
RUN pip install requests

ADD bin /usr/local/bin

RUN mkdir -p /feedback
WORKDIR /submission

FROM debian:stretch

ENV LANG C.UTF-8

RUN apt-get update -qqy && apt-get install -qqy --no-install-recommends \
    sudo \
    curl \
    git \
    openssh-client \
    python-pip \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN pip install requests \
  && rm -rf /root/.cache

ADD bin /usr/local/bin

RUN mkdir -p /feedback
WORKDIR /submission

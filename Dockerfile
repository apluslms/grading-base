FROM debian:stretch-slim

ENV LANG =C.UTF-8

RUN apt-get update -qqy && DEBIAN_FRONTEND=noninteractive apt-get install -qqy --no-install-recommends \
    -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" \
    sudo \
    ca-certificates \
    curl \
    git \
    openssh-client \
    python-requests \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

ADD bin /usr/local/bin

RUN mkdir -p /feedback
WORKDIR /submission

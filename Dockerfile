FROM debian:stretch-slim

ENV LANG=C.UTF-8

RUN apt-get update -qqy && DEBIAN_FRONTEND=noninteractive apt-get install -qqy --no-install-recommends \
    -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" \
    runit \
    ca-certificates \
    curl \
    jo \
    git \
    openssh-client \
    python3-requests \
 && cp /usr/bin/chpst /usr/local/bin \
 && dpkg -P runit \
 && (cd /usr/local/bin && ln -s chpst setuidgid && ln -s chpst softlimit && ln -s chpst setlock) \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

COPY bin /usr/local/bin
COPY grade-wrapper.sh /gw
RUN mkdir -p /feedback /submission /exercise \
 && chmod 0770 /feedback \
 && chmod 0555 /gw /usr/local/bin/*

ENV USER=root HOME=/root
WORKDIR /submission
ENTRYPOINT ["/gw"]
CMD ["/exercise/run.sh"]

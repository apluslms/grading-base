FROM debian:buster-20190812-slim

ENV LANG=C.UTF-8 USER=root HOME=/root

# Tools for dockerfiles and image management
COPY rootfs /

# Base tools that are used by all images
RUN apt_install \
    runit \
    gettext-base \
    ca-certificates \
    curl \
    jo \
    jq \
    time \
    git \
    openssh-client \
 # Copy single binaries from packages and remove packages
 && cp /usr/bin/chpst \
       /usr/bin/envsubst \
       /usr/local/bin \
 && dpkg -P runit gettext-base \
 && apt-get -qqy autoremove \
 && dpkg -l|awk '/^rc/ {print $2}'|xargs -r dpkg -P \
 && (cd /usr/local/bin && ln -s chpst setuidgid && ln -s chpst softlimit && ln -s chpst setlock) \
\
 # Create basic folders
 && mkdir -p /feedback /submission /exercise \
 && chmod 0770 /feedback \
\
 # Change HOME for nobody from /nonexistent to /tmp as set by capture
 && usermod -d /tmp nobody

# Base grading tools
COPY bin /usr/local/bin

# Base environment
WORKDIR /submission
ENTRYPOINT ["/gw"]
CMD ["/exercise/run.sh"]

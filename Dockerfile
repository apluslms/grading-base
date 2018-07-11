FROM debian:stretch-slim

ENV LANG=C.UTF-8 USER=root HOME=/root

# Tools for dockerfiles and image management
COPY rootfs /

# Base tools that are used by all images
RUN apt_install \
    runit \
    ca-certificates \
    curl \
    jo \
    jq \
    time \
    git \
    openssh-client \
    python3-requests \
 && cp /usr/bin/chpst /usr/local/bin \
 && dpkg -P runit \
 && (cd /usr/local/bin && ln -s chpst setuidgid && ln -s chpst softlimit && ln -s chpst setlock) \
\
 # Create basic folders
 && mkdir -p /feedback /submission /exercise \
 && chmod 0770 /feedback

# Base grading tools
COPY bin /usr/local/bin

# Base environment
WORKDIR /submission
ENTRYPOINT ["/gw"]
CMD ["/exercise/run.sh"]

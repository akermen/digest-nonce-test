#------------------------------------------------------------------------------
#
#  Dockerfile
#
#  Created by Ahmet Kermen on 14.01.2022.
#
#------------------------------------------------------------------------------
ARG DEBIAN_FRONTEND=noninteractive
ARG VERSION=0.9.59
#------------------------------------------------------------------------------
FROM ubuntu:18.04
#------------------------------------------------------------------------------
ARG DEBIAN_FRONTEND
ARG VERSION
#------------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    apt-utils \
    build-essential \
    ca-certificates \
    wget && \
    rm -rf /var/lib/apt/lists/*
#------------------------------------------------------------------------------
WORKDIR /build
#------------------------------------------------------------------------------
RUN wget \
    -nv \
    -O libmicrohttpd-${VERSION}.tar.gz \
    https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-${VERSION}.tar.gz \
    && tar xvfz libmicrohttpd-${VERSION}.tar.gz > /dev/null \
    && rm libmicrohttpd-${VERSION}.tar.gz \
    && mv libmicrohttpd-${VERSION} libmicrohttpd \
    && cd libmicrohttpd \
    && ./configure \
        --prefix=/usr \
        --disable-https \
     && make \
     && make install
#------------------------------------------------------------------------------
EXPOSE 8080
#------------------------------------------------------------------------------
ENTRYPOINT [ "/build/libmicrohttpd/src/examples/digest_auth_example", "8080" ]
#------------------------------------------------------------------------------

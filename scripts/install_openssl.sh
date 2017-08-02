docker run -it --rm --name openssl ubuntu:16.04 bash
RUN apt-get update \
&& apt-get install -y -qq sudo build-essential autoconf automake libtool-bin libz-dev \
    subversion git wget \
    python libpcre3-dev libexpat1-dev \
    pkg-config \
&& useradd -m -s /bin/bash tester -p $(perl -e 'print crypt("password", "salt")')
&& usermod -aG sudo tester \
RUN cd /home/tester
USER tester
&& wget https://www.openssl.org/source/openssl-1.1.0.tar.gz \
&& tar -zxf openssl-1.1.0.tar.gz \
&& cd openssl-1.1.0 \
#&& ./config --prefix=/usr/local --openssldir=/etc/ssl --libdir=lib shared zlib-dynamic
&& ./config --prefix=/usr/local
&& make \
&& sudo make install \
&& cd .. \
&& rm -f open openssl-1.1.0.tar.gz
&& rm -Rf openssl-1.1.0
&& git clone https://github.com/zmartzone/token_bind.git \
&& cd token_bind \
&& sed -i '/OPENSSL_DIR=\/usr\/local/c\OPENSSL_DIR=\/usr\/lib' Makefile \
&& cd example \
&& sed -i '/OPENSSL_DIR=\/usr\/local/c\OPENSSL_DIR=\/usr\/lib' Makefile \
&& make


FROM ubuntu:16.04

## ARGs are set with --buildarg on docker build
ARG VNC_HOME=/headless

ENV DEBIAN_FRONTEND noninteractive
ENV HOME ${VNC_HOME}
ENV NO_VNC_HOME $HOME/noVNC
ENV STARTUPDIR /dockerstartup

### Install some common tools
RUN echo "Install some common tools for further installation" \
&& set -ex;  apt-get update -y -q \
&& apt-get install -y -q sudo vim wget net-tools iputils-ping dnsutils locales

### Install xvnc-server & noVNC - HTML5 based VNC viewer
RUN echo "Install TigerVNC server" \
&& set -ex; wget -qO- https://dl.bintray.com/tigervnc/stable/tigervnc-1.8.0.x86_64.tar.gz | tar xz --strip 1 -C /

### Install Chrome
RUN echo "Install Chrome Browser" \
&& set -ex; wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
&& echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
&& apt-get update -y -q \
&& apt-get install -y -q google-chrome-stable \
&& apt-get install -y -q firefox

RUN echo "Install noVNC - HTML5 based VNC viewer" \
&& set -ex; mkdir -p $NO_VNC_HOME/utils/websockify \
&& wget -qO- https://github.com/kanaka/noVNC/archive/v0.6.1.tar.gz | tar xz --strip 1 -C $NO_VNC_HOME \
&& wget -qO- https://github.com/kanaka/websockify/archive/v0.8.0.tar.gz | tar xz --strip 1 -C $NO_VNC_HOME/utils/websockify \
&& chmod +x -v $NO_VNC_HOME/utils/*.sh \
## create index.html to forward automatically to `vnc_auto.html`
&& ln -s $NO_VNC_HOME/vnc_auto.html $NO_VNC_HOME/index.html

RUN echo "Install nss-wrapper to be able to execute image as non-root user" \
&& set -ex; apt-get install -y -q libnss-wrapper libnss3-tools gettext

RUN echo "Install Xfce4 UI components" \
&& set -ex; apt-get install -y -q supervisor xfce4 xterm \
&& apt-get purge -y -q pm-utils xscreensaver*

#############################################
## Do not install (apt-get) beyond this line
#############################################
RUN echo "Clean up apt indexes" \
&& set -ex; apt-get clean \
&& rm -rf /var/lib/apt/lists/*

RUN echo "Set locale to en_US" \
&& set -ex; locale-gen en_US.UTF-8 \
&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

WORKDIR $HOME

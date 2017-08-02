FROM vnc_base
ARG VNC_HOME=/headless
ARG ROOTCA
ARG ROOTCA_NICKNAME
ARG VNC_USER
ARG VNC_PW=vncpassword

ENV HOME ${VNC_HOME}
ENV NO_VNC_HOME $HOME/noVNC
## Connection ports for controlling the UI:
# VNC port:5900
# noVNC webport, connect via http://IP:6900/?password=vncpassword
ENV DISPLAY :0
ENV VNC_PORT 5900
ENV NO_VNC_PORT 6900
ENV ROOTCA_NICKNAME ${ROOTCA_NICKNAME}
ENV ROOTCA ${ROOTCA}
ENV VNC_COL_DEPTH 24
ENV VNC_RESOLUTION 1280x1024
ENV VNC_PW ${VNC_PW}

EXPOSE $VNC_PORT
EXPOSE $NO_VNC_PORT

### Add all install scripts for further steps
ENV INST_SCRIPTS $HOME/install
ADD .tmp/common/install/ $INST_SCRIPTS/
RUN find $INST_SCRIPTS -name '*.sh' -exec chmod a+x {} +

### Install firfox and chrome browser
# RUN $INST_SCRIPTS/chromium.sh

### Install xfce UI
ADD .tmp/common/xfce/ $HOME/

### configure startup
ADD .tmp/common/scripts $STARTUPDIR

COPY .tmp/ssl/${ROOTCA} ${ROOTCA}
RUN echo "Add user ${VNC_USER}" \
&& set -ex; useradd -M -d $HOME -s /bin/bash -g root ${VNC_USER} \
&& usermod -aG sudo ${VNC_USER} \
&& cp /etc/skel/.bashrc  . \
&& cp /etc/skel/.bash_logout  . \
&& cp /etc/skel/.profile . \
&& chmod -R 775 $HOME
RUN $INST_SCRIPTS/set_user_permission.sh $STARTUPDIR $HOME

RUN echo "add 'souce generate_container_user' to .bashrc" \
&& echo 'source $STARTUPDIR/generate_container_user' >> $HOME/.bashrc

RUN cp ${ROOTCA} /etc/ssl/certs/${ROOTCA}

RUN echo "Create Chrome data folder, and reset permissions" \
&& set -ex; cd $HOME && mkdir chrome-data \
&& chown ${VNC_USER}:root . \
&& chown ${VNC_USER}:root .bashrc .profile .config \
&& find $HOME -name '*' -exec chown ${VNC_USER}:root {} +

# Perform extra stuff as normal user
USER ${VNC_USER}
RUN echo "Add the root SSL cert for Chrome" \
&& set -ex; mkdir -p $HOME/.pki/nssdb
RUN certutil -d "sql:.pki/nssdb" -N --empty-password
RUN certutil -d "sql:.pki/nssdb" -A -t "CT,C,C" -n ${ROOTCA_NICKNAME} -i ${ROOTCA}

ENTRYPOINT ["/dockerstartup/vnc_startup.sh"]
CMD ["--tail-log"]

FROM openjdk:latest
EXPOSE 9999 9030 9031 9041 9042
ARG PF_VERSION
VOLUME /root
ENV DEBIAN_FRONTEND noninteractive

ENV POSTGRES_HOSTNAME='empty'
COPY .tmp/scripts/ /
RUN chmod 777 /startup.sh
COPY pingfederate-${PF_VERSION}.zip /
RUN unzip -q pingfederate-${PF_VERSION}.zip \
    && mv pingfederate-${PF_VERSION}/pingfederate /opt
COPY .tmp/pfconfigs /opt
ENTRYPOINT ["/startup.sh"]
# ENTRYPOINT ["sh", "-c", "/root/pingfederate/bin/run.sh", "BACKGROUND"]
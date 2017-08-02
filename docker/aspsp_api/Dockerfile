FROM  node_base
ENV HOME /home/node
ENV APP_HOME /opt/share
ENV PORT 8080
EXPOSE $PORT

RUN apk add --no-cache git

# Create data volume
RUN mkdir -p "$APP_HOME" \
    && chown -R node:node "$APP_HOME" \
    && chmod 777 "$APP_HOME"
    # this 777 will be replaced by 700 at runtime (allows semi-arbitrary "--user" values)
COPY .tmp/ "${HOME}/"
RUN chmod -R 777 ${HOME}/* \
    && cp ${HOME}/docker-entrypoint.sh /usr/local/bin/ \
    && cp ${HOME}/ssl/root.cert.pem /etc/ssl/certs
USER node

VOLUME $APP_HOME
WORKDIR $APP_HOME

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["yarn", "start"]
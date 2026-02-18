# APP SETUP
FROM ghcr.io/jaodev-ph/thursday_appserver/base:latest AS app-setup

EXPOSE 5031
COPY ./requirements.txt /
ARG GITHUB_TOKEN
RUN echo "Token is: ${GITHUB_TOKEN}"
RUN pip3 install git+https://jaodev-ph:${GITHUB_TOKEN}@github.com/jaodev-ph/python-library

RUN pip3 install -r /requirements.txt --retries 30 --default-timeout=60

# DEVELOPMENT
FROM app-setup AS development
COPY . /srv/app
WORKDIR /srv/app
ENV ROOTPATH /srv/app
CMD gunicorn \
    --bind 0.0.0.0:5031 \
    --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
    --workers 1 \
    --threads 2 \
    --worker-connections 128 \
    --proxy-protocol \
    --reload \
    --max-requests 256 \
    --worker-connections 512 \
    --timeout 300 \
    --graceful-timeout 1 \
    --log-level debug \
    wsgi:app

# PRODUCTION
FROM development AS production
HEALTHCHECK CMD curl --fail http://localhost:9031/healthcheck || exit 1
ARG RELEASE=unknown
RUN echo "${RELEASE}" | tee -a /srv/release.nfo
RUN rm -rf /srv/hivesac /requirements*.txt
RUN apt-get autoremove -y
CMD gunicorn \
    --bind 0.0.0.0:5031 \
    --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
    --workers 2 \
    --threads 4 \
    --max_requests 256 \
    --max_requests_jitter 32 \
    --timeout 300 \
    --max-requests 1000\
    --worker-connections 2048 \
    --proxy-protocol \
    --preload \
    --keep-alive 10 \
    wsgi:app

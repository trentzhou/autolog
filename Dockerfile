FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y \
        python-flask \
        python-requests \
        python-feedparser \
        curl && \
    rm -rf /var/lib/apt/lists/*
EXPOSE 80

COPY src /autolog
WORKDIR /autolog
RUN ["/bin/mkdir", "/autolog_data"]
VOLUME /autolog_data

ENV BAIDU_TOKEN=1ef059103bc02c7f1cd9b35e5bcab3ab \
    DATA_DIR=/autolog_data \
    TZ="CST" \
    CITY="Nanjing" \
    PORT="80" \
    TITLE="Autolog" \
    POST_MAGIC="the-very-secret-word"

ENTRYPOINT ["/autolog/entrypoint.sh"]

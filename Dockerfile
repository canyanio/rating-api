FROM python:3.8-alpine3.10
WORKDIR /src
COPY . /src
RUN python3 setup.py sdist bdist_wheel

FROM python:3.8-alpine3.10
LABEL maintainer="Canyan Engineering Team <team@canyan.io>"
ENV VERSION 0.1.0

COPY ./scripts/wait-for /usr/bin/wait-for
RUN chmod +x /usr/bin/wait-for

COPY --from=0 /src/dist/rating_api-0.1.0-py3-none-any.whl /tmp/rating_api-0.1.0-py3-none-any.whl
RUN true && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev libffi-dev make && \
    pip install /tmp/rating_api-0.1.0-py3-none-any.whl && \
    apk del --no-cache .build-deps && \
    rm /tmp/rating_api-0.1.0-py3-none-any.whl && \
    rm -fr /root/.cache

ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

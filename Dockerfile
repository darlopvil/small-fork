FROM alpine:3.20

ENV APP_ENV=/opt/venv
ENV PATH="${APP_ENV}/bin:$PATH"

WORKDIR $APP_ENV

COPY . .

RUN apk add --no-cache py3-pip uwsgi-python3 && \
  python3 -m venv $APP_ENV && \
  pip install --no-cache-dir . && \
  adduser -D -H small

EXPOSE 8002

USER small:small

ENTRYPOINT ["/opt/venv/entrypoint.sh"]

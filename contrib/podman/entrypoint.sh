#!/bin/sh
set -eu

port="${PORT:-8002}"

args="--plugin python3 \
    --http-socket 0.0.0.0:${port} \
    --master \
    --module small.app:app \
    -H /opt/venv"

if [ "${UWSGI_PROCESSES:-}" ]; then
    args="${args} --processes ${UWSGI_PROCESSES}"
fi

if [ "${UWSGI_THREADS:-}" ]; then
    args="${args} --threads ${UWSGI_THREADS}"
fi

exec /usr/bin/uwsgi ${args}

#!/bin/sh

set -e

if ! [ -z "$RATING_API_MONGODB_URI" ] && [ -z "$NO_WAIT_FOR" ]; then
    HOST_AND_PORT=$(echo $RATING_API_MONGODB_URI | python3 -c "import sys; from urllib.parse import urlparse; data = sys.stdin.read().strip(); result = urlparse(data); host = result.netloc.split('@', 1)[-1]; sys.stdout.write(host)")
    echo "Waiting for ${HOST_AND_PORT}..."
    /usr/bin/wait-for $HOST_AND_PORT -t 60
fi

exec $@

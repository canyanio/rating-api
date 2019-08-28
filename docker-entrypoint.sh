#!/bin/sh

set -e

if ! [ -z "$MONGODB_URI" ]; then
    wait-for -t 60 $MONGODB_URI
fi

exec $@

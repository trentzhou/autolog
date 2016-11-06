#!/usr/bin/env bash

if [ -n "$1" ]; then
    exec "$@"
else
    exec python ./run.py
fi

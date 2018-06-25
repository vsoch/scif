#!/bin/bash

CONTAINER_NAME=${1:-}

echo "Testing exec of commands:"
docker run -it "${CONTAINER_NAME}" exec hello-world-echo echo "Hello World!"
docker run -it "${CONTAINER_NAME}" exec hello-world-script ls /
docker run -it "${CONTAINER_NAME}" exec hello-world-env env

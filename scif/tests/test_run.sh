#!/bin/bash

CONTAINER_NAME=${1:-}

echo "Testing run of each app:"
docker run -it "${CONTAINER_NAME}" run hello-world-echo
docker run -it "${CONTAINER_NAME}" run hello-world-script
docker run -it "${CONTAINER_NAME}" run hello-world-custom "Meatball"
docker run -it "${CONTAINER_NAME}" run hello-world-env | echo "Success"

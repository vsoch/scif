#!/bin/bash

source functions.sh

CONTAINER_NAME=${1:-}

stest 0 docker run -it ${CONTAINER_NAME} test hello-world-script
echo "Tests pass should return 0, returned $?"
stest 255 docker run -it ${CONTAINER_NAME} test hello-world-script 255
echo "Failed test should return 255, returned $?"
stest 1 docker run -it ${CONTAINER_NAME} test hello-world-echo
echo "Missing tests should return 1, returned $?"

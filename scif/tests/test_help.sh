#!/bin/bash

CONTAINER_NAME=${1:-}

echo "The help for each app is the following:"
for app in $(docker run -it --rm=false ${CONTAINER_NAME} apps); 
    do
    echo ${app}
    docker run -it --rm=false "${CONTAINER_NAME}" help ${app}
done

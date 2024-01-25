#!/bin/bash

CONTAINER_NAME=${1:-}

echo "Testing exec of commands:"
docker run -it "${CONTAINER_NAME}" exec hello-world-echo echo "Hello World!"
docker run -it "${CONTAINER_NAME}" exec hello-world-script ls /
docker run -it "${CONTAINER_NAME}" exec hello-world-env env

OUT=$(docker run -it "${CONTAINER_NAME}" --quiet exec hello-world-env echo [e]OMG | tr -d '\n\t\r ')
if [ "$OUT" == "TACOS" ]; then
   echo "Variable Substitution Success: $OUT"
else
   echo "Variable subsitution for e[OMG] failed"
	 exit 1
fi

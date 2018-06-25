#!/bin/bash

stest() {

    # The error code is the first argument

    ERROR="${1:-}"
    shift

    # Get the return value

    "$@"
    RETVAL="$?"

    if [ "$ERROR" = "0" -a "$RETVAL" != "0" ]; then
        printf "%13s ERROR\n" "[retval:$RETVAL]"
        exit 1
    elif [ "$ERROR" != "0" -a "$RETVAL" = "0" ]; then
        printf "ERROR\n" "[retval:$RETVAL]"
        exit 1
    else
        printf "OK\n [retval:$RETVAL]"
    fi
}

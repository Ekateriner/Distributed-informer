#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
context=$( echo "$DIR/../")
echo "Docker context: $context"

docker build -t alert-system-build $context -f $DIR/Dockerfile
#docker rmi $(docker images -f "dangling=true" -q)

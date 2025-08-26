#!/bin/bash

build_and_run_docker() {
    if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
        echo "Usage: build_and_run_docker <image_name> <container_name> <port_mapping>"
        return 1
    fi

    local image_name=$1
    local container_name="${2}_$(date +%s)"
    local port_mapping=$3

    docker build -t $image_name .

    docker stop $container_name 2>/dev/null
    docker rm $container_name 2>/dev/null

    docker run -d --name $container_name -p $port_mapping $image_name

    trap "docker stop $container_name" EXIT

    docker wait $container_name
}

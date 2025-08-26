#!/bin/bash

kill_process_on_port() {
    if [ -z "$1" ]; then
        echo "Usage: kill_process_on_port <port>"
        return 1
    fi
    kill $(lsof -t -i:$1) 2>/dev/null
}

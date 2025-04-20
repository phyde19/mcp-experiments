#!/bin/bash

container="shared-box"
command="$1"

docker exec -it "$container" bash -c "$command"
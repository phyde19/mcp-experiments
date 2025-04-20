#!/bin/bash

container="shared-box"
command="$*"

echo -e "command:\n$command\n"

docker exec -it "$container" "$command"
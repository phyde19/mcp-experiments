#!/bin/bash

container="shared-box"
sandbox="/home/sandbox"
filename="hello.txt"

dexec() {
  docker exec -it "$container" bash -c "$1"
}

dexec "mkdir -p '$sandbox'"
dexec "touch '$sandbox/$filename'" 
dexec "echo hello from the outside >> '$sandbox/$filename'"

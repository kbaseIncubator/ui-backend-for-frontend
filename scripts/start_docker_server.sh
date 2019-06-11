#!/bin/sh
set -e

# Build docker image 'BFF'
docker build . -t bff

# Export environment variables
export KBASE_ENDPOINT=https://kbase.us/services


# Create/start a new docker container and run it on port 5000. 
docker run -i -t -v $(pwd):/app -e DEVELOPMENT -e KBASE_ENDPOINT -p 5000:5000 bff

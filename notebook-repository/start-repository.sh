#!/bin/sh

# Create the docker network if it does not yet exist
docker network create repo

# Start the Notebook Repository container
docker run --rm --net repo -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock genepattern/notebook-repository

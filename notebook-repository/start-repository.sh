#!/bin/sh

# Get the arguments
for ARGUMENT in "$@"
do

    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)

    case "$KEY" in
            --data)              DATA=${VALUE} ;;
            *)
    esac

done

# Assign defaults to arguments
if [ -z "$DATA" ]
then
      DATA=/data
fi

# Copy variable for second use (bash is a harsh mistress)
export DATA_DIR=$DATA

# Create the docker network if it does not yet exist
docker network create repo

# Start the Notebook Repository container
docker run --rm --net=repo --name=notebook-repository -e DATA_DIR=$DATA -p 80:80 -v $DATA_DIR:/data -v /var/run/docker.sock:/var/run/docker.sock genepattern/notebook-repository

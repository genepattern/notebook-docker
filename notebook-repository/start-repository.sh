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
NETWORK_EXISTS=$(docker network inspect repo)
if ! NETWORK_EXISTS=="[]"
then
    docker network create repo
fi

# Set up the mounted data directory, if necessary
[[ -d $DATA_DIR/repository ]] || mkdir $DATA_DIR/repository
[[ -d $DATA_DIR/users ]] || mkdir $DATA_DIR/users
[[ -d $DATA_DIR/shared ]] || mkdir $DATA_DIR/shared
[[ -d $DATA_DIR/auth ]] || mkdir $DATA_DIR/auth

export DB_EXISTS=false
export CONFIG_EXISTS=false
export SETTINGS_EXISTS=false

[[ -f $DATA_DIR/db.sqlite3 ]] && export DB_EXISTS=true
[[ -f $DATA_DIR/jupyterhub_config.py ]] && export CONFIG_EXISTS=true
[[ -f $DATA_DIR/settings.py ]] && export SETTINGS_EXISTS=true

if ! $DB_EXISTS || ! $CONFIG_EXISTS || ! $SETTINGS_EXISTS
then
    echo "INSIDE THE BIG IF"
    docker run --rm --name=copy_data genepattern/notebook-repository &
    sleep 10

    if [ DB_EXISTS==false ]
    then
        docker cp copy_data:/data/db.sqlite3 $DATA_DIR/db.sqlite3
    fi

    if [ CONFIG_EXISTS==false ]
    then
        docker cp copy_data:/data/jupyterhub_config.py $DATA_DIR/jupyterhub_config.py
    fi

    if [ SETTINGS_EXISTS==false ]
    then
        docker cp copy_data:/data/settings.py $DATA_DIR/settings.py
    fi

    docker stop copy_data
fi

# Start the Notebook Repository container
docker run --rm --net=repo --name=notebook_repository -e DATA_DIR=$DATA -p 80:80 -v $DATA_DIR:/data -v /var/run/docker.sock:/var/run/docker.sock genepattern/notebook-repository

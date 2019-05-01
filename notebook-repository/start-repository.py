#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess

##########################################
# Get the arguments passed to the script #
##########################################

# Handle the --data and --port options
parser = argparse.ArgumentParser(description='Start the Docker container for the Notebook Repository')
parser.add_argument('-d', '--data', type=str, default='/data', help='Set the data directory to be mounted in the container')
parser.add_argument('-p', '--port', type=int, default=80, help='Set the port the repository will be available at')
parser.add_argument('-n', '--network', type=str, default='repo', help='The name of the Docker network to run on')

# Parse the arguments
args = parser.parse_args()

##########################################
# Set up the network, if necessary       #
##########################################

network_summary = subprocess.run(f'docker network inspect {args.network}'.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
network_exists = False if network_summary == '[]\n' else True
if not network_exists:
    subprocess.run(f'docker network create {args.network}'.split())

##########################################
# Set up the data directory, if needed   #
##########################################

# Check if /data exists and create lazily if needed
if not os.path.exists(args.data):
    os.mkdir(args.data)
if not os.path.isdir(args.data):
    sys.exit(f'{args.data} is not a directory')

# Check if subdirectories exist and create lazily if needed
required_subdirs = ['repository', 'users', 'shared']
for subdir in required_subdirs:
    subdir_path = os.path.join(args.data, subdir)
    if not os.path.exists(subdir_path):
        os.mkdir(subdir_path)
    if not os.path.isdir(subdir_path):
        sys.exit(f'{subdir_path} is not a directory')

# Check if necessary files exist
db_exists = os.path.exists(os.path.join(args.data, 'db.sqlite3'))
config_exists = os.path.exists(os.path.join(args.data, 'jupyterhub_config.py'))
settings_exists = os.path.exists(os.path.join(args.data, 'settings.py'))

# Start temp container and copy files, if necessary
if not db_exists or not config_exists or not settings_exists:
    print('Starting temporary container')
    subprocess.Popen('docker run --name=copy_data genepattern/notebook-repository'.split())
    subprocess.run('sleep 10'.split())

# Get the database, if necessary
if not db_exists:
    print('Copying database')
    subprocess.run(f'docker cp copy_data:/data/db.sqlite3 {args.data}/db.sqlite3'.split())

# Get the config file, if necessary
if not os.path.exists(os.path.join(args.data, 'jupyterhub_config.py')):
    print('Copying configuration')
    subprocess.run(f'docker cp copy_data:/data/jupyterhub_config.py {args.data}/jupyterhub_config.py'.split())

# Get the settings file, if necessary
if not os.path.exists(os.path.join(args.data, 'settings.py')):
    print('Copying settings')
    subprocess.run(f'docker cp copy_data:/data/settings.py {args.data}/settings.py'.split())

# Clean up the temporary container
if not db_exists or not config_exists or not settings_exists:
    print('Shutting down temporary container')
    subprocess.run('docker stop copy_data'.split())
    subprocess.run('docker rm copy_data'.split())

##########################################
# Start the Notebook Repository          #
##########################################

try:
    subprocess.run(f'docker run --rm --net={args.network} --name=notebook_repository -e DATA_DIR={args.data} -p {args.port}:80 -v {args.data}:/data -v /var/run/docker.sock:/var/run/docker.sock genepattern/notebook-repository'.split())
except KeyboardInterrupt:
    print('Shutting down Notebook Repository')

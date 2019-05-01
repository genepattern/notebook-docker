# GenePattern Notebook Repository

This is a dockerized instance of the GenePattern Notebook Repository, a customized DockerHub deployment
running the GenePattern Notebook environment.

## Installing the Notebook Repository

To start an instance of the Notebook Repository, first pull both the Notebook Repository and the
GenePattern Notebook docker containers:

> docker pull genepattern/notebook-repository
> docker pull genepattern/genepattern-notebook

Next, make sure you have a directory ready on the host file system that will store the persistent state of
the repository. By default this will be located at `/data`, but this can be overridden (see below).

## Starting the Notebook Repository

We recommend starting the Notebook Repository container using the `start-repository.py` script included in
this directory. This will start the container with all of the docker options needed to run. It will also
lazily set up your data directory, if necessary, and configure docker to launch single-user containers as
siblings of the Notebook Repository container.

You can override the location of your data directory by passing in the `--DATA` parameter. If you do not,
the container will assume that it lives at `/data` on the host file system. See the example below.

> ./start-repository.py --data=/path/to/data

You can also override the default port number (port 80) by setting `--port` or the default Docker network
name (repo) by setting `--network`.

## Configuring the Notebook Repository

The Notebook Repository can be configured by tweaking the `jupyterhub_config.py` and `settings.py` files
in the `/data` directory. The former file configured JupyterHub, while the later file configures the
notebook repository's publishing and sharing webservice. At very minimum, we recommend that you change the
secret key in `settings.py` from its default to a value of your choosing.
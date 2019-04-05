# GenePattern Notebook Repository

This is a dockerized instance of the GenePattern Notebook Repository, a customized DockerHub deployment
running the GenePattern Notebook environment.

# Installing the Notebook Repository

To start an instance of the Notebook Repository, first pull both the Notebook Repository and the
GenePattern Notebook docker containers:

> docker pull genepattern/notebook-repository
> docker pull genepattern/genepattern-notebook

Next, make sure you have a directory ready on the host file system that will store the persistent state of
the repository. By default this will be located at `/data`, but this can be overridden (see below).

# Starting the Notebook Repository

We recommend starting the Notebook Repository container using the `start-repository.sh` script included in
this directory. This will start the container with all of the docker options needed to run. It will also
lazily set up your data directory, if necessary, and configure docker to launch single-user containers as
siblings of the Notebook Repository container.

You can override the location of your data directory by passing in the `--DATA` parameter. If you do not,
the container will assume that it lives at `/data` on the host file system. See the example below.

> ./start-repository.sh --data=/path/to/data

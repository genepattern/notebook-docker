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

The `stop-repository.py` script can be used to stop the repository.

## Configuring the Notebook Repository

The Notebook Repository can be configured by tweaking the `jupyterhub_config.py` and `settings.py` files
in the `/data` directory. The former file configures JupyterHub, while the latter file configures the
notebook repository's publishing and sharing webservice. At very minimum, we recommend that you change the
secret key in `settings.py` from its default to a value of your choosing.

## Issues with Docker Swarm

We've run into issues configuring the repository to run with SwarmSpawner because of a bug mounting the
shared volume. Below is a hack to get around that bug. We'd welcome a better solution, but in the
meantime thought it would be useful to share this with the community.

```python
from dockerspawner import SwarmSpawner
from docker.types import Mount

class SwarmSpawner2(SwarmSpawner):

    @property
    def mounts(self):
        if len(self.volume_binds):
            driver = self.mount_driver_config
            return [
                Mount(
                    target=vol["bind"],
                    source=host_loc,
                    type="bind",
                    read_only=vol["mode"] == "ro",
                    driver_config=None,  # This needs to be None or the spawner throws an error
                )
                for host_loc, vol in self.volume_binds.items()
            ]

        else:
            return []

c.JupyterHub.spawner_class = SwarmSpawner2

# Configure DockerSpawner
# c.JupyterHub.spawner_class = 'dockerspawner.SwarmSpawner'

# c.SwarmSpawner.host_ip = '0.0.0.0'
c.SwarmSpawner2.image = 'genepattern/genepattern-notebook'
c.SwarmSpawner2.network_name = 'repo'
c.SwarmSpawner2.extra_host_config = { 'network_mode': 'repo' }
c.SwarmSpawner2.remove_containers = True
c.SwarmSpawner2.debug = True

# Mount the user's directory in the singleuser containers
if 'DATA_DIR' in os.environ:
    c.SwarmSpawner2.volumes = {
        os.environ['DATA_DIR'] + '/users/{raw_username}': '/home/jovyan',    # Mount users directory
    }
```
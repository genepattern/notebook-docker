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
from tornado import gen

class FixedSwarmSpawner(SwarmSpawner):

   @gen.coroutine
    def start_object(self):
        """Not actually starting anything
        but use this to wait for the container to be running.
        Spawner.start shouldn't return until the Spawner
        believes a server is *running* somewhere,
        not just requested.
        """

        dt = 1.0

        while True:
            yield gen.sleep(dt)
            service = yield self.get_task()
            if not service:
                raise RuntimeError("Service %s not found" % self.service_name)

            status = service["Status"]
            state = status["State"].lower()
            self.log.debug("Service %s state: %s", self.service_id[:7], state)
            if state in {"new", "assigned", "accepted", "starting", "pending", "preparing"}:
                # not ready yet, wait before checking again
                yield gen.sleep(dt)
                # exponential backoff
                dt = min(dt * 1.5, 11)
            else:
                break
        if state != "running":
            raise RuntimeError(
                "Service %s not running: %s" % (self.service_name, pformat(status))
            )

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

c.JupyterHub.spawner_class = FixedSwarmSpawner

# Configure DockerSpawner
c.FixedSwarmSpawner.image = 'genepattern/genepattern-notebook'
c.FixedSwarmSpawner.network_name = 'repo'
c.FixedSwarmSpawner.extra_host_config = { 'network_mode': 'repo' }
c.FixedSwarmSpawner.remove_containers = True
c.FixedSwarmSpawner.debug = True

# Mount the user's directory in the singleuser containers
if 'DATA_DIR' in os.environ:
    c.FixedSwarmSpawner.volumes = {
        os.environ['DATA_DIR'] + '/users/{raw_username}': '/home/jovyan',    # Mount users directory
    }
```
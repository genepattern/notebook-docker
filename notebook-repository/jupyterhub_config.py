import os

c = get_config()

#  This is the address on which the proxy will bind. Sets protocol, ip, base_url
c.JupyterHub.bind_url = 'http://:80'

# Listen on all interfaces
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'notebook_repository'

# Configure the GenePattern Authenticator
c.JupyterHub.authenticator_class = 'gpauthenticator.GenePatternAuthenticator'
c.Authenticator.admin_users = {'admin'}

# Configure DockerSpawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

c.DockerSpawner.host_ip = '0.0.0.0'
c.DockerSpawner.image = 'genepattern/genepattern-notebook'
c.DockerSpawner.network_name = 'repo'
# c.DockerSpawner.extra_host_config = { 'network_mode': 'repo' }
c.DockerSpawner.remove_containers = True
c.DockerSpawner.debug = True

# Mount the user's directory in the singleuser containers
if 'DATA_DIR' in os.environ:
    c.DockerSpawner.volumes = {
        os.environ['DATA_DIR'] + '/users/{raw_username}': '/home/jovyan',    # Mount users directory
    }

# Services API configuration
c.JupyterHub.services = [
    {
        'name': 'sharing',
        'admin': True,
        'url': 'http://127.0.0.1:8000/',
        'cwd': '/srv/notebook-repository',
        'command': ['/opt/conda/envs/repository/bin/python', './manage.py', 'runserver', '0.0.0.0:8000']
    },
    {
        'name': 'cull-idle',
        'admin': True,
        'command': ['python', '/srv/notebook-repository/scripts/cull-idle.py', '--timeout=3600']
    }
]

# Connect to the database in /data
c.JupyterHub.db_url = '/data/jupyterhub.sqlite'

# Write to the log file
c.JupyterHub.extra_log_file = '/data/jupyterhub.log'

# Number of days for a login cookie to be valid. Default is two weeks.
c.JupyterHub.cookie_max_age_days = 1

# File in which to store the cookie secret.
c.JupyterHub.cookie_secret_file = '/srv/jupyterhub/jupyterhub_cookie_secret'

# SSL/TLS will be handled outside of the container
c.JupyterHub.confirm_no_ssl = True

# Grant admin users permission to access single-user servers.
c.JupyterHub.admin_access = True

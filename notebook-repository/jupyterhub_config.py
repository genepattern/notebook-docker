import os
from projects.hub import UserHandler, PreviewHandler, pre_spawn_hook

c = get_config()

#  This is the address on which the proxy will bind. Sets protocol, ip, base_url
c.JupyterHub.bind_url = 'http://:80'

# Listen on all interfaces
c.JupyterHub.hub_ip = '0.0.0.0'
# c.JupyterHub.hub_connect_ip = 'notebook_repository'

# Configure the GenePattern Authenticator
c.JupyterHub.authenticator_class = 'gpauthenticator.GenePatternAuthenticator'
c.GenePatternAuthenticator.users_dir_path = '/data/users'
c.GenePatternAuthenticator.default_nb_dir = '/data/default'
c.Authenticator.admin_users = ['admin']

# Configure DockerSpawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.host_ip = '0.0.0.0'
c.DockerSpawner.image = 'genepattern/genepattern-notebook:21.03'
c.DockerSpawner.image_whitelist = {
    'Legacy': 'genepattern/genepattern-notebook:21.03',
    'R 3.6': 'genepattern/notebook-r36:20.10'
}
c.DockerSpawner.network_name = 'repo'
c.DockerSpawner.remove_containers = True
c.DockerSpawner.debug = True
c.DockerSpawner.pre_spawn_hook = lambda spawner: pre_spawn_hook(spawner, userdir=os.environ['DATA_DIR'] + '/users')
c.DockerSpawner.volumes = {
    os.path.join(os.environ['DATA_DIR'] + '/users/{raw_username}/{servername}'): '/home/jovyan',  # Mount users directory
}

# Mount the user's directory in the singleuser containers
if 'DATA_DIR' in os.environ:
    c.DockerSpawner.pre_spawn_hook = lambda spawner: os.makedirs(os.path.join(os.environ['DATA_DIR'], 'users', spawner.user.name, spawner.name), 0o777, exist_ok=True)
    c.DockerSpawner.volumes = {
        os.environ['DATA_DIR'] + '/users/{raw_username}': '/home/jovyan',    # Mount users directory
    }

# Add the theme config
c.JupyterHub.logo_file = '/opt/conda/share/jupyterhub/static/images/gpnb.png'
c.JupyterHub.template_paths = ['/srv/notebook-repository/theme/templates']

# Named server config
c.JupyterHub.allow_named_servers = True
c.JupyterHub.default_url = '/home'
c.JupyterHub.extra_handlers = [('user.json', UserHandler), ('preview', PreviewHandler)]
c.DockerSpawner.name_template = "{prefix}-{username}-{servername}"

# Services API configuration
c.JupyterHub.services = [
    {
        'name': 'projects',
        'admin': True,
        'url': 'http://127.0.0.1:3000/',
        'cwd': '/srv/notebook-repository/',
        'environment': {
            'IMAGE_WHITELIST': ','.join(c.DockerSpawner.image_whitelist.keys())
        },
        'command': ['python', 'start-projects.py',
                    f'--config=/data/projects_config.py']
    },
    {
        'name': 'cull-idle',
        'admin': True,
        'command': ['python', '/srv/notebook-repository/scripts/cull-idle.py', '--timeout=3600']
    }
]

# Enable CORS
origin = '*'
c.Spawner.args = [f'--NotebookApp.allow_origin={origin}', '--NotebookApp.allow_credentials=True', "--NotebookApp.tornado_settings={\"headers\":{\"Referrer-Policy\":\"no-referrer-when-downgrade\"}}"]
c.JupyterHub.tornado_settings = {
    'headers': {
        'Referrer-Policy': 'no-referrer-when-downgrade',
        'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Credentials': 'true',
    },
}

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

# Dockerfile for running an instance of the GenePattern Notebook Repository

# Pull a known good jupyterhub image from the official Jupyter stacks
# Built 01-25-2022
FROM jupyterhub/jupyterhub:2.1.1

MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>

#############################################
##      System updates                     ##
#############################################

RUN apt-get update && apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 \
    libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 \
    libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 \
    libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget nano \
    docker.io libcurl4 curl gcc python3-dev libmysqlclient-dev \
    && pip install awscli jupyterhub_idle_culler sqlalchemy tornado jinja2 traitlets requests pymysql dockerspawner \
    && ln -s /usr/bin/python3 /usr/bin/python

#############################################
##      Create the data volume             ##
#############################################

RUN mkdir /data

#############################################
##      Force builds with new releases     ##
#############################################

RUN echo '22.02, JupyterHub 2.1.1 Upgrade'

#############################################
##      Add the repository webservice      ##
#############################################

RUN git clone https://github.com/genepattern/notebook-repository.git /srv/notebook-repository/

#############################################
##      Configure the repository           ##
#############################################

# Add to the PYTHONPATH
RUN cp -r /srv/notebook-repository/projects /usr/local/lib/python3.8/dist-packages/

# Create subdirectories in the data directory
RUN mkdir /data/repository
RUN mkdir /data/users
RUN mkdir /data/shared
RUN mkdir /data/defaults

#############################################
##      Install Authenticator & Spawner    ##
#############################################


RUN ln -s /srv/notebook-repository/nbrepo /usr/local/lib/python3.8/dist-packages/nbrepo
RUN mv /srv/notebook-repository/gpauthenticator /usr/local/lib/python3.8/dist-packages/

#############################################
##      Add the config files               ##
#############################################

COPY ./jupyterhub_config.py /data/
COPY ./projects_config.py /data/

#############################################
##      Add the GenePattern theme          ##
#############################################

# Add the theme assets to JupyterHub
RUN cp /srv/notebook-repository/theme/images/* /usr/local/share/jupyterhub/static/images/
RUN cp /srv/notebook-repository/theme/css/* /usr/local/share/jupyterhub/static/css/
RUN cp /srv/notebook-repository/theme/js/* /usr/local/share/jupyterhub/static/js/

# Import the theme
RUN { echo '@import url("/hub/static/css/genepattern.css");'; cat /usr/local/share/jupyterhub/static/css/style.min.css; } \
    > /tmp/style.min.css && mv /tmp/style.min.css /usr/local/share/jupyterhub/static/css/style.min.css

#############################################
##  $NB_USER                               ##
##      Enable nano and vi                 ##
#############################################

ENV TERM xterm

#############################################
##      Start JupyterHub                   ##
#############################################

CMD ["jupyterhub", "-f", "/data/jupyterhub_config.py"]
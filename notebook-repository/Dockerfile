# Dockerfile for running an instance of the GenePattern Notebook Repository

# Pull a known good jupyterhub image from the official Jupyter stacks
# Built 01-17-2020
FROM jupyterhub/jupyterhub:1.1

MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>

#############################################
##      System updates                     ##
#############################################

RUN apt-get update && apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 \
    libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 \
    libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 \
    libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget nano \
    docker.io libcurl4 curl gcc python3-dev libmysqlclient-dev \
    && pip install awscli mysqlclient

#############################################
##      Create the data volume             ##
#############################################

RUN mkdir /data

#############################################
##      Install conda                      ##
#############################################

RUN wget -q https://repo.continuum.io/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh -O /tmp/miniconda.sh  && \
    echo '751786b92c00b1aeae3f017b781018df */tmp/miniconda.sh' | md5sum -c - && \
    bash /tmp/miniconda.sh -f -b -p /opt/conda && \
    /opt/conda/bin/conda install --yes -c conda-forge \
      python=3.7 sqlalchemy tornado jinja2 traitlets requests pip pycurl ruamel.yaml jupyterhub=1.1.0 \
      nodejs configurable-http-proxy && \
    /opt/conda/bin/pip install --upgrade pip && \
    rm /tmp/miniconda.sh
ENV PATH=/opt/conda/bin:$PATH

#############################################
##      Force builds with new releases     ##
#############################################

RUN echo '22.01, Tornado async fix'

#############################################
##      Add the repository webservice      ##
#############################################

RUN git clone https://github.com/genepattern/notebook-repository.git /srv/notebook-repository/

#############################################
##      Configure the repository           ##
#############################################

# Add to the PYTHONPATH
RUN cp -r /srv/notebook-repository/projects /opt/conda/lib/python3.7/site-packages/

# Create subdirectories in the data directory
RUN mkdir /data/repository
RUN mkdir /data/users
RUN mkdir /data/shared
RUN mkdir /data/defaults

#############################################
##      Install Authenticator & Spawner    ##
#############################################

RUN pip install dockerspawner==12.0.0
RUN ln -s /srv/notebook-repository/nbrepo /opt/conda/lib/python3.7/site-packages/nbrepo
RUN mv /srv/notebook-repository/gpauthenticator /opt/conda/lib/python3.7/site-packages/

#############################################
##      Add the config files               ##
#############################################

COPY ./jupyterhub_config.py /data/
COPY ./projects_config.py /data/

#############################################
##      Add the GenePattern theme          ##
#############################################

# Add the theme assets to JupyterHub
RUN cp /srv/notebook-repository/theme/images/* /opt/conda/share/jupyterhub/static/images/
RUN cp /srv/notebook-repository/theme/css/* /opt/conda/share/jupyterhub/static/css/
RUN cp /srv/notebook-repository/theme/js/* /opt/conda/share/jupyterhub/static/js/

# Import the theme
RUN { echo '@import url("/hub/static/css/genepattern.css");'; cat /opt/conda/share/jupyterhub/static/css/style.min.css; } \
    > /tmp/style.min.css && mv /tmp/style.min.css /opt/conda/share/jupyterhub/static/css/style.min.css

#############################################
##  $NB_USER                               ##
##      Enable nano and vi                 ##
#############################################

ENV TERM xterm

#############################################
##      Start JupyterHub                   ##
#############################################

CMD ["jupyterhub", "-f", "/data/jupyterhub_config.py"]
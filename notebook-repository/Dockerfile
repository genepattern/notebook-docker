# Dockerfile for running an instance of the GenePattern Notebook Repository

# Pull the latest known good jupyterhub image from the official Jupyter stacks
# Built 04-01-2019
FROM jupyterhub/jupyterhub:0.9.6

MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>

#############################################
##      System updates                     ##
#############################################

RUN apt-get update && apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 \
    libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 \
    libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 \
    libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget nano docker.io
RUN pip install awscli

#############################################
##      Create the data volume             ##
#############################################

RUN mkdir /data

#############################################
##      Create the repository environment  ##
#############################################

# Create the Python 3.6 environment
RUN /opt/conda/bin/conda update -y conda
RUN /opt/conda/bin/conda create -y --name repository python=3.6 pip

RUN /bin/bash -c "source activate repository && \
    pip install Django==1.10 \
                markdown==2.6.6 \
                djangorestframework==3.4.4 \
                django-filter==0.14.0 \
                django-crispy-forms==1.6.0 \
                django-cors-middleware==1.3.1 \
                pyppeteer==0.0.25 \
                requests==2.21.0 \
                jupyterhub==0.9.6"

#############################################
##      Force builds with new releases     ##
#############################################

RUN echo 'notebook-repository 19.07'

#############################################
##      Add the repository webservice      ##
#############################################

RUN git clone https://github.com/genepattern/notebook-repository.git /srv/notebook-repository/

#############################################
##      Configure the repository           ##
#############################################

# Add the repository webservice settings
COPY ./settings.py /data
RUN rm /srv/notebook-repository/nbrepo/settings.py
RUN ln -s /data/settings.py /srv/notebook-repository/nbrepo/settings.py

# Create subdirectories in data directory
RUN mkdir /data/repository
RUN mkdir /data/users
RUN mkdir /data/shared
RUN mkdir /data/defaults

RUN /bin/bash -c "source activate repository && \
    /srv/notebook-repository/manage.py makemigrations"
RUN /bin/bash -c "source activate repository && \
    /srv/notebook-repository/manage.py migrate --run-syncdb"
RUN /bin/bash -c "source activate repository && \
    /srv/notebook-repository/manage.py collectstatic --noinput"

#############################################
##      Install Authenticator & Spawner    ##
#############################################

RUN pip install dockerspawner==0.11.1
RUN ln -s /srv/notebook-repository/nbrepo /opt/conda/lib/python3.6/site-packages/nbrepo
RUN mv /srv/notebook-repository/authenticator/gpauthenticator.py /opt/conda/lib/python3.6/site-packages/

#############################################
##      Add the jupyterhub_config file     ##
#############################################

COPY ./jupyterhub_config.py /data/

#############################################
##      Add the GenePattern theme          ##
#############################################

# Add the theme assets to JupyterHub
RUN mv /srv/notebook-repository/theme/images/* /opt/conda/share/jupyterhub/static/images/
RUN mv /srv/notebook-repository/theme/css/* /opt/conda/share/jupyterhub/static/css/
RUN mv /srv/notebook-repository/theme/templates/* /opt/conda/share/jupyterhub/templates/

# Import the theme
RUN { echo '@import url("/hub/static/css/genepattern.css");'; cat /opt/conda/share/jupyterhub/static/css/style.min.css; } \
    > /tmp/style.min.css && mv /tmp/style.min.css /opt/conda/share/jupyterhub/static/css/style.min.css

#############################################
##      Start JupyterHub                   ##
#############################################

CMD ["jupyterhub", "-f", "/data/jupyterhub_config.py"]
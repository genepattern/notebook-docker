# Dockerfile for running an instance of the GenePattern Notebook Repository

# Pull the latest known good jupyterhub image from the official Jupyter stacks
# Built 02-14-2019
FROM jupyterhub/jupyterhub:0.9.4

MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>

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
                jupyterhub==0.9.4"

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
RUN mkdir /data/auth

RUN /bin/bash -c "source activate repository && \
    /srv/notebook-repository/manage.py makemigrations"
RUN /bin/bash -c "source activate repository && \
    /srv/notebook-repository/manage.py migrate --run-syncdb"

#############################################
##      Install Authenticator & Spawner    ##
#############################################

RUN /opt/conda/bin/conda install --yes -c conda-forge dockerspawner==0.11.0
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
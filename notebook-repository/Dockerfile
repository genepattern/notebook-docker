# Dockerfile for running an instance of the GenePattern Notebook Repository

# Pull the latest known good jupyterhub image from the official Jupyter stacks
# Built 02-14-2019
FROM jupyterhub/jupyterhub:0.9.4

MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>

#############################################
##  ROOT                                   ##
##      Add the repository webservice      ##
#############################################

RUN git clone https://github.com/genepattern/notebook-repository.git /srv/notebook-repository/
# TODO: Configure the service

#############################################
##  ROOT                                   ##
##      Install Authenticator & Spawner    ##
#############################################

RUN /opt/conda/bin/conda install --yes -c conda-forge dockerspawner==0.11.0
RUN mv /srv/notebook-repository/authenticator/gpauthenticator.py /opt/conda/lib/python3.6/site-packages/

#############################################
##  ROOT                                   ##
##      Add the jupyterhub_config file     ##
#############################################

COPY ./jupyterhub_config.py /srv/jupyterhub/
# TODO: Finish connfig, including services API
# TODO: Also copy lines from prod repo to make sure all bases covered

#############################################
##  ROOT                                   ##
##      Add the GenePattern theme          ##
#############################################

# TODO

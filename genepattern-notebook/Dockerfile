# Dockerfile for running the GenePattern Notebook Environment

# Pull the latest known good scipy notebook image from the official Jupyter stacks
# Built 10-24-2018
FROM jupyter/scipy-notebook:ebb42274ac29

MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>

EXPOSE 8888

#############################################
##  ROOT                                   ##
##      Install Docker                     ##
#############################################

USER root

# Install the missing Qt4 API (used by matplotlib)
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Install Docker from Docker Inc. repositories.
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update && apt-get install -y docker-ce

# Install the magic wrapper.
RUN wget https://raw.githubusercontent.com/jpetazzo/dind/master/wrapdocker --output-document=/usr/local/bin/wrapdocker
RUN chmod +x /usr/local/bin/wrapdocker

# Set up the Docker service
RUN gpasswd -a $NB_USER docker
RUN newgrp docker

#############################################
##  ROOT                                   ##
##      Update QT4                         ##
#############################################

USER root

# Install the missing Qt4 API (used by matplotlib)
RUN apt-get install -y python-qt4

#############################################
##  ROOT                                   ##
##      Install R and rpy2                 ##
#############################################

USER root

# Install R and RPY2
RUN apt-get install gpg -y
RUN sh -c 'echo "deb http://cran.rstudio.com/bin/linux/ubuntu bionic-cran35/" >> /etc/apt/sources.list'
RUN gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9
RUN gpg -a --export E084DAB9 | sudo apt-key add -
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install r-base r-base-dev -y
RUN pip install rpy2==2.8.5 --ignore-installed
RUN mkdir -p /home/$NB_USER/.ipython/profile_default/startup
RUN echo '%load_ext rpy2.ipython' >> /home/$NB_USER/.ipython/profile_default/startup/mymagics.ipy
RUN chown $NB_USER:users /home/$NB_USER/.ipython -R

# Install R libraries
RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > /usr/lib/R/.Rprofile
RUN Rscript -e "install.packages('ggplot2')"
RUN Rscript -e "source('https://bioconductor.org/biocLite.R')"

#############################################
##  $NB_USER                               ##
##      Force builds with new releases     ##
#############################################

USER $NB_USER

RUN echo 'nbtools 0.2.4, genepattern-notebook 0.8.5'

#############################################
##  $NB_USER                               ##
##      Update the theme                   ##
#############################################

USER $NB_USER

# Copy the logo
COPY ./logo.png /opt/conda/lib/python3.6/site-packages/notebook/static/base/images/logo.png

# Copy the favicon
COPY ./favicon.ico /opt/conda/lib/python3.6/site-packages/notebook/static/base/images/favicon.ico

# Install the custom theme
COPY ./custom.css /opt/conda/lib/python3.6/site-packages/notebook/static/custom/custom.css
COPY ./custom.js /opt/conda/lib/python3.6/site-packages/notebook/static/custom/custom.js

#############################################
##  ROOT                                   ##
##      Configure nbextensions             ##
#############################################

USER root

# Install GenePattern nbextensions in default Python environment
RUN pip install -v nbtools genepattern-notebook jupyter_wysiwyg

# Enable the extensions
RUN jupyter nbextension enable --sys-prefix --py nbtools
RUN jupyter nbextension enable --sys-prefix --py genepattern
RUN jupyter nbextension enable --sys-prefix --py jupyter_wysiwyg

# Enable Notebook Repository frontend
RUN git clone https://github.com/genepattern/notebook-repository-frontend.git
RUN cd notebook-repository-frontend && jupyter nbextension install repo
RUN cd notebook-repository-frontend && jupyter nbextension enable --sys-prefix repo/js/main
RUN cd notebook-repository-frontend && jupyter nbextension enable --sys-prefix --section=tree repo/js/main
RUN rm -r notebook-repository-frontend

# Enable Notebook Repository hints
RUN git clone https://github.com/genepattern/notebook-tour.git
RUN cd notebook-tour && jupyter nbextension install hints
RUN cd notebook-tour && jupyter nbextension enable --sys-prefix --section=tree hints/js/main
RUN rm -r notebook-tour

# Install the collapsible_headings extension
RUN mkdir /opt/conda/share/jupyter/nbextensions/collapsible_headings
RUN wget https://github.com/ipython-contrib/jupyter_contrib_nbextensions/raw/master/src/jupyter_contrib_nbextensions/nbextensions/collapsible_headings/main.js -O /opt/conda/share/jupyter/nbextensions/collapsible_headings/main.js
RUN wget https://github.com/ipython-contrib/jupyter_contrib_nbextensions/raw/master/src/jupyter_contrib_nbextensions/nbextensions/collapsible_headings/main.css -O /opt/conda/share/jupyter/nbextensions/collapsible_headings/main.css
RUN echo '{"load_extensions": {"collapsible_headings/main": true}}' > /opt/conda/etc/jupyter/nbconfig/notebook.d/collapsible_headings.json

# Install the igv.js extension
RUN pip install -v igv==0.9.5
RUN jupyter serverextension enable --sys-prefix --py igv
RUN jupyter nbextension install --sys-prefix --py igv
RUN jupyter nbextension enable --sys-prefix --py igv

# Install the cytoscape extension
RUN pip install -v cyjupyter==0.2.0
RUN jupyter nbextension enable --sys-prefix --py cyjupyter

#############################################
##  $NB_USER                               ##
##      Create the Python 3.6 environment  ##
#############################################

USER $NB_USER

# Create the Python 3.6 environment
RUN conda update -y conda
RUN conda create -y --name python3.6 python=3.6 anaconda ipykernel==5.1.0

# Add the basic scipy packages to environment (copied from jupyter/scipy-notebook)
# The unusual /bin/bash ... && ... call is necessary because weird interactions between conda and docker
RUN /bin/bash -c "source activate python3.6 && \
    conda install -y 'tornado=5.1.1' 'ipywidgets=7.2*' 'conda-forge::blas=*=openblas' 'pandas=0.23*' 'numexpr=2.6*' 'matplotlib=2.2*' 'scipy=1.1*' 'seaborn=0.9*' \
    'scikit-learn=0.19*' 'scikit-image=0.14*' 'sympy=1.1*' 'cython=0.28*' 'patsy=0.5*' 'statsmodels=0.9*' 'cloudpickle=0.5*' 'dill=0.2*' 'numba=0.38*' \
    'bokeh=0.13*' 'sqlalchemy=1.2*' 'hdf5=1.10*' 'h5py=2.7*' 'vincent=0.4.*' 'beautifulsoup4=4.6.*' 'protobuf=3.*' 'xlrd=1.1.0'"

# Install the GenePattern Notebook Environment packages
# The unusual /bin/bash ... && ... call is necessary because weird interactions between conda and docker
RUN /bin/bash -c "source activate python3.6 && \
    conda install -y -c conda-forge 'biopython==1.70' 'igraph==0.7.1' 'babel==2.4.0' 'louvain==0.6.1' 'beakerx==1.2.0'"
RUN /bin/bash -c "source activate python3.6 && \
    pip install nbtools genepattern-python genepattern-notebook jupyter_wysiwyg \
    'igv==0.9.5' 'cyjupyter==0.2.0' 'ccalnoir==2.6' 'cuzcatlan==0.9.0' 'ndex2==1.2.0.*' \
    'anndata==0.5.10' 'enum34==1.1.6' 'ijson==2.3' 'joblib==0.11' 'natsort==5.2.0' 'plotly==2.4.1' \
    'pysolr==3.7.0' 'rpy2==2.8.5' 'scanpy==0.4.2' 'tqdm==4.23.4' 'validators==0.12.0' 'pysam==0.15.1' 'hca==4.4.10' 'simplegeneric==0.8.1'"

# Ugly hack for the single-cell notebook. Remove this once that notebook is refactored.
RUN wget -O /opt/conda/envs/python3.6/lib/python3.6/site-packages/singlecell.py https://github.com/genepattern/single_cell_clustering_notebook/raw/master/singlecell.py

#############################################
##  $NB_USER                               ##
##      Create the Python 3.7 environment  ##
#############################################

USER $NB_USER

# Create the Python 3.7 environment
RUN conda create -y --name python3.7 python=3.7 anaconda ipykernel==5.1.0

# Add the basic scipy packages to environment (copied from jupyter/scipy-notebook)
# The unusual /bin/bash ... && ... call is necessary because weird interactions between conda and docker
RUN /bin/bash -c "source activate python3.7 && \
    conda install -y 'tornado=5.1.1' 'ipywidgets=7.2*' 'conda-forge::blas=*=openblas' 'pandas' 'numexpr' 'matplotlib' 'scipy' 'seaborn' \
    'scikit-learn' 'scikit-image' 'sympy' 'cython' 'patsy' 'statsmodels' 'cloudpickle' 'dill' 'numba' \
    'bokeh' 'sqlalchemy' 'hdf5' 'h5py' 'vincent' 'beautifulsoup4' 'protobuf' 'xlrd' 'simplegeneric'"

# Install the GenePattern Notebook Environment packages
# The unusual /bin/bash ... && ... call is necessary because weird interactions between conda and docker
RUN /bin/bash -c "source activate python3.7 && \
    conda install -y -c conda-forge 'biopython' 'igraph' 'babel' 'louvain' 'tzlocal' "
RUN /bin/bash -c "source activate python3.7 && \
    conda install -y -c bioconda 'pysam'"
RUN /bin/bash -c "source activate python3.7 && \
    pip install nbtools genepattern-python genepattern-notebook jupyter_wysiwyg"
RUN /bin/bash -c "source activate python3.7 && \
    pip install 'igv==0.9.5' 'cyjupyter==0.2.0' 'ccalnoir==2.7' 'cuzcatlan==0.9.3' 'ndex2==1.2.0.*' 'py2cytoscape==0.7.0' "
RUN /bin/bash -c "source activate python3.7 && \
    pip install 'plotly==2.4.1' 'rpy2==2.8.5' 'opencv-python==4.0.0.21' 'hca==4.8.0' "
RUN /bin/bash -c "source activate python3.7 && \
    pip install scanpy memory_profiler"
RUN /bin/bash -c "source activate python3.7 && \
    pip install -e git://github.com/LankyCyril/genefab.git#egg=genefab"

#############################################
##  ROOT                                   ##
##      Configure Jupyter kernels          ##
#############################################

USER root

# Add the environments as Jupyter kernels
RUN /bin/bash -c "source activate python3.6 && python -m ipykernel install --name python3.6 --display-name 'Python 3.6'"
RUN /bin/bash -c "source activate python3.7 && python -m ipykernel install --name python3.7 --display-name 'Python 3.7'"

# Remove the default Python kernel
RUN rm -r /opt/conda/share/jupyter/kernels/python3
RUN echo 'c.KernelSpecManager.ensure_native_kernel = False' >> /etc/jupyter/jupyter_notebook_config.py

#############################################
##  root                                   ##
##      Clean up build environment         ##
#############################################

USER root

RUN rm -r work
RUN rm -r src

#############################################
##  $NB_USER                               ##
##      Enable nano and vi                 ##
#############################################

USER $NB_USER

ENV TERM xterm
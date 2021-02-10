# Dockerfile for running the GenePattern Notebook Environment

# Pull the latest known good minimal notebook image from the official Jupyter stacks
# Built 09-30-2020
#FROM jupyter/minimal-notebook:150731d32f85

# JTL latest image on 12/3/20
FROM jupyter/minimal-notebook:5cfa60996e84


MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>

EXPOSE 8888

#############################################
##  ROOT                                   ##
##      Install missing libraries          ##
#############################################

USER root

# Install the missing Qt4 API (used by matplotlib)  # CUT: python-qt4
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl software-properties-common python3-pyqt5 \
    libxtst6 libssl-dev libcurl4-openssl-dev gpg build-essential python-dev default-jdk apt-utils libxml2-dev libxml2

#############################################
##  ROOT                                   ##
##      Install Docker                     ##
#############################################

USER root

# Install Docker from Docker Inc. repositories.
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get install -y docker-ce

# Install the magic wrapper.
RUN wget https://raw.githubusercontent.com/jpetazzo/dind/master/wrapdocker --output-document=/usr/local/bin/wrapdocker && \
    chmod +x /usr/local/bin/wrapdocker

# Set up the Docker service
RUN gpasswd -a $NB_USER docker && \
    newgrp docker

#############################################
##  ROOT                                   ##
##      Install R and rpy2                 ##
#############################################

USER root

RUN apt-get install -y libudunits2-dev libopenblas-dev libxt-dev
RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install --update-deps -y r-monocle3=0.2.1 r-seurat=3.0.2 r-getopt=1.20.3 r-optparse=1.6.4 r-dplyr=0.8.0.1

# Write Rprofile
RUN printf 'options(install.packages.compile.from.source = "always")\noptions(repos = "http://cran.r-project.org")\noptions(bitmapType="cairo")\n' > /opt/conda/lib/R/etc/Rprofile.site

# Install common R libraries
RUN /opt/conda/bin/Rscript -e "install.packages('openssl')" && \
    /opt/conda/bin/Rscript -e "install.packages('curl')" && \
    /opt/conda/bin/Rscript -e "install.packages('httr')" && \
    /opt/conda/bin/Rscript -e "install.packages('ggplot2')" && \
    /opt/conda/bin/Rscript -e "install.packages('BiocManager')" && \
    /opt/conda/bin/Rscript -e "install.packages('IRkernel')" && \
    /opt/conda/bin/Rscript -e "install.packages(c('Matrix', 'stringi'))" && \
    conda install --update-deps -y bioconductor-deseq2=1.26.0 bioconductor-summarizedexperiment=1.16.0 && \
    /opt/conda/bin/Rscript -e "BiocManager::install(c('CoGAPS', 'ComplexHeatmap'))" && \
    /opt/conda/bin/Rscript -e "BiocManager::install(c('DESeq2'))"

RUN chmod 777 /opt

#############################################
##  $NB_USER                               ##
##      Install Globus client              ##
#############################################

USER $NB_USER

RUN mkdir -p /opt/gcp

RUN wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz -O /tmp/globusconnectpersonal-latest.tgz && \
    tar -xzvf /tmp/globusconnectpersonal-latest.tgz -C /opt && \
    mv $(find /opt -type 'd' -name 'globus*' -maxdepth 1) /opt/gcp

#############################################
##  $NB_USER                               ##
##      Force builds with new releases     ##
#############################################

RUN echo '21.02, Updating to base build'

#############################################
##  $NB_USER                               ##
##      Update the theme                   ##
#############################################

USER $NB_USER

# Copy the logo and favicon
COPY ./logo.png ./favicon.ico /opt/conda/lib/python3.8/site-packages/notebook/static/base/images/

# Install the custom theme
COPY ./custom.css ./custom.js ./theme.css ./background.jpg /opt/conda/lib/python3.8/site-packages/notebook/static/custom/

#############################################
##  ROOT                                   ##
##      Configure nbextensions             ##
#############################################

USER root

# Install GenePattern nbextensions in default Python environment
RUN pip install -v nbtools genepattern-notebook jupyter_wysiwyg

# Enable the extensions
RUN jupyter nbextension enable --sys-prefix --py nbtools && \
    jupyter nbextension enable --sys-prefix --py genepattern && \
    jupyter nbextension enable --sys-prefix --py jupyter_wysiwyg

# Enable Notebook Repository frontend
RUN git clone https://github.com/genepattern/notebook-repository-frontend.git && \
    cd notebook-repository-frontend && \
    jupyter nbextension install repo && \
    jupyter nbextension enable --sys-prefix repo/js/main && \
    jupyter nbextension enable --sys-prefix --section=tree repo/js/main && \
    rm -r ../notebook-repository-frontend

# Enable Notebook Repository hints
RUN git clone https://github.com/genepattern/notebook-tour.git && \
    cd notebook-tour && \
    jupyter nbextension install hints && \
    jupyter nbextension enable --sys-prefix --section=tree hints/js/main && \
    jupyter nbextension enable --sys-prefix --section=notebook hints/js/main && \
    rm -r ../notebook-tour

# Install the collapsible_headings extension
RUN mkdir /opt/conda/share/jupyter/nbextensions/collapsible_headings && \
    wget https://github.com/ipython-contrib/jupyter_contrib_nbextensions/raw/master/src/jupyter_contrib_nbextensions/nbextensions/collapsible_headings/main.js -O /opt/conda/share/jupyter/nbextensions/collapsible_headings/main.js && \
    wget https://github.com/ipython-contrib/jupyter_contrib_nbextensions/raw/master/src/jupyter_contrib_nbextensions/nbextensions/collapsible_headings/main.css -O /opt/conda/share/jupyter/nbextensions/collapsible_headings/main.css && \
    echo '{"load_extensions": {"collapsible_headings/main": true}}' > /opt/conda/etc/jupyter/nbconfig/notebook.d/collapsible_headings.json

# Install the toc2 extension
RUN mkdir /opt/conda/share/jupyter/nbextensions/toc2 && \
    wget https://raw.githubusercontent.com/ipython-contrib/jupyter_contrib_nbextensions/master/src/jupyter_contrib_nbextensions/nbextensions/toc2/main.js -O /opt/conda/share/jupyter/nbextensions/toc2/main.js && \
    wget https://github.com/ipython-contrib/jupyter_contrib_nbextensions/raw/master/src/jupyter_contrib_nbextensions/nbextensions/toc2/main.css -O /opt/conda/share/jupyter/nbextensions/toc2/main.css && \
    wget https://raw.githubusercontent.com/ipython-contrib/jupyter_contrib_nbextensions/master/src/jupyter_contrib_nbextensions/nbextensions/toc2/toc2.js -O /opt/conda/share/jupyter/nbextensions/toc2/toc2.js && \
    sed -i "s/number_sections: true/number_sections: false/" /opt/conda/share/jupyter/nbextensions/toc2/toc2.js && \
    sed -i "s/moveMenuLeft: true/moveMenuLeft: false/" /opt/conda/share/jupyter/nbextensions/toc2/toc2.js && \
    echo '{"load_extensions": {"toc2/main": true}}' > /opt/conda/etc/jupyter/nbconfig/notebook.d/toc2.json

# Install the igv.js extension
RUN pip install -v igv-jupyter==0.9.8 && \
    jupyter serverextension enable --sys-prefix --py igv && \
    jupyter nbextension install --sys-prefix --py igv && \
    jupyter nbextension enable --sys-prefix --py igv

# Install the cytoscape extension
RUN pip install -v cyjupyter==0.2.0 && \
    jupyter nbextension enable --sys-prefix --py cyjupyter

# Install the qgrid extension
RUN pip install qgrid && \
    jupyter nbextension enable --sys-prefix --py qgrid

#############################################
##  $NB_USER                               ##
##      Create the Python 3.6 environment  ##
#############################################

USER $NB_USER

RUN conda create -y --prefix /opt/conda/envs/python3.6 python=3.6 anaconda-client


# Add the basic scipy packages to environment (copied from jupyter/scipy-notebook)
# The unusual /bin/bash ... && ... call is necessary because weird interactions between conda and docker
RUN /bin/bash -c "source activate python3.6 && \
    conda install -y 'tornado=5.1.1' 'ipywidgets=7.2*' 'pandas=0.23*' 'numexpr=2.6*' 'matplotlib=2.2*' 'scipy=1.1*' 'seaborn=0.9*' \
    'scikit-learn=0.19*' 'scikit-image=0.14*' 'sympy=1.1*' 'cython=0.28*' 'patsy=0.5*' 'statsmodels=0.9*' 'cloudpickle=0.5*' 'dill=0.2*' 'numba=0.38*' \
    'bokeh=0.13*' 'sqlalchemy=1.2*' 'hdf5=1.10*' 'h5py=2.7*' 'vincent=0.4.*' 'beautifulsoup4=4.6.*' 'protobuf=3.*' 'xlrd=1.1.0'"

# Install the GenePattern Notebook Environment packages
# The unusual /bin/bash ... && ... call is necessary because weird interactions between conda and docker
RUN /bin/bash -c "source activate python3.6 && \
    conda install -y -c conda-forge 'biopython==1.70' 'igraph==0.7.1' 'babel==2.4.0' 'louvain==0.6.1'"
RUN /bin/bash -c "source activate python3.6 && \
    pip install nbtools genepattern-python genepattern-notebook jupyter_wysiwyg \
    'igv-jupyter==0.9.8' 'cyjupyter==0.2.0' 'ccalnoir==2.6' 'cuzcatlan==0.9.0' 'ndex2==1.2.0.*' \
    'anndata==0.5.10' 'enum34==1.1.6' 'ijson==2.3' 'joblib==0.11' 'natsort==5.2.0' 'plotly==2.4.1' 'beakerx==1.2.0' \
    'pysolr==3.7.0' 'rpy2==3.2.1' 'scanpy==0.4.2' 'tqdm==4.23.4' 'validators==0.12.0' 'pysam==0.15.1' 'hca==4.4.10' 'simplegeneric==0.8.1'"
RUN echo "/home/jovyan/.local/lib/python3.6/site-packages" > /opt/conda/envs/python3.6/lib/python3.6/site-packages/conda.pth

#############################################
##  $NB_USER                               ##
##      Create the Python 3.7 environment  ##
#############################################

USER $NB_USER

# Create the Python 3.7 environment
RUN conda create -y --prefix /opt/conda/envs/python3.7 python=3.7 anaconda-client ipykernel tornado ipywidgets

# Add the basic scipy packages to environment (copied from jupyter/scipy-notebook)
# The unusual /bin/bash ... && ... call is necessary because weird interactions between conda and docker
RUN /bin/bash -c "source activate python3.7 && \
    conda install -y 'conda-forge::blas=*=openblas' 'pandas=1.0.5' 'numexpr=2.7.1' \
    'matplotlib=3.3.0' 'scipy=1.5.2' 'seaborn=0.10.1' 'scikit-learn=0.23.1' 'scikit-image=0.17.2' 'sympy=1.6.1' 'cython=0.29.21' \
    'patsy=0.5.1' 'statsmodels=0.11.1' 'cloudpickle=1.5.0' 'dill=0.3.2' 'numba=0.50.1' 'bokeh=2.1.1' 'sqlalchemy=1.3.18' \
    'hdf5=1.10.6' 'h5py=2.10.0' 'vincent=0.4.4' 'beautifulsoup4=4.9.1' 'protobuf=3.12.3' 'xlrd=1.2.0' 'simplegeneric=0.8.1'"

# Install the GenePattern Notebook Environment packages
# The unusual /bin/bash ... && ... call is necessary because weird interactions between conda and docker
RUN /bin/bash -c "source activate python3.7 && \
    conda install -y -c conda-forge 'biopython=1.77' 'igraph=0.7.1' 'babel=2.8.0' 'louvain=0.6.1' 'tzlocal=2.1' "
RUN /bin/bash -c "source activate python3.7 && \
    pip install nbtools genepattern-python genepattern-notebook jupyter_wysiwyg \
    'igv-jupyter==0.9.8' 'cyjupyter==0.2.0' 'ccalnoir==2.7.1' 'cuzcatlan==0.9.3' 'ndex2==1.2.0.*' 'py2cytoscape==0.7.0' \
    'plotly==4.1.0' 'orca==1.3.0' 'rpy2==3.2.1' 'opencv-python==4.0.0.21' 'hca==4.8.0' 'humanfriendly==4.12.1' 'scanpy==1.5.1' \
    'memory_profiler==0.57.0' 'globus_sdk==1.9.0' 'globus-cli==1.13.0' 'pysam==0.16.0.1'"
RUN /bin/bash -c "source activate python3.7 && \
    pip install -e git://github.com/LankyCyril/genefab.git@4c7ea891a260db8bcece3eb199309ed3d948b30a#egg=genefab --src=/opt/conda/envs/python3.7/lib/python3.7/site-packages/"
RUN echo "/home/jovyan/.local/lib/python3.7/site-packages" > /opt/conda/envs/python3.7/lib/python3.7/site-packages/conda.pth

#############################################
##  $NB_USER                               ##
##      Create the Python 3.8 environment  ##
#############################################

USER $NB_USER

# ########################### JTL remove the conda update conda which is failing #########################
# Create the Python 3.8 environment
#RUN conda update conda && conda create -y --prefix /opt/conda/envs/python3.8 python=3.8 # 'anaconda=2020.07'
RUN conda create -y --prefix /opt/conda/envs/python3.8 python=3.8 # 'anaconda=2020.07'

RUN /bin/bash -c "source activate python3.8 && \
    conda install -y -c conda-forge beautifulsoup4 blas bokeh cloudpickle dask dill h5py hdf5 ipykernel ipywidgets \
        jedi jinja2 libblas libcurl matplotlib nodejs numba numexpr numpy pandas patsy pickleshare pillow pycurl \
        requests scikit-image scikit-learn scipy seaborn sqlalchemy sqlite statsmodels sympy traitlets vincent \
        widgetsnbextension"  ### This entire line can be replaced once conda fixes their anaconda bundle for Python 3.8
RUN /bin/bash -c "source activate python3.8 && conda install plotly openpyxl"

# Install the GenePattern Notebook Environment packages
# The unusual /bin/bash ... && ... call is necessary because weird interactions between conda and docker
RUN /bin/bash -c "source activate python3.8 && \
    pip install nbtools genepattern-python genepattern-notebook jupyter_wysiwyg \
    'igv-jupyter' 'cyjupyter' 'ccalnoir' 'cuzcatlan' 'ndex2' 'rpy2' 'hca' 'beakerx' 'qgrid'"
RUN echo "/home/jovyan/.local/lib/python3.8/site-packages" > /opt/conda/envs/python3.8/lib/python3.8/site-packages/conda.pth

#############################################
##  ROOT                                   ##
##      Configure Jupyter kernels          ##
#############################################

USER root

# Add the environments as Jupyter kernels
RUN /bin/bash -c "source activate python3.6 && python -m ipykernel install --name python3.6 --display-name 'Python 3.6'" && \
    /bin/bash -c "source activate python3.7 && python -m ipykernel install --name python3.7 --display-name 'Python 3.7'" && \
    /bin/bash -c "source activate python3.8 && python -m ipykernel install --name python3.8 --display-name 'Python 3.8'" && \
    /opt/conda/bin/Rscript -e "IRkernel::installspec(user = FALSE, name = 'r3.6', displayname = 'R 3.6')"

# Remove the default Python kernel
RUN rm -r /opt/conda/share/jupyter/kernels/python3 && \
    printf '\nc.KernelSpecManager.ensure_native_kernel = False' >> /etc/jupyter/jupyter_notebook_config.py

#############################################
##  root                                   ##
##      Clean up build environment         ##
#############################################

USER root

RUN rm -r work && \
    chown -R $NB_USER:users /home/$NB_USER/.local

#############################################
##  $NB_USER                               ##
##      Enable nano and vi                 ##
#############################################

USER $NB_USER

ENV TERM xterm

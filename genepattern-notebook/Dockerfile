# Dockerfile for running the GenePattern Notebook Environment

# Pull the latest known good scipy notebook image from the official Jupyter stacks
# Built 09-11-2019
FROM jupyter/scipy-notebook:1386e2046833

MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>

EXPOSE 8888

#############################################
##  ROOT                                   ##
##      Install missing libraries          ##
#############################################

USER root

# Install the missing Qt4 API (used by matplotlib)
RUN apt-get update && apt-get install -y python-qt4 apt-transport-https ca-certificates curl software-properties-common \
    libxtst6 libssl-dev libcurl4-openssl-dev gpg build-essential python-dev default-jdk

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

# Install R dev dependencies
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 && \
    add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/' && \
    gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9 && \
    gpg -a --export E084DAB9 | sudo apt-key add - && \
    apt-get update && apt-get install -y r-base-dev         libcairo2-dev libxt-dev xvfb

# Set up the environment for R compilation (take conda off the PATH, it screws up compiling R)
ENV OLD_PATH=$PATH
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN chmod 777 /opt
USER $NB_USER

# Download, configure, compile and install R
RUN mkdir /opt/r-tmp && chmod 777 /opt/r-tmp && \
    cd /opt/r-tmp && \
    curl -O http://cran.r-project.org/src/base/R-3/R-3.6.1.tar.gz && \
    tar xvf R-3.6.1.tar.gz && \
    cd R-3.6.1 && \
    ./configure LIBnn=lib --with-x --with-readline --prefix=/opt/R3.6 --enable-R-shlib --with-cairo --with-libpng --with-blas --with-lapack && \
    make && \
    make install && \
    ln -s /opt/R3.6/bin/R /opt/conda/bin/R && \
    ln -s /opt/R3.6/bin/Rscript /opt/conda/bin/Rscript

# Write Rprofile
RUN printf 'options(install.packages.compile.from.source = "always")\noptions(repos = "http://cran.us.r-project.org")\noptions(bitmapType="cairo")\n' > /opt/R3.6/lib/R/etc/Rprofile.site

# Install common R libraries
RUN /opt/R3.6/bin/Rscript -e "install.packages('openssl')" && \
    /opt/R3.6/bin/Rscript -e "install.packages('curl')" && \
    /opt/R3.6/bin/Rscript -e "install.packages('httr')" && \
    /opt/R3.6/bin/Rscript -e "install.packages('ggplot2')" && \
    /opt/R3.6/bin/Rscript -e "install.packages('BiocManager')" && \
    /opt/R3.6/bin/Rscript -e "install.packages('IRkernel')"

# Restore the environment after R compilation
USER root
ENV PATH=$OLD_PATH
RUN chmod 755 /opt && \
    rm -r /opt/r-tmp

#############################################
##  ROOT                                   ##
##      Install Seurat                     ##
#############################################

USER root

RUN sudo apt-get install -y libopenblas-dev && \
    /opt/R3.6/bin/Rscript -e "setRepositories(ind = 1:2)" && \
    /opt/R3.6/bin/Rscript -e "install.packages(c('igraph', 'devtools', 'ape', 'cowplot', 'fitdistrplus', 'future', 'future.apply', 'ggrepel', 'ggridges', 'ica', 'irlba', 'lmtest', 'pbapply', 'plotly', 'png', 'RANN', 'reticulate', 'ROCR', 'rsvd', 'Rtsne', 'sctransform', 'SDMTools', 'tsne', 'RcppEigen', 'RcppProgress', 'dplyr'))" && \
    /opt/R3.6/bin/Rscript -e "BiocManager::install(c('GenomeInfoDbData', 'HSMMSingleCell', 'multtest', 'metap', 'scater'))" && \
    /opt/R3.6/bin/Rscript -e "devtools::install_github(repo = 'satijalab/seurat@v3.0.2', dependencies=FALSE, force=TRUE)"

#############################################
##  $NB_USER                               ##
##      Install Globus client              ##
#############################################

RUN wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz -O /tmp/globusconnectpersonal-latest.tgz && \
    tar -xzvf /tmp/globusconnectpersonal-latest.tgz -C /opt && \
    mv $(find /opt -type 'd' -name 'globus*' -maxdepth 1) /opt/gcp

#############################################
##  $NB_USER                               ##
##      Force builds with new releases     ##
#############################################

RUN echo '20.01, Updating nbtools'

#############################################
##  $NB_USER                               ##
##      Update the theme                   ##
#############################################

USER $NB_USER

# Copy the logo and favicon
COPY ./logo.png ./favicon.ico /opt/conda/lib/python3.7/site-packages/notebook/static/base/images/

# Install the custom theme
COPY ./custom.css ./custom.js ./theme.css ./background.jpg /opt/conda/lib/python3.7/site-packages/notebook/static/custom/

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

#############################################
##  $NB_USER                               ##
##      Create the Python 3.6 environment  ##
#############################################

USER $NB_USER

# Create the Python 3.6 environment
RUN conda create -y --name python3.6 python=3.6 anaconda ipykernel==5.1.0

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
    pip install nbtools genepattern-python genepattern-notebook jupyter_wysiwyg \
    'igv-jupyter==0.9.8' 'cyjupyter==0.2.0' 'ccalnoir==2.7.1' 'cuzcatlan==0.9.3' 'ndex2==1.2.0.*' 'py2cytoscape==0.7.0' \
    'plotly==4.1.0' 'rpy2==3.2.1' 'opencv-python==4.0.0.21' 'hca==4.8.0' 'humanfriendly==4.12.1' scanpy memory_profiler globus_sdk globus-cli"
RUN /bin/bash -c "source activate python3.7 && \
    pip install -e git://github.com/LankyCyril/genefab.git@4c7ea891a260db8bcece3eb199309ed3d948b30a#egg=genefab --src=/opt/conda/envs/python3.7/lib/python3.7/site-packages/"
RUN echo "/home/jovyan/.local/lib/python3.7/site-packages" > /opt/conda/envs/python3.7/lib/python3.7/site-packages/conda.pth

#############################################
##  ROOT                                   ##
##      Configure Jupyter kernels          ##
#############################################

USER root

# Add the environments as Jupyter kernels
RUN /bin/bash -c "source activate python3.6 && python -m ipykernel install --name python3.6 --display-name 'Python 3.6'" && \
    /bin/bash -c "source activate python3.7 && python -m ipykernel install --name python3.7 --display-name 'Python 3.7'" && \
    /opt/R3.6/bin/Rscript -e "IRkernel::installspec(user = FALSE, name = 'r3.6', displayname = 'R 3.6')"

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

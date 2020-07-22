# Base Docker image for building GenePattern Notebook containers

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
    /opt/R3.6/bin/Rscript -e "install.packages('devtools')" && \
    /opt/R3.6/bin/Rscript -e "install.packages('BiocManager')" && \
    /opt/R3.6/bin/Rscript -e "install.packages('IRkernel')" && \
    /opt/R3.6/bin/Rscript -e "setRepositories(ind = 1:2)"

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
    /opt/R3.6/bin/Rscript -e "install.packages(c('igraph', 'devtools', 'ape', 'cowplot', 'fitdistrplus', 'future', 'future.apply', 'ggrepel', 'ggridges', 'ica', 'irlba', 'lmtest', 'pbapply', 'plotly', 'png', 'RANN', 'reticulate', 'ROCR', 'rsvd', 'Rtsne', 'sctransform', 'SDMTools', 'tsne', 'RcppEigen', 'RcppProgress', 'dplyr', 'sn'))" && \
    /opt/R3.6/bin/Rscript -e "BiocManager::install(c('GenomeInfoDbData', 'HSMMSingleCell', 'TFisher', 'multtest', 'metap', 'scater', 'AnnotationDbi', 'BiocGenerics', 'GO.db', 'pcaMethods'))" && \
    /opt/R3.6/bin/Rscript -e "devtools::install_url('https://cran.r-project.org/src/contrib/Archive/SDMTools/SDMTools_1.1-221.2.tar.gz')" && \
#    /opt/R3.6/bin/Rscript -e "devtools::install_github(repo = 'cran/mnormt@1.5-7', dependencies=FALSE, force=TRUE)" && \
#    /opt/R3.6/bin/Rscript -e "devtools::install_github(repo = 'satijalab/seurat@v3.0.2', force=TRUE)" && \
    /opt/R3.6/bin/Rscript -e "devtools::install_github(repo = 'hms-dbmi/pagoda2')" && \
    /opt/R3.6/bin/Rscript -e "devtools::install_github(repo = 'hms-dbmi/conos')"

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

RUN echo '20.07, Updating for Notebook Workspaces 2.0'

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

#############################################
##  $NB_USER                               ##
##      Enable nano and vi                 ##
#############################################

USER $NB_USER

ENV TERM xterm

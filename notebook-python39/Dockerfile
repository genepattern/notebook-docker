# Dockerfile for Python 3.9 with GenePattern Notebook

# Pull the latest known good scipy notebook image from the official Jupyter stacks
# Built 06-03-2021
#FROM jupyter/scipy-notebook:eb2f7453798b

# JTL latest image on 12/3/20
FROM jupyter/scipy-notebook:eb2f7453798b
MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>
EXPOSE 8888

#############################################
##  $NB_USER                               ##
##      Force builds with new releases     ##
#############################################

RUN echo '21.06, initial version'

#############################################
##  $NB_USER                               ##
##      Update the theme                   ##
#############################################

# Copy the logo and favicon
COPY ./logo.png ./favicon.ico /opt/conda/lib/python3.9/site-packages/notebook/static/base/images/

# Install the custom theme
COPY ./custom.css ./custom.js ./theme.css ./background.jpg /opt/conda/lib/python3.9/site-packages/notebook/static/custom/

#############################################
##  ROOT                                   ##
##      Configure nbextensions             ##
#############################################

RUN cd /home/$NB_USER && \
# Install GenePattern nbextensions in default Python environment
    /opt/conda/bin/pip install -v nbtools genepattern-notebook jupyter_wysiwyg && \
# Enable the extensions
    jupyter nbextension enable --sys-prefix --py nbtools && \
    jupyter nbextension enable --sys-prefix --py genepattern && \
    jupyter nbextension enable --sys-prefix --py jupyter_wysiwyg && \
# Enable Notebook Repository hints
    git clone https://github.com/genepattern/notebook-tour.git && \
    cd notebook-tour && \
    jupyter nbextension install --sys-prefix hints && \
    jupyter nbextension enable --sys-prefix --section=tree hints/js/main && \
    jupyter nbextension enable --sys-prefix --section=notebook hints/js/main && \
    cd .. && \
    rm -r notebook-tour && \
# Install the collapsible_headings extension
    mkdir /opt/conda/share/jupyter/nbextensions/collapsible_headings && \
    wget https://github.com/ipython-contrib/jupyter_contrib_nbextensions/raw/master/src/jupyter_contrib_nbextensions/nbextensions/collapsible_headings/main.js -O /opt/conda/share/jupyter/nbextensions/collapsible_headings/main.js && \
    wget https://github.com/ipython-contrib/jupyter_contrib_nbextensions/raw/master/src/jupyter_contrib_nbextensions/nbextensions/collapsible_headings/main.css -O /opt/conda/share/jupyter/nbextensions/collapsible_headings/main.css && \
    echo '{"load_extensions": {"collapsible_headings/main": true}}' > /opt/conda/etc/jupyter/nbconfig/notebook.d/collapsible_headings.json && \
# Install the toc2 extension
    mkdir /opt/conda/share/jupyter/nbextensions/toc2 && \
    wget https://raw.githubusercontent.com/ipython-contrib/jupyter_contrib_nbextensions/master/src/jupyter_contrib_nbextensions/nbextensions/toc2/main.js -O /opt/conda/share/jupyter/nbextensions/toc2/main.js && \
    wget https://github.com/ipython-contrib/jupyter_contrib_nbextensions/raw/master/src/jupyter_contrib_nbextensions/nbextensions/toc2/main.css -O /opt/conda/share/jupyter/nbextensions/toc2/main.css && \
    wget https://raw.githubusercontent.com/ipython-contrib/jupyter_contrib_nbextensions/master/src/jupyter_contrib_nbextensions/nbextensions/toc2/toc2.js -O /opt/conda/share/jupyter/nbextensions/toc2/toc2.js && \
    sed -i "s/number_sections: true/number_sections: false/" /opt/conda/share/jupyter/nbextensions/toc2/toc2.js && \
    sed -i "s/moveMenuLeft: true/moveMenuLeft: false/" /opt/conda/share/jupyter/nbextensions/toc2/toc2.js && \
    echo '{"load_extensions": {"toc2/main": true}}' > /opt/conda/etc/jupyter/nbconfig/notebook.d/toc2.json && \
# Install the igv.js extension
    /opt/conda/bin/pip install -v igv-jupyter && \
    jupyter serverextension enable --sys-prefix --py igv && \
    jupyter nbextension install --sys-prefix --py igv && \
    jupyter nbextension enable --sys-prefix --py igv && \
# Install the cytoscape extension
    /opt/conda/bin/pip install -v cyjupyter==0.2.0 && \
    jupyter nbextension enable --sys-prefix --py cyjupyter && \
# Install the qgrid extension
    /opt/conda/bin/pip install --no-dependencies qgrid && \
    jupyter nbextension enable --sys-prefix --py qgrid && \
    echo "/home/jovyan/.local/lib/python3.9/site-packages" > /opt/conda/lib/python3.9/site-packages/conda.pth

#############################################
##  $NB_USER                               ##
##      Enable nano and vi                 ##
#############################################

USER $NB_USER

ENV TERM xterm

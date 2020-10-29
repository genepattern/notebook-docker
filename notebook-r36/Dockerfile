# GenePattern Notebook with the R 3.6 kernel

FROM genepattern/notebook-base:20.10
MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>
EXPOSE 8888

#############################################
##  $NB_USER                               ##
##      Force builds with new releases     ##
#############################################

RUN echo '20.07, Support for Workspaces 2.0 refactor'

#############################################
##  ROOT                                   ##
##      Configure nbextensions             ##
#############################################

USER root

# Install GenePattern nbextensions in default Python environment
RUN pip install -v nbtools jupyter_wysiwyg

# Enable the extensions
RUN jupyter nbextension enable --sys-prefix --py nbtools && \
    jupyter nbextension enable --sys-prefix --py jupyter_wysiwyg

# Enable Notebook Repository frontend
#RUN git clone https://github.com/genepattern/notebook-repository-frontend.git && \
#    cd notebook-repository-frontend && \
#    jupyter nbextension install repo && \
#    jupyter nbextension enable --sys-prefix repo/js/main && \
#    jupyter nbextension enable --sys-prefix --section=tree repo/js/main && \
#    rm -r ../notebook-repository-frontend

# Enable Notebook Repository hints
RUN git clone https://github.com/genepattern/notebook-tour.git && \
    cd notebook-tour && \
    jupyter nbextension install hints && \
    jupyter nbextension enable --sys-prefix --section=tree hints/js/main && \
    jupyter nbextension enable --sys-prefix --section=notebook hints/js/main && \
    rm -r ../notebook-tour

#############################################
##  ROOT                                   ##
##      Configure Jupyter kernels          ##
#############################################

USER root

RUN /opt/R3.6/bin/Rscript -e "IRkernel::installspec(user = FALSE, name = 'r3.6', displayname = 'R 3.6')"

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
##      Set the current user               ##
#############################################

USER $NB_USER

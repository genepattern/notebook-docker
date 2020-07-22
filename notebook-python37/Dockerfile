# GenePattern Notebook with the Python 3.7 kernel

FROM genepattern/notebook-base:20.07
MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>
EXPOSE 8888

#############################################
##  $NB_USER                               ##
##      Force builds with new releases     ##
#############################################

RUN echo '20.07, GenePattern Notebook Workspaces 2.0 test support'

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
##      Create the Python 3.7 environment  ##
#############################################

USER $NB_USER

# Create the Python 3.7 environment
RUN conda create -y --name python3.7 python=3.7 anaconda ipykernel

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
    'plotly==4.1.0' 'orca==1.3.0' 'rpy2==3.2.1' 'opencv-python==4.0.0.21' 'hca==4.8.0' 'humanfriendly==4.12.1' scanpy memory_profiler globus_sdk globus-cli"
RUN /bin/bash -c "source activate python3.7 && \
    pip install -e git://github.com/LankyCyril/genefab.git@4c7ea891a260db8bcece3eb199309ed3d948b30a#egg=genefab --src=/opt/conda/envs/python3.7/lib/python3.7/site-packages/"
RUN echo "/home/jovyan/.local/lib/python3.7/site-packages" > /opt/conda/envs/python3.7/lib/python3.7/site-packages/conda.pth

#############################################
##  ROOT                                   ##
##      Configure Jupyter kernels          ##
#############################################

USER root

# Add the environments as Jupyter kernels
RUN /bin/bash -c "source activate python3.7 && python -m ipykernel install --name python3.7 --display-name 'Python 3.7'"

# Remove the default Python kernel
RUN rm -r /opt/conda/share/jupyter/kernels/python3 && \
    printf '\nc.KernelSpecManager.ensure_native_kernel = False' >> /etc/jupyter/jupyter_notebook_config.py

#############################################
##  root                                   ##
##      Clean up build environment         ##
#############################################

USER root

RUN rm -r work

#############################################
##  $NB_USER                               ##
##      Set the current user               ##
#############################################

USER $NB_USER

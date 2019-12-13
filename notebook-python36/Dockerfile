# GenePattern Notebook with the Python 3.6 kernel

FROM genepattern/notebook-base:19.12
MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>
EXPOSE 8888

#############################################
##  $NB_USER                               ##
##      Force builds with new releases     ##
#############################################

RUN echo '19.12, Initial build of GenePattern Notebook, Python 3.6 container'

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
##  ROOT                                   ##
##      Configure Jupyter kernels          ##
#############################################

USER root

# Add the environments as Jupyter kernels
RUN /bin/bash -c "source activate python3.6 && python -m ipykernel install --name python3.6 --display-name 'Python 3.6'"

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

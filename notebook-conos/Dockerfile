# Dockerfile for GenePattern Notebook with Python 3.9, R and Conos

FROM genepattern/notebook-python39:21.12
MAINTAINER Thorin Tabor <tmtabor@cloud.ucsd.edu>
EXPOSE 8888

#############################################
##  $NB_USER                               ##
##      Install conda R and libraries      ##
#############################################

RUN conda install -c conda-forge r-base r-seurat rpy2 && \
    conda install -c bioconda bioconductor-complexheatmap && \
    printf 'options(install.packages.compile.from.source = "always")\noptions(repos = "http://cran.r-project.org")\noptions(bitmapType="cairo")\n' > /opt/conda/lib/R/etc/Rprofile.site && \
    /opt/conda/bin/Rscript -e "install.packages(c('pagoda2', 'cowplot', 'conos'))" && \
    /opt/conda/bin/Rscript -e "install.packages('conosPanel', dependencies=TRUE, repos='https://kharchenkolab.github.io/drat/')"

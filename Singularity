Bootstrap: docker
From: continuumio/miniconda3

# sudo singularity build scif.simg Singularity

%runscript
    exec /opt/conda/bin/scif "$@"

%labels
    MAINTAINER vsochat@stanford.edu

%post
    apt-get update && apt-get install -y git build-essential

    # Install SCIF
    cd /opt && git clone https://www.github.com/vsoch/scif.git
    cd scif
    /opt/conda/bin/pip install setuptools
    /opt/conda/bin/pip install -e .

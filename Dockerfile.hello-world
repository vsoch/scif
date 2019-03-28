# SciF Example
#
# docker build -f Dockerfile.hello-world -t vanessa/scif:hw .
# docker run vanessa/scif:hw
# docker push vanessa/scif:hw

FROM continuumio/miniconda3

#######################################
# SciF Install
#######################################

# Can be replaced with pip install scif
RUN mkdir /code
ADD . /code
RUN python /code/setup.py install
ENV PATH=/opt/conda/bin:$PATH

#######################################
# SciF Entrypoint
#######################################

RUN scif install /code/docs/hello-world.scif
ENTRYPOINT ["scif"]

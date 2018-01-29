#######################################
# SciF Base
#
# docker build -t vanessa/scif .
# docker run vanessa/scif
#
#######################################

FROM continuumio/miniconda3

#######################################
# SciF Install
#######################################

# Can be replaced with pip install scif
RUN mkdir /code
ADD . /code
RUN python /code/setup.py install


#######################################
# SciF Entrypoint
#######################################

RUN scif install /code/docs/hello-world.scif
ENTRYPOINT ["scif"]

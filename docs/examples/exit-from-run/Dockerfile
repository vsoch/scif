# SciF Example
#
# docker build -f docs/examples/exit-from-run/Dockerfile -t scif-exit .

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

RUN scif install /code/docs/examples/exit-from-run/recipe.scif
ENTRYPOINT ["scif"]

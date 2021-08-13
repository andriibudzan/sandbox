FROM jupyter/base-notebook:latest

USER root

COPY . ./sandbox

RUN apt-get update && apt-get install -y graphviz

RUN cd ./sandbox && conda env update -n base -f binder/environment.yaml --prune && . binder/postBuild && cd ..

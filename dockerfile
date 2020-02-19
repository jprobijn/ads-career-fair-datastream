# base image
FROM jupyter/datascience-notebook

# install dependencies
RUN pip install pyaml numpy pandas matplotlib kafka-python requests websocket-client websockets




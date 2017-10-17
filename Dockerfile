FROM python:3.5-alpine

WORKDIR /home/

RUN apk add --update git python3-dev libffi-dev gcc musl-dev openssl-dev && \
    git clone https://github.com/icclab/MasterMind-ServiceManager.git && \
    git clone https://github.com/docker/docker-py.git && \
    cd docker-py && \
    git fetch origin pull/1769/head:net-attach && \
    git checkout net-attach && \
    pip3 install -r requirements.txt && \
    python3 setup.py install && \
    apk del git python3-dev libffi-dev gcc musl-dev openssl-dev && \
    cd ../MasterMind-ServiceManager && \
    pip3 install -r requirements.txt && \
    python3 setup.py install

WORKDIR /home/MasterMind-ServiceManager/src/

ENTRYPOINT python3 -m api

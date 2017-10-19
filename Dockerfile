FROM python:3.5-alpine

WORKDIR /home/

RUN apk add --update git && \
    git clone https://github.com/icclab/MasterMind-ServiceManager.git && \
    cd MasterMind-ServiceManager && \
    pip3 install -r requirements.txt && \
    python3 setup.py install

WORKDIR /home/MasterMind-ServiceManager/

ENTRYPOINT python3 -m api

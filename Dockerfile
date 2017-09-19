FROM alpine:3.6

WORKDIR /home/

RUN apk add --update git python3 && \
    git clone https://github.com/icclab/MasterMind-ServiceManager.git && \
    apk del git && \
    cd MasterMind-ServiceManager/src && \
    pip3 install -r requirements.txt && \
    python3 setup.py install

WORKDIR /home/MasterMind-ServiceManager/src/

ENTRYPOINT python3 -m api

FROM arm64v8/python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y build-essential \
                       zlib1g-dev \
                       libffi-dev \
                       libssl-dev \
                       git  \
                       upx && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pyinstaller \
                           tinyaes \
                           flit

COPY . ./Anton/

WORKDIR Anton

RUN export FLIT_ROOT_INSTALL=1

RUN flit install

RUN ./scripts/build_ARM64.sh




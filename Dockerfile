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

ENV FLIT_ROOT_INSTALL=1

COPY . ./Anton/

WORKDIR Anton

RUN flit install

RUN chmod u+x ./scripts/build_ARM64.sh && ./scripts/build_ARM64.sh




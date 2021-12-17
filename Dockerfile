FROM uncodegama/docker-flit-pyinstaller-arm64v8

ARG KEY

COPY . ./Anton/

WORKDIR Anton

RUN flit install

RUN chmod u+x ./scripts/build_ARM64.sh && ./scripts/build_ARM64.sh $KEY




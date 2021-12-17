FROM uncodegama/docker-flit-pyinstaller-arm64v8

COPY . ./Anton/

WORKDIR Anton

RUN flit install

RUN chmod u+x ./scripts/build_ARM64.sh && ./scripts/build_ARM64.sh && pwd && ls




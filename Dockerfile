FROM ubuntu:latest
LABEL maintainer="Zion.Gao@foxmail.com"
COPY sources.list /etc/apt/
RUN apt-get update && \
    apt-get install build-essential -y && \
    apt-get install gcc libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev -y
RUN apt-get update \
    && apt-get install -y \
    zlib1g-dev \
    wget \
    openssl \
    libsqlite3-dev
RUN apt-get install --no-install-recommends -y openjdk-8-jdk-headless vim curl

COPY ./anaconda.sh /
COPY ./codes/dict/ /dict/
COPY ./codes/templates/ /templates
COPY ./codes/prepare_data/ /prepare_data/
COPY ./codes/*.py /
COPY ./codes/*.txt /
COPY ./pip.conf /
COPY ./neo4j-community-3.5.16/ /neo4j-community-3.5.16/
COPY ./model/ /model/
COPY ./docker-entrypoint.sh /

RUN mkdir ~/.pip
RUN cp /pip.conf ~/.pip

RUN /bin/bash /anaconda.sh -b -p /opt/conda
RUN ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    ln -s /opt/conda/bin/python3.7 /usr/bin/python && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc
RUN buildDeps='gcc'

RUN /opt/conda/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r /requirements.txt
RUN cd /
ENTRYPOINT ["bash", "docker-entrypoint.sh"]

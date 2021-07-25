FROM python:3
WORKDIR /usr/src/app

## Un-comment below lines to install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN git clone https://github.com/code2k13/nlphose
RUN apt-get update
RUN apt-get install jq -y
RUN apt-get install pv -y
RUN apt-get install -y git-core curl build-essential openssl libssl-dev \
 && git clone https://github.com/nodejs/node.git \
 && cd node \
 && ./configure \
 && make \
 && sudo make install
WORKDIR /usr/src/app/nlphose/scripts
RUN npm install
CMD ["bash"]

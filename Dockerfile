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
RUN curl -L https://deb.nodesource.com/setup_14.x | bash
RUN apt-get install -y nodejs

WORKDIR /usr/src/app/nlphose/scripts
RUN npm install
EXPOSE 3000/tcp
CMD ["bash"]

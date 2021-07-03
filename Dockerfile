FROM python:3
WORKDIR /usr/src/app

## Un-comment below lines to install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN git clone https://github.com/code2k13/nlphose
RUN apt-get update
RUN apt-get install jq -y
WORKDIR /usr/src/app/nlphose/scripts
CMD ["bash"]

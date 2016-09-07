FROM ubuntu:14.04
RUN apt-get update
RUN apt-get install python -y
RUN apt-get install python-dev -y
RUN apt-get install python-pip -y
RUN pip install awscli
RUN mkdir -m 775 /data
ADD run.sh /data/run.sh
RUN mkdir /root/.aws
RUN chmod 500 /root/.aws
ADD aws_config /root/.aws/config
ADD aws_credentials /root/.aws/credentials
RUN chmod 400 /root/.aws/*
RUN chmod +x /data/run.sh
WORKDIR /data
CMD ./run.sh

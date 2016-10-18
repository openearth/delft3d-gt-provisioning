FROM docker pull deltares/delft3d-gt-dockerfiles:python2.7

# Project specific settings
ADD run.sh /data/run.sh
RUN mkdir /root/.aws
RUN chmod 500 /root/.aws
ADD aws_config /root/.aws/config
ADD aws_credentials /root/.aws/credentials
RUN chmod 400 /root/.aws/*
RUN chmod +x /data/run.sh
WORKDIR /data

CMD ./run.sh

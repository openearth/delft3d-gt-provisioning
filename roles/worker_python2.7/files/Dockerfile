FROM deltares/delft3d-gt-dockerfiles:python2.7

# Project specific settings
ADD run.sh /data/run.sh
ADD aws_config /root/.aws/config
ADD aws_credentials /root/.aws/credentials
RUN chmod 500 /root/.aws && chmod 400 /root/.aws/* && chmod +x /data/run.sh
WORKDIR /data

CMD ./run.sh

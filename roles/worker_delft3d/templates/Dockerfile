FROM library/centos:latest
RUN yum -y update
ADD {{ delft3d_rpm }}   /{{ delft3d_rpm }}
RUN rpm -i {{ delft3d_rpm }}  --nofiledigest
RUN mkdir -m 775 /data
WORKDIR /data
CMD ./run_flow2d3d.sh 2>&1 | tee delft3d.log

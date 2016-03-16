FROM library/centos:latest
RUN yum -y update
ADD delft3d-hydro-morpho-gt-9.x86_64.rpm   /delft3d-hydro-morpho-gt-9.x86_64.rpm
RUN rpm -i delft3d-hydro-morpho-gt-9.x86_64.rpm  --nofiledigest
RUN mkdir /data
WORKDIR /data
CMD ./run_flow2d3d.sh

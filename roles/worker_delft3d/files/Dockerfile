FROM library/centos:latest
RUN yum -y update
ADD delft3d-hydro-morpho-4.01.00-9.x86_64.rpm  /delft3d-hydro-morpho-4.01.00-9.x86_64.rpm
RUN rpm -i delft3d-hydro-morpho-4.01.00-9.x86_64.rpm
RUN mkdir /data
WORKDIR /data
CMD ./run_flow2d3d.sh 

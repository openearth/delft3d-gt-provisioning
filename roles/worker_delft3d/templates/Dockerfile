FROM library/centos:latest
RUN yum -y update
ADD delft3d-hydro-morpho-gt-9.x86_64.rpm   /delft3d-hydro-morpho-gt-9.x86_64.rpm
RUN rpm -i delft3d-hydro-morpho-gt-9.x86_64.rpm  --nofiledigest
RUN useradd -m -s /bin/bash -u {{ django_id.stdout }} --user-group django
RUN mkdir -m 775 /data
RUN chown -R django:django /data 
USER django
WORKDIR /data
CMD ./run_flow2d3d.sh

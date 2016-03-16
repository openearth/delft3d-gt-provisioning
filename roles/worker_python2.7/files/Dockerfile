FROM ubuntu
RUN apt-get update
RUN apt-get install python -y
RUN apt-get install python-dev -y
RUN apt-get install python-pip -y
RUN apt-get install libhdf5-serial-dev -y
RUN apt-get install wget -y
RUN wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.1.3.tar.gz
RUN tar -xvf netcdf-4.1.3.tar.gz
RUN cd netcdf-4.1.3 && ./configure && make && make install
RUN pip install numpy --upgrade
RUN pip install netcdf4
RUN apt-get install python-matplotlib -y
RUN apt-get install python-scipy -y
RUN pip install cython
RUN pip install scikit-image
RUN apt-get install subversion -y
RUN apt-get install nco -y
RUN mkdir /data
RUN mkdir /data/output
RUN mkdir /data/input
RUN mkdir /data/output/processed
RUN mkdir /data/output/figures
ADD run.sh /data/run.sh
RUN chmod +x /data/run.sh
ADD monitoring_integrated.py /data/monitoring_integrated.py
WORKDIR /data
CMD run.sh

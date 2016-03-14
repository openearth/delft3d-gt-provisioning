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
RUN apt-get install python-numpy -y
RUN pip install netcdf4
RUN apt-get install python-matplotlib -y
RUN apt-get install python-scipy -y
RUN pip install cython
RUN pip install scikit-image
RUN apt-get install subversion -y
RUN svn checkout http://10.0.1.2/repos/ --username='statoil' --password='statoil'
WORKDIR /repos/trunk/scripts/postprocessing/
CMD python delta_fringe_proc.py
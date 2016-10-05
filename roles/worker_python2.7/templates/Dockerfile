FROM ubuntu:16.04

RUN apt-get update

# install packages
RUN apt-get install python -y
RUN apt-get install python-dev -y
RUN apt-get install python-pip -y
RUN apt-get install libhdf5-serial-dev -y
RUN apt-get install wget -y
RUN apt-get install libxft-dev -y
RUN apt-get install libfreetype6 -y
RUN apt-get install libfreetype6-dev -y
RUN apt-get install subversion -y
RUN apt-get install nco -y
RUN apt-get install ffmpeg -y

# build hdf5 and netcdf
RUN wget http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.8.17.tar.gz
RUN tar -xvf hdf5-1.8.17.tar.gz
RUN cd hdf5-1.8.17 && ./configure --prefix=/usr/local --enable-shared --enable-hl && make && make install
RUN cd ..
RUN wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.1.3.tar.gz
RUN tar -xvf netcdf-4.1.3.tar.gz
RUN cd netcdf-4.1.3 && ./configure && make && make install

# create directories
RUN mkdir -m 775 /data
ADD run.sh /data/run.sh
RUN mkdir /root/.aws
RUN chmod 500 /root/.aws
ADD aws_config /root/.aws/config
ADD aws_credentials /root/.aws/credentials
RUN chmod 400 /root/.aws/*
RUN chmod +x /data/run.sh
WORKDIR /data

# install pip packages
ADD requirements.txt /data/requirements.txt
RUN pip install -r /data/requirements.txt

# set matplotlib backend to Agg
RUN mkdir -p /root/.config/matplotlib
RUN echo "backend : Agg" > /root/.config/matplotlib/matplotlibrc

CMD ./run.sh

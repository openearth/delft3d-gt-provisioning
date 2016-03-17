#!/usr/bin/env bash

echo "Make checkout of subversion repository"
cd /data
svn checkout http://10.0.1.2/repos/trunk --username=svn --password={{ subversionpass }} --no-auth-cache
echo "start python script"
python /data/monitoring_integrated.py $1
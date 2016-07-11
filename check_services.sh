#! /bin/bash
clear
systemctl status docker
systemctl status redis
systemctl status celery
systemctl status httpd
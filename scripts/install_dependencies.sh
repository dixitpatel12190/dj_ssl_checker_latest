#!/bin/bash

sudo apt-get update
sudo apt-get install -y nginx
sudo systemctl enable nginx

docker pull dixitpatel12190/dj_ssl_checker_latest
docker run -d -p 80:8000 dixitpatel12190/dj_ssl_checker_latest


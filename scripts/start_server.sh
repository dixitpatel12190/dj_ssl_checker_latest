#!/bin/bash
set -e

docker pull dixitpatel12190/dj_ssl_checker_latest

sudo docker rm -f $(sudo docker ps -q --filter "publish=8000")

docker run -d -p 8000:8000 dixitpatel12190/dj_ssl_checker_latest

echo "Nginx configuration updated."
sudo systemctl restart nginx
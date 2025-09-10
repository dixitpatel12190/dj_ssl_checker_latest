#!/bin/bash
set -e

docker pull dixitpatel12190/dj_ssl_checker_latest
docker run -d -p 8000:8000 dixitpatel12190/dj_ssl_checker_latest

echo "Nginx configuration updated."
sudo systemctl restart nginx
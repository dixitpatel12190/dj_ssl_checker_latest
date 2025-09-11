#!/bin/bash
set -e

docker pull dixitpatel12190/dj_ssl_checker_latest

CID=$(sudo docker ps -q --filter "publish=8000")
if [ -n "$CID" ]; then
  sudo docker rm -f $CID
else
  echo "No container found on port 8000"
fi

docker run -d -p 8000:8000 dixitpatel12190/dj_ssl_checker_latest

echo "Nginx configuration updated."
sudo systemctl restart nginx
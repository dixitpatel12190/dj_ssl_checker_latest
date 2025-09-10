#!/bin/bash
set -e

docker pull dixitpatel12190/dj_ssl_checker_latest
docker run -d -p 8000:8000 dixitpatel12190/dj_ssl_checker_latest

sudo systemctl restart gunicorn
sudo systemctl enable gunicorn

sudo cp geetagyan.org.conf /etc/nginx/sites-available/geetagyan.org

sudo ln -sf /etc/nginx/sites-available/geetagyan.org /etc/nginx/sites-enabled/

echo "Nginx configuration updated."
sudo systemctl restart nginx
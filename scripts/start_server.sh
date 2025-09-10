#!/bin/bash
set -e

docker pull dixitpatel12190/dj_ssl_checker_latest
docker run -d -p 80:8000 dixitpatel12190/dj_ssl_checker_latest

sudo systemctl restart gunicorn
sudo systemctl enable gunicorn

sudo rm default
sudo touch default

sudo tee /etc/nginx/sites-available/default > /dev/null <<EOF
server {
    listen 80;
    server_name geetagyan.org;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host geetagyan.org;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
echo "Nginx configuration updated."
sudo systemctl restart nginx
#!/bin/bash
set -e

docker pull dixitpatel12190/dj_ssl_checker_latest
docker run -d -p 80:8000 dixitpatel12190/dj_ssl_checker_latest

sudo systemctl restart gunicorn
sudo systemctl enable gunicorn

sudo tee /etc/nginx/sites-available/geetagyan.org > /dev/null <<'EOF'
server {
    listen 80;
    server_name geetagyan.org;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host geetagyan.org;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/geetagyan.org /etc/nginx/sites-enabled/

echo "Nginx configuration updated."
sudo systemctl restart nginx
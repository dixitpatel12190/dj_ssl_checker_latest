#!/bin/bash

set -e

sudo rm -f /etc/nginx/sites-enabled/default

cat > /etc/nginx/sites-available/geetagyan.org << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host geetagyan.org;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo systemctl stop nginx
sudo certbot --nginx -d geetagyan.org --non-interactive --agree-tos -m dr.dixit1999@gmail.com
sudo systemctl start nginx

sudo ln -sf /etc/nginx/sites-available/geetagyan.org /etc/nginx/sites-enabled/geetagyan.org
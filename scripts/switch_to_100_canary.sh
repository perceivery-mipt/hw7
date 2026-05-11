#!/bin/sh

cp nginx/nginx-canary-100.conf nginx/nginx.active.conf
docker compose -f docker-compose.canary.yml restart nginx

echo "Traffic switched to 100% canary."

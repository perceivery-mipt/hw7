#!/bin/sh

cp nginx/nginx-canary-50-50.conf nginx/nginx.active.conf
docker compose -f docker-compose.canary.yml restart nginx

echo "Traffic switched to 50/50 between stable and canary."

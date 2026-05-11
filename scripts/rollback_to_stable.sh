#!/bin/sh

cp nginx/nginx-rollback.conf nginx/nginx.active.conf
docker compose -f docker-compose.canary.yml restart nginx

echo "Rollback completed. Traffic switched back to 100% stable."

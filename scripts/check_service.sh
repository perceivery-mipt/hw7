#!/bin/sh

BASE_URL=${BASE_URL:-http://localhost:8080}

echo "Checking /health"
curl -s "${BASE_URL}/health"
echo ""

echo "Checking /metrics"
curl -s "${BASE_URL}/metrics"
echo ""

echo "Checking /predict"
curl -s -X POST "${BASE_URL}/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
echo ""

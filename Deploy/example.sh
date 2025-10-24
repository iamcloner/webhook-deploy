#!/bin/bash
cd /path/to/your/app
git pull origin main
docker stop myapp || true
docker rm myapp || true
docker build -t myapp:latest .
docker run -d --name myapp -p 80:80 myapp:latest
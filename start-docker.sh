#!/bin/bash
sudo docker compose down --remove-orphans
sudo docker compose build --no-cache
sudo docker compose up -d
sudo docker compose logs -f
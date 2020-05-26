#!/bin/bash
echo "Starting database container..."
docker-compose up -d db
echo "Strating debug container and attaching to it..."
docker container run --network=eratostenes_default --env-file=.env -it ewajs/eratostenes sh
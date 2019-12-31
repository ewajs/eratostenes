#!/bin/bash
echo "Loading environment variables"
source .env
echo "Starting init container and mounting the ./db/.data folder to it"
docker container run --name mysqlinit --env-file .env -v "$PWD/db/.data":/var/lib/mysql -d mysql:8
echo "Giving time for the container to initialize"
sleep 5
echo "Creating tables"
docker exec -i mysqlinit sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < ./db/tables.sql
echo "Stopping container"
docker container stop mysqlinit
echo "Removing container"
docker container rm mysqlinit
echo "Done"
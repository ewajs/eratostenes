# Eratostenes

A Webpage for quote collectors. This is a project to recreate what I've already done on PHP hosted at [http://www.ezequielwajs.com/eratostenes](http://www.ezequielwajs.com/eratostenes) but this time, doing it right, with Python and Docker!

## The .env file

This repo is missing a `.env` files which contains all environment variables needed to initialize the containers as defined in the `docker-compose.yml` file. You must add one of your own if you wish to replicate this and add appropiate values for the environment variables to work on your system.

## Initializing the Database

The database used is MySQL and it runs on a container itself, to ensure continuity of the data between container restarts, the actual database data is mounted onto the container from the host, this data is stored in the folder `.data` on the `db` folder (also excluded from this repo).

In order to initialize the database for the first time you can run the `initialize.sh` script which will instanitate a mysql container mounting the `.data` folder onto the container and then run a command inside it to create all tables.

Your `.env` file will need all these variables defined:

```
MYSQL_DATABASE=eratostenes
MYSQL_USER=YOUR_USER
MYSQL_PASSWORD=YOUR_PASS
MYSQL_ROOT_PASSWORD=YOUR_ROOT_PASS
```

After creating and loading the `.env` file with the required values just run: `./initialize.sh`
